"""
Cursor API Python SDK

A comprehensive Python SDK for interacting with the Cursor API.
"""

import os
import time
import asyncio
import aiohttp
import requests
from typing import List, Dict, Optional, Union, Any
from dataclasses import dataclass
from functools import wraps
import json


@dataclass
class CursorConfig:
    """Configuration for Cursor API client."""
    api_key: str
    base_url: str = "https://api.cursor.sh/v1"
    timeout: int = 30
    max_retries: int = 3
    rate_limit_per_minute: int = 60


class CursorAPIError(Exception):
    """Custom exception for Cursor API errors."""
    def __init__(self, message: str, status_code: Optional[int] = None, response: Optional[Dict] = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class RateLimiter:
    """Rate limiter for API requests."""
    
    def __init__(self, max_requests: int, time_window: int):
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []
    
    async def wait_for_slot(self):
        """Wait for an available request slot."""
        now = time.time()
        self.requests = [req_time for req_time in self.requests if now - req_time < self.time_window]
        
        if len(self.requests) >= self.max_requests:
            oldest_request = self.requests[0]
            wait_time = self.time_window - (now - oldest_request)
            await asyncio.sleep(wait_time)
        
        self.requests.append(now)


class CursorAPI:
    """Main Cursor API client."""
    
    def __init__(self, api_key: Optional[str] = None, config: Optional[CursorConfig] = None):
        """Initialize the Cursor API client.
        
        Args:
            api_key: Your Cursor API key. If not provided, will try to get from CURSOR_API_KEY env var.
            config: Optional configuration object.
        """
        if config:
            self.config = config
        else:
            api_key = api_key or os.getenv('CURSOR_API_KEY')
            if not api_key:
                raise ValueError("API key must be provided either directly or via CURSOR_API_KEY environment variable")
            
            self.config = CursorConfig(api_key=api_key)
        
        self.rate_limiter = RateLimiter(
            self.config.rate_limit_per_minute,
            60  # 1 minute window
        )
        self.session = None
    
    async def __aenter__(self):
        """Async context manager entry."""
        self.session = aiohttp.ClientSession(
            timeout=aiohttp.ClientTimeout(total=self.config.timeout)
        )
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        if self.session:
            await self.session.close()
    
    def _handle_response(self, response: requests.Response) -> Dict:
        """Handle API response and raise appropriate errors."""
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"message": response.text}
        
        if not response.ok:
            raise CursorAPIError(
                message=data.get("message", f"HTTP {response.status_code}"),
                status_code=response.status_code,
                response=data
            )
        
        return data
    
    async def _handle_async_response(self, response: aiohttp.ClientResponse) -> Dict:
        """Handle async API response and raise appropriate errors."""
        try:
            data = await response.json()
        except json.JSONDecodeError:
            text = await response.text()
            data = {"message": text}
        
        if not response.ok:
            raise CursorAPIError(
                message=data.get("message", f"HTTP {response.status}"),
                status_code=response.status,
                response=data
            )
        
        return data
    
    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        model: str = "cursor-1.0",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Send a chat completion request.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            model: The model to use for completion.
            temperature: Controls randomness in the response.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters to pass to the API.
        
        Returns:
            API response dictionary.
        """
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            **kwargs
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        for attempt in range(self.config.max_retries):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=self.config.timeout)
                return self._handle_response(response)
            except requests.exceptions.RequestException as e:
                if attempt == self.config.max_retries - 1:
                    raise CursorAPIError(f"Request failed after {self.config.max_retries} attempts: {str(e)}")
                time.sleep(2 ** attempt)  # Exponential backoff
    
    async def chat_completion_async(
        self,
        messages: List[Dict[str, str]],
        model: str = "cursor-1.0",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        **kwargs
    ) -> Dict:
        """Send an async chat completion request.
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys.
            model: The model to use for completion.
            temperature: Controls randomness in the response.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters to pass to the API.
        
        Returns:
            API response dictionary.
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager or call init_session()")
        
        await self.rate_limiter.wait_for_slot()
        
        url = f"{self.config.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.config.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messages": messages,
            "model": model,
            "temperature": temperature,
            **kwargs
        }
        
        if max_tokens:
            data["max_tokens"] = max_tokens
        
        for attempt in range(self.config.max_retries):
            try:
                async with self.session.post(url, headers=headers, json=data) as response:
                    return await self._handle_async_response(response)
            except aiohttp.ClientError as e:
                if attempt == self.config.max_retries - 1:
                    raise CursorAPIError(f"Request failed after {self.config.max_retries} attempts: {str(e)}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff
    
    def generate_code(
        self,
        prompt: str,
        language: str = "python",
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate code based on a prompt.
        
        Args:
            prompt: The code generation prompt.
            language: The programming language for the generated code.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters.
        
        Returns:
            Generated code as string.
        """
        messages = [
            {
                "role": "system",
                "content": f"You are a helpful coding assistant. Generate {language} code based on the user's request."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat_completion(messages, max_tokens=max_tokens, **kwargs)
        return response["choices"][0]["message"]["content"]
    
    async def generate_code_async(
        self,
        prompt: str,
        language: str = "python",
        max_tokens: int = 1000,
        **kwargs
    ) -> str:
        """Generate code asynchronously based on a prompt.
        
        Args:
            prompt: The code generation prompt.
            language: The programming language for the generated code.
            max_tokens: Maximum number of tokens to generate.
            **kwargs: Additional parameters.
        
        Returns:
            Generated code as string.
        """
        messages = [
            {
                "role": "system",
                "content": f"You are a helpful coding assistant. Generate {language} code based on the user's request."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = await self.chat_completion_async(messages, max_tokens=max_tokens, **kwargs)
        return response["choices"][0]["message"]["content"]
    
    def review_code(
        self,
        code: str,
        language: str = "python",
        focus_areas: Optional[List[str]] = None
    ) -> str:
        """Review code and provide suggestions.
        
        Args:
            code: The code to review.
            language: The programming language of the code.
            focus_areas: Specific areas to focus on (e.g., ["performance", "security", "readability"]).
        
        Returns:
            Code review as string.
        """
        focus_text = ""
        if focus_areas:
            focus_text = f" Focus on: {', '.join(focus_areas)}."
        
        prompt = f"""Please review this {language} code and provide suggestions for improvement.{focus_text}

Code:
{code}

Please provide:
1. Code quality and best practices analysis
2. Potential bugs or issues
3. Performance optimizations
4. Readability improvements
5. Security considerations (if applicable)"""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
    
    def generate_tests(
        self,
        code: str,
        language: str = "python",
        test_framework: Optional[str] = None
    ) -> str:
        """Generate unit tests for code.
        
        Args:
            code: The code to generate tests for.
            language: The programming language.
            test_framework: Specific test framework to use (e.g., "pytest", "unittest").
        
        Returns:
            Generated test code as string.
        """
        framework_text = f" using {test_framework}" if test_framework else ""
        
        prompt = f"""Generate comprehensive unit tests for this {language} code{framework_text}:

{code}

Include:
- Test cases for normal operation
- Edge cases
- Error conditions
- Proper test structure and naming
- Mocking where appropriate"""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
    
    def generate_documentation(
        self,
        code: str,
        language: str = "python",
        doc_format: str = "docstring"
    ) -> str:
        """Generate documentation for code.
        
        Args:
            code: The code to document.
            language: The programming language.
            doc_format: Documentation format (e.g., "docstring", "markdown", "html").
        
        Returns:
            Generated documentation as string.
        """
        prompt = f"""Generate {doc_format} documentation for this {language} code:

{code}

Include:
1. Function/class descriptions
2. Parameter explanations
3. Return value descriptions
4. Usage examples
5. Any important notes or warnings
6. Type hints (if applicable)"""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
    
    def refactor_code(
        self,
        code: str,
        improvements: List[str],
        language: str = "python"
    ) -> str:
        """Refactor code with specific improvements.
        
        Args:
            code: The code to refactor.
            improvements: List of improvements to apply.
            language: The programming language.
        
        Returns:
            Refactored code as string.
        """
        improvements_text = ", ".join(improvements)
        
        prompt = f"""Please refactor this {language} code with the following improvements: {improvements_text}

Original code:
{code}

Please provide the refactored version with explanations of the changes."""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
    
    def debug_code(
        self,
        code: str,
        error_message: str,
        language: str = "python"
    ) -> str:
        """Debug code with error information.
        
        Args:
            code: The problematic code.
            error_message: The error message received.
            language: The programming language.
        
        Returns:
            Debugging solution as string.
        """
        prompt = f"""I'm getting this error with my {language} code:

Error: {error_message}

Code:
{code}

Please help me debug this issue and provide a solution."""

        messages = [
            {
                "role": "user",
                "content": prompt
            }
        ]
        
        response = self.chat_completion(messages)
        return response["choices"][0]["message"]["content"]
    
    async def batch_process(
        self,
        prompts: List[str],
        **kwargs
    ) -> List[str]:
        """Process multiple prompts asynchronously.
        
        Args:
            prompts: List of prompts to process.
            **kwargs: Additional parameters for chat completion.
        
        Returns:
            List of responses.
        """
        if not self.session:
            raise RuntimeError("Session not initialized. Use async context manager or call init_session()")
        
        tasks = []
        for prompt in prompts:
            messages = [{"role": "user", "content": prompt}]
            task = self.chat_completion_async(messages, **kwargs)
            tasks.append(task)
        
        responses = await asyncio.gather(*tasks, return_exceptions=True)
        
        results = []
        for response in responses:
            if isinstance(response, Exception):
                results.append(f"Error: {str(response)}")
            else:
                results.append(response["choices"][0]["message"]["content"])
        
        return results
    
    def init_session(self):
        """Initialize the async session manually."""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                timeout=aiohttp.ClientTimeout(total=self.config.timeout)
            )
    
    def close_session(self):
        """Close the async session manually."""
        if self.session:
            asyncio.create_task(self.session.close())
            self.session = None


# Convenience functions
def rate_limit(calls_per_minute: int = 60):
    """Decorator for rate limiting functions."""
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


# Example usage and utility functions
def create_cursor_client(api_key: Optional[str] = None) -> CursorAPI:
    """Create a Cursor API client with default configuration.
    
    Args:
        api_key: Optional API key. If not provided, will use environment variable.
    
    Returns:
        Configured CursorAPI instance.
    """
    return CursorAPI(api_key=api_key)


async def example_usage():
    """Example usage of the Cursor API SDK."""
    async with CursorAPI() as cursor:
        # Generate code
        code = await cursor.generate_code_async(
            "Create a function to calculate fibonacci numbers",
            language="python"
        )
        print("Generated code:", code)
        
        # Review code
        review = cursor.review_code(code, language="python")
        print("Code review:", review)
        
        # Generate tests
        tests = cursor.generate_tests(code, language="python", test_framework="pytest")
        print("Generated tests:", tests)


if __name__ == "__main__":
    # Run example
    asyncio.run(example_usage())