# asdlc/llm_client.py
"""
Módulo cliente para interação com APIs de LLM.

MODO DE EXECUÇÃO:
  - ANTIGRAVITY (padrão): A variável ASDLC_ENGINE=antigravity no .env desativa
    chamadas externas. O Antigravity (IDE) é o cérebro via Skills.
  - EXTERNAL_API: Defina ASDLC_ENGINE=external no .env para usar a API OpenAI.
"""

import os
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__name__)


def get_llm_client():
    """Carrega a chave da API e retorna um cliente OpenAI.
    
    Só funciona quando ASDLC_ENGINE=external no .env.
    No modo antigravity (padrão), levanta uma exceção clara.
    """
    load_dotenv()
    engine_mode = os.getenv("ASDLC_ENGINE", "antigravity").lower()
    
    if engine_mode != "external":
        raise RuntimeError(
            "A-SDLC: Motor externo desativado (ASDLC_ENGINE=antigravity).\n"
            "Para usar a API OpenAI, defina ASDLC_ENGINE=external no seu .env.\n"
            "Para usar o Antigravity como cérebro, use a Skill @asdlc_implementation no chat da IDE."
        )
    
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY não configurada no .env.")
    
    logger.info("Modo EXTERNAL_API ativado. Usando OpenAI.")
    return OpenAI(api_key=api_key)


def call_llm(prompt: str, model: str = None, max_tokens: int = None) -> str:
    """
    Envia um prompt para a API da LLM e retorna a resposta.
    Só funciona quando ASDLC_ENGINE=external.
    """
    try:
        load_dotenv()
        if model is None:
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        if max_tokens is None:
            max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2048"))

        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

        logger.info(f"Enviando prompt para o modelo {model}...")
        client = get_llm_client()

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente especialista em engenharia de software."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        content = response.choices[0].message.content
        logger.info("Resposta da LLM recebida com sucesso.")
        return content.strip()
    except RuntimeError as e:
        # Captura o bloqueio do modo antigravity
        logger.error(str(e))
        return f"ERRO: {e}"
    except Exception as e:
        logger.error(f"Erro ao chamar a API da LLM: {e}")
        return f"ERRO: Falha ao comunicar com a API. Detalhes: {e}"
