#!/usr/bin/env python3
"""
Command-line interface for the Cursor API SDK.
"""

import argparse
import asyncio
import json
import sys
from pathlib import Path
from typing import Optional

from .cursor_api import CursorAPI, CursorAPIError


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Cursor API SDK Command Line Interface",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate code
  cursor-api generate "Create a Python function to calculate fibonacci numbers"
  
  # Review code from a file
  cursor-api review --file mycode.py
  
  # Generate tests
  cursor-api tests --file mycode.py --framework pytest
  
  # Chat with the AI
  cursor-api chat "What is the best way to handle errors in Python?"
  
  # Debug code with error
  cursor-api debug --file mycode.py --error "IndexError: list index out of range"
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    generate_parser = subparsers.add_parser("generate", help="Generate code")
    generate_parser.add_argument("prompt", help="Code generation prompt")
    generate_parser.add_argument("--language", "-l", default="python", help="Programming language")
    generate_parser.add_argument("--output", "-o", help="Output file path")
    generate_parser.add_argument("--max-tokens", type=int, default=1000, help="Maximum tokens to generate")
    
    # Review command
    review_parser = subparsers.add_parser("review", help="Review code")
    review_parser.add_argument("--file", "-f", required=True, help="File to review")
    review_parser.add_argument("--language", "-l", default="python", help="Programming language")
    review_parser.add_argument("--focus", nargs="+", help="Focus areas (e.g., performance security readability)")
    review_parser.add_argument("--output", "-o", help="Output file path")
    
    # Tests command
    tests_parser = subparsers.add_parser("tests", help="Generate unit tests")
    tests_parser.add_argument("--file", "-f", required=True, help="File to generate tests for")
    tests_parser.add_argument("--language", "-l", default="python", help="Programming language")
    tests_parser.add_argument("--framework", help="Test framework (e.g., pytest, unittest)")
    tests_parser.add_argument("--output", "-o", help="Output file path")
    
    # Chat command
    chat_parser = subparsers.add_parser("chat", help="Chat with the AI")
    chat_parser.add_argument("message", help="Message to send")
    chat_parser.add_argument("--temperature", "-t", type=float, default=0.7, help="Response temperature")
    chat_parser.add_argument("--max-tokens", type=int, help="Maximum tokens to generate")
    
    # Debug command
    debug_parser = subparsers.add_parser("debug", help="Debug code with error")
    debug_parser.add_argument("--file", "-f", required=True, help="File with the error")
    debug_parser.add_argument("--error", "-e", required=True, help="Error message")
    debug_parser.add_argument("--language", "-l", default="python", help="Programming language")
    debug_parser.add_argument("--output", "-o", help="Output file path")
    
    # Documentation command
    docs_parser = subparsers.add_parser("docs", help="Generate documentation")
    docs_parser.add_argument("--file", "-f", required=True, help="File to document")
    docs_parser.add_argument("--language", "-l", default="python", help="Programming language")
    docs_parser.add_argument("--format", default="docstring", help="Documentation format")
    docs_parser.add_argument("--output", "-o", help="Output file path")
    
    # Refactor command
    refactor_parser = subparsers.add_parser("refactor", help="Refactor code")
    refactor_parser.add_argument("--file", "-f", required=True, help="File to refactor")
    refactor_parser.add_argument("--improvements", "-i", nargs="+", required=True, help="Improvements to apply")
    refactor_parser.add_argument("--language", "-l", default="python", help="Programming language")
    refactor_parser.add_argument("--output", "-o", help="Output file path")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    try:
        asyncio.run(run_command(args))
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except CursorAPIError as e:
        print(f"Cursor API Error: {e.message}", file=sys.stderr)
        if e.status_code:
            print(f"Status Code: {e.status_code}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)


async def run_command(args):
    """Run the specified command."""
    async with CursorAPI() as cursor:
        if args.command == "generate":
            await handle_generate(cursor, args)
        elif args.command == "review":
            await handle_review(cursor, args)
        elif args.command == "tests":
            await handle_tests(cursor, args)
        elif args.command == "chat":
            await handle_chat(cursor, args)
        elif args.command == "debug":
            await handle_debug(cursor, args)
        elif args.command == "docs":
            await handle_docs(cursor, args)
        elif args.command == "refactor":
            await handle_refactor(cursor, args)


async def handle_generate(cursor: CursorAPI, args):
    """Handle the generate command."""
    code = await cursor.generate_code_async(
        args.prompt,
        language=args.language,
        max_tokens=args.max_tokens
    )
    
    if args.output:
        Path(args.output).write_text(code)
        print(f"Generated code saved to {args.output}")
    else:
        print("Generated code:")
        print(code)


async def handle_review(cursor: CursorAPI, args):
    """Handle the review command."""
    code = Path(args.file).read_text()
    review = cursor.review_code(
        code,
        language=args.language,
        focus_areas=args.focus
    )
    
    if args.output:
        Path(args.output).write_text(review)
        print(f"Code review saved to {args.output}")
    else:
        print("Code review:")
        print(review)


async def handle_tests(cursor: CursorAPI, args):
    """Handle the tests command."""
    code = Path(args.file).read_text()
    tests = cursor.generate_tests(
        code,
        language=args.language,
        test_framework=args.framework
    )
    
    if args.output:
        Path(args.output).write_text(tests)
        print(f"Generated tests saved to {args.output}")
    else:
        print("Generated tests:")
        print(tests)


async def handle_chat(cursor: CursorAPI, args):
    """Handle the chat command."""
    messages = [{"role": "user", "content": args.message}]
    
    response = await cursor.chat_completion_async(
        messages,
        temperature=args.temperature,
        max_tokens=args.max_tokens
    )
    
    print("AI Response:")
    print(response["choices"][0]["message"]["content"])


async def handle_debug(cursor: CursorAPI, args):
    """Handle the debug command."""
    code = Path(args.file).read_text()
    solution = cursor.debug_code(
        code,
        args.error,
        language=args.language
    )
    
    if args.output:
        Path(args.output).write_text(solution)
        print(f"Debug solution saved to {args.output}")
    else:
        print("Debug solution:")
        print(solution)


async def handle_docs(cursor: CursorAPI, args):
    """Handle the docs command."""
    code = Path(args.file).read_text()
    docs = cursor.generate_documentation(
        code,
        language=args.language,
        doc_format=args.format
    )
    
    if args.output:
        Path(args.output).write_text(docs)
        print(f"Generated documentation saved to {args.output}")
    else:
        print("Generated documentation:")
        print(docs)


async def handle_refactor(cursor: CursorAPI, args):
    """Handle the refactor command."""
    code = Path(args.file).read_text()
    refactored = cursor.refactor_code(
        code,
        args.improvements,
        language=args.language
    )
    
    if args.output:
        Path(args.output).write_text(refactored)
        print(f"Refactored code saved to {args.output}")
    else:
        print("Refactored code:")
        print(refactored)


if __name__ == "__main__":
    main()