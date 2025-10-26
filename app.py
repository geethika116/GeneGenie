import re
import fitz  # PyMuPDF
import os
import pandas as pd
import streamlit as st
from openai import OpenAI

# ==============================
# API Clients
# ==============================
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
ncbi_api_key = os.getenv("NCBI_API_KEY")  # reserved for future features

# ==============================
# Streamlit Page Config & Dark Theme
# ==============================
st.set_page_config(
    page_title="🧬 Gene Genie",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
    <style>
    /* Dark theme */
    .stApp { background-color: #0f1419; }
    #MainMenu, footer, header { visibility: hidden; }
    .main-title { font-size: 3rem; font-weight: 700; color: #ffffff; margin-bottom: 1rem; display: flex; align-items: center; gap: 1rem; }
    .dna-icon { font-size: 2.5rem; }
    .subtitle { font-size: 1rem; color: #e0e0e0; margin-bottom: 2rem; }
    .upload-label { font-size: 0.875rem; color: #e0e0e0; margin-bottom: 0.5rem; font-weight: 500; }
    [data-testid="stFileUploader"] { background-color: #1a1f2e; border: 2px dashed #3a4556; border-radius: 8px; padding: 3rem 2rem; }
    [data-testid="stFileUploader"] section { border: none; background-color: transparent; }
    [data-testid="stFileUploader"] section button { background-color: #2d3748; border: 1px solid #4a5568; border-radius: 6px; color: #e0e0e0; padding: 0.5rem 1.5rem; font-weight: 500; }
    [data-testid="stFileUploader"] section button:hover { background-color: #3a4556; border-color: #5a6578; }
    [data-testid="stFileUploader"] section div[data-testid="stMarkdownContainer"] p { color: #9ca3af; font-size: 0.875rem; }
    p, span, div, label { color: #e0e0e0; }
    small { color: #9ca3af; }
    </style>
""", unsafe_allow_html=True)

# ==============================
# Header
# ==============================
st.markdown("""
    <div class="main-title">
        <span class="dna-icon">🧬</span>
        <span>Gene Genie</span>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <div class="subtitle">
        Upload a research article PDF to extract DNA/RNA sequences with context and AI summaries!
    </div>
""", unsafe_allow_html=True)

st.markdown('<div class="upload-label">Upload a PDF</div>', unsafe_allow_html=True)

# ==============================
# PDF Extraction Functions
# ==============================
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    text = re.sub(r'-\n', '', text)
    text = re.sub(r'\n', ' ', text)
    return text

def split_sentences(text):
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]

def extract_sequences(text):
    pattern = r"[ATGC]{8,}|[AUGC]{8,}"
    sentences = split_sentences(text)
    extracted = []
    for sent in sentences:
        matches = re.findall(pattern, sent)
        if matches:
            matches.sort(key=len, reverse=True)
            seen = set()
            for seq in matches:
                if not any(seq in s for s in seen):
                    extracted.append({"sequence": seq, "context": sent, "summary": ""})
                    seen.add(seq)
    return extracted

def summarize_with_gpt(sequence, context):
    try:
        prompt = f"""
        Analyze the following biological sequence and explain its possible context:
        Sequence: {sequence}
        Context: {context}
        Provide a concise, scientific explanation.
        """
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=400,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ Error: {e}"

def download_csv(sequences):
    df = pd.DataFrame(sequences)
    return df.to_csv(index=False)

# ==============================
# Streamlit App Logic
# ==============================
uploaded_file = st.file_uploader("Drag and drop file here", type=["pdf"])

if uploaded_file is not None:
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    st.info(f"File size: {uploaded_file.size / 1024:.2f} KB")
    
    if st.button("🧬 Extract DNA/RNA Sequences", use_container_width=True):
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
            csv_data = download_csv(sequences)
            st.download_button(
                label="📥 Download CSV of Sequences",
                data=csv_data,
                file_name="gene_sequences.csv",
                mime="text/csv"
            )
        else:
            st.warning("No DNA/RNA sequences found in this PDF.")

