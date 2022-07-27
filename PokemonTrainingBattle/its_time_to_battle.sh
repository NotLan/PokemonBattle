#!/usr/bin/env bash
echo "Its time to battle!"
echo "How many battles would you like to run?"
read -p "Number of Battles: " runs

poetry run pytest --flake-finder --flake-runs=$runs tests/battle.py -vvvvvv
