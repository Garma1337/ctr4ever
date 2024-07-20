#!/bin/bash

echo "Starting test suite ..."

python -m unittest discover -v --pattern "*test.py" --top-level-directory ../ctr4ever/tests/unit

echo "Test suite finished"
