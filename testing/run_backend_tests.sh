#!/bin/bash

echo "Starting test suite ..."

python -m unittest discover --pattern "*test.py" --top-level-directory ../ctr4ever

echo "Test suite finished"
