# Cursor API SDK

A comprehensive SDK for interacting with the Cursor API, providing AI-powered code generation, review, testing, and documentation capabilities.

## Features

- 🤖 **AI Code Generation** - Generate code from natural language descriptions
- 🔍 **Code Review** - Get AI-powered code reviews and suggestions
- 🧪 **Test Generation** - Automatically generate unit tests for your code
- 📚 **Documentation** - Generate comprehensive documentation
- 🔧 **Code Refactoring** - Refactor code with specific improvements
- 🐛 **Debugging** - Get help debugging code with error messages
- 💬 **Chat Interface** - Interactive chat with the AI assistant
- ⚡ **Async Support** - Full async/await support for high-performance applications
- 🚀 **Rate Limiting** - Built-in rate limiting and retry logic
- 📦 **Multiple Languages** - Support for JavaScript/TypeScript and Python

## Installation

### Python SDK

```bash
pip install cursor-api-sdk
```

Or install from source:

```bash
git clone https://github.com/yourusername/cursor-api-sdk.git
cd cursor-api-sdk
pip install -e .
```

### JavaScript SDK

```bash
npm install cursor-api-sdk
```

Or install from source:

```bash
git clone https://github.com/yourusername/cursor-api-sdk.git
cd cursor-api-sdk
npm install
npm run build
```

## Quick Start

### Python

```python
import os
from cursor_api_sdk import CursorAPI

# Set your API key
os.environ['CURSOR_API_KEY'] = 'your-api-key-here'

# Create a client
cursor = CursorAPI()

# Generate code
code = cursor.generate_code(
    "Create a function to calculate fibonacci numbers",
    language="python"
)
print(code)

# Review code
review = cursor.review_code(code, language="python")
print(review)

# Generate tests
tests = cursor.generate_tests(code, language="python", test_framework="pytest")
print(tests)
```

### JavaScript

```javascript
import { CursorAPI } from 'cursor-api-sdk';

const cursor = new CursorAPI(process.env.CURSOR_API_KEY);

// Generate code
const code = await cursor.generateCode(
  'Create a React component for a todo list',
  'jsx'
);
console.log(code);

// Review code
const review = await cursor.reviewCode(code, 'jsx');
console.log(review);
```

### Command Line Interface (Python)

```bash
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
```

## API Reference

### Python SDK

#### CursorAPI Class

The main client class for interacting with the Cursor API.

```python
from cursor_api_sdk import CursorAPI

cursor = CursorAPI(api_key="your-api-key")
```

##### Methods

- `chat_completion(messages, model="cursor-1.0", temperature=0.7, max_tokens=None, **kwargs)` - Send chat completion requests
- `generate_code(prompt, language="python", max_tokens=1000, **kwargs)` - Generate code from a prompt
- `review_code(code, language="python", focus_areas=None)` - Review code and provide suggestions
- `generate_tests(code, language="python", test_framework=None)` - Generate unit tests
- `generate_documentation(code, language="python", doc_format="docstring")` - Generate documentation
- `refactor_code(code, improvements, language="python")` - Refactor code with specific improvements
- `debug_code(code, error_message, language="python")` - Debug code with error information

##### Async Methods

- `chat_completion_async(messages, model="cursor-1.0", temperature=0.7, max_tokens=None, **kwargs)` - Async chat completion
- `generate_code_async(prompt, language="python", max_tokens=1000, **kwargs)` - Async code generation
- `batch_process(prompts, **kwargs)` - Process multiple prompts asynchronously

### JavaScript SDK

#### CursorAPI Class

```javascript
import { CursorAPI } from 'cursor-api-sdk';

const cursor = new CursorAPI(apiKey);
```

##### Methods

- `chatCompletion(messages, options)` - Send chat completion requests
- `generateCode(prompt, language, options)` - Generate code from a prompt
- `reviewCode(code, language, options)` - Review code and provide suggestions
- `generateTests(code, language, testFramework, options)` - Generate unit tests
- `generateDocumentation(code, language, format, options)` - Generate documentation
- `refactorCode(code, improvements, language, options)` - Refactor code
- `debugCode(code, errorMessage, language, options)` - Debug code

## Examples

### Code Generation

```python
# Generate a React component
code = cursor.generate_code(
    "Create a React component for a user profile card with avatar, name, and bio",
    language="jsx"
)

# Generate a Python class
code = cursor.generate_code(
    "Create a Python class for managing a shopping cart with add, remove, and total methods",
    language="python"
)
```

### Code Review

```python
code = """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
"""

review = cursor.review_code(
    code, 
    language="python",
    focus_areas=["performance", "readability"]
)
```

### Test Generation

```python
code = """
def add_numbers(a, b):
    return a + b
"""

tests = cursor.generate_tests(
    code,
    language="python",
    test_framework="pytest"
)
```

### Documentation Generation

```python
code = """
def calculate_area(radius):
    return 3.14159 * radius * radius
"""

docs = cursor.generate_documentation(
    code,
    language="python",
    doc_format="docstring"
)
```

### Code Refactoring

```python
code = """
def process_data(data):
    result = []
    for item in data:
        if item > 0:
            result.append(item * 2)
    return result
"""

refactored = cursor.refactor_code(
    code,
    improvements=["use list comprehension", "add type hints"],
    language="python"
)
```

### Debugging

```python
code = """
def get_item(items, index):
    return items[index]
"""

solution = cursor.debug_code(
    code,
    "IndexError: list index out of range",
    language="python"
)
```

## Configuration

### Environment Variables

Set your Cursor API key as an environment variable:

```bash
export CURSOR_API_KEY="your-api-key-here"
```

### Custom Configuration

```python
from cursor_api_sdk import CursorAPI, CursorConfig

config = CursorConfig(
    api_key="your-api-key",
    base_url="https://api.cursor.sh/v1",
    timeout=30,
    max_retries=3,
    rate_limit_per_minute=60
)

cursor = CursorAPI(config=config)
```

## Rate Limiting

The SDK includes built-in rate limiting to respect API limits:

```python
# Custom rate limiting
from cursor_api_sdk import rate_limit

@rate_limit(calls_per_minute=30)
def my_api_function():
    # Your API calls here
    pass
```

## Error Handling

```python
from cursor_api_sdk import CursorAPI, CursorAPIError

try:
    cursor = CursorAPI()
    result = cursor.generate_code("Some prompt")
except CursorAPIError as e:
    print(f"API Error: {e.message}")
    print(f"Status Code: {e.status_code}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Async Usage

```python
import asyncio
from cursor_api_sdk import CursorAPI

async def main():
    async with CursorAPI() as cursor:
        # Generate code asynchronously
        code = await cursor.generate_code_async(
            "Create a Python function to sort a list",
            language="python"
        )
        print(code)
        
        # Batch process multiple prompts
        prompts = [
            "Create a function to validate email",
            "Create a function to generate random password",
            "Create a function to format date"
        ]
        
        results = await cursor.batch_process(prompts)
        for i, result in enumerate(results):
            print(f"Result {i+1}: {result}")

asyncio.run(main())
```

## CLI Usage

The Python SDK includes a command-line interface:

```bash
# Generate code
cursor-api generate "Create a Python function to calculate fibonacci numbers" --language python

# Review code from file
cursor-api review --file mycode.py --language python --focus performance readability

# Generate tests
cursor-api tests --file mycode.py --language python --framework pytest --output tests.py

# Chat with AI
cursor-api chat "What are the best practices for Python error handling?" --temperature 0.8

# Debug code
cursor-api debug --file mycode.py --error "TypeError: unsupported operand type(s) for +: 'int' and 'str'" --language python

# Generate documentation
cursor-api docs --file mycode.py --language python --format markdown --output README.md

# Refactor code
cursor-api refactor --file mycode.py --improvements "use list comprehension" "add type hints" --language python --output refactored.py
```

## Best Practices

1. **Always handle errors gracefully** - Use try-catch blocks and check for API errors
2. **Use environment variables for API keys** - Never hardcode sensitive information
3. **Implement rate limiting** - Respect API limits to avoid being blocked
4. **Cache responses when appropriate** - Reduce API calls for repeated requests
5. **Provide clear context** - Give detailed prompts for better results
6. **Test generated code** - Always review and test AI-generated code before using in production
7. **Use async methods for high-performance applications** - Leverage async/await for better performance

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- 📧 Email: your.email@example.com
- 🐛 Issues: [GitHub Issues](https://github.com/yourusername/cursor-api-sdk/issues)
- 📖 Documentation: [GitHub Wiki](https://github.com/yourusername/cursor-api-sdk/wiki)

## Changelog

### Version 1.0.0
- Initial release
- Python SDK with full async support
- JavaScript SDK
- Command-line interface
- Comprehensive documentation
- Rate limiting and error handling
- Code generation, review, testing, and documentation features

