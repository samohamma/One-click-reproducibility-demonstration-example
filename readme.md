# RERITE – One-Click Reproducibility  
*A Demonstration Project for Reproducible Research Workflows in Python*

This project is part of the materials presented in **Tools for Practicing Reproducible Research Collaboration** during:

**REproducible Research In Transportation Engineering (RERITE)**  
*A Hands-On Tutorial 2.0 – Reproducible Manuscripts*  
**RERITE @ IEEE ITSC 2025 — November 18, 2025**

It provides a small, self-contained example of how to design, run, and document a **fully reproducible research workflow** using Python, Anaconda, and Jupyter Notebook. The project demonstrates how to structure files, generate deterministic outputs, and automatically build a LaTeX/PDF manuscript from analysis results.

---

## What This Example Demonstrates

- A clean folder layout for reproducible research  
- Environment control using `environment.yml`  
- Deterministic generation of results (CSV + figures) in `/results`  
- Automatic manuscript assembly (LaTeX + PDF) in `/reports`  
- A workflow that runs identically on any machine with the provided environment  
- Full compatibility with **Code Ocean** for containerized reproducibility  

---

## Project Structure

```
RERITE_demo/
│
├── data/            # Input dataset (mtcars)
├── scripts/         # Analysis, plotting, and manuscript generator
├── results/         # Reproducible outputs (CSV, PNG)
├── reports/         # Auto-generated LaTeX + PDF manuscript
├── environment.yml  # Reproducible Conda environment
├── readme.md  # Reproducible Conda environment
└── main.ipynb       # End-to-end reproducible workflow

```

---

## Environment Setup (Step 0A)

**Option A — Navigator:**  
Environments → Import → select `environment.yml` → name it `RERITE_demo` → Import  
(Do **not** launch Jupyter from Navigator.)

**Option B — Command Line:**  
```bash
conda env create -f environment.yml
```

---

## Running the Project (Step 0B)

To run this project correctly, always open **Anaconda Prompt** and execute:

```bash
conda activate RERITE_demo
cd path\to\RERITE_demo
jupyter lab
```

Launching Jupyter from anywhere else will not load the correct environment.

---

## Reproducibility on Code Ocean

This project can be uploaded directly into **Code Ocean**, where the same workflow runs within a containerized environment for fully transparent and citable reproducibility.

---

## License

This example is provided for instructional use as part of the RERITE tutorial series. You may adapt it for your own reproducibility workflows.
