from typing import Literal

from pydantic import BaseModel, Field


class TriagemRequest(BaseModel):
    mensagem: str = Field(
        min_length=5,
        max_length=2000,
        description="Mensagem enviada pelo cliente"
    )


class TriagemResponse(BaseModel):
    categoria: Literal[
        "duvida",
        "reclamacao",
        "solicitacao",
        "problema_tecnico"
    ]

    prioridade: Literal["baixa", "media", "alta"]

    resumo: str
    setor: Literal[
        "atendimento",
        "relacionamento",
        "administrativo",
        "suporte_tecnico"
    ]

    justificativa: str