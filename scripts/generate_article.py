from pathlib import Path
from textwrap import dedent
import pandas as pd
import shutil

FIG_EXTS = {".png", ".jpg", ".jpeg", ".pdf"}
TAB_EXTS = {".csv", ".tsv"}


# ---------------- Path resolver (Windows-safe, Code Ocean-aware) ---------------- #

def _in_code_ocean() -> bool:
    return Path("/reports").exists() and Path("/scripts").exists()
    
def _resolve(path_str: str) -> Path:
    """
    If running locally and given an absolute like '/reports' or '/results',
    map it to '<cwd>/reports' or '<cwd>/results'. In Code Ocean, keep absolute.
    """
    p = Path(path_str)
    if p.is_absolute() and not _in_code_ocean():
        if path_str.startswith("/results") or path_str.startswith("/reports"):
            return Path.cwd() / path_str.lstrip("/")
    return p if p.is_absolute() else (Path.cwd() / p)

# ---------------- Utilities ---------------- #

def _discover_figures(dir_path: Path):
    d = Path(dir_path)
    return [p for p in sorted(d.rglob("*"))
            if p.is_file() and p.suffix.lower() in FIG_EXTS]

def _discover_tables(dir_path: Path):
    d = Path(dir_path)
    return [p for p in sorted(d.rglob("*"))
            if p.is_file() and p.suffix.lower() in TAB_EXTS]

def _csv_to_tabular_str(p: Path, max_rows: int = 50) -> str:
    """
    Read CSV/TSV and convert to a LaTeX tabular string, with:
    - At most `max_rows` rows
    - Booktabs style
    - Floats formatted to 2 decimal places
    - Special handling for summary_by_cyl to get grouped headers:
          mpg (mean, median, std), hp (...), wt (...)
    """
    sep = "," if p.suffix.lower() == ".csv" else "\t"
    df = pd.read_csv(p, sep=sep)

    if len(df) > max_rows:
        df = df.head(max_rows)

    # SPECIAL CASE: pretty presentation for summary_by_cyl
    if p.stem == "summary_by_cyl":
        # Expect columns: cyl, mpg_mean, mpg_median, mpg_std, hp_mean, ..., wt_std
        if "cyl" in df.columns:
            df = df.set_index("cyl")

        # Build MultiIndex columns: (mpg, mean), (mpg, median), ...
        new_cols = []
        for col in df.columns:
            if "_" in col:
                base, stat = col.split("_", 1)
                new_cols.append((base, stat))
            else:
                # Fallback: treat as a single-level column
                new_cols.append((col, ""))

        df.columns = pd.MultiIndex.from_tuples(new_cols)

        # Round floats for readability
        df = df.round(2)

        # Column format: one 'l' for index + 'r' for each numeric column
        col_fmt = "l" + "r" * df.shape[1]

        latex = df.to_latex(
            index=True,
            escape=True,
            longtable=False,
            column_format=col_fmt,
            multicolumn=True,
            multicolumn_format="c",
            float_format="%.2f",
        )

    else:
        # Generic path for all other tables
        df = df.round(2)
        latex = df.to_latex(
            index=False,
            escape=True,
            longtable=False,
            column_format="".join(["l"] * len(df.columns)),
            float_format="%.2f",
        )

    # Normalize rules (booktabs-compatible)
    latex = latex.replace("\\hline", "\\midrule")
    return latex



# ---------------- Builders ---------------- #

def begin_document(title: str, authors: list, affiliation: str, abstract_text: str) -> str:
    authors_block = " \\\\ ".join(authors or [])
    return dedent(f"""
    \\documentclass[preprint,12pt]{{elsarticle}}
    \\usepackage{{graphicx}}
    \\usepackage{{booktabs}}
    \\usepackage{{siunitx}}
    \\usepackage{{hyperref}}
    \\usepackage{{caption}}
    \\captionsetup{{font=small}}
    \\journal{{ }}

    \\begin{{document}}

    \\begin{{frontmatter}}
    \\title{{{title}}}
    \\author[aff1]{{{authors_block}}}
    \\address[aff1]{{{affiliation}}}
    \\begin{{abstract}}
    {abstract_text}
    \\end{{abstract}}
    \\begin{{keyword}}
    reproducibility \\sep manuscript \\sep Code Ocean
    \\end{{keyword}}
    \\end{{frontmatter}}

    \\section{{Introduction}}
    This manuscript was auto-generated from pipeline outputs.

    """).lstrip()

def generate_figures(results_dir: str | Path, docs_dir: str | Path) -> str:
    """
    Copy all figures from results -> docs and include them.
    Manuscript will live in /docs, so include by filename only.
    """
    results = _resolve(str(results_dir))
    docs = _resolve(str(docs_dir))

    docs.mkdir(parents=True, exist_ok=True)
    figs = _discover_figures(results)
    for fig in _discover_figures(results):
        target = docs / fig.name
        # Copy or overwrite to keep docs current
        shutil.copy2(fig, target)

    figs = _discover_figures(docs)
    section = ["\\section{Figures}"]
    if not figs:
        section.append("No figures found in /docs.")
    else:
        for i, fig in enumerate(figs, start=1):
            fname = fig.name
            section.append(dedent(f"""
            \\begin{{figure}}[ht]
            \\centering
            \\includegraphics[width=0.9\\linewidth]{{{fname}}}
            \\caption{{Place holder for caption}}
            \\label{{fig:{fig.stem}}}
            \\end{{figure}}
            """).strip())
    return "\n".join(section) + "\n"

def generate_tables(results_dir: str | Path) -> str:
    """Read CSV/TSV from results and include as LaTeX tables."""
    results = _resolve(str(results_dir))
    tabs = _discover_tables(results)

    section = ["\\section{Tables}"]
    if not tabs:
        section.append("No tables found in /results.")
    else:
        for i, t in enumerate(tabs, start=1):
            try:
                latex = _csv_to_tabular_str(t)
            except Exception as e:
                latex = dedent(f"""
                % Failed to read {t.name}: {e}
                \\begin{{tabular}}{{l}}
                \\toprule
                Unable to render table {t.name}.\\\\
                \\bottomrule
                \\end{{tabular}}
                """).strip()
            section.append(dedent(f"""
            \\begin{{table}}[ht]
            \\caption{{Place holder for caption}}
            \\label{{tab:{t.stem}}}
            \\centering
            {latex}
            \\end{{table}}
            """).strip())
    return "\n".join(section) + "\n"

def end_document() -> str:
    return dedent(r"""
    \section{Methods}
    Brief description of methods.

    \section{Results}
    Summary of key results.

    \section{Discussion}
    Discussion and limitations.

    \section{Conclusion}
    Final remarks.

    \bibliographystyle{elsarticle-num}
    \bibliography{references}
    \end{document}
    """).lstrip()


# ---------------- Orchestrator ---------------- #

def build_elsevier_manuscript(
    results_dir: str = "/results",
    docs_dir: str = "/reports",
    out_path: str = "/reports/manuscript.tex",
    title: str = "Auto-generated Elsevier Manuscript",
    authors: list | None = None,
    affiliation: str = "Affiliation",
    abstract_text: str = "Auto-generated manuscript compiled from pipeline outputs.",
) -> str:
    """
    Create LaTeX by concatenating:
    begin_document → figures (copied results→docs, then included) → tables (from results) → end_document.
    Handles local vs Code Ocean absolute paths.
    """
    authors = authors or []

    # Resolve directories
    results = _resolve(results_dir)
    docs = _resolve(docs_dir)
    out = _resolve(out_path)

    # Ensure folders exist
    docs.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)

    # Build manuscript sections
    parts = []
    parts.append(begin_document(title, authors, affiliation, abstract_text))
    parts.append(generate_figures(results, docs))
    parts.append(generate_tables(results))
    parts.append(end_document())

    # Write .tex file
    tex = "\n".join(parts)
    out.write_text(tex, encoding="utf-8")

    # ---------- PDF BUILD ----------
    import subprocess

    try:
        # First LaTeX pass
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", out.name],
            cwd=out.parent,
            check=True
        )

        # Run BibTeX only if references file exists
        if (out.parent / "references.bib").exists():
            subprocess.run(
                ["bibtex", out.with_suffix(".aux").name],
                cwd=out.parent,
                check=True
            )

        # Second LaTeX pass (resolve refs, TOC, etc.)
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", out.name],
            cwd=out.parent,
            check=True
        )

        print("PDF generated:", out.parent / out.with_suffix(".pdf").name)

    except Exception as e:
        print("PDF compilation failed:", e)
    # -------------------------------

    return str(out)

