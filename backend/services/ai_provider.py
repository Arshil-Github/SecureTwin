# backend/services/ai_provider.py
import time
import logging
from typing import Optional, Dict, Any
from pydantic import BaseModel
from backend.config import settings

logger = logging.getLogger(__name__)

class AIResponse(BaseModel):
    text: str
    provider: str
    tokens_used: int
    latency_ms: int
    error: Optional[str] = None

class AIProvider:
    
    def __init__(self):
        self.provider = settings.AI_PROVIDER # "claude" or "gemini"
        self._claude_client = None
        self._gemini_model = None

    def _get_claude(self):
        if not self._claude_client:
            import anthropic
            self._claude_client = anthropic.Anthropic(api_key=settings.ANTHROPIC_API_KEY)
        return self._claude_client

    def _get_gemini(self):
        if not self._gemini_model:
            import google.generativeai as genai
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self._gemini_model = genai.GenerativeModel("gemini-1.5-flash") # Updated to 1.5
        return self._gemini_model

    async def complete(self, prompt: str, system: str = "", max_tokens: int = 500, temperature: float = 0.3) -> AIResponse:
        start_time = time.time()
        try:
            if self.provider == "claude":
                client = self._get_claude()
                message = client.messages.create(
                    model="claude-3-5-sonnet-20240620",
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system,
                    messages=[{"role": "user", "content": prompt}]
                )
                text = message.content[0].text
                tokens = message.usage.input_tokens + message.usage.output_tokens
            else: # gemini
                model = self._get_gemini()
                # Gemini combined system and prompt for simplicity in flash
                full_prompt = f"{system}\n\n{prompt}" if system else prompt
                response = model.generate_content(
                    full_prompt,
                    generation_config={"max_output_tokens": max_tokens, "temperature": temperature}
                )
                text = response.text
                tokens = 0 # Gemini token usage info is slightly different to extract
            
            latency = int((time.time() - start_time) * 1000)
            logger.info(f"AI Call: provider={self.provider}, tokens={tokens}, latency={latency}ms")
            return AIResponse(text=text, provider=self.provider, tokens_used=tokens, latency_ms=latency)
            
        except Exception as e:
            latency = int((time.time() - start_time) * 1000)
            logger.error(f"AI Call Failed: {str(e)}")
            return AIResponse(text="", provider=self.provider, tokens_used=0, latency_ms=latency, error=str(e))

    async def complete_structured(self, prompt: str, system: str, output_schema: dict, max_tokens: int = 800) -> Optional[dict]:
        # Simplified for hackathon: use complete and manual JSON parsing
        # Real version would use function calling
        json_prompt = f"{prompt}\n\nReturn ONLY valid JSON matching this schema: {output_schema}"
        response = await self.complete(json_prompt, system=system, max_tokens=max_tokens)
        
        if response.error:
            return None
            
        import json
        import re
        try:
            # Extract JSON from potential markdown code blocks
            match = re.search(r'\{.*\}', response.text, re.DOTALL)
            if match:
                return json.loads(match.group())
            return json.loads(response.text)
        except Exception as e:
            logger.error(f"Failed to parse structured AI response: {str(e)}")
            return None

ai_provider = AIProvider()
