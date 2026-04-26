# asdlc/llm_client.py
"""
Módulo cliente para interação com APIs de LLM (OpenAI e OpenRouter).
Suporta roteamento de modelos por tipo de agente.
"""

import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def get_llm_client():
    """Carrega as chaves e retorna o cliente adequado (OpenRouter ou OpenAI)."""
    load_dotenv(override=True)
    engine_mode = os.getenv("ASDLC_ENGINE", "antigravity").lower()
    
    if engine_mode != "external":
        raise RuntimeError(
            "A-SDLC: Motor externo desativado (ASDLC_ENGINE=antigravity).\n"
            "Use as Skills no chat da IDE para custo zero."
        )

    or_key = os.getenv("OPENROUTER_API_KEY")
    oa_key = os.getenv("OPENAI_API_KEY")

    if or_key:
        logger.info("Usando OpenRouter como provedor de LLM.")
        return OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=or_key,
            timeout=60.0,
            default_headers={
                "HTTP-Referer": "https://github.com/jota-f/A-SDLC",
                "X-Title": "A-SDLC Framework",
            }
        )
    elif oa_key:
        logger.info("Usando OpenAI nativo como provedor de LLM.")
        return OpenAI(api_key=oa_key, timeout=60.0)
    else:
        raise ValueError("Nenhuma chave de API (OPENROUTER ou OPENAI) encontrada no .env.")

def call_llm(prompt: str, agent_type: str = "general", max_tokens: int = None) -> str:
    """
    Envia um prompt para a LLM roteando o modelo pelo tipo de agente.
    """
    try:
        load_dotenv(override=True)
        client = get_llm_client()
        
        # Mapeamento de Modelos por Agente (Estritamente via .env)
        model_map = {
            "code": os.getenv("MODEL_CODE"),
            "architecture": os.getenv("MODEL_ARCH"),
            "test": os.getenv("MODEL_TEST"),
            "requirements": os.getenv("MODEL_REQ"),
            "review": os.getenv("MODEL_REVIEW"),
            "general": os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
        }

        model = model_map.get(agent_type) or model_map["general"]
        
        # Limite de tokens específico para Review (Kimi) conforme solicitado
        if agent_type == "review" and max_tokens is None:
            max_tokens = 1024 # Limite de saída para o Reviewer caro
        elif max_tokens is None:
            max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "4096"))

        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.3"))

        logger.info(f"Agente [{agent_type}] chamando modelo [{model}]...")
        
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": f"Você é um {agent_type} agent especialista no framework A-SDLC."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        
        if not response or not hasattr(response, 'choices') or len(response.choices) == 0:
            return "ERRO: Resposta inválida ou vazia da API (sem choices)."
            
        content = response.choices[0].message.content
        return content.strip() if content else "ERRO: Resposta vazia da LLM (content is None)."
        
    except RuntimeError as e:
        return f"MODO ANTIGRAVITY: {str(e)}"
    except Exception as e:
        logger.error(f"Erro na chamada LLM: {e}")
        return f"ERRO: {str(e)}"
