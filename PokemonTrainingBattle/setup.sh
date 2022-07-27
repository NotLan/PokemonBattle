#!/usr/bin/env bash

echo -e "Starting setup!\n"
echo "Checking for poetry installation..."
# If the command poetry doesn't exist
if ! command -v poetry &> /dev/null
then
  echo "Installing poetry..."
  # Install poetry to poetry's bin directory
  # This is $HOME/.poetry/bin on Unix
  # and %USERPROFILE%\.poetry\bin on Windows
  curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 -
  source "$HOME/.poetry/env"
fi

echo -e "Updating dependencies...\n"
poetry install
poetry run playwright install

echo -e "Setup complete!\n"
echo "Use poetry to run pytest:"
echo "  poetry run pytest tests/"
echo "  poetry run pytest tests/<somedir>"
echo "  poetry run pytest tests/<somedir>/<sometest>.py"
echo "  poetry run pytest --headed --reportportal tests/"
