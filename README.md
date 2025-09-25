# OmniRx (Omni-channel Agentic Talk-to-Data for Commercial Pharma)

![CI](https://github.com/katemartian/omnix-demo/actions/workflows/ci.yml/badge.svg)

## Data & docs (demo)
Synthetic star schema in `data/` (`fact_sales`, `dim_hcp`, `dim_geo`, `dim_payer`) and two demo docs in `data/docs/` for RAG. No real patient/HCP data.

## Run the demo UI
```bash
source .venv/bin/activate
streamlit run app/Home.py
```