// Cursor API Examples - JavaScript

// Example 1: Basic Chat Completion
async function basicChatExample() {
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
          content: 'Write a JavaScript function to reverse a string'
        }
      ],
      model: 'cursor-1.0',
      temperature: 0.7
    })
  });

  const data = await response.json();
  console.log('Generated code:', data.choices[0].message.content);
}

// Example 2: Code Generation with Context
async function generateCodeWithContext() {
  const context = `
    // Existing code in the project
    class User {
      constructor(name, email) {
        this.name = name;
        this.email = email;
      }
    }
  `;

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
          content: `You are a helpful coding assistant. Use this context: ${context}`
        },
        {
          role: 'user',
          content: 'Create a method to validate the user email'
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 3: Code Review
async function reviewCode(code) {
  const prompt = `Please review this code and provide suggestions for improvement:

${code}

Please focus on:
1. Code quality and best practices
2. Potential bugs or issues
3. Performance optimizations
4. Readability improvements`;

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
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 4: Generate Unit Tests
async function generateTests(code, language = 'javascript') {
  const prompt = `Generate comprehensive unit tests for this ${language} code:

${code}

Include:
- Test cases for normal operation
- Edge cases
- Error conditions
- Use Jest for JavaScript or pytest for Python`;

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
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 5: Documentation Generator
async function generateDocumentation(code, language = 'javascript') {
  const prompt = `Generate comprehensive documentation for this ${language} code:

${code}

Include:
1. Function/class descriptions
2. Parameter explanations
3. Return value descriptions
4. Usage examples
5. Any important notes or warnings`;

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
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 6: Refactor Code
async function refactorCode(code, improvements = []) {
  const prompt = `Please refactor this code with the following improvements: ${improvements.join(', ')}

Original code:
${code}

Please provide the refactored version with explanations of the changes.`;

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
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 7: Generate API Client
async function generateAPIClient(apiSpec) {
  const prompt = `Generate a JavaScript API client based on this API specification:

${apiSpec}

The client should:
- Use fetch for HTTP requests
- Include proper error handling
- Have TypeScript types (if possible)
- Include JSDoc comments
- Follow modern JavaScript best practices`;

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
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 8: Debug Code
async function debugCode(code, errorMessage) {
  const prompt = `I'm getting this error with my code:

Error: ${errorMessage}

Code:
${code}

Please help me debug this issue and provide a solution.`;

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
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 9: Generate Configuration Files
async function generateConfigFile(type, options = {}) {
  const prompt = `Generate a ${type} configuration file with the following options:

${JSON.stringify(options, null, 2)}

Please provide a complete, production-ready configuration file.`;

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
          content: prompt
        }
      ],
      model: 'cursor-1.0'
    })
  });

  const data = await response.json();
  return data.choices[0].message.content;
}

// Example 10: Batch Processing
async function batchProcess(prompts) {
  const results = [];
  
  for (const prompt of prompts) {
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
            content: prompt
          }
        ],
        model: 'cursor-1.0'
      })
    });

    const data = await response.json();
    results.push(data.choices[0].message.content);
    
    // Add delay to respect rate limits
    await new Promise(resolve => setTimeout(resolve, 1000));
  }
  
  return results;
}

// Utility function for error handling
async function handleCursorAPIRequest(requestFunction) {
  try {
    const response = await requestFunction();
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(`Cursor API Error: ${error.message || response.statusText}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error('Cursor API request failed:', error);
    throw error;
  }
}

// Rate limiting utility
class RateLimiter {
  constructor(maxRequests = 60, timeWindow = 60000) {
    this.maxRequests = maxRequests;
    this.timeWindow = timeWindow;
    this.requests = [];
  }

  async waitForSlot() {
    const now = Date.now();
    this.requests = this.requests.filter(time => now - time < this.timeWindow);
    
    if (this.requests.length >= this.maxRequests) {
      const oldestRequest = this.requests[0];
      const waitTime = this.timeWindow - (now - oldestRequest);
      await new Promise(resolve => setTimeout(resolve, waitTime));
    }
    
    this.requests.push(now);
  }
}

// Example usage
async function main() {
  const rateLimiter = new RateLimiter(30, 60000); // 30 requests per minute
  
  try {
    // Example 1: Basic chat
    await rateLimiter.waitForSlot();
    await basicChatExample();
    
    // Example 2: Code review
    const codeToReview = `
      function calculateSum(a, b) {
        return a + b;
      }
    `;
    
    await rateLimiter.waitForSlot();
    const review = await reviewCode(codeToReview);
    console.log('Code review:', review);
    
    // Example 3: Generate tests
    await rateLimiter.waitForSlot();
    const tests = await generateTests(codeToReview);
    console.log('Generated tests:', tests);
    
  } catch (error) {
    console.error('Error in main:', error);
  }
}

// Export functions for use in other modules
module.exports = {
  basicChatExample,
  generateCodeWithContext,
  reviewCode,
  generateTests,
  generateDocumentation,
  refactorCode,
  generateAPIClient,
  debugCode,
  generateConfigFile,
  batchProcess,
  handleCursorAPIRequest,
  RateLimiter
};

// Run if this file is executed directly
if (require.main === module) {
  main();
}