#!/usr/bin/env python3
"""
⚗️ Heisenberg // VibeCheck Guard Engine
Zero-dependency policy gatekeeper and host interceptor for AI coding agents.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

if sys.platform == "win32":
    try:
        if hasattr(sys.stdout, "reconfigure"):
            sys.stdout.reconfigure(encoding="utf-8")
        if hasattr(sys.stderr, "reconfigure"):
            sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

CONTROL_PATHS = (
    ".agents/", ".heisenberg/", ".cursor/", ".claude/", ".gemini/",
    "AGENTS.md", "CLAUDE.md", ".cursorrules", ".windsurfrules",
)
WRITE_TOOL_NAMES = {
    "write_to_file", "replace_file_content", "multi_replace_file_content",
    "Write", "TabWrite", "edit_file", "Edit", "str_replace_editor",
}

FRAMEWORK_TRIGGER_SKILL = "framework-language-guide"
SCAFFOLD_ANCHORS = {"package.json", "pyproject.toml", "Cargo.toml", "go.mod", "pom.xml"}


def read_json(path: Path) -> dict[str, Any] | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def workspace_from(payload: dict[str, Any], explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).resolve()
    for key in ("workspacePaths", "workspace_roots"):
        paths = payload.get(key)
        if isinstance(paths, list) and paths:
            return Path(paths[0]).resolve()
    return Path(payload.get("cwd", ".")).resolve()


def policy_paths(workspace: Path) -> dict[str, Path]:
    agents_root = workspace / ".agents"
    legacy_root = workspace / ".heisenberg"
    root = agents_root if agents_root.is_dir() else legacy_root
    return {
        "root": root,
        "policy": root / "policy.json",
        "skills": root / "skills.json",
        "tasks": root / "tasks",
        "artifacts": root / "artifacts",
        "receipts": root / "receipts",
        "rules": root / "rules",
    }


def all_manifests(paths: dict[str, Path]) -> list[tuple[Path, dict[str, Any]]]:
    manifests: list[tuple[Path, dict[str, Any]]] = []
    if not paths["tasks"].is_dir():
        return manifests
    for candidate in sorted(paths["tasks"].glob("*.json")):
        data = read_json(candidate)
        if data and isinstance(data, dict):
            manifests.append((candidate, data))
    return manifests


def active_manifests(paths: dict[str, Path]) -> list[tuple[Path, dict[str, Any]]]:
    return [
        item for item in all_manifests(paths)
        if item[1].get("status") in {"planned", "approved", "implementing", "verifying"}
    ]


def validate(workspace: Path, require_task: bool = False) -> tuple[bool, list[str], list[str]]:
    paths = policy_paths(workspace)
    errors: list[str] = []
    warnings: list[str] = []

    if not (workspace / "AGENTS.md").is_file():
        errors.append("AGENTS.md is missing at project root")

    policy = read_json(paths["policy"])
    skills = read_json(paths["skills"])

    if policy is None:
        errors.append(f"{paths['root'].name}/policy.json is missing or invalid JSON")
    if skills is None:
        errors.append(f"{paths['root'].name}/skills.json is missing or invalid JSON")

    if errors:
        return False, errors, warnings

    manifests = all_manifests(paths)
    if require_task and not manifests:
        errors.append("No active task manifest found in tasks/")

    known_skills = (skills or {}).get("skills", {})
    required_sets = (skills or {}).get("required_skill_sets", {})

    for path, manifest in manifests:
        task_id = manifest.get("task_id")
        task_type = manifest.get("task_type")
        status = manifest.get("status")
        selected = manifest.get("selected_skills", [])
        required = manifest.get("required_artifacts", [])
        pre_edit = manifest.get("required_before_edit", [])

        if not task_id or not isinstance(selected, list) or not selected:
            errors.append(f"{path.name}: task_id and selected_skills array are required")
            continue

        if not isinstance(pre_edit, list):
            errors.append(f"{path.name}: required_before_edit must be an array")

        if status not in {"planned", "approved", "implementing", "verifying", "complete", "blocked"}:
            errors.append(f"{path.name}: invalid status {status!r}")

        unknown = [skill for skill in selected if skill not in known_skills]
        if unknown:
            errors.append(f"{path.name}: unknown skills: {', '.join(unknown)}")

        expected_skills = required_sets.get(task_type, [])
        missing_skills = [skill for skill in expected_skills if skill not in selected]
        if missing_skills:
            errors.append(f"{path.name}: task type {task_type!r} requires skills: {', '.join(missing_skills)}")

        missing_sources = [
            skill for skill in selected
            if skill in known_skills and not (workspace / known_skills[skill].get("source", "")).is_file()
        ]
        if missing_sources:
            errors.append(f"{path.name}: skill source file is missing: {', '.join(missing_sources)}")

        artifacts_to_check = []
        if status in {"approved", "implementing", "verifying", "complete"}:
            artifacts_to_check.extend(pre_edit)
        if status in {"verifying", "complete"}:
            artifacts_to_check.extend(required)

        for artifact in dict.fromkeys(artifacts_to_check):
            artifact_file = paths["artifacts"] / task_id / artifact
            if not artifact_file.is_file():
                errors.append(f"{path.name}: missing required artifact {artifact}")
            elif artifact == "understanding.md":
                try:
                    artifact_text = artifact_file.read_text(encoding="utf-8")
                    if "Skill Attestation" not in artifact_text and "Prime Directive" not in artifact_text:
                        errors.append(
                            f"{artifact_file.name}: missing mandatory 'Skill Attestation' header "
                            f"quoting active skill's Prime Directive"
                        )
                except OSError:
                    pass

        receipt = paths["receipts"] / f"{task_id}.json"
        if status == "complete" and not receipt.is_file():
            errors.append(f"{path.name}: complete task is missing receipt {receipt.name}")

    if not active_manifests(paths):
        if manifests:
            warnings.append("All tasks are complete. Create a new manifest before editing product code.")
        else:
            warnings.append("No active task manifest found; Heisenberg is in bootstrap mode.")

    return not errors, errors, warnings


def target_path(payload: dict[str, Any], host: str) -> str:
    if host == "antigravity":
        args = payload.get("toolCall", {}).get("args", {})
        return str(args.get("TargetFile", args.get("target_file", "")))
    tool_input = payload.get("tool_input", {})
    return str(tool_input.get("path", tool_input.get("file_path", "")))


def is_control_path(path: str) -> bool:
    normalized = path.replace("\\", "/")
    return any(normalized.endswith(item) or f"/{item}" in normalized for item in CONTROL_PATHS)


def tool_name(payload: dict[str, Any], host: str) -> str:
    if host == "antigravity":
        return str(payload.get("toolCall", {}).get("name", ""))
    return str(payload.get("tool_name", payload.get("tool", "")))


def emit(host: str, event: str, allowed: bool, message: str = "") -> int:
    badge = "⚗️ [HEISENBERG VIBE-CHECK]"
    full_msg = f"{badge} {message}" if message else badge

    if host == "antigravity":
        if event == "pre-tool":
            print(json.dumps({"decision": "allow" if allowed else "deny", "reason": full_msg}))
        elif event == "pre-invocation":
            print(json.dumps({"injectSteps": [{"ephemeralMessage": full_msg}]}))
        elif event == "stop" and not allowed:
            print(json.dumps({"decision": "continue", "reason": full_msg}))
        else:
            print("{}")
    elif host == "cursor":
        print(json.dumps({"permission": "allow" if allowed else "deny", "agent_message": full_msg, "user_message": full_msg}))
    else:
        print(full_msg if not allowed else "")
    return 0 if allowed else 1


def hook(args: argparse.Namespace) -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        payload = {}

    workspace = workspace_from(payload, args.workspace)
    paths = policy_paths(workspace)
    valid, errors, warnings = validate(workspace)

    if args.event in {"session", "pre-invocation"}:
        msg = "Vibe-Check active. Pure laboratory mode." if valid else "Bootstrap needed: " + "; ".join(errors)
        return emit(args.host, args.event, True, msg)

    if args.event == "pre-tool":
        name = tool_name(payload, args.host)
        path = target_path(payload, args.host)

        if name not in WRITE_TOOL_NAMES or is_control_path(path):
            return emit(args.host, args.event, True)

        manifests = active_manifests(paths)
        if not manifests:
            return emit(args.host, args.event, False, "CONTAMINATION DETECTED: Create an active task manifest in .agents/tasks/ before modifying product code.")

        _, manifest = manifests[0]
        status = manifest.get("status")
        if status not in {"approved", "implementing"}:
            return emit(args.host, args.event, False, f"Task status is '{status}'. Must be 'approved' or 'implementing' to edit code.")

        files_in_scope = manifest.get("files_in_scope", [])
        if files_in_scope and path:
            norm_target = path.replace("\\", "/").lstrip("/")
            in_scope = any(
                norm_target.endswith(f.replace("\\", "/").lstrip("/")) or
                f.replace("\\", "/").lstrip("/") in norm_target
                for f in files_in_scope
            )
            if not in_scope:
                return emit(args.host, args.event, False, f"SCOPE VIOLATION: '{path}' is not declared in files_in_scope for {manifest.get('task_id')}.")

        task_id = manifest.get("task_id", "")
        missing = [
            artifact for artifact in manifest.get("required_before_edit", [])
            if not (paths["artifacts"] / task_id / artifact).is_file()
        ]
        if missing:
            return emit(args.host, args.event, False, f"MISSING PRE-EDIT ARTIFACTS: Generate {', '.join(missing)} first.")

        return emit(args.host, args.event, True)

    if args.event == "stop" or args.event == "pre-commit":
        valid, errors, _ = validate(workspace)
        if not valid:
            return emit(args.host, args.event, False, "Commit blocked. Vibe-Check failed: " + "; ".join(errors))
        return emit(args.host, args.event, True)

    return emit(args.host, args.event, True)


def print_banner():
    try:
        print("""
 ⚗️  H E I S E N B E R G  //  V I B E C H E C K
 ===============================================
  99.1% Pure Governance Engine for AI Agents
""")
    except UnicodeEncodeError:
        print("""
 [HEISENBERG // VIBECHECK]
 ===============================================
  99.1% Pure Governance Engine for AI Agents
""")


def main() -> int:
    parser = argparse.ArgumentParser(description="⚗️ Heisenberg Vibe-Check Engine")
    subparsers = parser.add_subparsers(dest="command", required=True)

    validate_parser = subparsers.add_parser("validate", help="Validate workspace compliance")
    validate_parser.add_argument("--workspace", default=".")
    validate_parser.add_argument("--require-task", action="store_true")

    hook_parser = subparsers.add_parser("hook", help="Lifecycle hook interceptor")
    hook_parser.add_argument("--host", choices=("antigravity", "cursor", "claude", "git"), default="git")
    hook_parser.add_argument("--event", required=True)
    hook_parser.add_argument("--workspace")

    args = parser.parse_args()

    if args.command == "validate":
        print_banner()
        workspace = Path(args.workspace).resolve()
        valid, errors, warnings = validate(workspace, args.require_task)

        if valid:
            try:
                print("✅ VIBE-CHECK PASSED: Codebase is 99.1% pure. All gates satisfied.\n")
                if warnings:
                    for w in warnings:
                        print(f"⚠️  Note: {w}")
            except UnicodeEncodeError:
                print("[PASS] VIBE-CHECK PASSED: Codebase is 99.1% pure. All gates satisfied.\n")
                if warnings:
                    for w in warnings:
                        print(f"[*] Note: {w}")
            return 0
        else:
            try:
                print("❌ VIBE-CHECK FAILED: Contamination detected in workspace:\n")
                for e in errors:
                    print(f"   • {e}")
                print("\n⛔ Fix the violations before proceeding.\n")
            except UnicodeEncodeError:
                print("[FAIL] VIBE-CHECK FAILED: Contamination detected in workspace:\n")
                for e in errors:
                    print(f"   * {e}")
                print("\n[!] Fix the violations before proceeding.\n")
            return 1

    return hook(args)


if __name__ == "__main__":
    raise SystemExit(main())
