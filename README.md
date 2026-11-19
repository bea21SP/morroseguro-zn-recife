# MorroSeguro ZN — Recife (RPA 2 & RPA 3)

Plataforma cívica para mapeamento preventivo de encostas, obras irregulares, drenagem e gargalos de mobilidade nos morros da Zona Norte do Recife.

## Estrutura do Projeto (Pronto para VS Code)
- `frontend/index.html` — Interface Web/PWA interativa com mapa Leaflet, filtros por bairro e integração Gemini.
- `backend/main.py` — API FastAPI com ETL do Portal Dados Abertos Recife (CKAN) e triagem multimodal via SDK oficial `google-genai`.
- `database/schema.sql` — Modelagem espacial PostgreSQL + PostGIS (`ST_DWithin` para agrupamento de relatos).
- `.env.example` — Arquivo modelo para inserir sua chave `GEMINI_API_KEY`.

## Como rodar localmente no VS Code
1. Copie `.env.example` para `.env` e cole sua `GEMINI_API_KEY` gerada no Google AI Studio.
2. Para abrir o frontend imediatamente: clique com o botão direito em `frontend/index.html` e selecione **Open with Live Server**.
3. Para rodar o backend Python:
   ```bash
   cd backend
   python -m venv .venv
   source .venv/bin/activate  # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```