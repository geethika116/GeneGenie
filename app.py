import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Gene Genie",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS for dark theme and styling
st.markdown("""
    <style>
    /* Dark theme */
    .stApp {
        background-color: #0f1419;
    }
    
    /* Hide default Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Title styling */
    .main-title {
        font-size: 3rem;
        font-weight: 700;
        color: #ffffff;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    
    .dna-icon {
        font-size: 2.5rem;
    }
    
    /* Subtitle styling */
    .subtitle {
        font-size: 1rem;
        color: #e0e0e0;
        margin-bottom: 2rem;
    }
    
    /* Upload section label */
    .upload-label {
        font-size: 0.875rem;
        color: #e0e0e0;
        margin-bottom: 0.5rem;
        font-weight: 500;
    }
    
    /* File uploader container */
    [data-testid="stFileUploader"] {
        background-color: #1a1f2e;
        border: 2px dashed #3a4556;
        border-radius: 8px;
        padding: 3rem 2rem;
    }
    
    [data-testid="stFileUploader"] section {
        border: none;
        background-color: transparent;
    }
    
    [data-testid="stFileUploader"] section button {
        background-color: #2d3748;
        border: 1px solid #4a5568;
        border-radius: 6px;
        color: #e0e0e0;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
    }
    
    [data-testid="stFileUploader"] section button:hover {
        background-color: #3a4556;
        border-color: #5a6578;
    }
    
    /* Upload text styling */
    [data-testid="stFileUploader"] section div[data-testid="stMarkdownContainer"] p {
        color: #9ca3af;
        font-size: 0.875rem;
    }
    
    /* Make the whole app text lighter */
    p, span, div, label {
        color: #e0e0e0;
    }
    
    /* Style the file limit text */
    small {
        color: #9ca3af;
    }
    </style>
""", unsafe_allow_html=True)

def main():
    # Header with icon and title
    st.markdown("""
        <div class="main-title">
            <span class="dna-icon">🧬</span>
            <span>Gene Genie</span>
        </div>
    """, unsafe_allow_html=True)
    
    # Subtitle
    st.markdown("""
        <div class="subtitle">
            Upload a research article PDF to extract DNA/RNA sequences with context and AI summaries!
        </div>
    """, unsafe_allow_html=True)
    
    # Upload section
    st.markdown('<div class="upload-label">Upload a PDF</div>', unsafe_allow_html=True)
    
    # File uploader
    uploaded_file = st.file_uploader(
        "Drag and drop file here",
        type=['pdf'],
        label_visibility="visible",
        help="Limit 200MB per file • PDF"
    )
    
    # Display file info if uploaded
    if uploaded_file is not None:
        st.success(f"✅ File uploaded: {uploaded_file.name}")
        st.info(f"File size: {uploaded_file.size / 1024:.2f} KB")
        
        # Add a process button
        if st.button("🧬 Extract DNA/RNA Sequences", use_container_width=True):
            st.info("Processing would happen here...")

if __name__ == "__main__":
    main()
