import re
import os
import io
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Try to import PyMuPDF
try:
    import fitz
except Exception:
    fitz = None


# ==============================
# Load OpenAI API Key
# ==============================
api_key = None

try:
    api_key = st.secrets.get("OPENAI_API_KEY") if hasattr(st, "secrets") else None
except Exception:
    api_key = None

if not api_key:
    api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    try:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
    except Exception:
        pass

client = OpenAI(api_key=api_key) if api_key else None


# ==============================
# Streamlit Config
# ==============================
st.set_page_config(
    page_title="🧬 Gene Genie",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.stApp { background-color: #0f1419; }
#MainMenu, footer, header { visibility: hidden; }
.main-title { font-size: 3rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; }
.subtitle { font-size: 1rem; color: #e0e0e0; margin-bottom: 2rem; }
p, span, div, label { color: #e0e0e0; }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-title">
🧬 Gene Genie
</div>
<div class="subtitle">
Upload a research article PDF to extract DNA/RNA sequences with minimal clean context.
</div>
""", unsafe_allow_html=True)


# ==============================
# PDF Extraction
# ==============================
def extract_text_from_pdf(uploaded_file):
    uploaded_file.seek(0)
    file_bytes = uploaded_file.read()

    if fitz:
        try:
            doc = fitz.open(stream=file_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text("text") + "\n"
        except Exception:
            text = ""
    else:
        try:
            from PyPDF2 import PdfReader
            reader = PdfReader(io.BytesIO(file_bytes))
            text = "\n".join([page.extract_text() or "" for page in reader.pages])
        except Exception:
            text = ""

    # Clean PDF artifacts
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.upper()


# ==============================
# CLEAN SEQUENCE EXTRACTION
# ==============================
def extract_sequences(text, flank_tokens=2, min_length=8):
    """
    Extract DNA/RNA sequences with minimal surrounding context.
    Removes fragments and duplicates.
    """

    # DNA or RNA pattern
    pattern = rf"\b[ATGC]{{{min_length},}}\b|\b[AUGC]{{{min_length},}}\b"

    # Tokenize document
    tokens = re.findall(r"\b\w+\b", text)

    # First pass: collect sequences
    raw_sequences = [
        token for token in tokens
        if re.fullmatch(pattern, token)
    ]

    # Deduplicate + sort longest first
    unique_sequences = sorted(set(raw_sequences), key=len, reverse=True)

    # Remove fragments (substrings of longer sequences)
    filtered_sequences = []
    for seq in unique_sequences:
        if not any(seq in longer and seq != longer for longer in filtered_sequences):
            filtered_sequences.append(seq)

    results = []
    seen_contexts = set()

    # Extract limited context windows
    for i, token in enumerate(tokens):
        if token in filtered_sequences:
            start = max(0, i - flank_tokens)
            end = min(len(tokens), i + flank_tokens + 1)
            context = " ".join(tokens[start:end])

            if context not in seen_contexts:
                results.append({
                    "sequence": token,
                    "context": context,
                    "summary": ""
                })
                seen_contexts.add(context)

    return results


# ==============================
# GPT SUMMARY
# ==============================
def summarize_with_gpt(sequence, context):
    if not client:
        return ""

    try:
        prompt = f"""
        Analyze this biological sequence briefly.

        Sequence: {sequence}
        Local Context: {context}

        Provide a concise scientific explanation.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.2
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error: {e}"


# ==============================
# CSV Export
# ==============================
def download_csv(sequences):
    df = pd.DataFrame(sequences)
    return df.to_csv(index=False)


# ==============================
# Streamlit Logic
# ==============================
uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

if uploaded_file:

    st.success(f"File uploaded: {uploaded_file.name}")

    if st.button("🧬 Extract Sequences", use_container_width=True):

        with st.spinner("Extracting PDF text..."):
            text = extract_text_from_pdf(uploaded_file)

        if not text:
            st.error("Could not extract text from PDF.")
        else:
            with st.spinner("Scanning for DNA/RNA sequences..."):
                sequences = extract_sequences(text)

            if not sequences:
                st.warning("No DNA/RNA sequences found.")
            else:
                st.success(f"Found {len(sequences)} unique sequences.")

                if api_key:
                    with st.spinner("Generating AI summaries..."):
                        for item in sequences:
                            item["summary"] = summarize_with_gpt(
                                item["sequence"],
                                item["context"]
                            )

                for i, item in enumerate(sequences, 1):
                    with st.expander(f"Sequence {i}"):
                        st.code(item["sequence"])
                        st.write(f"**Context:** {item['context']}")
                        if item["summary"]:
                            st.write(f"**AI Summary:** {item['summary']}")

                csv_data = download_csv(sequences)

                st.download_button(
                    "📥 Download CSV",
                    csv_data,
                    "gene_sequences.csv",
                    "text/csv"
                )
