# Streamlit Python Template

A clean, minimal Streamlit application template ready for development.

## Structure

```
.
├── app.py              # Main application file
├── pages/              # Multi-page apps (optional)
├── components/         # Reusable components (optional)
└── utils/              # Utility functions (optional)
```

## Getting Started

1. The main application is in `app.py`
2. Run the app (it starts automatically on Replit)
3. Edit `app.py` to customize your application

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
