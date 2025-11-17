# RERITE – One-Click Reproducibility  
*A Demonstration Project for Reproducible Research Workflows in Python*

This repository extends the original **Transport Demo Project — mtcars (R-exact)** into a fully reproducible workflow used in:

**Tools for Practicing Reproducible Research Collaboration**  
**REproducible Research In Transportation Engineering (RERITE)**  
*A Hands-On Tutorial 2.0 – Reproducible Manuscripts*  
**RERITE @ IEEE ITSC 2025 — November 18, 2025**

The goal is to demonstrate how to create, run, and share a reproducible analysis pipeline using Python, Anaconda, and Jupyter Notebook. This includes:

- a clean project folder structure,  
- deterministic analysis outputs (`/results`),  
- auto-generated LaTeX/PDF manuscripts (`/reports`),  
- environment control through `environment.yml`, and  
- compatibility with both local setups and **Code Ocean**.

---

## Dataset

This demo uses the exact **mtcars** dataset from base R (same columns, same values).  
A convenience file `data/mtcars_with_model.csv` includes model names as a separate column.

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
└── main.ipynb       # End-to-end reproducible workflow
```

---

## Environment Setup

### Option A — Using Anaconda Navigator  
1. Open **Anaconda Navigator** → Environments → **Import**  
2. Select `environment.yml`  
3. Name the environment **`RERITE_demo`**  
4. Click **Import**  
5. Close Navigator (do **not** launch Jupyter from here)

### Option B — Command Line  
```bash
conda env create -f environment.yml
```

---

## Running the Project (Important)

Always run the notebook from **Anaconda Prompt**, not from Navigator or VS Code.

```bash
conda activate RERITE_demo
cd path\to\RERITE_demo
jupyter lab
```

This ensures that the correct environment is loaded, allowing the manuscript and figures to build without errors.

---

## How to Use the Notebook

Open `main.ipynb` and run the cells top-to-bottom. The notebook will:

1. Load the mtcars dataset from `/data`
2. Compute per-cylinder summary statistics  
3. Produce reproducible CSV and PNG outputs in `/results`
4. Automatically build a LaTeX manuscript and PDF inside `/reports`
5. Demonstrate an end-to-end reproducible research workflow

---

## Reproducibility on Code Ocean

This project can be uploaded directly into **Code Ocean**, where:

- the environment is automatically recreated,  
- the workflow executes deterministically, and  
- the manuscript builds identically inside a container.

This provides a fully portable and citable execution capsule.

---

## License

This example is provided for instructional use within the RERITE tutorial. You may reuse or extend it for your own reproducibility workflows.
