# Quantum Investment Optimization Model (QIOM) 🚀🛸

A Streamlit app for quantum-inspired fund allocation across countries (India vs China/Singapore/South Korea). Uses QUBO solvers to maximize Z = α*Innovation + β*Return under budget constraint.

## Features
- Excel upload (columns: Year, Country, RD, VC, Startups, Patents, Return)
- Sliders: α/budget/β
- Quantum (scipy enumeration) vs Classical solvers
- India sector recs (% RD/VC/Startups/Patents based on gaps)
- Results table, comparison plot

## Local Run
```bash
pip install -r requirements.txt
streamlit run app.py
```
Visit http://localhost:8501
## Architecture
main.py: core pipeline
src/: modules (data_loader, preprocessing min-max norm, model Z-score, qubo, solvers pure-python)
app.py: Streamlit UI

Sample data in data/dataset.xlsx

