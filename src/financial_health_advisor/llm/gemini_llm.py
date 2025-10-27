import os
import google.generativeai as genai
from typing import List, Optional
from crewai.llm import BaseLLM

class GeminiLLM(BaseLLM):
    """Custom Gemini LLM implementation for CrewAI"""
    
    def __init__(self):
        model_name = os.getenv("GEMINI_MODEL", "models/gemini-pro-latest")
        super().__init__(model=model_name)
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel(model_name)
    
    def get_model_name(self) -> str:
        return os.getenv("GEMINI_MODEL", "models/gemini-pro-latest")

    def format_prompt(self, messages: List[dict]) -> str:
        """Format messages into a single prompt string that Gemini can understand"""
        formatted_prompt = []
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            
            if role == "system":
                formatted_prompt.append(f"Instructions: {content}\n")
            elif role == "user":
                formatted_prompt.append(f"User: {content}\n")
            elif role == "assistant":
                formatted_prompt.append(f"Assistant: {content}\n")
        
        return "\n".join(formatted_prompt)

    def call(
        self,
        prompt: str,
        functions: Optional[List[dict]] = None,
        **kwargs
    ) -> str:
        """Required implementation of the call method"""
        try:
            if isinstance(prompt, str):
                response = self.model.generate_content(prompt)
            else:
                # If prompt is a list of messages, format it
                formatted_prompt = self.format_prompt(prompt)
                response = self.model.generate_content(formatted_prompt)

            # Robustly extract text from varying Gemini response shapes
            # Prefer .text, then .candidates, then dict-style outputs
            if hasattr(response, 'text') and response.text:
                return response.text

            if hasattr(response, 'candidates') and response.candidates:
                first = response.candidates[0]
                # candidate may have .content or .message or .text
                if hasattr(first, 'content'):
                    return first.content
                if hasattr(first, 'text'):
                    return first.text
                if hasattr(first, 'message'):
                    return getattr(first, 'message')

            # dict-like response handling
            if isinstance(response, dict):
                # common keys: 'candidates', 'output', 'content'
                if 'candidates' in response and response['candidates']:
                    cand = response['candidates'][0]
                    if isinstance(cand, dict):
                        return cand.get('content') or cand.get('text') or str(cand)
                if 'output' in response:
                    out = response['output']
                    if isinstance(out, list) and out:
                        item = out[0]
                        if isinstance(item, dict):
                            return item.get('content') or item.get('text') or str(item)
                if 'content' in response:
                    return response['content']

            # Fallback to stringifying the response
            return str(response)
        except Exception as e:
            print(f"Error in Gemini call: {e}")
            return f"Error: {str(e)}"
    
    async def generate_response(self, prompt: str) -> str:
        """Generate a response for a single prompt"""
        return self.call(prompt)
    
    async def generate_chat_response(
        self,
        messages: List[dict],
        max_tokens: int = None,
        temperature: float = None
    ) -> str:
        """Generate a response in chat format"""
        try:
            formatted_prompt = self.format_prompt(messages)
            response = self.model.generate_content(formatted_prompt)

            # Reuse the same robust extraction logic as call()
            if hasattr(response, 'text') and response.text:
                return response.text
            if hasattr(response, 'candidates') and response.candidates:
                first = response.candidates[0]
                if hasattr(first, 'content'):
                    return first.content
                if hasattr(first, 'text'):
                    return first.text
            if isinstance(response, dict):
                return response.get('content') or str(response)
            return str(response)
        except Exception as e:
            print(f"Error in chat response: {e}")
            return f"Error: {str(e)}"