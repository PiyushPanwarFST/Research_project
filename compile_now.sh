#!/bin/bash

# Simple LaTeX Compilation Script
# This script compiles SSR_XgE copy.tex

set -e  # Exit on error

cd /Users/piyushpanwar/research_project/src

TEX_FILE="SSR_XgE copy.tex"
BASE_NAME="SSR_XgE copy"

echo "=========================================="
echo "LaTeX Compilation"
echo "=========================================="
echo ""
echo "Compiling: $TEX_FILE"
echo ""

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "❌ ERROR: pdflatex not found!"
    echo ""
    echo "Please install LaTeX first:"
    echo "  brew install --cask basictex"
    echo ""
    echo "Then restart your terminal or run:"
    echo "  eval \"\$(/usr/libexec/path_helper)\""
    echo ""
    exit 1
fi

echo "✅ pdflatex found: $(which pdflatex)"
echo ""

# Compile (simple compilation, no bibliography needed)
echo "Running pdflatex..."
pdflatex "$TEX_FILE"

echo ""
echo "=========================================="
echo "✅ Compilation Complete!"
echo "=========================================="
echo ""
echo "📄 PDF file: ${BASE_NAME}.pdf"
echo ""

# Try to open the PDF (macOS)
if [ -f "${BASE_NAME}.pdf" ]; then
    echo "Opening PDF..."
    open "${BASE_NAME}.pdf" 2>/dev/null || echo "Please open ${BASE_NAME}.pdf manually"
else
    echo "⚠️  PDF file not found. Check for errors above."
fi

