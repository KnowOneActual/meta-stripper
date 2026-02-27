"""Command-line interface for meta-stripper."""

import argparse
import sys
from pathlib import Path
from typing import List, Optional

from . import __version__
from .core import display_metadata, strip_metadata

# List of supported extensions for recursive processing
SUPPORTED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".xlsx",
    ".pptx",
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
}


def get_files_to_process(paths: List[Path], recursive: bool = False) -> List[Path]:
    """Get a list of files to process, optionally recursing into directories.

    Args:
        paths: List of input paths (files or directories)
        recursive: Whether to recurse into directories

    Returns:
        List of paths to files that should be processed
    """
    files = []
    for path in paths:
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            if recursive:
                # Use glob to find all files and filter by extension
                # This is more efficient than multiple rglob calls
                for p in path.rglob("*"):
                    if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS:
                        files.append(p)
            else:
                # If not recursive, just warn about directories
                print(f"⚠ Warning: {path} is a directory. Use --recursive to process.")

    # Remove duplicates and ensure paths exist
    unique_files = sorted(list(set(f for f in files if f.exists())))
    return unique_files


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.

    Args:
        args: List of arguments to parse (defaults to sys.argv)

    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog="metastripper",
        description="Privacy-focused metadata removal tool for documents and images",
        epilog="Supported formats: PDF, DOCX, XLSX, PPTX, JPEG, PNG, WebP",
    )

    parser.add_argument("files", nargs="+", type=Path, help="File(s) or director(ies) to process")

    parser.add_argument(
        "-o", "--output", type=Path, help="Output file path (only valid for single file input)"
    )

    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Recursively process directories"
    )

    parser.add_argument(
        "-i", "--in-place", action="store_true", help="Modify files in-place (overwrites original)"
    )

    parser.add_argument(
        "--backup", action="store_true", help="Create a backup file when using --in-place"
    )

    parser.add_argument(
        "--dry-run", action="store_true", help="Show which files would be processed without modification"
    )

    parser.add_argument(
        "--keep",
        nargs="+",
        metavar="FIELD",
        help="Selective preservation: Keep only these metadata fields",
    )

    parser.add_argument(
        "--remove",
        nargs="+",
        metavar="FIELD",
        help="Selective removal: Remove only these metadata fields",
    )

    parser.add_argument(
        "-s", "--show", action="store_true", help="Display metadata without stripping"
    )

    parser.add_argument("-v", "--verbose", action="store_true", help="Enable verbose output")

    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")

    return parser.parse_args(args)


def print_metadata(filepath: Path, metadata: Optional[dict]) -> None:
    """Pretty print metadata from a file.

    Args:
        filepath: Path to the file
        metadata: Metadata dictionary or None
    """
    print(f"\n{'='*60}")
    print(f"Metadata for: {filepath.name}")
    print(f"{'='*60}")

    if metadata:
        for key, value in metadata.items():
            print(f"{key:20} : {value}")
    else:
        print("No metadata found.")
    print(f"{'='*60}\n")


def process_file(
    filepath: Path,
    output_path: Optional[Path],
    show_only: bool,
    verbose: bool,
    in_place: bool = False,
    backup: bool = False,
    dry_run: bool = False,
    keep_fields: Optional[list] = None,
    remove_fields: Optional[list] = None,
) -> bool:
    """Process a single file.

    Args:
        filepath: Path to input file
        output_path: Optional output path
        show_only: If True, only display metadata
        verbose: Enable verbose output
        in_place: If True, overwrite original file
        backup: If True, create backup of original
        dry_run: If True, don't perform actual processing
        keep_fields: Optional list of fields to preserve
        remove_fields: Optional list of fields to explicitly remove

    Returns:
        True if successful, False otherwise
    """
    try:
        if not filepath.exists():
            print(f"✗ Error: File not found: {filepath}", file=sys.stderr)
            return False

        if show_only:
            # Display metadata mode
            metadata = display_metadata(filepath)
            print_metadata(filepath, metadata)
            return True

        if dry_run:
            if verbose:
                print(f"[DRY-RUN] Processing: {filepath}")
            return True

        # Strip metadata mode
        if verbose:
            print(f"Processing: {filepath}")

        # Determine output location
        final_output = output_path
        if in_place:
            # For in-place, strip to a temporary file first
            temp_output = filepath.parent / f".tmp_{filepath.name}"
            try:
                strip_metadata(
                    filepath,
                    temp_output,
                    keep_fields=keep_fields,
                    remove_fields=remove_fields,
                )

                if backup:
                    backup_path = filepath.with_suffix(filepath.suffix + ".bak")
                    filepath.replace(backup_path)
                    if verbose:
                        print(f"  Backup created: {backup_path}")

                # Replace original with the temporary clean version
                temp_output.replace(filepath)
                print(f"✓ Successfully stripped metadata from {filepath.name} (in-place)")
                return True
            finally:
                if temp_output.exists():
                    temp_output.unlink()
        else:
            result_path = strip_metadata(
                filepath, output_path, keep_fields=keep_fields, remove_fields=remove_fields
            )
            print(f"✓ Successfully stripped metadata from {filepath.name}")
            print(f"  Output saved to: {result_path}")
            return True

    except (ValueError, FileNotFoundError) as e:
        print(f"✗ Error: {e}", file=sys.stderr)
        return False
    except Exception as e:
        print(f"✗ Unexpected error processing {filepath}: {e}", file=sys.stderr)
        return False


def main() -> int:
    """Main entry point for CLI.

    Returns:
        Exit code (0 for success, 1 for error)
    """
    args = parse_args()

    # Get all files to process (handles recursion)
    files_to_process = get_files_to_process(args.files, args.recursive)

    if not files_to_process:
        if not any(p.is_dir() for p in args.files):
            print("✗ Error: No valid files found to process", file=sys.stderr)
            return 1
        return 0

    # Validate arguments
    if args.output and len(files_to_process) > 1:
        print("✗ Error: --output can only be used with a single input file", file=sys.stderr)
        return 1

    if args.in_place and args.output:
        print("✗ Error: --in-place and --output are mutually exclusive", file=sys.stderr)
        return 1

    if args.keep and args.remove:
        print("✗ Error: --keep and --remove are mutually exclusive", file=sys.stderr)
        return 1

    if args.dry_run:
        print(f"--- DRY RUN: Found {len(files_to_process)} files to process ---")
        if not args.verbose:
            for f in files_to_process:
                print(f"  [DRY-RUN] Would process: {f}")

    # Process files
    success_count = 0
    total_count = len(files_to_process)

    for filepath in files_to_process:
        if process_file(
            filepath,
            args.output,
            args.show,
            args.verbose,
            args.in_place,
            args.backup,
            args.dry_run,
            keep_fields=args.keep,
            remove_fields=args.remove,
        ):
            success_count += 1

    # Summary for multiple files
    if total_count > 1 and not args.show:
        print(f"\n{'='*60}")
        if args.dry_run:
            print(f"Dry-run summary: {total_count} files would be processed")
        else:
            print(f"Summary: {success_count}/{total_count} files processed successfully")
        print(f"{'='*60}")

    return 0 if success_count == total_count or args.dry_run else 1


if __name__ == "__main__":
    sys.exit(main())
