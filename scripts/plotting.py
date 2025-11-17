from pathlib import Path
import pandas as pd

def plot_mpg_vs_hp(df: pd.DataFrame | None = None, input_csv: str | None = None,
                   output_png: str = "results/mtcars_mpg_vs_hp.png") -> str:
    """Scatter: horsepower vs mpg; color by cylinders; size by weight.
    - If `df` is provided, use it.
    - Else if `input_csv` is provided, read from CSV (legacy behavior).
    - Else, load from plotnine via `load_mtcars()` for zero-file setups.
    """
    from .load_data import load_mtcars

    Path(output_png).parent.mkdir(parents=True, exist_ok=True)
    if df is None:
        if input_csv:
            df = pd.read_csv(input_csv)
        else:
            df = load_mtcars()

    import matplotlib.pyplot as plt
    plt.figure()
    groups = df.groupby("cyl")
    for cyl, sub in groups:
        plt.scatter(sub["hp"], sub["mpg"], s=sub["wt"]*35, label=f"{int(cyl)} cyl")
    plt.title("mtcars: MPG vs HP (size ~ wt)")
    plt.xlabel("Horsepower (hp)")
    plt.ylabel("Miles per gallon (mpg)")
    plt.legend(title="cyl")
    plt.tight_layout()
    plt.savefig(output_png)
    plt.close()
    return output_png

if __name__ == "__main__":
    print(plot_mpg_vs_hp())
