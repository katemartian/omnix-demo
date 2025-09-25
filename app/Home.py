import json
import pandas as pd
import streamlit as st

from omnix.agents.planner import ask as plan_ask

st.set_page_config(page_title="OmniRx Demo", page_icon="💊", layout="wide")
st.title("OmniRx — Agentic Talk-to-Data (Demo)")

with st.sidebar:
    st.markdown("**Examples**")
    if st.button("Trend last 6 weeks RX in ON"):
        st.session_state["q"] = "Trend last 6 weeks RX in ON"
    if st.button("Which HCP segment underperformed vs forecast in Ontario?"):
        st.session_state["q"] = "Which HCP segment underperformed vs forecast in Ontario?"
    if st.button("Summarize formulary constraints for Drug X in Ontario"):
        st.session_state["q"] = "Summarize formulary constraints for Drug X in Ontario"
    st.divider()
    st.caption("This is a synthetic demo; no real patient/HCP data.")

q = st.text_input("Ask a question", value=st.session_state.get("q", ""))
go = st.button("Run", type="primary")

if go and q.strip():
    with st.spinner("Thinking…"):
        out = plan_ask(q)

    st.subheader("Answer")

    if out.get("route") == "data":
        rows = out.get("result", [])
        if rows:
            df = pd.DataFrame(rows)
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No rows returned.")
        with st.expander("SQL"):
            st.code(out.get("sql", ""), language="sql")

    elif out.get("route") == "docs":
        if out.get("blocked"):
            st.error(f"Blocked by guardrail: {out.get('reason')}")
        else:
            st.markdown(out.get("answer", ""))
            cits = out.get("citations", [])
            if cits:
                st.caption("Citations:")
                for c in cits:
                    st.write(f"• {c['doc']} (chunk {c['chunk_id']}), score {c['score']}")
            else:
                st.warning("No citations found.")

    st.divider()
    st.subheader("Trace")
    st.code(json.dumps(out.get("trace", {}), indent=2))
