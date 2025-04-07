import os
import re

BASE_PACKAGE = "persichetti"
TOP_DIR = os.path.join(os.getcwd(), BASE_PACKAGE)

# Regex patterns for bad imports
BAD_IMPORT_PATTERNS = [
    r'^import (\w+)',                                # e.g. import core
    r'^from (\w+) import (\w+)',                     # e.g. from core import x
    r'^from (\.\w+|\.\.+) import (\w+)',             # e.g. from . import x (relative)
]

def check_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    rel_path = os.path.relpath(filepath, TOP_DIR)
    module_path = rel_path.replace('\\', '/').replace('.py', '').replace('/', '.')
    if module_path.endswith('__init__'):
        module_path = module_path.rsplit('.', 1)[0]

    problems = []

    for i, line in enumerate(lines):
        for pattern in BAD_IMPORT_PATTERNS:
            match = re.match(pattern, line.strip())
            if match:
                problems.append((i+1, line.strip()))

    return module_path, problems


def main():
    print(f"🔍 Scanning '{TOP_DIR}' for bad imports...\n")
    total_issues = 0
    for root, _, files in os.walk(TOP_DIR):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                module_path, problems = check_file(filepath)
                if problems:
                    print(f"📄 {filepath}:")
                    for lineno, bad_line in problems:
                        print(f"  Line {lineno}: {bad_line}")
                    print()
                    total_issues += len(problems)

    if total_issues == 0:
        print("✅ No bad imports found. Everything looks clean.")
    else:
        print(f"⚠️ Found {total_issues} import issues that may need fixing.")


if __name__ == '__main__':
    main()
