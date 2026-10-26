#!/usr/bin/env python3
"""Tests for George OMP role preparation, safe isolation, and cleanup helpers."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest import mock
from pathlib import Path

# Insert tools directory into sys.path
TOOLS_DIR = Path(__file__).resolve().parents[1] / "skills" / "george-orchestrate" / "tools"
sys.path.insert(0, str(TOOLS_DIR))

from omp_roles import (
    NAME_REGEX,
    VALID_THINKING_LEVELS,
    cleanup_roles,
    prepare_roles,
    validate_roles_input,
)


class OmpRolesTests(unittest.TestCase):
    def setUp(self):
        self.test_dir = tempfile.mkdtemp(prefix="test_omp_roles_")
        self.project_path = Path(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_prepare_and_cleanup_roundtrip(self):
        """Prepare valid roles, verify receipt and created files, then clean up."""
        role_input = {
            "run_id": "run-test-001",
            "roles": [
                {
                    "name": "george-omp-sandbox-worker",
                    "description": "Worker with limited sandbox access",
                    "model": "commandcode/deepseek/deepseek-v4.1-flash",
                    "thinking": "high",
                    "tools": ["read", "write", "bash"],
                    "brief": "Execute task in sandbox only.",
                },
                {
                    "name": "george-omp-reviewer",
                    "description": "Reviewer with read-only access",
                    "model": "google-antigravity/gemini-3.8-flash",
                    "thinking": "minimal",
                    "tools": ["read"],
                    "brief": "Review artifacts without modifications.",
                },
            ],
        }

        receipt_file = self.project_path / "receipt.json"
        receipt = prepare_roles(self.project_path, role_input, receipt_path=receipt_file)

        self.assertEqual(receipt["run_id"], "run-test-001")
        self.assertEqual(len(receipt["roles"]), 2)
        self.assertEqual(len(receipt["ownership"]), 2)
        self.assertTrue(receipt_file.exists())

        # Inspect generated files exist and contain basic frontmatter tags
        worker_file = self.project_path / ".omp" / "agents" / "george-omp-sandbox-worker.md"
        reviewer_file = self.project_path / ".omp" / "agents" / "george-omp-reviewer.md"
        self.assertTrue(worker_file.exists())
        self.assertTrue(reviewer_file.exists())

        worker_content = worker_file.read_text(encoding="utf-8")
        self.assertIn("name: george-omp-sandbox-worker", worker_content)
        self.assertIn("spawns: []", worker_content)

        reviewer_content = reviewer_file.read_text(encoding="utf-8")
        self.assertIn("name: george-omp-reviewer", reviewer_content)
        self.assertIn("spawns: []", reviewer_content)

        # Verify receipt statuses and hashes
        for role_entry in receipt["roles"]:
            self.assertEqual(role_entry["status"], "requested-not-observed")
            self.assertEqual(role_entry["spawns"], [])
            file_bytes = Path(role_entry["definition_path"]).read_bytes()
            expected_hash = f"sha256:{hashlib.sha256(file_bytes).hexdigest()}"
            self.assertEqual(role_entry["content_hash"], expected_hash)

        # Cleanup
        summary = cleanup_roles(receipt)
        self.assertEqual(len(summary["cleaned"]), 2)
        self.assertEqual(len(summary["preserved_modified"]), 0)
        self.assertFalse(worker_file.exists())
        self.assertFalse(reviewer_file.exists())
        # .omp/agents should be safely pruned when empty
        self.assertFalse((self.project_path / ".omp" / "agents").exists())

    def test_cleanup_preserves_modified_files(self):
        """Files altered after preparation must be preserved during cleanup."""
        role_input = {
            "run_id": "run-test-002",
            "roles": [
                {
                    "name": "george-omp-worker-mod",
                    "description": "Worker file to be modified",
                    "model": "@task",
                    "tools": ["read"],
                    "brief": "Initial brief.",
                }
            ],
        }

        receipt = prepare_roles(self.project_path, role_input)
        target_file = Path(receipt["roles"][0]["definition_path"])
        self.assertTrue(target_file.exists())

        # Modify file content
        target_file.write_text("MODIFIED CONTENT BY USER", encoding="utf-8")

        summary = cleanup_roles(receipt)
        self.assertEqual(len(summary["cleaned"]), 0)
        self.assertEqual(len(summary["preserved_modified"]), 1)
        self.assertTrue(target_file.exists())
        self.assertEqual(target_file.read_text(encoding="utf-8"), "MODIFIED CONTENT BY USER")

    def test_cleanup_preserves_foreign_files(self):
        """Foreign agent files not in receipt must never be touched or deleted."""
        agents_dir = self.project_path / ".omp" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        foreign_file = agents_dir / "existing_user_agent.md"
        foreign_file.write_text("--- \nname: user-agent\n---", encoding="utf-8")

        role_input = {
            "run_id": "run-test-003",
            "roles": [
                {
                    "name": "george-omp-ephemeral",
                    "description": "Ephemeral role",
                    "model": "@smol",
                    "tools": ["read"],
                }
            ],
        }
        receipt = prepare_roles(self.project_path, role_input)

        summary = cleanup_roles(receipt)
        self.assertEqual(len(summary["cleaned"]), 1)
        # Foreign file must still exist
        self.assertTrue(foreign_file.exists())
        self.assertTrue(agents_dir.exists())

    def test_cleanup_rejects_outside_definition_path_and_preserves_file(self):
        """Receipt pointing outside project root with matching hash must fail and not delete outside file."""
        outside_dir = tempfile.mkdtemp(prefix="outside_foreign_")
        try:
            outside_file = Path(outside_dir) / "george-omp-sensitive.md"
            secret_data = b"TOP_SECRET_USER_FILE_CONTENT"
            outside_file.write_bytes(secret_data)
            matching_hash = f"sha256:{hashlib.sha256(secret_data).hexdigest()}"

            malicious_receipt = {
                "run_id": "run-attack-001",
                "project_path": str(self.project_path),
                "roles": [
                    {
                        "name": "george-omp-sensitive",
                        "definition_path": str(outside_file.resolve()),
                        "content_hash": matching_hash,
                    }
                ],
                "ownership": [str(outside_file.resolve())],
            }

            with self.assertRaises(ValueError):
                cleanup_roles(malicious_receipt)

            # File outside project MUST NOT be deleted
            self.assertTrue(outside_file.exists())
            self.assertEqual(outside_file.read_bytes(), secret_data)
        finally:
            shutil.rmtree(outside_dir, ignore_errors=True)

    def test_cleanup_does_not_follow_replaced_symlink(self):
        """If a role definition path was replaced with a symlink, cleanup must not unlink or follow it."""
        user_file = self.project_path / "user_important_doc.txt"
        user_file.write_text("IMPORTANT ORIGINAL TEXT", encoding="utf-8")

        role_input = {
            "run_id": "run-symlink-test",
            "roles": [
                {
                    "name": "george-omp-target-symlink",
                    "description": "Role target for symlink test",
                    "model": "@task",
                    "tools": ["read"],
                }
            ],
        }
        receipt = prepare_roles(self.project_path, role_input)
        target_path = Path(receipt["roles"][0]["definition_path"])
        self.assertTrue(target_path.exists())

        # Replace target with a symlink pointing to user_file
        target_path.unlink()
        target_path.symlink_to(user_file)
        self.assertTrue(target_path.is_symlink())

        summary = cleanup_roles(receipt)

        # The symlinked user file must never be deleted or altered
        self.assertTrue(user_file.exists())
        self.assertEqual(user_file.read_text(encoding="utf-8"), "IMPORTANT ORIGINAL TEXT")
        self.assertNotIn(str(target_path), summary["cleaned"])
        self.assertEqual(len(summary["preserved_modified"]), 1)
        self.assertEqual(summary["preserved_modified"][0]["actual_hash"], "symlink")

    def test_prepare_rejects_broken_symlink_destination(self):
        """Preparation must fail closed and refuse to overwrite broken symlinks."""
        agents_dir = self.project_path / ".omp" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        broken_symlink = agents_dir / "george-omp-broken-worker.md"
        broken_symlink.symlink_to(self.project_path / "non_existent_target.md")
        self.assertTrue(broken_symlink.is_symlink())
        self.assertFalse(broken_symlink.exists())  # broken link exists() is False

        role_input = {
            "run_id": "run-broken-test",
            "roles": [
                {
                    "name": "george-omp-broken-worker",
                    "description": "Worker with broken symlink collision",
                    "model": "@task",
                    "tools": ["read"],
                }
            ],
        }

        with self.assertRaises(FileExistsError):
            prepare_roles(self.project_path, role_input)

        # Symlink must be intact and not overwritten with new content
        self.assertTrue(broken_symlink.is_symlink())
        self.assertFalse(broken_symlink.exists())

    def test_prepare_exclusive_creation_collision(self):
        """Exclusive creation (open with 'xb') fails if target appears concurrently."""
        agents_dir = self.project_path / ".omp" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        pre_existing = agents_dir / "george-omp-concurrent.md"
        pre_existing.write_text("PRE-EXISTING CONCURRENT CONTENT", encoding="utf-8")

        role_input = {
            "run_id": "run-exclusive-test",
            "roles": [
                {
                    "name": "george-omp-concurrent",
                    "description": "Role hitting collision",
                    "model": "@task",
                    "tools": ["read"],
                }
            ],
        }

        with self.assertRaises(FileExistsError):
            prepare_roles(self.project_path, role_input)

        self.assertEqual(pre_existing.read_text(encoding="utf-8"), "PRE-EXISTING CONCURRENT CONTENT")

    def test_prepare_rejects_existing_receipt_and_rolls_back(self):
        """If receipt path already exists, prepare must fail without overwriting it and rollback all role writes."""
        receipt_file = self.project_path / "existing_foreign_receipt.json"
        receipt_file.write_text("FOREIGN PRE-EXISTING RECEIPT", encoding="utf-8")

        role_input = {
            "run_id": "run-receipt-collision",
            "roles": [
                {
                    "name": "george-omp-receipt-test",
                    "description": "Role for receipt test",
                    "model": "@task",
                    "tools": ["read"],
                }
            ],
        }

        with self.assertRaises(FileExistsError):
            prepare_roles(self.project_path, role_input, receipt_path=receipt_file)

        # Foreign receipt is preserved
        self.assertEqual(receipt_file.read_text(encoding="utf-8"), "FOREIGN PRE-EXISTING RECEIPT")
        # Role file must not be left behind
        worker_file = self.project_path / ".omp" / "agents" / "george-omp-receipt-test.md"
        self.assertFalse(worker_file.exists())

    def test_prepare_rollback_preserves_concurrently_modified_file(self):
        """Rollback on failure must not delete files whose content was modified since creation."""
        agents_dir = self.project_path / ".omp" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        role1_dest = agents_dir / "george-omp-role-one.md"

        role_input = {
            "run_id": "run-rollback-mod",
            "roles": [
                {
                    "name": "george-omp-role-one",
                    "description": "First role",
                    "model": "@task",
                    "tools": ["read"],
                },
                {
                    "name": "george-omp-fail-two",
                    "description": "Second role that will fail",
                    "model": "@task",
                    "tools": ["read"],
                },
            ],
        }

        original_open = open

        def hooked_open(file, mode="r", *args, **kwargs):
            if "george-omp-fail-two.md" in str(file):
                if role1_dest.exists():
                    role1_dest.write_text("CONCURRENT EDIT ON ROLE 1", encoding="utf-8")
                raise IOError("Simulated disk error writing role 2")
            return original_open(file, mode, *args, **kwargs)

        with mock.patch("builtins.open", side_effect=hooked_open):
            with self.assertRaises(IOError):
                prepare_roles(self.project_path, role_input)

        # Role 1 was modified concurrently, so rollback must PRESERVE it
        self.assertTrue(role1_dest.exists())
        self.assertEqual(role1_dest.read_text(encoding="utf-8"), "CONCURRENT EDIT ON ROLE 1")

    def test_model_validation_rejects_control_characters_and_whitespace(self):
        """Model identifier with control characters or whitespace must be rejected to prevent YAML injection."""
        # Newline injection attempt
        with self.assertRaises(ValueError) as ctx:
            prepare_roles(self.project_path, {
                "run_id": "run-model-inject-1",
                "roles": [
                    {
                        "name": "george-omp-injector",
                        "description": "desc",
                        "model": "openai/gpt-5\nadmin: true",
                        "tools": ["read"],
                    }
                ],
            })
        self.assertIn("illegal", str(ctx.exception).lower())

        # Carriage return injection attempt
        with self.assertRaises(ValueError):
            prepare_roles(self.project_path, {
                "run_id": "run-model-inject-2",
                "roles": [
                    {
                        "name": "george-omp-injector",
                        "description": "desc",
                        "model": "model\rname",
                        "tools": ["read"],
                    }
                ],
            })

        # Whitespace inside model
        with self.assertRaises(ValueError):
            prepare_roles(self.project_path, {
                "run_id": "run-model-inject-3",
                "roles": [
                    {
                        "name": "george-omp-injector",
                        "description": "desc",
                        "model": "model with spaces",
                        "tools": ["read"],
                    }
                ],
            })

    def test_atomic_validation_no_partial_write(self):
        """If any role in batch is invalid, zero files are created."""
        role_input = {
            "run_id": "run-test-004",
            "roles": [
                {
                    "name": "george-omp-valid-one",
                    "description": "Valid role",
                    "model": "@task",
                    "tools": ["read"],
                },
                {
                    "name": "invalid-name-without-prefix",
                    "description": "Invalid role",
                    "model": "@task",
                    "tools": ["read"],
                },
            ],
        }

        agents_dir = self.project_path / ".omp" / "agents"
        with self.assertRaises(ValueError) as ctx:
            prepare_roles(self.project_path, role_input)

        self.assertIn("Invalid role name", str(ctx.exception))
        valid_file = agents_dir / "george-omp-valid-one.md"
        self.assertFalse(valid_file.exists())

    def test_collision_rejection_no_overwrite(self):
        """If a target role file already exists, preparation fails closed and does not overwrite."""
        agents_dir = self.project_path / ".omp" / "agents"
        agents_dir.mkdir(parents=True, exist_ok=True)
        existing_file = agents_dir / "george-omp-existing.md"
        existing_file.write_text("ORIGINAL PRE-EXISTING CONTENT", encoding="utf-8")

        role_input = {
            "run_id": "run-test-005",
            "roles": [
                {
                    "name": "george-omp-existing",
                    "description": "Colliding role",
                    "model": "@task",
                    "tools": ["read"],
                }
            ],
        }

        with self.assertRaises(FileExistsError):
            prepare_roles(self.project_path, role_input)

        self.assertEqual(existing_file.read_text(encoding="utf-8"), "ORIGINAL PRE-EXISTING CONTENT")

    def test_duplicate_names_in_batch_rejected(self):
        """Duplicate role names in the same input batch must fail validation."""
        role_input = {
            "run_id": "run-test-006",
            "roles": [
                {
                    "name": "george-omp-dup",
                    "description": "Role 1",
                    "model": "@task",
                    "tools": ["read"],
                },
                {
                    "name": "george-omp-dup",
                    "description": "Role 2",
                    "model": "@smol",
                    "tools": ["write"],
                },
            ],
        }
        with self.assertRaises(ValueError) as ctx:
            prepare_roles(self.project_path, role_input)
        self.assertIn("Duplicate role name", str(ctx.exception))

    def test_thinking_level_validation_and_conflict(self):
        """Unsupported thinking levels or conflicts with model suffix must fail."""
        role_input_invalid_think = {
            "run_id": "run-test-007",
            "roles": [
                {
                    "name": "george-omp-think-test",
                    "description": "Role with bad thinking",
                    "model": "@task",
                    "thinking": "extreme_thinking_unsupported",
                    "tools": ["read"],
                }
            ],
        }
        with self.assertRaises(ValueError) as ctx:
            prepare_roles(self.project_path, role_input_invalid_think)
        self.assertIn("Unsupported thinking level", str(ctx.exception))

        role_input_conflict = {
            "run_id": "run-test-008",
            "roles": [
                {
                    "name": "george-omp-conflict",
                    "description": "Role with conflicting thinking",
                    "model": "openai/gpt-5-mini:low",
                    "thinking": "high",
                    "tools": ["read"],
                }
            ],
        }
        with self.assertRaises(ValueError) as ctx:
            prepare_roles(self.project_path, role_input_conflict)
        self.assertIn("conflicts with explicit thinking", str(ctx.exception))

    def test_tools_safety_isolation(self):
        """Tools must be explicit list; spawns is always set to [] for isolation."""
        role_input_no_tools = {
            "run_id": "run-test-009",
            "roles": [
                {
                    "name": "george-omp-no-tools",
                    "description": "Role without tools list",
                    "model": "@task",
                    "tools": "read,write",
                }
            ],
        }
        with self.assertRaises(ValueError) as ctx:
            prepare_roles(self.project_path, role_input_no_tools)
        self.assertIn("must be an explicit list", str(ctx.exception))

        role_input_empty_tools = {
            "run_id": "run-test-010",
            "roles": [
                {
                    "name": "george-omp-safe-empty",
                    "description": "Role with empty tools",
                    "model": "@smol",
                    "tools": [],
                }
            ],
        }
        receipt = prepare_roles(self.project_path, role_input_empty_tools)
        target_file = Path(receipt["roles"][0]["definition_path"])
        content = target_file.read_text(encoding="utf-8")
        self.assertIn("tools: []", content)
        self.assertIn("spawns: []", content)
        cleanup_roles(receipt)

    def test_path_traversal_prevention(self):
        """Role files attempting path traversal or escaping project root must be rejected."""
        with self.assertRaises(ValueError):
            prepare_roles(self.project_path / "non_existent_subdir", {
                "run_id": "run-fail",
                "roles": [{"name": "george-omp-ok", "description": "x", "model": "m", "tools": []}],
            })

        with self.assertRaises(ValueError):
            prepare_roles(self.project_path, {
                "run_id": "run-fail",
                "roles": [{"name": "george-omp-../../escape", "description": "x", "model": "m", "tools": []}],
            })

    def test_symlink_escape_rejection(self):
        """Symlinked .omp or .omp/agents pointing outside project root must fail."""
        outside_dir = tempfile.mkdtemp(prefix="outside_dir_")
        try:
            omp_link = self.project_path / ".omp"
            omp_link.symlink_to(outside_dir)

            with self.assertRaises(ValueError) as ctx:
                prepare_roles(self.project_path, {
                    "run_id": "run-symlink",
                    "roles": [{"name": "george-omp-test", "description": "x", "model": "m", "tools": []}],
                })
            self.assertIn("Symlink traversal detected", str(ctx.exception))
        finally:
            shutil.rmtree(outside_dir, ignore_errors=True)

    def test_cli_invocation(self):
        """CLI prepare and cleanup work end-to-end via commandline execution."""
        cli_script = TOOLS_DIR / "omp_roles.py"
        input_data = {
            "run_id": "run-cli-001",
            "roles": [
                {
                    "name": "george-omp-cli-worker",
                    "description": "CLI worker",
                    "model": "@task",
                    "tools": ["read"],
                    "brief": "CLI task brief.",
                }
            ],
        }
        input_file = self.project_path / "input.json"
        input_file.write_text(json.dumps(input_data), encoding="utf-8")
        receipt_file = self.project_path / "cli_receipt.json"

        # Prepare via CLI
        prep_res = subprocess.run(
            [
                sys.executable,
                str(cli_script),
                "prepare",
                "--project",
                str(self.project_path),
                "--input",
                str(input_file),
                "--receipt",
                str(receipt_file),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(prep_res.returncode, 0, f"CLI prepare failed: {prep_res.stderr}")
        self.assertTrue(receipt_file.exists())
        worker_file = self.project_path / ".omp" / "agents" / "george-omp-cli-worker.md"
        self.assertTrue(worker_file.exists())

        # Cleanup via CLI
        clean_res = subprocess.run(
            [
                sys.executable,
                str(cli_script),
                "cleanup",
                "--receipt",
                str(receipt_file),
            ],
            capture_output=True,
            text=True,
        )
        self.assertEqual(clean_res.returncode, 0, f"CLI cleanup failed: {clean_res.stderr}")
        self.assertFalse(worker_file.exists())


if __name__ == "__main__":
    unittest.main()
