"""Streamlit chat UI.  Run:  streamlit run app.py"""
from pathlib import Path

import streamlit as st

import config
import gemini_client as gc
import local_docs as ld

st.set_page_config(page_title="Doc Answer Desk", layout="wide")


@st.cache_resource
def gemini():
    return gc.get_client()


with st.sidebar:
    st.header("Documents")
    folder = Path(st.text_input("Folder path", value=config.DOCS_DIR)).expanduser()
    top_k = st.slider("Files to read per question", 1, 10, config.TOP_K_FILES)
    if st.button("New conversation"):
        st.session_state.clear()
        st.rerun()
    st.divider()
    st.subheader("Files consulted")
    for name in st.session_state.get("sources", []):
        st.markdown(f"- {name}")

st.title("Doc Answer Desk")
st.caption(f"Answers from files in `{folder}` using {config.GEMINI_MODEL}.")

st.session_state.setdefault("history", [])
st.session_state.setdefault("sources", [])

for m in st.session_state.history:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

question = st.chat_input("Ask about your documents…")
if not question:
    st.stop()

with st.chat_message("user"):
    st.markdown(question)

with st.chat_message("assistant"):
    with st.status("Loading documents…", expanded=False) as status:
        docs, errors = ld.load_docs(folder)
        for err in errors:
            st.warning(f"Could not read {err}")
        status.write(f"{len(docs)} file(s) in folder")

        if ld.fits_in_context(docs):
            files = docs
            status.write("Whole folder fits in context: sending all files")
        else:
            keywords = gc.rewrite_query(gemini(), question, st.session_state.history)
            status.write(f"Keywords: {', '.join(keywords)}")
            files = ld.rank(docs, keywords, top_k)

        for f in files:
            status.write(f"Using: {f.name}" + (" (truncated)" if f.truncated else ""))
        status.update(label=f"Using {len(files)} file(s)", state="complete")

    if not files:
        answer = "No matching files found. Try different wording or check the folder path."
        st.markdown(answer)
    else:
        answer = st.write_stream(gc.answer_stream(gemini(), question, files, st.session_state.history))
        st.session_state.sources = sorted({*st.session_state.sources, *(f.name for f in files)})

st.session_state.history += [
    {"role": "user", "content": question},
    {"role": "assistant", "content": answer if isinstance(answer, str) else str(answer)},
]
st.rerun()
