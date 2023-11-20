#!/bin/bash

source .venv/bin/activate
pip install --upgrade pytrends
git add -A .
git commit -m "Upgrade Pytrends library"
git push
