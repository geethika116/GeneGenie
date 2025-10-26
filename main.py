import re
import fitz  # PyMuPDF
import os
import pandas as pd
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file (for local development)
load_dotenv()

# ==============================
# API Clients
# ==============================
# Get API key from environment variable or Streamlit secrets
api_key = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY", None)

client = OpenAI(api_key=api_key)
ncbi_api_key = os.getenv("NCBI_API_KEY")  # reserved for future features

# ==============================
# Streamlit Setup
# ==============================
st.set_page_config(page_title="🧬 Gene Genie", page_icon="🧬", layout="wide")
st.title("🧬 Gene Genie")
st.write("Upload a research article PDF to extract DNA/RNA sequences with context and AI summaries!")

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
    """
    Split text into sentences using punctuation while preserving order.
    This avoids splitting sequences across line breaks.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


# ==============================
# Sequence Extraction
# ==============================
def extract_sequences(text):
    """
    Extract DNA/RNA sequences (>=8 bases) from text in PDF order.
    Context includes the sequence itself exactly as in PDF.
    Avoid duplicate substrings within the same sentence.
    """
    pattern = r"[ATGC]{8,}|[AUGC]{8,}"  # DNA or RNA sequences >=8 bases
    sentences = split_sentences(text)
    extracted = []

    for sent in sentences:
        matches = re.findall(pattern, sent)
        if matches:
            # Keep longest sequences first to avoid substring duplicates
            matches.sort(key=len, reverse=True)
            seen = set()
            for seq in matches:
                if not any(seq in s for s in seen):
                    extracted.append({
                        "sequence": seq,
                        "context": sent,
                        "summary": ""
                    })
                    seen.add(seq)
    return extracted


# ==============================
# AI Summary with GPT
# ==============================
def summarize_with_gpt(sequence, context):
    """Summarize sequence in context using OpenAI GPT model."""
    try:
        prompt = f"""
        Analyze the following biological sequence and explain its possible context:
        Sequence: {sequence}
        Context: {context}
        Provide a concise, scientific explanation.
        """

        response = client.chat.completions.create(
            model="gpt-4o",  # use GPT-4o for detailed scientific summaries
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"⚠️ Error: {e}"


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

                if os.getenv("OPENAI_API_KEY"):
                    if st.button(f"Summarize Sequence {i}", key=f"summarize_{i}"):
                        summary = summarize_with_gpt(item['sequence'], item['context'])
                        item["summary"] = summary
                        st.info(summary)

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
