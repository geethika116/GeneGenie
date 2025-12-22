import re
import fitz  # PyMuPDF
import os
import pandas as pd
import streamlit as st

# ==============================
# Streamlit Setup
# ==============================
st.set_page_config(page_title="🧬 Gene Genie", page_icon="🧬", layout="wide")
st.title("🧬 Gene Genie")
st.write("Upload a research article PDF to extract DNA/RNA sequences!")

# ==============================
# PDF Text Extraction
# ==============================
def extract_text_from_pdf(file):
    """Extract all text from a PDF file using PyMuPDF."""
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"

    # Remove soft line breaks inside sentences to preserve sequences
    text = re.sub(r'-\n', '', text)  # remove hyphenation
    text = re.sub(r'\n', ' ', text)  # convert line breaks to spaces
    return text

# ==============================
# Sentence Splitting
# ==============================
def split_sentences(text):
    """Split text into sentences while preserving order."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

# ==============================
# Sequence Extraction
# ==============================
def extract_sequences(text):
    """
    Extract DNA/RNA sequences (>=8 bases) from text in PDF order.
    Context includes the sequence itself exactly as in PDF.
    """
    pattern = r"[ATGC]{8,}|[AUGC]{8,}"  # DNA or RNA sequences >=8 bases
    sentences = split_sentences(text)
    extracted = []

    for sent in sentences:
        matches = re.findall(pattern, sent)
        if matches:
            matches.sort(key=len, reverse=True)
            seen = set()
            for seq in matches:
                if not any(seq in s for s in seen):
                    extracted.append({
                        "sequence": seq,
                        "context": sent
                    })
                    seen.add(seq)
    return extracted

# ==============================
# CSV Export
# ==============================
def download_csv(sequences):
    """Convert sequences list to CSV for download."""
    df = pd.DataFrame(sequences)
    return df.to_csv(index=False)

# ==============================
# Streamlit App Logic
# ==============================
uploaded_file = st.file_uploader("Upload a PDF", type=["pdf"])

if uploaded_file is not None:
    with st.spinner("Extracting text from PDF..."):
        text = extract_text_from_pdf(uploaded_file)
    st.success("✅ PDF text extracted!")

    with st.spinner("Searching for DNA/RNA sequences..."):
        sequences = extract_sequences(text)

    if sequences:
        st.write(f"### Found {len(sequences)} sequences in the document:")

        for i, item in enumerate(sequences, 1):
            with st.expander(f"Sequence {i}"):
                st.code(item['sequence'], language="text")
                st.write(f"**Context:** {item['context']}")

        # ----------------------
        # CSV Download Button
        # ----------------------
        csv_data = download_csv(sequences)
        st.download_button(
            label="📥 Download CSV of Sequences",
            data=csv_data,
            file_name="gene_sequences.csv",
            mime="text/csv"
        )

    else:
        st.warning("No DNA/RNA sequences found in this PDF.")
