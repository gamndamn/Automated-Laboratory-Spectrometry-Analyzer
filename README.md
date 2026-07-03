This tool automates the process of raw data cleaning and peak detection for laboratory R&D teams.

Attention: In real-world projects, this application is tailored to process actual raw data files directly from analytical instruments. However, for demonstration purposes in this public repository, it features built-in automated data generation so you can test the functionality instantly without needing a proprietary lab file.

Features:
- Drag-and-drop raw CSV data upload.
- Automatic noise filtering and Peak detection.
- Interactive data visualization (Plotly/Streamlit).
- One-click clean CSV/Excel export for managers.

How to run locally:
1. pip install streamlit pandas numpy
2. streamlit run app.py
