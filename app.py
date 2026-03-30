import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
from main import main  # reuse pipeline
from src.model import india_sector_recommendation, compute_scores, objective
from src.data_loader import load_data
from src.preprocessing import filter_years, normalize

st.set_page_config(page_title="QIOM", page_icon="🛸", layout="wide")

st.title("🛸 Quantum Investment Optimization Model (QIOM)")
st.markdown("Upload Excel (Year, Country, RD, VC, Startups, Patents, Return) & watch LIVE param changes!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Dataset")
    uploaded_file = st.file_uploader("Choose Excel file", type="xlsx")

with col2:
    st.subheader("⚙️ Live Parameters")
    alpha = st.slider("α Innovation weight", 0.0, 1.0, 0.5)
    beta = st.slider("β Return weight", 0.0, 1.0, 0.5)
    budget = st.slider("Budget (max investments)", 1, 10, 3)

if uploaded_file is not None:
    temp_path = "temp_dataset.xlsx"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Loaded: {uploaded_file.name}")

    # LIVE RECS w/o Run button - recompute on slider change
    df_live = load_data(temp_path)
    df_live = filter_years(df_live)
    df_live = normalize(df_live)
    df_live = compute_scores(df_live)
    df_live = objective(df_live, alpha=alpha, beta=beta)
    
    recs_live = india_sector_recommendation(df_live, alpha, beta)
    st.subheader("🔴 LIVE India Sector Allocation (sliders → instant update)")
    st.markdown(recs_live['summary'])
    for detail in recs_live['details']:
        st.markdown(f"**• {detail}**")

    col_live1, col_live2 = st.columns(2)
    with col_live1:
        fig, ax = plt.subplots()
        ax.bar(recs_live['sectors'], recs_live['gaps'])
        ax.set_title('Live Weighted Gaps')
        ax.set_ylabel('Gap')
        st.pyplot(fig)

    with col_live2:
        fig, ax = plt.subplots()
        ax.pie(recs_live['weights'], labels=recs_live['sectors'], autopct='%1.1f%%')
        ax.set_title('Live Allocation %')
        st.pyplot(fig)

    st.markdown("**🎛️ Sliders update LIVE above**")

    col_opt1, col_opt2 = st.columns(2)
    with col_opt1:
        if st.button("🚀 Run Full Optimization", type="primary"):
            with st.spinner("Running solvers..."):
                main(path=temp_path, budget=budget, alpha=alpha, beta=beta)

            if os.path.exists('results/output.csv'):
                df_results = pd.read_csv('results/output.csv')
                st.subheader("📊 Results Table")
                st.dataframe(df_results, width="stretch")

            if os.path.exists('results/plots/comparison.png'):
                st.subheader("📈 Quantum vs Classical Plot")
                img = plt.imread('results/plots/comparison.png')
                st.image(img, width="stretch")

            st.success("✅ Optimization done!")

    with col_opt2:
        st.info("**Live preview** above shows param effects instantly.\n**Run** computes solvers/results.")

else:
    st.info("👆 Upload Excel to enable LIVE previews & optimization")

if os.path.exists('temp_dataset.xlsx'):
    try:
        os.remove('temp_dataset.xlsx')
    except:
        pass

st.markdown("---")


