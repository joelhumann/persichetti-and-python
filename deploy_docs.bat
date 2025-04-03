@echo off
echo 🔄 Generating .rst files...
sphinx-apidoc -f -o docs\source persichetti --separate

echo 🔧 Building docs...
sphinx-build -b html docs\source docs\build\html

echo 📁 Copying HTML to top-level /docs...
robocopy docs\build\html docs /MIR /XD .doctrees source build

echo 📦 Committing and pushing to main...
git add docs
git commit -m "Auto-update Sphinx documentation"
git push origin main

echo ✅ Deployment complete.
pause
