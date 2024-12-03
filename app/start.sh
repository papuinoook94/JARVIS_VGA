#!/bin/bash

# Iniciar backend
python main.py --host 127.0.0.1 --port 8000 &

# Iniciar frontend
sleep 5
python -m streamlit run app.py --server.port=8501 --server.address=127.0.0.1
