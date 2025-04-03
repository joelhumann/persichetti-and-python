#!/bin/bash
set -e

echo "🔄 Generating .rst files..."
sphinx-apidoc -f -o docs/source/ persichetti --separate

echo "🔧 Building docs..."
sphinx-build -b html docs/source docs/build/html

echo "📁 Deploying to top-level /docs/..."
rsync -a --delete docs/build/html/ docs/ \
  --exclude source --exclude build --exclude conf.py --exclude index.rst

echo "📦 Committing and pushing..."
git add docs/
git commit -m "Auto-update Sphinx documentation"
git push origin main

echo "✅ Done!"
