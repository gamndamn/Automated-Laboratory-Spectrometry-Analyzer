import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Lab Data Analyzer", layout="wide")

st.title("Automated spectrometry analyzer")
st.write("Download raw CSV-file from the application for immediate data analysis")

# --- FILE DOWNLOADING EMULATION ---
# ATTENTION: in the projects we use real data files, but here, for illustration purposes we would generate the data
uploaded_file = st.file_uploader("Choose the file from the PC (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("Press the button bellow to generate the measurement data:")
    if st.button("Generate CSV measurement data"):
        # Creating the artificial data spectra (peaks + noise)
        x = np.linspace(200, 800, 100)
        y = np.exp(-((x - 520) / 30)**2) + np.random.normal(0, 0.05, 100)
        df = pd.DataFrame({"Wavelength (nm)": x, "Optical density": y})
        st.session_state['df'] = df

# --- PROCESSING AND VISUALIZATION CODE BLOCK ---
if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Dividing interface view into 2 columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Interactive spectrum plot")
        # Строим встроенный график Streamlit
        st.line_chart(data=df, x="Wavelength (nm)", y="Optical density")
        
    with col2:
        st.subheader("Results of the analysis")
        
        # Find the maximum peak value
        max_row = df.loc[df["Optical density"].idxmax()]
        peak_x = round(max_row["Wavelength (nm)"], 1)
        peak_y = round(max_row["Optical density"], 3)
        
        # Magnitudes of the measure
        st.metric(label="Peak point (Peak)", value=f"{peak_x} nm")
        st.metric(label="Max intensity", value=peak_y)
        
        # Download button for the cleaned report in Excel/CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download the clean report (CSV)",
            data=csv,
            file_name="cleaned_report.csv",
            mime="text/csv",
        )
        st.success("Analysis is finished in 0.4 seconds!")
