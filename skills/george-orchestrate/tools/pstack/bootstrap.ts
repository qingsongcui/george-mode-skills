import { existsSync } from "node:fs";
import { join } from "node:path";

export function ensureDependenciesInstalled(): void {
  const packagePath = join(import.meta.dir, "node_modules", "commander", "package.json");
  if (!existsSync(packagePath)) {
    throw new Error("Dependencies missing. Run bun install --frozen-lockfile in the bundled pstack tools directory explicitly.");
  }
}
