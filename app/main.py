from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from app.schemas import TriagemRequest, TriagemResponse
from app.services.ai_service import classify_message

load_dotenv()

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
        raise HTTPException(
            status_code=503,
            detail=str(error)
        )

    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Não foi possível processar a mensagem com a IA."
        )