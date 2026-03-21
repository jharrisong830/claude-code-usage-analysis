# Claude Code Usage Analysis

## Goal

A Marimo notebook project for analyzing Claude Code session statistics over time. The notebook aggregates per-session JSON files, computes summary statistics, and renders interactive reports. Reports can be exported as static HTML or WASM for sharing.

## Data Source

Session payloads are written to `~/.claude-usage/<session_id>.json` by the statusline script. One file per session.

### Schema

```json
{
  "session_id": "string",
  "updated_at": "ISO8601 timestamp",
  "model": "string",
  "cwd": "string",
  "cost_usd": "number",
  "duration_ms": "number",
  "lines_added": "number",
  "lines_removed": "number",
  "context_window": {
    "used_percentage": "number",
    "size": "number"
  },
  "tokens": {
    "current": {
      "input": "number",
      "output": "number",
      "cache_write": "number",
      "cache_read": "number"
    },
    "total": {
      "input": "number",
      "output": "number"
    }
  }
}
```

## Tooling

- **Runtime**: Python, managed with `uv`
- **Notebook**: Marimo (`marimo edit` for development, `marimo export html` or WASM for sharing)
- **Platform**: macOS (Homebrew)

## Export

- Static HTML: `marimo export html <notebook>.py -o report.html`
- Interactive WASM: works if all dependencies have Pyodide-compatible wheels (pandas, polars, altair, plotly all do)
