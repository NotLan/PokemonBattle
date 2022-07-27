#!/usr/bin/env bash
echo "Its time to battle!"
echo "How many battles would you like to run?"
read -p "Number of Battles: " runs
read -p "Run in headed?(Yes/No): " headed

if [ $headed == 'Yes' ]
then
    poetry run pytest --headed --flake-finder --flake-runs=$runs tests/battle.py -vvvvvv
else
    poetry run pytest --flake-finder --flake-runs=$runs tests/battle.py -vvvvvv
fi

read -p "Would you like to see the Stats for pokemon battles?(Yes/No): " outcome

if [ $outcome == 'Yes' ]
then
  less 'battle_outcomes.json'
else
  echo "Have a good day!"
fi
