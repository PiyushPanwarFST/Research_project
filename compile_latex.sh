#!/bin/bash

# LaTeX Compilation Script for extended_paper.tex
# Make sure LaTeX is installed before running this script

echo "=========================================="
echo "LaTeX Compilation Script"
echo "=========================================="
echo ""

# Navigate to project directory
cd /Users/piyushpanwar/research_project

# Check if pdflatex is available
if ! command -v pdflatex &> /dev/null; then
    echo "❌ ERROR: pdflatex not found!"
    echo ""
    echo "Please install LaTeX first:"
    echo "  brew install --cask basictex"
    echo ""
    echo "Then restart your terminal or run:"
    echo "  eval \"\$(/usr/libexec/path_helper)\""
    exit 1
fi

echo "✅ pdflatex found: $(which pdflatex)"
echo ""

# Determine which .tex file to compile
TEX_FILE=""

if [ -f "extended_paper.tex" ]; then
    TEX_FILE="extended_paper.tex"
    echo "📄 Found: extended_paper.tex"
elif [ -f "src/SSR_XgE copy.tex" ]; then
    TEX_FILE="src/SSR_XgE copy.tex"
    echo "📄 Found: src/SSR_XgE copy.tex"
else
    echo "❌ ERROR: No .tex file found!"
    echo "Please ensure you have a .tex file in the project directory."
    exit 1
fi

BASE_NAME=$(basename "$TEX_FILE" .tex)
DIR_NAME=$(dirname "$TEX_FILE")

echo "📝 Compiling: $TEX_FILE"
echo "📁 Output directory: $DIR_NAME"
echo ""

# Step 1: First pdflatex run
echo "Step 1/4: Running pdflatex (first pass)..."
cd "$DIR_NAME"
pdflatex "$(basename "$TEX_FILE")" || {
    echo "❌ Error in first pdflatex run"
    exit 1
}
echo "✅ First pass complete"
echo ""

# Step 2: Check if .bib file exists
BIB_FILE="${BASE_NAME}.bib"
if [ -f "$BIB_FILE" ]; then
    echo "Step 2/4: Running BibTeX..."
    bibtex "$BASE_NAME" || {
        echo "⚠️  Warning: BibTeX had issues (this is okay if you don't have citations)"
    }
    echo "✅ BibTeX complete"
    echo ""
    
    # Step 3: Second pdflatex run
    echo "Step 3/4: Running pdflatex (second pass)..."
    pdflatex "$(basename "$TEX_FILE")" || {
        echo "❌ Error in second pdflatex run"
        exit 1
    }
    echo "✅ Second pass complete"
    echo ""
    
    # Step 4: Third pdflatex run
    echo "Step 4/4: Running pdflatex (third pass)..."
    pdflatex "$(basename "$TEX_FILE")" || {
        echo "❌ Error in third pdflatex run"
        exit 1
    }
    echo "✅ Third pass complete"
else
    echo "Step 2/4: No .bib file found, skipping BibTeX..."
    echo "⚠️  If you have citations, make sure you have a .bib file"
    echo ""
fi

echo ""
echo "=========================================="
echo "✅ Compilation Complete!"
echo "=========================================="
echo ""
echo "📄 PDF file: $DIR_NAME/${BASE_NAME}.pdf"
echo ""

# Try to open the PDF (macOS)
if [ -f "${BASE_NAME}.pdf" ]; then
    echo "Opening PDF..."
    open "${BASE_NAME}.pdf" 2>/dev/null || echo "Please open ${BASE_NAME}.pdf manually"
fi

