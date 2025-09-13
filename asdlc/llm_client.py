# asdlc/llm_client.py
"""
Módulo cliente para interação com APIs de LLM.
"""
import os
import logging
from openai import OpenAI
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

def get_llm_client():
    """Carrega a chave da API e retorna um cliente OpenAI."""
    load_dotenv()
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.warning("OPENAI_API_KEY não encontrada no arquivo .env. A chamada à LLM irá falhar.")
        # Você pode optar por levantar um erro aqui se a chave for estritamente necessária
        # raise ValueError("OPENAI_API_KEY não configurada.")
    return OpenAI(api_key=api_key)

def call_llm(prompt: str, model: str = None, max_tokens: int = None) -> str:
    """
    Envia um prompt para a API da LLM e retorna a resposta.
    """
    try:
        # Carregar configurações do .env se não especificadas
        load_dotenv()
        if model is None:
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        if max_tokens is None:
            max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2048"))
        
        temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))
        
        logger.info(f"Enviando prompt para o modelo {model}...")
        client = get_llm_client()
        if not client.api_key:
            return "ERRO: Chave da API da OpenAI não configurada. Verifique seu arquivo .env."

        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "Você é um assistente especialista em engenharia de software."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        content = response.choices[0].message.content
        logger.info("Resposta da LLM recebida com sucesso.")
        return content.strip()
    except Exception as e:
        logger.error(f"Erro ao chamar a API da LLM: {e}")
        return f"ERRO: Falha ao comunicar com a API. Detalhes: {e}" 