"""Command-line interface for meta-stripper."""

import sys
import argparse
from pathlib import Path
from typing import List, Optional
from . import __version__
from .core import strip_metadata, display_metadata


def parse_args(args: Optional[List[str]] = None) -> argparse.Namespace:
    """Parse command-line arguments.
    
    Args:
        args: List of arguments to parse (defaults to sys.argv)
        
    Returns:
        Parsed arguments namespace
    """
    parser = argparse.ArgumentParser(
        prog='metastripper',
        description='Privacy-focused metadata removal tool for documents',
        epilog='Supported formats: PDF, DOCX'
    )
    
    parser.add_argument(
        'files',
        nargs='+',
        type=Path,
        help='File(s) to process'
    )
    
    parser.add_argument(
        '-o', '--output',
        type=Path,
        help='Output file path (only valid for single file input)'
    )
    
    parser.add_argument(
        '-s', '--show',
        action='store_true',
        help='Display metadata without stripping'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
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


def process_file(filepath: Path, output_path: Optional[Path], show_only: bool, verbose: bool) -> bool:
    """Process a single file.
    
    Args:
        filepath: Path to input file
        output_path: Optional output path
        show_only: If True, only display metadata
        verbose: Enable verbose output
        
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
        else:
            # Strip metadata mode
            if verbose:
                print(f"Processing: {filepath}")
                
            result_path = strip_metadata(filepath, output_path)
            
            print(f"✓ Successfully stripped metadata from {filepath.name}")
            print(f"  Output saved to: {result_path}")
            return True
            
    except ValueError as e:
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
    
    # Validate arguments
    if args.output and len(args.files) > 1:
        print("✗ Error: --output can only be used with a single input file", file=sys.stderr)
        return 1
    
    # Process files
    success_count = 0
    total_count = len(args.files)
    
    for filepath in args.files:
        if process_file(filepath, args.output, args.show, args.verbose):
            success_count += 1
    
    # Summary for multiple files
    if total_count > 1 and not args.show:
        print(f"\n{'='*60}")
        print(f"Summary: {success_count}/{total_count} files processed successfully")
        print(f"{'='*60}")
    
    return 0 if success_count == total_count else 1


if __name__ == '__main__':
    sys.exit(main())
