#!/bin/bash

# Start Streamlit app on port 8000 (for Azure)
streamlit run app.py --server.port 8000 --server.address 0.0.0.0 --server.enableCORS false
