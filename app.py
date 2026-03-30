import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import shutil
from main import main  # reuse pipeline
from src.model import india_sector_recommendation

st.set_page_config(page_title="QIOM", page_icon="🛸", layout="wide")

st.title(" Quantum Investment Optimization Model (QIOM)")
st.markdown("Upload your Excel dataset (columns: Year, Country, RD, VC, Startups, Patents, Return) and optimize investments!")

col1, col2 = st.columns(2)

with col1:
    st.subheader("📁 Upload Dataset")
    uploaded_file = st.file_uploader("Choose Excel file", type="xlsx", help="Dataset with investment metrics")

with col2:
    st.subheader("⚙️ Parameters")
    alpha = st.slider("Alpha (Innovation weight)", 0.0, 1.0, 0.5)
    beta = st.slider("Beta (Return weight)", 0.0, 1.0, 0.5)
    budget = st.slider("Budget (max investments)", 1, 10, 3)

if uploaded_file is not None:
    # Save uploaded file
    temp_path = "temp_dataset.xlsx"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    st.success(f"✅ Uploaded: {uploaded_file.name}")
    st.info(f"Using: {temp_path}")

    if st.button("🚀 Run Quantum Optimization", type="primary"):
        with st.spinner("Optimizing with QAOA & Classical solver..."):
            main(path=temp_path, budget=budget, alpha=alpha, beta=beta)

        # Display results if exist
        if os.path.exists('results/output.csv'):
            df_results = pd.read_csv('results/output.csv')
            st.subheader("📊 Optimization Results")
            st.dataframe(df_results, use_container_width=True)

        if os.path.exists('results/plots/comparison.png'):
            st.subheader("📈 Comparison Plot (Quantum vs Classical)")
            img = plt.imread('results/plots/comparison.png')
            st.image(img, use_column_width=True)

        st.success("🎉 Optimization complete! Check results/ folder.")
        
        # India sector recommendations with graphs & pie chart (parameter responsive)
        recs = india_sector_recommendation(df_results, alpha, beta)
        st.subheader("🇮🇳 India Sector Fund Allocation Recommendations")
        st.markdown(recs['summary'])
        for detail in recs['details']:
            st.markdown(f"**• {detail}**")

        # Graphs: Bar chart gaps & Pie allocation
        col1, col2 = st.columns(2)
        with col1:
            fig, ax = plt.subplots()
            ax.bar(recs['sectors'], recs['gaps'])
            ax.set_title('India vs Global: Weighted Sector Gaps (neg=prioritize)')
            ax.set_ylabel('Gap')
            st.pyplot(fig)

        with col2:
            fig, ax = plt.subplots()
            ax.pie(recs['weights'], labels=recs['sectors'], autopct='%1.1f%%')
            ax.set_title('Fund Allocation %')
            st.pyplot(fig)

        st.markdown("**Insights:** Allocation changes with α Innovation/β Return weights. Neg gaps prioritized.")

else:
    st.info("👆 Upload an Excel file to start")

    # Cleanup temp on rerun (optional)
    if os.path.exists('temp_dataset.xlsx'):
        try:
            os.remove('temp_dataset.xlsx')
        except:
            pass

# Footer
st.markdown("---")

