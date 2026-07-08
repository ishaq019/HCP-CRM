import json
from typing import Any

from fastapi import HTTPException, status
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_groq import ChatGroq

from app.config import get_settings


class MissingGroqApiKeyError(RuntimeError):
    pass


class LLMService:
    def __init__(self, model: str | None = None, temperature: float = 0.1):
        self.settings = get_settings()
        self.model = model or self.settings.groq_model
        self.temperature = temperature

    def _client(self) -> ChatGroq:
        if not self.settings.groq_api_key:
            raise MissingGroqApiKeyError(
                "GROQ_API_KEY is not configured. Add it to backend/.env to use AI agent features."
            )
        return ChatGroq(
            model=self.model,
            temperature=self.temperature,
            groq_api_key=self.settings.groq_api_key,
        )

    def invoke_json(self, template: str, variables: dict[str, Any]) -> dict[str, Any]:
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self._client() | JsonOutputParser()
        try:
            result = chain.invoke(variables)
            if isinstance(result, dict):
                return result
            return json.loads(str(result))
        except MissingGroqApiKeyError:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Groq/LangChain JSON generation failed: {exc}",
            ) from exc

    def invoke_text(self, template: str, variables: dict[str, Any]) -> str:
        prompt = PromptTemplate.from_template(template)
        chain = prompt | self._client() | StrOutputParser()
        try:
            return chain.invoke(variables).strip()
        except MissingGroqApiKeyError:
            raise
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Groq/LangChain text generation failed: {exc}",
            ) from exc


def raise_ai_configuration_error(exc: MissingGroqApiKeyError) -> None:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(exc)) from exc
