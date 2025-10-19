import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Streamlit Template",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main content
def main():
    st.title("🚀 Streamlit Python Template")
    st.markdown("A clean starting point for your Streamlit application")
    
    # Welcome section
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("""
        ### Welcome!
        This is a minimal Streamlit template ready for you to build upon.
        
        **Features included:**
        - ✓ Clean project structure
        - ✓ Sidebar navigation ready
        - ✓ Responsive layout
        - ✓ Easy to customize
        """)
        
        # Example input
        st.subheader("Quick Example")
        user_input = st.text_input("Enter your name:", placeholder="Your name here")
        if user_input:
            st.success(f"Hello, {user_input}! 👋")
    
    with col2:
        st.info("💡 **Getting Started**\n\nEdit `app.py` to customize this template for your needs.")
        
        # Example button
        if st.button("Click me!", use_container_width=True):
            st.balloons()
            st.success("Button clicked! 🎉")

# Sidebar
with st.sidebar:
    st.header("Navigation")
    st.markdown("Add your navigation items here")
    
    st.divider()
    
    st.subheader("About")
    st.markdown("""
    This is a Streamlit Python template.
    
    Modify this file to build your application.
    """)

# Run the app
if __name__ == "__main__":
    main()
