# Doc Answer Desk (Gemini Flash + local folder)

## Setup
1. Gemini: get an AI Studio key **or** run `gcloud auth application-default login` for Vertex AI.
2. Install and configure:
   ```bash
   python3 -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   cp .env .env   # fill in the <PLACEHOLDERS>
   ```
3. Put your files (PDF, DOCX, XLSX, PPTX, TXT, MD, CSV) in `DOCS_DIR`.
4. Run: `streamlit run app.py`

## How it finds answers
1. Every supported file in `DOCS_DIR` (including subfolders) is loaded. Extracted text is cached until the file changes.
2. **Small folder** (total text ≤ `MAX_TOTAL_CHARS`, ~500k tokens): all files are sent to Gemini.
3. **Large folder**: Gemini rewrites the question into keywords, files are scored by keyword frequency
   (+ bonus for filename matches), and the top `TOP_K_FILES` are sent.
4. Gemini answers only from those files and cites them as **[file name]**. If the answer isn't there, it says so.

Limits: keyword scoring doesn't understand synonyms, and scanned (image-only) PDFs produce no text.

## Try it
`docs/hr-policy-sample.md` is a fictional HR policy for testing. Example questions:

| Question | Expected answer |
|---|---|
| How many annual leave days can I carry forward? | 5 days, used by 31 March |
| What is the notice period for a manager? | 2 months |
| How many days can I work from another country? | 20 working days, with HR and Legal approval |
| What is the daily meal limit on business travel? | USD 60 |
| Who do I escalate a grievance to after my HR Business Partner? | Head of People |
| What is the dental insurance policy? | Not found in the documents |

## Files
- `config.py` – settings and placeholders
- `local_docs.py` – load files from the folder, keyword ranking
- `gemini_client.py` – query rewriting and cited answer generation
- `app.py` – Streamlit chat UI
