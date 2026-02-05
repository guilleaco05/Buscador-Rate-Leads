#!/usr/bin/env python3
"""
Example Echo Script

Demonstrates a deterministic execution script following DOE principles.
This script echoes a message and writes it to a temporary file.
"""

import argparse
import os
import sys
from pathlib import Path


def echo_message(message: str, repeat_count: int = 1) -> str:
    """
    Echo a message a specified number of times.
    
    Args:
        message: The message to echo
        repeat_count: Number of times to repeat (default: 1)
    
    Returns:
        The echoed message(s) as a string
    """
    if not message:
        print("Warning: Empty message provided", file=sys.stderr)
        return ""
    
    if repeat_count < 1:
        print(f"Warning: Invalid repeat count {repeat_count}, using 1", file=sys.stderr)
        repeat_count = 1
    
    result = "\n".join([message] * repeat_count)
    return result


def write_to_tmp(content: str, filename: str = "echo_output.txt") -> bool:
    """
    Write content to a temporary file.
    
    Args:
        content: Content to write
        filename: Name of the file in .tmp/
    
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the project root (parent of execution/)
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        tmp_dir = project_root / ".tmp"
        
        # Ensure .tmp directory exists
        tmp_dir.mkdir(exist_ok=True)
        
        # Write the file
        output_path = tmp_dir / filename
        output_path.write_text(content)
        
        print(f"✓ Output written to: {output_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error writing to file: {e}", file=sys.stderr)
        return False


def main():
    """Main execution function"""
    parser = argparse.ArgumentParser(
        description="Echo a message (DOE system example)"
    )
    parser.add_argument(
        "--message",
        type=str,
        required=True,
        help="Message to echo"
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of times to repeat the message (default: 1)"
    )
    
    args = parser.parse_args()
    
    # Echo the message
    result = echo_message(args.message, args.repeat)
    
    # Output to console
    print("\n" + "="*50)
    print("ECHO OUTPUT:")
    print("="*50)
    print(result)
    print("="*50 + "\n")
    
    # Write to temporary file
    write_to_tmp(result)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
