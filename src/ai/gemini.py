
import google.generativeai as genai
from .base import AIPlatform
from typing import Optional


class Gemini(AIPlatform):
    def __init__(self, api_key: str, system_prompt: Optional[str] = None):
        self.api_key = api_key
        self.system_prompt = system_prompt
        genai.configure(api_key=self.api_key) # type: ignore

        # See more models at: https://ai.google.dev/gemini-api/docs/models
        self.model = genai.GenerativeModel("gemini-3-flash-preview") # type: ignore

    def chat(self, prompt: str) -> str:
        if self.system_prompt:
            prompt = f"{self.system_prompt}\n\n{prompt}"

        response = self.model.generate_content(prompt) # type: ignore
        return response.text