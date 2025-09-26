# OmniRx (Omni-channel Agentic Talk-to-Data for Commercial Pharma)

![CI](https://github.com/katemartian/omnix-demo/actions/workflows/ci.yml/badge.svg)

## Data & docs (demo)
Synthetic star schema in `data/` (`fact_sales`, `dim_hcp`, `dim_geo`, `dim_payer`) and two demo docs in `data/docs/` for RAG. No real patient/HCP data.

## Run the demo UI
```bash
source .venv/bin/activate
streamlit run app/Home.py
```
## Run with Docker
```bash
docker build -t omnix:latest .
docker run --rm -p 8000:8000 omnix:latest
# then:
# curl -X POST localhost:8000/ask -H "content-type: application/json" -d '{"query":"Trend last 4 weeks RX in ON"}'
```
