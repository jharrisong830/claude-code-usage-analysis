import marimo

__generated_with = "0.21.1"
app = marimo.App(width="full", app_title="claude-code-usage-analysis")


@app.cell
def __imports():
    import pandas as pd
    import altair as alt
    import json
    from pathlib import Path
    import marimo as mo

    return Path, alt, json, mo, pd


@app.cell
def __load_data(Path, json, pd):
    usage_dir = Path.home() / ".claude-usage"

    raw_data = [json.loads(f.read_text()) for f in usage_dir.glob("*.json")]

    df_main = pd.json_normalize(raw_data, sep="_")
    return (df_main,)


@app.cell
def __enrich(Path, df_main, pd):
    df = df_main.copy()
    print(df.head())
    df["updated_at"] = pd.to_datetime(df["updated_at"], utc=True)
    df["date"] = df["updated_at"].dt.floor("D")
    df["duration_min"] = (df["duration_ms"] / 60_000).round(1)
    df["project"] = df["project"].apply(lambda p: Path(p).name if isinstance(p, str) else "other")
    return (df,)


@app.cell
def __summary(df, mo):
    total_cost = df["cost_usd"].sum()
    total_sessions = len(df)
    total_hours = df["duration_ms"].sum() / 3_600_000
    total_lines_added = df["lines_added"].sum()

    summary = mo.hstack([
        mo.stat(f"${total_cost:.2f}", label="Total cost"),
        mo.stat(str(total_sessions), label="Sessions"),
        mo.stat(f"{total_hours:.1f}h", label="Total duration"),
        mo.stat(f"{total_lines_added:,}", label="Lines added"),
    ])
    return (summary,)


@app.cell
def _(summary):
    summary
    return


@app.cell
def __cost_over_time(alt, df, mo):
    cost_over_time = mo.ui.altair_chart(
        alt.Chart(df).mark_bar().encode(
            x=alt.X("date:T", title="Date"),
            y=alt.Y("cost_usd:Q", title="Cost (USD)"),
            tooltip=["date:T", "project:N", "cost_usd:Q", "duration_min:Q"],
        ).properties(title="Cost per session", height=300)
    )
    return (cost_over_time,)


@app.cell
def _(cost_over_time):
    cost_over_time
    return


@app.cell
def __cost_by_project(alt, df, mo):
    by_project = (
        df.groupby("project", as_index=False)["cost_usd"]
        .sum()
        .sort_values("cost_usd", ascending=False)
    )

    cost_by_project = mo.ui.altair_chart(
        alt.Chart(by_project).mark_bar().encode(
            x=alt.X("cost_usd:Q", title="Total cost (USD)"),
            y=alt.Y("project:N", sort="-x", title=None),
            tooltip=["project:N", "cost_usd:Q"],
        ).properties(title="Cost by project", height=200)
    )
    return (cost_by_project,)


@app.cell
def _(cost_by_project):
    cost_by_project
    return


@app.cell
def __session_table(df, mo):
    session_table = mo.ui.table(
        df[["date", "project", "model", "cost_usd", "duration_min", "lines_added", "lines_removed", "context_window_used_percentage", "cwd"]]
        .sort_values("date", ascending=False)
        .reset_index(drop=True)
    )
    return (session_table,)


@app.cell
def _(session_table):
    session_table
    return


if __name__ == "__main__":
    app.run()
