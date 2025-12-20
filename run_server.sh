#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
cd ml_inference_server
python main.py

