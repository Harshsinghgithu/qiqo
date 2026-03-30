# India Sector Recs Parameter Responsive Fix
Status: In Progress

1. [x] Kill streamlit server if running
2. Update src/model.py: Add alpha/beta params to india_sector_recommendation(df, alpha, beta) → recompute compute_scores/objective before gaps → weighted Innovation gaps change with sliders
3. Update main.py & app.py calls: pass alpha, beta to recs()
4. Test: streamlit run app.py → Verify allocation % changes with alpha/beta sliders
5. Git commit/push → Deploy auto-updates on Streamlit Cloud
6. [ ] COMPLETE ✅
