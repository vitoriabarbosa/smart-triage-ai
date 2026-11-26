import os

from google import genai
from google.genai import types

from app.schemas import TriagemResponse


SYSTEM_PROMPT = """
Você é um assistente especializado em triagem de mensagens
de atendimento ao cliente.

Sua tarefa é interpretar a mensagem recebida e identificar:

1. A categoria da mensagem.
2. O nível de prioridade.
3. Um resumo objetivo.
4. O setor responsável.
5. A justificativa da classificação.

Regras:

- duvida: perguntas ou pedidos de esclarecimento.
- reclamacao: insatisfação com produtos ou serviços.
- solicitacao: pedidos de serviços ou alterações.
- problema_tecnico: erros, falhas ou dificuldades técnicas.

Prioridade:
- baixa: situações sem urgência aparente.
- media: situações que precisam de atenção.
- alta: situações que impedem o cliente de utilizar um serviço
  ou apresentam impacto significativo.

Setores:
- duvida: atendimento.
- reclamacao: relacionamento.
- solicitacao: administrativo.
- problema_tecnico: suporte_tecnico.

Analise o contexto, não apenas palavras isoladas.
Não invente informações que não estejam na mensagem.
"""


def classify_message(message: str) -> TriagemResponse:
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError("GEMINI_API_KEY não configurada.")

    client = genai.Client(api_key=api_key)

    try:
        response = client.models.generate_content(
            model=os.getenv("GEMINI_MODEL", "gemini-3.8-flash"),
            contents=f"{SYSTEM_PROMPT}\n\nMensagem do cliente:\n{message}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=TriagemResponse,
                temperature=0.2
            )
        )

        return TriagemResponse.model_validate_json(response.text)

    finally:
        client.close()