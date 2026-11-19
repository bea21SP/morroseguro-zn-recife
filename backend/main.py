import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import httpx
from google import genai
from google.genai import types

load_dotenv()

app = FastAPI(title="MorroSeguro ZN API — Recife", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BAIRROS_MORROS_ZN = {
    "Alto José do Pinho", "Alto José Bonifácio", "Morro da Conceição",
    "Vasco da Gama", "Nova Descoberta", "Casa Amarela", "Macaxeira",
    "Dois Unidos", "Linha do Tiro", "Água Fria", "Beberibe", "Córrego do Jenipapo"
}

class TriagemRequest(BaseModel):
    bairro: str
    descricao: Optional[str] = ""
    imagem_base64: Optional[str] = None
    mime_type: str = "image/jpeg"

class TriagemResponse(BaseModel):
    valido_para_mapa: bool
    titulo_padronizado: str
    categoria: str
    urgencia: str
    afeta_transporte: bool
    impacto_mobilidade: str
    resumo_tecnico: str
    tags: List[str]

@app.get("/api/etl/dados-recife")
async def buscar_dados_recife():
    """Consulta datasets da Defesa Civil e EMLURB no CKAN do Recife."""
    url = "https://dados.recife.pe.gov.br/api/3/action/package_search"
    async with httpx.AsyncClient(timeout=15.0) as client:
        resp = await client.get(url, params={"q": "defesa civil", "rows": 5})
        resp.raise_for_status()
        return {"fonte": "Dados Abertos Recife", "bairros_alvo": sorted(BAIRROS_MORROS_ZN), "dados": resp.json()}

@app.post("/api/triagem-ia", response_model=TriagemResponse)
async def triagem_relato_ia(req: TriagemRequest):
    """Analisa foto e relato de morador usando Gemini 2.5 Flash com saída estruturada."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key == "COLE_SUA_CHAVE_AQUI":
        raise HTTPException(status_code=500, detail="Configure GEMINI_API_KEY no arquivo .env")

    client = genai.Client(api_key=api_key)
    prompt = (
        f"Analise este relato de encosta/obra irregular no bairro {req.bairro} (Zona Norte do Recife). "
        f"Descrição: {req.descricao}. Avalie risco de deslizamento, drenagem e impacto em ônibus/kombis."
    )

    contents = [prompt]
    if req.imagem_base64:
        import base64
        img_bytes = base64.b64decode(req.imagem_base64)
        contents.append(types.Part.from_bytes(data=img_bytes, mime_type=req.mime_type))

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=contents,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=TriagemResponse,
        ),
    )
    return response.parsed