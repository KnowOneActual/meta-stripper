#!/usr/bin/env python3
"""Script to automatically fix linting issues in handler files."""

import re
from pathlib import Path


def fix_bare_except(content: str) -> str:
    """Fix E722: Replace bare except with except Exception."""
    # Replace 'except:' with 'except Exception:'
    return re.sub(r'(\s+)except:\s*$', r'\1except Exception:', content, flags=re.MULTILINE)


def fix_exception_chaining(content: str) -> str:
    """Fix B904: Add 'from e' or 'from None' to raise statements in except blocks."""
    # Pattern: raise Exception(...) in except block
    # Add 'from e' if 'as e' exists, otherwise 'from None'
    
    # For cases with 'except Exception as e:'
    pattern1 = r'(except \w+(?:\.\w+)* as e:.*?\n.*?)(raise \w+\([^)]+\))'
    
    def replace_with_from_e(match):
        prefix = match.group(1)
        raise_stmt = match.group(2)
        if 'from' not in raise_stmt:
            return prefix + raise_stmt + ' from e'
        return match.group(0)
    
    content = re.sub(pattern1, replace_with_from_e, content, flags=re.DOTALL)
    return content


def fix_nested_with(content: str) -> str:
    """Fix SIM117: Combine nested with statements."""
    # Pattern: with X as y:\n    with ZipFile(a) as b:\n        with ZipFile(c) as d:
    pattern = r'(\s+)with (\S+)\(([^)]+)\) as (\w+):\s*\n\s+with (\S+)\(([^)]+)\) as (\w+):'
    replacement = r'\1with \2(\3) as \4, \5(\6) as \7:'
    return re.sub(pattern, replacement, content)


def fix_ret504(content: str) -> str:
    """Fix RET504: Remove unnecessary variable assignment before return."""
    # Pattern: var = {dict comp}\n            return var
    pattern = r'(\s+)(\w+) = (\{[^}]+\})\s*\n\s+return \2'
    replacement = r'\1return \3'
    return re.sub(pattern, replacement, content)


def fix_pth123(content: str) -> str:
    """Fix PTH123: Replace open() with Path.open()."""
    # This is trickier - need to check if Path is used
    # Replace 'with open(filepath' with 'with filepath.open('
    # Replace 'with open(input_path' with 'with input_path.open('
    # Replace 'with open(output_path' with 'with output_path.open('
    
    content = re.sub(r'with open\((filepath), "([rb]+)"\)', r'with \1.open("\2")', content)
    content = re.sub(r'with open\((input_path), "([rb]+)"\)', r'with \1.open("\2")', content)
    content = re.sub(r'with open\((output_path), "([rwb]+)"\)', r'with \1.open("\2")', content)
    content = re.sub(r'with open\((f_in), "([rb]+)"\)', r'with \1.open("\2")', content)
    content = re.sub(r'with open\((f_out), "([wb]+)"\)', r'with \1.open("\2")', content)
    
    return content


def fix_file(filepath: Path) -> bool:
    """Fix linting issues in a single file."""
    print(f"Fixing {filepath}...")
    
    content = filepath.read_text()
    original = content
    
    # Apply all fixes
    content = fix_bare_except(content)
    content = fix_exception_chaining(content)
    content = fix_nested_with(content)
    content = fix_ret504(content)
    content = fix_pth123(content)
    
    if content != original:
        filepath.write_text(content)
        print(f"  ✓ Fixed {filepath.name}")
        return True
    else:
        print(f"  - No changes needed for {filepath.name}")
        return False


def main():
    """Fix all handler files."""
    src_dir = Path("src/metastripper")
    handlers_dir = src_dir / "handlers"
    
    files_to_fix = [
        src_dir / "cli.py",
        handlers_dir / "base.py",
        handlers_dir / "pdf.py",
        handlers_dir / "docx.py",
        handlers_dir / "jpeg.py",
        handlers_dir / "png.py",
        handlers_dir / "webp.py",
        handlers_dir / "xlsx.py",
        handlers_dir / "pptx.py",
    ]
    
    fixed_count = 0
    for filepath in files_to_fix:
        if filepath.exists():
            if fix_file(filepath):
                fixed_count += 1
        else:
            print(f"Warning: {filepath} not found")
    
    print(f"\n✓ Fixed {fixed_count} files")
    print("\nNow run: make format && make check")


if __name__ == "__main__":
    main()
