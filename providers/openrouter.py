import os
import openai
from typing import Optional
import lib_llm_ext as llm
import pluginapi as plugin

class OpenRouterProvider(plugin.LLMProvider):

    def __init__(self):
        super().__init__()

    def config(self, config: dict) -> None:
        model = config.get("model", "z-ai/glm-5.2")
        self.delegate = OpenRouterProviderImpl("OpenRouter", "OPENROUTER_API_KEY",
                                               model, "https://openrouter.ai/api/v1")

    def chat(self, prompt: str, max_tokens: int = 6000, reasoning_mode: str = "medium") -> str:
        return self.delegate.chat(prompt, max_tokens, reasoning_mode)

def loadOmegaClawPlugin():
    plugin.registerLLMProvider("OpenRouter", OpenRouterProvider())

class OpenRouterProviderImpl(llm.AIProvider):
    """OpenRouter provider with reasoning mode enabled (reasoning tokens excluded from the response)."""

    def _create_client(self) -> Optional[openai.OpenAI]:
        """Create OpenRouter client from environment."""
        proxy_url = os.environ.get("GATEWAY_URL")
        if proxy_url:
            base_url = f"{proxy_url.rstrip('/')}/openrouter/"
            print(f"[lib_llm_ext.OpenRouterProviderImpl._create_client] Connecting via proxy: {base_url}")
            return openai.OpenAI(
                    api_key="proxy",
                    base_url=base_url,
                    )
        if self._var_name in os.environ:
            return openai.OpenAI(api_key=os.environ.get(self._var_name), base_url=self._base_url)

        return None

    def chat(self, content: str, max_tokens: int = 6000, reasoning: str = "medium", **kwargs) -> str:
        return super().chat(content, max_tokens, reasoning, extra_body={
            "reasoning": {
                "enabled": True,
                "max_tokens": 6000,
                "exclude": True,
            }
        }, **kwargs)
