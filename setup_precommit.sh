#!/bin/bash
# Setup pre-commit hooks for MediaHub Downloader

echo "Setting up pre-commit hooks..."

# Install pre-commit if not already installed
if ! command -v pre-commit &> /dev/null; then
    echo "Installing pre-commit..."
    pip install pre-commit
fi

# Install the hooks
echo "Installing pre-commit hooks..."
pre-commit install

# Run the hooks on all files to make sure everything is clean
echo "Running pre-commit hooks on all files..."
pre-commit run --all-files

echo "Pre-commit setup complete!"