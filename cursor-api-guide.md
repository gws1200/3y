# Cursor API Guide

## Overview

The Cursor API allows you to programmatically interact with Cursor, the AI-powered code editor. This guide covers how to use the Cursor API for various development tasks.

## Getting Started

### Prerequisites

- Cursor editor installed
- Node.js (for JavaScript/TypeScript examples)
- Python (for Python examples)

### Authentication

To use the Cursor API, you'll need to authenticate. The API typically uses API keys or OAuth tokens.

```bash
# Set your Cursor API key
export CURSOR_API_KEY="your-api-key-here"
```

## API Endpoints

### 1. Chat Completion

Send messages to Cursor's AI and get responses.

```javascript
// JavaScript example
const response = await fetch('https://api.cursor.sh/v1/chat/completions', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${process.env.CURSOR_API_KEY}`,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    messages: [
      {
        role: 'user',
        content: 'Write a function to calculate fibonacci numbers'
      }
    ],
    model: 'cursor-1.0',
    temperature: 0.7
  })
});

const data = await response.json();
console.log(data.choices[0].message.content);
```

```python
# Python example
import requests
import os

def chat_with_cursor(prompt):
    url = "https://api.cursor.sh/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {os.getenv('CURSOR_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    data = {
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "model": "cursor-1.0",
        "temperature": 0.7
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Usage
result = chat_with_cursor("Write a Python function to sort a list")
print(result['choices'][0]['message']['content'])
```

### 2. Code Generation

Generate code based on descriptions or requirements.

```javascript
async function generateCode(description, language = 'javascript') {
  const response = await fetch('https://api.cursor.sh/v1/code/generate', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.CURSOR_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      prompt: description,
      language: language,
      max_tokens: 1000
    })
  });
  
  return await response.json();
}

// Example usage
const code = await generateCode(
  'Create a React component for a todo list',
  'jsx'
);
```

### 3. Code Analysis

Analyze existing code for improvements, bugs, or documentation.

```python
def analyze_code(code, analysis_type="review"):
    url = "https://api.cursor.sh/v1/code/analyze"
    headers = {
        "Authorization": f"Bearer {os.getenv('CURSOR_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    data = {
        "code": code,
        "analysis_type": analysis_type,  # "review", "optimize", "document"
        "language": "python"
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
code_to_analyze = """
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)
"""

analysis = analyze_code(code_to_analyze, "optimize")
print(analysis['suggestions'])
```

### 4. File Operations

Read, write, and manage files through the API.

```javascript
// Read file
async function readFile(filePath) {
  const response = await fetch(`https://api.cursor.sh/v1/files/read`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.CURSOR_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      path: filePath
    })
  });
  
  return await response.json();
}

// Write file
async function writeFile(filePath, content) {
  const response = await fetch(`https://api.cursor.sh/v1/files/write`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.CURSOR_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      path: filePath,
      content: content
    })
  });
  
  return await response.json();
}
```

## Advanced Features

### 1. Context-Aware Code Generation

Provide context from your codebase for more accurate code generation.

```javascript
async function generateWithContext(prompt, contextFiles) {
  const response = await fetch('https://api.cursor.sh/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.CURSOR_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [
        {
          role: 'system',
          content: `You are a helpful coding assistant. Use the following context to help answer the user's question: ${JSON.stringify(contextFiles)}`
        },
        {
          role: 'user',
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });
  
  return await response.json();
}
```

### 2. Batch Operations

Process multiple files or generate multiple functions at once.

```python
def batch_code_generation(prompts, language="python"):
    url = "https://api.cursor.sh/v1/code/batch-generate"
    headers = {
        "Authorization": f"Bearer {os.getenv('CURSOR_API_KEY')}",
        "Content-Type": "application/json"
    }
    
    data = {
        "prompts": prompts,
        "language": language
    }
    
    response = requests.post(url, headers=headers, json=data)
    return response.json()

# Example usage
prompts = [
    "Create a function to validate email addresses",
    "Create a function to generate random passwords",
    "Create a function to format dates"
]

results = batch_code_generation(prompts)
for i, result in enumerate(results['generated_code']):
    print(f"Function {i+1}:")
    print(result)
    print()
```

## Error Handling

```javascript
async function handleCursorAPIRequest(requestFunction) {
  try {
    const response = await requestFunction();
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Cursor API Error: ${error.message}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Cursor API request failed:', error);
    throw error;
  }
}

// Usage
const result = await handleCursorAPIRequest(() => 
  fetch('https://api.cursor.sh/v1/chat/completions', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${process.env.CURSOR_API_KEY}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      messages: [{ role: 'user', content: 'Hello' }],
      model: 'cursor-1.0'
    })
  })
);
```

## Rate Limiting

The Cursor API has rate limits. Implement proper rate limiting in your applications:

```python
import time
import asyncio
from functools import wraps

def rate_limit(calls_per_minute=60):
    def decorator(func):
        last_call = 0
        min_interval = 60.0 / calls_per_minute
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            nonlocal last_call
            current_time = time.time()
            
            if current_time - last_call < min_interval:
                sleep_time = min_interval - (current_time - last_call)
                time.sleep(sleep_time)
            
            last_call = time.time()
            return func(*args, **kwargs)
        
        return wrapper
    return decorator

@rate_limit(calls_per_minute=30)
def cursor_api_call(prompt):
    # Your API call here
    pass
```

## Best Practices

1. **Always handle errors gracefully**
2. **Use environment variables for API keys**
3. **Implement rate limiting**
4. **Cache responses when appropriate**
5. **Provide clear context for better results**
6. **Test generated code before using in production**

## SDK Libraries

### JavaScript/TypeScript SDK

```bash
npm install cursor-api
```

```javascript
import { CursorAPI } from 'cursor-api';

const cursor = new CursorAPI(process.env.CURSOR_API_KEY);

// Chat completion
const response = await cursor.chat.completions.create({
  messages: [{ role: 'user', content: 'Hello' }],
  model: 'cursor-1.0'
});

// Code generation
const code = await cursor.code.generate({
  prompt: 'Create a React component',
  language: 'jsx'
});
```

### Python SDK

```bash
pip install cursor-api
```

```python
from cursor_api import CursorAPI

cursor = CursorAPI(api_key=os.getenv('CURSOR_API_KEY'))

# Chat completion
response = cursor.chat.completions.create(
    messages=[{"role": "user", "content": "Hello"}],
    model="cursor-1.0"
)

# Code generation
code = cursor.code.generate(
    prompt="Create a Python function",
    language="python"
)
```

## Examples

### 1. Code Review Bot

```python
import os
import requests
from typing import List, Dict

class CodeReviewBot:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.cursor.sh/v1"
    
    def review_code(self, code: str, language: str = "python") -> Dict:
        """Review code and provide suggestions for improvement."""
        url = f"{self.base_url}/code/analyze"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "code": code,
            "analysis_type": "review",
            "language": language
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.json()
    
    def generate_tests(self, code: str, language: str = "python") -> str:
        """Generate unit tests for the given code."""
        prompt = f"Generate comprehensive unit tests for the following {language} code:\n\n{code}"
        
        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": "cursor-1.0"
        }
        
        response = requests.post(url, headers=headers, json=data)
        return response.json()['choices'][0]['message']['content']

# Usage
bot = CodeReviewBot(os.getenv('CURSOR_API_KEY'))

code = """
def calculate_fibonacci(n):
    if n <= 1:
        return n
    return calculate_fibonacci(n-1) + calculate_fibonacci(n-2)
"""

review = bot.review_code(code)
tests = bot.generate_tests(code)
```

### 2. Automated Documentation Generator

```javascript
class DocumentationGenerator {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'https://api.cursor.sh/v1';
  }

  async generateDocs(code, language = 'javascript') {
    const prompt = `Generate comprehensive documentation for the following ${language} code. Include:
    1. Function/class descriptions
    2. Parameter explanations
    3. Return value descriptions
    4. Usage examples
    5. Any important notes or warnings

    Code:
    ${code}`;

    const response = await fetch(`${this.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messages: [{ role: 'user', content: prompt }],
        model: 'cursor-1.0'
      })
    });

    return await response.json();
  }

  async generateReadme(projectFiles) {
    const prompt = `Generate a comprehensive README.md file for a project with the following files:
    ${JSON.stringify(projectFiles, null, 2)}

    Include:
    1. Project description
    2. Installation instructions
    3. Usage examples
    4. API documentation
    5. Contributing guidelines
    6. License information`;

    const response = await fetch(`${this.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.apiKey}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        messages: [{ role: 'user', content: prompt }],
        model: 'cursor-1.0'
      })
    });

    return await response.json();
  }
}

// Usage
const docGen = new DocumentationGenerator(process.env.CURSOR_API_KEY);

const code = `
function calculateArea(radius) {
  return Math.PI * radius * radius;
}

class Circle {
  constructor(radius) {
    this.radius = radius;
  }
  
  getArea() {
    return calculateArea(this.radius);
  }
}
`;

const docs = await docGen.generateDocs(code);
console.log(docs.choices[0].message.content);
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**
   - Verify your API key is correct
   - Check if the API key has expired
   - Ensure proper authorization headers

2. **Rate Limiting**
   - Implement exponential backoff
   - Use request queuing
   - Monitor API usage

3. **Response Format Issues**
   - Always check response status codes
   - Handle different response formats
   - Validate response data

### Debug Mode

```javascript
const DEBUG = process.env.NODE_ENV === 'development';

async function debugCursorAPI(requestFunction) {
  if (DEBUG) {
    console.log('Making Cursor API request...');
    const startTime = Date.now();
    
    try {
      const result = await requestFunction();
      console.log(`Request completed in ${Date.now() - startTime}ms`);
      return result;
    } catch (error) {
      console.error('Request failed:', error);
      throw error;
    }
  } else {
    return await requestFunction();
  }
}
```

## Conclusion

The Cursor API provides powerful capabilities for AI-assisted coding. By following this guide and implementing the examples, you can integrate Cursor's AI capabilities into your development workflow effectively.

Remember to:
- Always test generated code
- Implement proper error handling
- Respect rate limits
- Keep your API keys secure
- Stay updated with API changes

For more information, visit the official Cursor API documentation.