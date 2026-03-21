import marimo

__generated_with = "0.21.1"
app = marimo.App(width="full", app_title="claude-code-usage-analysis")


@app.cell
def __imports():
    import pandas as pd
    import json
    from pathlib import Path
    import marimo as mo

    return Path, json, mo, pd


@app.cell
def __load_data(Path, json, pd):
    usage_dir = Path.home() / ".claude-usage"

    raw_data = [json.loads(f.read_text()) for f in usage_dir.glob("*.json")]

    df_main = pd.json_normalize(raw_data, sep="_")

    df_main.head()
    return (df_main,)


@app.cell
def _(df_main, mo):
    total_cost = df_main["cost_usd"].sum()
    total_sessions = len(df_main)
    total_hours = df_main["duration_ms"].sum() / 3_600_000
    total_lines_added = df_main["lines_added"].sum()

    summary = mo.hstack([
        mo.stat(f"${total_cost:.2f}", label="Total cost"),
        mo.stat(str(total_sessions), label="Sessions"),
        mo.stat(f"{total_hours:.1f}h", label="Total duration"),
        mo.stat(f"{total_lines_added:,}", label="Lines added")
    ])

    summary
    return


if __name__ == "__main__":
    app.run()
