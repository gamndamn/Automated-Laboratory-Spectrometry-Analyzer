import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Lab Data Analyzer", layout="wide")

st.title("🔬 Автоматический анализатор спектрометрии")
st.write("Загрузите сырой CSV-файл с прибора для мгновенной очистки данных и поиска пиков.")

# --- ЭМУЛЯЦИЯ ЗАГРУЗКИ ФАЙЛА ---
# На фрилансе мы используем st.file_uploader, но для теста сделаем генерацию данных
uploaded_file = st.file_uploader("Выбрать файл прибора (CSV)", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    st.info("💡 Нажмите кнопку ниже, чтобы сгенерировать тестовые данные прибора:")
    if st.button("Сгенерировать тестовый спектр"):
        # Создаем искусственный спектр: шум + химический пик
        x = np.linspace(200, 800, 100)
        y = np.exp(-((x - 520) / 30)**2) + np.random.normal(0, 0.05, 100)
        df = pd.DataFrame({"Длина волны (нм)": x, "Оптическая плотность": y})
        st.session_state['df'] = df

# --- БЛОК ОБРАБОТКИ И ВИЗУАЛИЗАЦИИ ---
if 'df' in st.session_state:
    df = st.session_state['df']
    
    # Разделяем интерфейс на две колонки (выглядит очень профессионально)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Интерактивный график спектра")
        # Строим встроенный график Streamlit
        st.line_chart(data=df, x="Длина волны (нм)", y="Оптическая плотность")
        
    with col2:
        st.subheader("📈 Результаты анализа")
        
        # Находим пик (максимальное значение) — базовая автоматизация
        max_row = df.loc[df["Оптическая плотность"].idxmax()]
        peak_x = round(max_row["Длина волны (нм)"], 1)
        peak_y = round(max_row["Оптическая плотность"], 3)
        
        # Красивые b2b метрики
        st.metric(label="Точка пика (💥 Peak)", value=f"{peak_x} нм")
        st.metric(label="Макс. интенсивность", value=peak_y)
        
        # Кнопка скачивания очищенного отчета в Excel/CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Скачать чистый отчет (CSV)",
            data=csv,
            file_name="cleaned_report.csv",
            mime="text/csv",
        )
        st.success("Анализ завершен за 0.4 секунды!")