# LaTeX Compilation Commands

## 📋 Installation Status
- ❌ LaTeX (pdflatex): NOT INSTALLED
- ❌ BibTeX: NOT INSTALLED

## 🔧 Step 1: Install LaTeX

Run this command in your terminal (requires password):
```bash
brew install --cask basictex
```

After installation, restart terminal OR run:
```bash
eval "$(/usr/libexec/path_helper)"
```

## ✅ Step 2: Verify Installation

Run these commands to check:
```bash
pdflatex --version
bibtex --version
```

## 📝 Step 3: Compile Your Paper

Your LaTeX file is located at: `src/SSR_XgE copy.tex`

### Option A: Simple Compilation (No Bibliography)
```bash
cd /Users/piyushpanwar/research_project/src
pdflatex "SSR_XgE copy.tex"
```

### Option B: Full Compilation (With Bibliography)
```bash
cd /Users/piyushpanwar/research_project/src

# Step 1: First pass
pdflatex "SSR_XgE copy.tex"

# Step 2: Run BibTeX (if you have citations)
bibtex "SSR_XgE copy"

# Step 3: Second pass
pdflatex "SSR_XgE copy.tex"

# Step 4: Third pass (to resolve all references)
pdflatex "SSR_XgE copy.tex"
```

### Option C: Use the Compilation Script
```bash
cd /Users/piyushpanwar/research_project
./compile_latex.sh
```

## 📄 Output
After compilation, you'll find:
- `SSR_XgE copy.pdf` in the `src/` directory

## 🚨 Note
The file `extended_paper.txt` is plain text, not LaTeX code. 
To compile it, you would need to convert it to proper LaTeX format first.

