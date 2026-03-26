import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]

ROOT_REQUIRED_FILES = {
    "README.md",
    "AGENTS.md",
    ".gitignore",
}
ROOT_OPTIONAL_COMPAT_FILES = {"CLAUDE.md"}

ROOT_REQUIRED_DIRS = {
    "dev",
    "scripts",
}
ROOT_OPTIONAL_DIRS = {"doc"}

RUNBOOK_ACTIVE_ALLOWED = {"README.md", "REGISTRY.md"}
SCRIPTS_ROOT_ALLOWED = {"README.md", "export_incident.py", "bitacora_append.py"}


def check_root(errors, warnings):
    root_entries = {p.name for p in REPO_ROOT.iterdir() if p.name != ".git"}
    for file_name in ROOT_REQUIRED_FILES:
        if file_name not in root_entries:
            errors.append(f"Missing required root file: {file_name}")
    for dir_name in ROOT_REQUIRED_DIRS:
        if dir_name not in root_entries:
            errors.append(f"Missing required root directory: {dir_name}")

    if "__pycache__" in root_entries:
        errors.append("Transient directory present in root: __pycache__")

    noisy = [name for name in sorted(root_entries) if name.endswith(".pyc")]
    for name in noisy:
        errors.append(f"Transient compiled file in root: {name}")


def check_scripts(errors, warnings):
    scripts_dir = REPO_ROOT / "scripts"
    if not scripts_dir.exists():
        errors.append("Missing scripts directory")
        return

    for required in ("dev", "ops", "migration"):
        if not (scripts_dir / required).exists():
            errors.append(f"Missing scripts subdirectory: scripts/{required}")

    root_files = {p.name for p in scripts_dir.iterdir() if p.is_file()}
    for file_name in root_files:
        if file_name not in SCRIPTS_ROOT_ALLOWED:
            warnings.append(f"Non-standard file in scripts root: scripts/{file_name}")


def check_runbooks(errors, warnings):
    runbooks_dir = REPO_ROOT / "dev" / "runbooks"
    if not runbooks_dir.exists():
        return

    files = {p.name for p in runbooks_dir.iterdir() if p.is_file()}
    for file_name in files:
        if file_name not in RUNBOOK_ACTIVE_ALLOWED:
            warnings.append(f"Unexpected file in active runbooks folder: dev/runbooks/{file_name}")

    legacy_runbooks = REPO_ROOT / "dev" / "records" / "legacy" / "runbooks"
    if files and not legacy_runbooks.exists():
        warnings.append("Active runbooks present without legacy quarantine folder")


def check_policies(errors):
    policy_dir = REPO_ROOT / "dev" / "policies"
    required = {
        "action_policy.md",
        "ai_engineering_governance.md",
        "exception_rules.md",
        "git_workflow_rules.md",
        "governance_manifest.md",
        "documentation_rules.md",
        "scripts_rules.md",
        "bitacora_rules.md",
        "naming_rules.md",
        "repo_layout_rules.md",
    }
    if not policy_dir.exists():
        errors.append("Missing dev/policies directory")
        return

    present = {p.name for p in policy_dir.iterdir() if p.is_file()}
    for name in sorted(required):
        if name not in present:
            errors.append(f"Missing policy file: dev/policies/{name}")


def main():
    errors = []
    warnings = []

    check_root(errors, warnings)
    check_scripts(errors, warnings)
    check_runbooks(errors, warnings)
    check_policies(errors)

    print("State0 compliance report")
    print("------------------------")
    print(f"Errors: {len(errors)}")
    print(f"Warnings: {len(warnings)}")

    if errors:
        print("\nErrors:")
        for item in errors:
            print(f"- {item}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"- {item}")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

