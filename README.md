# 🧬 Gene Genie

A DNA/RNA sequence extraction and analysis tool powered by Streamlit and OpenAI.

## Structure

```
.
├── main.py             # Main Streamlit application (Gene Genie)
├── app.py              # Alternative Streamlit UI
├── server/             # Express proxy server
├── client/             # React frontend (disabled, proxied to Streamlit)
└── attached_assets/    # Static assets
```

## Getting Started

### Running the Application

The application now defaults to the Streamlit interface. To start both the Express proxy server and Streamlit:

```bash
npm run dev
```

This will:
- Start the Express server on port 5000 (proxies to Streamlit)
- Start the Streamlit app on port 8501

Then visit **http://localhost:5000** to access the Gene Genie Streamlit application.

### Alternative: Run Servers Separately

```bash
# Terminal 1 - Express proxy server
npm run dev:server

# Terminal 2 - Streamlit app
npm run dev:streamlit
```

## Adding Pages

Create files in a `pages/` directory to add multiple pages:
- `pages/1_📊_Dashboard.py`
- `pages/2_⚙️_Settings.py`

## Common Patterns

### Layout
```python
col1, col2, col3 = st.columns(3)
with col1:
    st.write("Column 1")
```

### User Input
```python
name = st.text_input("Name")
age = st.number_input("Age", min_value=0)
agree = st.checkbox("I agree")
```

### Data Display
```python
import pandas as pd
df = pd.DataFrame(data)
st.dataframe(df)
st.line_chart(df)
```

## Resources

- [Streamlit Documentation](https://docs.streamlit.io)
- [API Reference](https://docs.streamlit.io/library/api-reference)
- [Gallery](https://streamlit.io/gallery)
