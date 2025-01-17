#!/bin/sh

echo "Running vecdb.py to create the vector database..."
python vecdb.py

echo "Running client.py to connect to the vector database..."
python client.py
