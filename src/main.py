from __future__ import annotations
from pathlib import Path
import typer
from rich import print
from .config import THRESHOLD
from .judge import judge_delta
from .snapshot import capture, load_store, save_store

app = typer.Typer()

@app.command()
def watch(url: str, store: Path = typer.Option(Path("data/snapshot.json"))):
    current = capture(url)
    prior = load_store(store)
    if prior is None:
        save_store(store, current)
        print(f"[green]Baseline saved[/green] → {store} (hash={current['hash'][:12]}…)")
        return
    if prior.get("hash") == current["hash"]:
        print("[green]No content hash change[/green]")
        return
    print("[yellow]Hash changed — asking Sentinel agent…[/yellow]")
    verdict = judge_delta(prior.get("text", ""), current["text"])
    score = float(verdict.get("score", 0))
    print(verdict)
    if score >= THRESHOLD:
        print(f"[red]MATERIAL[/red] score={score}")
    else:
        print(f"[cyan]Minor[/cyan] score={score}")
    save_store(store, current)

if __name__ == "__main__":
    app()
