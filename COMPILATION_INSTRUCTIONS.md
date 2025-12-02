# 📄 LaTeX Compilation Instructions

## ✅ **FILES CREATED:**

1. ✅ **`Updated_Results_Report.tex`** - Main report with graphs and claims
2. ✅ **`Supplementary_Data_Tables.tex`** - All 192 scenarios in tables

---

## 🔧 **COMPILATION STEPS:**

### **Option 1: Using Overleaf (Recommended)**

1. **Go to:** https://www.overleaf.com
2. **Create a new project** → Upload Project
3. **Upload these files:**

   - `Updated_Results_Report.tex`
   - `Supplementary_Data_Tables.tex`
   - `assets/` folder (with all 9 PNG images)

4. **Compile `Updated_Results_Report.tex`:**

   - Click "Recompile"
   - Check if all 9 graphs appear correctly
   - Download PDF: `Updated_Results_Report.pdf`

5. **Compile `Supplementary_Data_Tables.tex`:**
   - Click "Recompile"
   - Check if all tables are readable
   - Download PDF: `Supplementary_Data_Tables.pdf`

---

### **Option 2: Using Local LaTeX (pdflatex)**

**For Main Report:**

```bash
cd /Users/piyushpanwar/research_project
pdflatex Updated_Results_Report.tex
pdflatex Updated_Results_Report.tex  # Run twice for references
```

**For Supplementary Tables:**

```bash
pdflatex Supplementary_Data_Tables.tex
pdflatex Supplementary_Data_Tables.tex  # Run twice
```

---

## ✅ **VERIFICATION CHECKLIST:**

### **Main Report (`Updated_Results_Report.pdf`):**

- [ ] Title page appears correctly
- [ ] All 9 graphs are visible and clear
- [ ] Graph captions are correct
- [ ] All claims text is present
- [ ] Colab links are clickable
- [ ] No compilation errors

### **Supplementary Tables (`Supplementary_Data_Tables.pdf`):**

- [ ] Title page appears
- [ ] All 3 sections (R=0.4, R=0.5, R=0.7) are present
- [ ] Each section has 64 scenarios × 3 methods = 192 rows
- [ ] Tables are readable (landscape orientation)
- [ ] Bayes (IP) rows are bolded
- [ ] No compilation errors

---

## 📋 **GRAPH FILES MAPPING:**

The graphs are referenced in the LaTeX as:

**R=0.4:**

- MSE: `assets/Screenshot_2025-11-28_at_6.06.11_PM-c656172b-d233-43a3-be8f-73e302a01095.png`
- Bias: `assets/Screenshot_2025-11-28_at_6.06.42_PM-e7f24c29-6343-4102-ae0f-52a505520cac.png`
- Width: `assets/Screenshot_2025-11-28_at_6.07.01_PM-a6407a1e-5c68-4818-96c0-c7dd66f12121.png`

**R=0.5:**

- MSE: `assets/Screenshot_2025-11-28_at_6.10.44_PM-2bfd1df5-fc90-427f-a3aa-45f6e952c12e.png`
- Bias: `assets/Screenshot_2025-11-28_at_6.11.15_PM-97126cfd-bcb8-490d-b79f-79532f293197.png`
- Width: `assets/Screenshot_2025-11-28_at_6.11.40_PM-45455f13-6173-420b-84c2-7a6d21d1aa56.png`

**R=0.7:**

- MSE: `assets/Screenshot_2025-11-28_at_6.12.51_PM-9d704390-368b-4c46-80e4-1727db5188a3.png`
- Bias: `assets/Screenshot_2025-11-28_at_6.13.43_PM-ee08bff3-afcd-4360-b461-00c4e40c305e.png`
- Width: `assets/Screenshot_2025-11-28_at_6.13.55_PM-0165a897-7b20-4b91-9571-41abf1754cab.png`

**Make sure the `assets/` folder is in the same directory as the `.tex` files!**

---

## ⚠️ **TROUBLESHOOTING:**

### **Issue: Graphs not appearing**

- **Solution:** Make sure `assets/` folder is uploaded to Overleaf or in the same directory as `.tex` files

### **Issue: Table too wide**

- **Solution:** The supplementary tables use `landscape` orientation. If still too wide, reduce font size or adjust margins

### **Issue: Compilation errors**

- **Solution:** Make sure all packages are installed:
  - `graphicx`, `geometry`, `hyperref`, `float`, `caption`, `booktabs`, `longtable`, `amsmath`

---

## 📧 **READY FOR PROFESSOR:**

After compilation:

1. ✅ Review both PDFs
2. ✅ Verify all graphs are clear
3. ✅ Check all numbers match your claims
4. ✅ Attach both PDFs to email
5. ✅ Include Colab links in email body

**Good luck!** 🎉

