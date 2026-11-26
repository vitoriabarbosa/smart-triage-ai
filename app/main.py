import logging

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException

load_dotenv()

from app.schemas import TriagemRequest, TriagemResponse
from app.services.ai_service import classify_message

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Triage API",
    description="API de classificação inteligente de mensagens.",
    version="1.0.0"
)


@app.get("/")
def home():
    return {
        "message": "Smart Triage API is running!"
    }


@app.post("/triage", response_model=TriagemResponse)
def triage(request: TriagemRequest):
    try:
        return classify_message(request.mensagem)

    except RuntimeError as error:
        logger.exception("Erro de configuração ou processamento")
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception:
        logger.exception("Erro inesperado durante a triagem")
        raise HTTPException(
            status_code=502,
            detail="Não foi possível processar a mensagem com a IA."
        )