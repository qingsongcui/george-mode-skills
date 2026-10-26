#!/usr/bin/env python3
"""OMP role preparation, safe isolation, and cleanup helper.

Provides deterministic role file synthesis under .omp/agents/<name>.md,
atomic batch validation, symlink and traversal protections, exclusive creation,
and hash-verified safe cleanup preserving foreign and modified files.
"""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from typing import Any, Dict, List, Optional, Set, Tuple, Union

NAME_REGEX = re.compile(r"^george-omp-[a-zA-Z0-9_\-]+$")
VALID_THINKING_LEVELS = {"off", "none", "minimal", "low", "medium", "high", "xhigh", "max"}
SAFE_TOOL_REGEX = re.compile(r"^[a-zA-Z0-9_.:/-]+$")
HASH_REGEX = re.compile(r"^sha256:[a-f0-9]{64}$")


def _is_safe_subpath(child: Path, parent: Path) -> bool:
    """Verify that resolved child path is strictly inside resolved parent directory."""
    try:
        resolved_child = child.resolve()
        resolved_parent = parent.resolve()
        return resolved_child.is_relative_to(resolved_parent) and resolved_child != resolved_parent
    except (ValueError, RuntimeError):
        return False


def _check_symlink_safety(project_path: Path) -> None:
    """Ensure .omp and .omp/agents (if existing) are not symlinks and do not escape project root."""
    omp_dir = project_path / ".omp"
    if omp_dir.is_symlink():
        raise ValueError(f"Symlink traversal detected: {omp_dir} is a symlink")
    if omp_dir.exists() and not _is_safe_subpath(omp_dir, project_path):
        raise ValueError(f"Symlink traversal detected: {omp_dir} resolves outside project directory")

    agents_dir = omp_dir / "agents"
    if agents_dir.is_symlink():
        raise ValueError(f"Symlink traversal detected: {agents_dir} is a symlink")
    if agents_dir.exists() and not _is_safe_subpath(agents_dir, project_path):
        raise ValueError(f"Symlink traversal detected: {agents_dir} resolves outside project directory")


def _extract_model_thinking_suffix(model_str: str) -> Optional[str]:
    """Extract thinking suffix like ':high' from model selector if present."""
    match = re.search(r":([a-zA-Z0-9_\-]+)$", model_str)
    if match:
        suffix = match.group(1).lower()
        if suffix in VALID_THINKING_LEVELS:
            return suffix
    return None


def validate_roles_input(
    project_path: Path,
    input_data: Dict[str, Any],
) -> Tuple[str, List[Dict[str, Any]], Dict[str, Path]]:
    """Validate the entire input batch prior to any file writes.

    Returns (run_id, validated_roles, target_files_map).
    Raises ValueError or FileExistsError on any invalid input, symlink, or collision.
    """
    if not isinstance(input_data, dict):
        raise ValueError("Input data must be a JSON object")

    run_id = input_data.get("run_id")
    if not isinstance(run_id, str) or not run_id.strip():
        raise ValueError("run_id must be a non-empty string")

    roles = input_data.get("roles")
    if not isinstance(roles, list) or not roles:
        raise ValueError("roles must be a non-empty list of role definitions")

    if not project_path.exists() or not project_path.is_dir():
        raise ValueError(f"Project directory does not exist or is not a directory: {project_path}")

    _check_symlink_safety(project_path)

    agents_dir = (project_path / ".omp" / "agents").resolve()
    seen_names: Set[str] = set()
    validated_roles: List[Dict[str, Any]] = []
    target_files: Dict[str, Path] = {}

    for idx, role in enumerate(roles):
        if not isinstance(role, dict):
            raise ValueError(f"Role item at index {idx} must be a dictionary")

        name = role.get("name")
        if not isinstance(name, str) or not name.strip():
            raise ValueError(f"Role item at index {idx} has missing or empty name")
        name = name.strip()

        if not NAME_REGEX.match(name):
            raise ValueError(
                f"Invalid role name '{name}': must start with 'george-omp-' and contain only alphanumeric, dash, or underscore"
            )

        lower_name = name.lower()
        if lower_name in ("main", "sub"):
            raise ValueError(f"Role name '{name}' is reserved")

        if name in seen_names:
            raise ValueError(f"Duplicate role name in batch: '{name}'")
        seen_names.add(name)

        desc = role.get("description")
        if not isinstance(desc, str) or not desc.strip():
            raise ValueError(f"Role '{name}' description must be a non-empty string")
        if any(ord(c) < 32 and c not in "\n\t" for c in desc):
            raise ValueError(f"Role '{name}' description contains illegal control characters")

        model = role.get("model")
        if not isinstance(model, str) or not model.strip():
            raise ValueError(f"Role '{name}' model must be a non-empty string")
        model_val = model.strip()
        if any(ord(c) < 32 or ord(c) == 127 for c in model_val):
            raise ValueError(f"Role '{name}' model contains illegal control characters: {model!r}")
        if any(c.isspace() for c in model_val):
            raise ValueError(f"Role '{name}' model contains illegal whitespace: {model!r}")

        thinking = role.get("thinking")
        norm_thinking: Optional[str] = None
        if thinking is not None:
            if not isinstance(thinking, str):
                raise ValueError(f"Role '{name}' thinking must be a string or null")
            thinking_str = thinking.strip().lower()
            if thinking_str:
                if thinking_str not in VALID_THINKING_LEVELS:
                    raise ValueError(
                        f"Unsupported thinking level '{thinking}' for role '{name}'. Allowed: {sorted(VALID_THINKING_LEVELS)}"
                    )
                norm_thinking = thinking_str

        model_suffix = _extract_model_thinking_suffix(model_val)
        if model_suffix and norm_thinking:
            if model_suffix != norm_thinking:
                raise ValueError(
                    f"Model selector level suffix ':{model_suffix}' conflicts with explicit thinking '{norm_thinking}' for role '{name}'"
                )

        tools = role.get("tools")
        if tools is None or not isinstance(tools, (list, tuple)):
            raise ValueError(f"Role '{name}' tools must be an explicit list of string tool names")

        clean_tools: List[str] = []
        for t in tools:
            if not isinstance(t, str) or not t.strip():
                raise ValueError(f"Tool name in role '{name}' must be a non-empty string")
            tool_name = t.strip()
            if not SAFE_TOOL_REGEX.match(tool_name):
                raise ValueError(f"Unsafe or invalid tool name '{tool_name}' in role '{name}'")
            clean_tools.append(tool_name)

        brief = role.get("brief")
        if brief is not None and not isinstance(brief, str):
            raise ValueError(f"Role '{name}' brief must be a string")
        clean_brief = (brief or "").strip()

        target_file = agents_dir / f"{name}.md"
        if not _is_safe_subpath(target_file, project_path):
            raise ValueError(f"Path traversal detected for role file: {target_file}")

        # Broken or foreign symlinks and existing files must both be rejected
        if target_file.is_symlink() or target_file.exists():
            raise FileExistsError(f"Role destination already exists or is a symlink: {target_file}")

        target_files[name] = target_file
        validated_roles.append({
            "name": name,
            "description": desc.strip(),
            "model": model_val,
            "thinking": norm_thinking,
            "tools": clean_tools,
            "brief": clean_brief,
        })

    return run_id, validated_roles, target_files


def render_agent_markdown(
    name: str,
    description: str,
    model: str,
    thinking: Optional[str],
    tools: List[str],
    brief: str,
) -> str:
    """Render valid OMP agent definition with safe YAML frontmatter.

    spawns is always explicitly set to [] to prevent subagent recursion.
    """
    lines = [
        "---",
        f"name: {name}",
        f"description: {json.dumps(description, ensure_ascii=False)}",
        f"model: {json.dumps(model, ensure_ascii=False)}",
    ]
    if thinking:
        lines.append(f"thinking-level: {thinking}")

    if not tools:
        lines.append("tools: []")
    else:
        lines.append("tools:")
        for t in tools:
            lines.append(f"  - {t}")

    lines.append("spawns: []")
    lines.append("---")
    lines.append("")
    if brief:
        lines.append(brief)
        lines.append("")

    return "\n".join(lines)


def prepare_roles(
    project: Union[str, Path],
    role_input: Union[Dict[str, Any], str, Path],
    receipt_path: Optional[Union[str, Path]] = None,
) -> Dict[str, Any]:
    """Validate batch and write .omp/agents/<name>.md files atomically with exclusive creation."""
    project_path = Path(project).resolve()

    if isinstance(role_input, (str, Path)):
        p = Path(role_input)
        if p.exists() and p.is_file():
            input_dict = json.loads(p.read_text(encoding="utf-8"))
        else:
            input_dict = json.loads(str(role_input))
    elif isinstance(role_input, dict):
        input_dict = role_input
    else:
        raise ValueError("role_input must be a dict, JSON string, or path to JSON file")

    if receipt_path:
        rpath = Path(receipt_path).resolve()
        if rpath.is_symlink() or rpath.exists():
            raise FileExistsError(f"Receipt destination already exists or is a symlink: {rpath}")

    run_id, validated_roles, target_files = validate_roles_input(project_path, input_dict)

    agents_dir = project_path / ".omp" / "agents"
    _check_symlink_safety(project_path)
    agents_dir.mkdir(parents=True, exist_ok=True)
    _check_symlink_safety(project_path)

    written_files: List[Tuple[Path, bytes, Dict[str, Any], str]] = []
    receipt_written = False
    try:
        for role in validated_roles:
            target_file = target_files[role["name"]]
            if target_file.is_symlink():
                raise FileExistsError(f"Role destination is a symlink: {target_file}")

            md_content = render_agent_markdown(
                name=role["name"],
                description=role["description"],
                model=role["model"],
                thinking=role["thinking"],
                tools=role["tools"],
                brief=role["brief"],
            )
            raw_bytes = md_content.encode("utf-8")
            sha256_hex = hashlib.sha256(raw_bytes).hexdigest()

            with open(target_file, "xb") as f:
                f.write(raw_bytes)
            written_files.append((target_file, raw_bytes, role, sha256_hex))

        roles_receipt: List[Dict[str, Any]] = []
        ownership: List[str] = []

        for fpath, raw_bytes, role, sha256_hex in written_files:
            sha256_hash = f"sha256:{sha256_hex}"
            resolved_path = str(fpath.resolve())
            roles_receipt.append({
                "name": role["name"],
                "definition_path": resolved_path,
                "relative_path": f".omp/agents/{role['name']}.md",
                "content_hash": sha256_hash,
                "requested_model": role["model"],
                "requested_thinking": role["thinking"],
                "tools": role["tools"],
                "spawns": [],
                "status": "requested-not-observed",
            })
            ownership.append(resolved_path)

        receipt = {
            "run_id": run_id,
            "project_path": str(project_path),
            "created_at": datetime.now(timezone.utc).isoformat(),
            "roles": roles_receipt,
            "ownership": ownership,
        }

        if receipt_path:
            rpath = Path(receipt_path).resolve()
            if rpath.is_symlink():
                raise FileExistsError(f"Receipt destination is a symlink: {rpath}")
            rpath.parent.mkdir(parents=True, exist_ok=True)
            receipt_bytes = json.dumps(receipt, ensure_ascii=False, indent=2).encode("utf-8")
            with open(rpath, "xb") as rf:
                rf.write(receipt_bytes)
            receipt_written = True

    except Exception as exc:
        for fpath, _, _, expected_hex in written_files:
            try:
                if fpath.is_file() and not fpath.is_symlink():
                    if hashlib.sha256(fpath.read_bytes()).hexdigest() == expected_hex:
                        fpath.unlink()
            except Exception:
                pass

        if receipt_written and receipt_path:
            try:
                rp = Path(receipt_path).resolve()
                if rp.is_file() and not rp.is_symlink():
                    rp.unlink()
            except Exception:
                pass

        try:
            if agents_dir.exists() and agents_dir.is_dir() and not agents_dir.is_symlink():
                if _is_safe_subpath(agents_dir, project_path) and not any(agents_dir.iterdir()):
                    agents_dir.rmdir()
                    omp_dir = project_path / ".omp"
                    if omp_dir.exists() and omp_dir.is_dir() and not omp_dir.is_symlink():
                        if _is_safe_subpath(omp_dir, project_path) and not any(omp_dir.iterdir()):
                            omp_dir.rmdir()
        except Exception:
            pass

        raise exc

    return receipt


def cleanup_roles(receipt_input: Union[Dict[str, Any], str, Path]) -> Dict[str, Any]:
    """Clean up prepared roles with strict batch pre-validation and symlink refusal."""
    if isinstance(receipt_input, (str, Path)):
        p = Path(receipt_input)
        if p.exists() and p.is_file():
            receipt = json.loads(p.read_text(encoding="utf-8"))
        else:
            receipt = json.loads(str(receipt_input))
    elif isinstance(receipt_input, dict):
        receipt = receipt_input
    else:
        raise ValueError("Receipt input must be a dict, JSON string, or path to JSON file")

    if not isinstance(receipt, dict):
        raise ValueError("Receipt must be a JSON object")

    project_path_str = receipt.get("project_path")
    if not isinstance(project_path_str, str) or not project_path_str.strip():
        raise ValueError("Receipt missing or empty 'project_path'")

    project_path = Path(project_path_str).resolve()
    if not project_path.exists() or not project_path.is_dir():
        raise ValueError(f"Project directory does not exist or is not a directory: {project_path}")

    _check_symlink_safety(project_path)
    omp_dir = project_path / ".omp"
    agents_dir = omp_dir / "agents"

    roles = receipt.get("roles")
    if not isinstance(roles, list) or not roles:
        raise ValueError("Receipt 'roles' must be a non-empty list")

    ownership = receipt.get("ownership")
    if not isinstance(ownership, list):
        raise ValueError("Receipt 'ownership' must be a list")

    expected_paths: List[str] = []
    for idx, role_item in enumerate(roles):
        if not isinstance(role_item, dict):
            raise ValueError(f"Role item at index {idx} in receipt must be a dictionary")

        name = role_item.get("name")
        if not isinstance(name, str) or not NAME_REGEX.match(name):
            raise ValueError(f"Role at index {idx} has invalid name or missing prefix: {name!r}")

        def_path_str = role_item.get("definition_path")
        if not isinstance(def_path_str, str) or not def_path_str.strip():
            raise ValueError(f"Role '{name}' missing definition_path in receipt")

        expected_def_file = (agents_dir / f"{name}.md").resolve()
        try:
            given_def_file = Path(def_path_str).resolve()
        except Exception:
            raise ValueError(f"Invalid definition_path for role '{name}': {def_path_str}")

        if given_def_file != expected_def_file:
            raise ValueError(
                f"Role '{name}' definition_path ({def_path_str}) does not match expected {expected_def_file}"
            )

        if not _is_safe_subpath(given_def_file, project_path):
            raise ValueError(f"Role file escapes project path: {given_def_file}")

        content_hash = role_item.get("content_hash")
        if not isinstance(content_hash, str) or not HASH_REGEX.match(content_hash):
            raise ValueError(f"Role '{name}' has invalid content_hash format: {content_hash!r}")

        expected_paths.append(str(expected_def_file))

    normalized_ownership = [str(Path(p).resolve()) for p in ownership if isinstance(p, str)]
    if sorted(normalized_ownership) != sorted(expected_paths) or len(ownership) != len(roles):
        raise ValueError("Receipt ownership list does not match roles definition paths")

    cleaned: List[str] = []
    preserved_modified: List[Dict[str, Any]] = []
    missing: List[str] = []

    for role_item in roles:
        def_path_str = role_item["definition_path"]
        expected_hash = role_item["content_hash"]
        def_path = Path(def_path_str)

        if def_path.is_symlink():
            preserved_modified.append({
                "path": def_path_str,
                "expected_hash": expected_hash,
                "actual_hash": "symlink",
                "reason": "file is a symlink; symlinks are never followed or unlinked",
            })
            continue

        if not def_path.exists():
            missing.append(def_path_str)
            continue

        if not def_path.is_file():
            preserved_modified.append({
                "path": def_path_str,
                "expected_hash": expected_hash,
                "actual_hash": "not_regular_file",
                "reason": "target path is not a regular file",
            })
            continue

        actual_bytes = def_path.read_bytes()
        actual_hash = f"sha256:{hashlib.sha256(actual_bytes).hexdigest()}"
        if actual_hash == expected_hash:
            def_path.unlink()
            cleaned.append(def_path_str)
        else:
            preserved_modified.append({
                "path": def_path_str,
                "expected_hash": expected_hash,
                "actual_hash": actual_hash,
                "reason": "content modified since preparation",
            })

    if agents_dir.exists() and agents_dir.is_dir() and not agents_dir.is_symlink():
        try:
            if _is_safe_subpath(agents_dir, project_path) and not any(agents_dir.iterdir()):
                agents_dir.rmdir()
                if omp_dir.exists() and omp_dir.is_dir() and not omp_dir.is_symlink():
                    if _is_safe_subpath(omp_dir, project_path) and not any(omp_dir.iterdir()):
                        omp_dir.rmdir()
        except OSError:
            pass

    return {
        "cleaned": cleaned,
        "preserved_modified": preserved_modified,
        "missing": missing,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="omp_roles.py",
        description="George OMP role preparation and cleanup helper",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    prepare_p = subparsers.add_parser("prepare", help="Prepare OMP project roles")
    prepare_p.add_argument("--project", required=True, help="Target project root directory")
    prepare_p.add_argument("--input", required=True, help="Path to input JSON file or raw JSON string")
    prepare_p.add_argument("--receipt", required=True, help="Path to write output receipt JSON")

    cleanup_p = subparsers.add_parser("cleanup", help="Clean up prepared OMP project roles")
    cleanup_p.add_argument("--receipt", required=True, help="Path to receipt JSON file or raw JSON string")

    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        if args.command == "prepare":
            receipt = prepare_roles(
                project=args.project,
                role_input=args.input,
                receipt_path=args.receipt,
            )
            print(json.dumps(receipt, ensure_ascii=False, indent=2))
            return 0

        elif args.command == "cleanup":
            summary = cleanup_roles(receipt_input=args.receipt)
            print(json.dumps(summary, ensure_ascii=False, indent=2))
            return 0

        else:
            parser.print_help()
            return 1
    except Exception as exc:
        sys.stderr.write(f"Error [{args.command}]: {exc}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
