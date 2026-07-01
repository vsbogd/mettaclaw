import lib_llm_ext as llm
import pluginapi as plugin

class OpenAIProvider(plugin.LLMProvider):

    def __init__(self):
        super().__init__()

    def config(self, config: dict) -> None:
        model = config.get("model", "gpt-5.5")
        self.delegate = OpenAIProviderImpl("OpenAI", "OPENAI_API_KEY",
                                           model, "https://api.openai.com/v1")

    def chat(self, prompt: str, max_tokens: int = 6000, reasoning_mode: str = "medium") -> str:
        return self.delegate.chat(prompt, max_tokens, reasoning_mode)

def loadOmegaClawPlugin():
    plugin.registerLLMProvider("OpenAI", OpenAIProvider())

class OpenAIProviderImpl(llm.AIProvider):
    """OpenAI provider using the Responses API (reasoning models)."""

    def chat(self, content: str, max_tokens: int = 6000, reasoning: str = "medium", **kwargs) -> str:
        """Send chat request via the Responses API, initializing client if needed."""
        self._ensure_client()

        if self._client is None:
            raise RuntimeError(f"{self.name} not configured (set {self._var_name})")

        if ":-:-:-:" in content:
            sysmsg, usermsg = content.split(":-:-:-:", 1)
        else:
            sysmsg, usermsg = "", content
        usermsg = usermsg.strip()
        if not usermsg:
            usermsg = "EMPTY / NO NEW USER INPUT."
        try:
            response = self._client.responses.create(
                model=self._model_name,
                instructions=sysmsg,
                input=usermsg,
                max_output_tokens=max_tokens,
                reasoning={"effort": reasoning},
                **kwargs
            )

            raw = response.output_text
            llm._log_raw(self._name, self._model_name, raw)
            return self._clean_text(raw)
        except Exception as e:
            print(f"[lib_llm_ext.OpenAIProviderImpl.chat] Exception while communicating with LLM: {e}")
            return ""

