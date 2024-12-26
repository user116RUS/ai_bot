#!/bin/bash

ssh localhost -p222
cd ~/ai_v2/ai_bot
source venv/bin/activate
python3 manage.py $@