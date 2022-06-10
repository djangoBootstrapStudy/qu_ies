#!/usr/bin/env bash

echo "Run black"
./venv/Scripts/black.exe .


echo "Run isort"
./venv/Scripts/isort.exe .


echo "Run tests"
python manage.py test

echo "black, isort, tests Done."
sleep 9999
