import pandas as pd
from pathlib import Path

def summarize_by_cyl(
    df: pd.DataFrame | None = None,
    input_csv: str | None = None,
    output_csv: str = "results/summary_by_cyl.csv"
) -> pd.DataFrame:
    """Compute summary stats by cylinder count (mpg, hp, wt)."""

    from .load_data import load_mtcars

    # Ensure directory
    Path(output_csv).parent.mkdir(parents=True, exist_ok=True)

    # Load df
    if df is None:
        if input_csv:
            df = pd.read_csv(input_csv)
        else:
            df = load_mtcars()
    # Optional: extra safety rounding
    df = df.round(2)
    # Compute summary table
    summary = (
        df.groupby("cyl")[["mpg", "hp", "wt"]]
          .agg(['mean', 'median', 'std'])
          .round(2)
    )

    # Flatten column MultiIndex
    summary.columns = [f"{col}_{stat}" for col, stat in summary.columns]

    # Save
    summary.to_csv(output_csv)

    return summary

if __name__ == "__main__":
    s = summarize_by_cyl()
    print(s.head())
