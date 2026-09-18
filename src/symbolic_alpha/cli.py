import os
import sys
import time
import click
import numpy as np
from rich.console import Console
from rich.panel import Panel

from symbolic_alpha.evaluator import ChimeraEngine, InstructionBuilder
from symbolic_alpha.orthogonality_filter import TriHurdleFilter
from symbolic_alpha.genetic_synthesizer import GeneticSynthesizer

console = Console()


@click.group()
def cli():
    """Symbolic Alpha Synthesizer: High-Performance Mathematical Alpha Discovery."""
    pass


@cli.command()
@click.option("--features", default=10, help="Number of synthetic features.")
@click.option("--rows", default=5000, help="Number of rows per era.")
@click.option("--eras", default=10, help="Number of distinct eras.")
@click.option("--generations", default=5, help="Number of genetic generations.")
@click.option("--pop-size", default=30, help="Population size per generation.")
@click.option("--vault", default="data/alpha_vault.json", help="Path to alpha vault output.")
def mine(features: int, rows: int, eras: int, generations: int, pop_size: int, vault: str):
    """Run autonomous genetic alpha mining on simulated multi-era market data."""
    header = (
        "[bold cyan]Symbolic Alpha Synthesizer[/bold cyan] - Autonomous Genetic Mining Engine\n"
        f"Features: {features} | Total Rows: {rows * eras:,} | Eras: {eras} | Generations: {generations}"
    )
    console.print(Panel.fit(header, border_style="cyan"))

    np.random.seed(42)
    total_rows = rows * eras
    feat_matrix = np.random.randn(total_rows, features).astype(np.float32)
    latent_signal = np.tanh(feat_matrix[:, 0] - feat_matrix[:, 1]) * np.sin(feat_matrix[:, 2])
    target = latent_signal + 0.15 * np.random.randn(total_rows).astype(np.float32)
    era_labels = np.repeat([f"era_{i:03d}" for i in range(eras)], rows)

    os.makedirs(os.path.dirname(vault) if os.path.dirname(vault) else ".", exist_ok=True)
    filter_gate = TriHurdleFilter(min_sharpe=0.8, max_factor_corr=0.35, min_positive_era_ratio=0.60)
    synthesizer = GeneticSynthesizer(
        num_features=features,
        pop_size=pop_size,
        tournament_size=3,
        max_depth=4,
        vault_path=vault,
        filter_gate=filter_gate
    )

    t0 = time.perf_counter()
    res_vault = synthesizer.evolve_on_dataset(feat_matrix, target, era_labels, generations=generations)
    dur = time.perf_counter() - t0

    console.print(f"\n[bold green]Mining Complete in {dur:.2f}s![/bold green] Cataloged {len(res_vault.entries)} alphas -> {vault}")


@cli.command()
@click.option("--rows", default=100000, help="Number of rows for benchmark.")
def benchmark(rows: int):
    """Benchmark vectorized C++ kernel throughput on Apple Silicon / ARM64."""
    console.print(f"[*] Benchmarking C++ vectorized engine across {rows:,} rows...")
    engine = ChimeraEngine(capacity_rows=rows)
    f0 = np.random.randn(rows).astype(np.float32)
    f1 = np.random.randn(rows).astype(np.float32)
    features = np.column_stack([f0, f1])

    ib = InstructionBuilder()
    ib.load_feat(0, 0)
    ib.load_feat(1, 1)
    ib.sub(2, 0, 1)
    ib.abs(3, 0)
    ib.load_imm(4, 1.0)
    ib.add(5, 3, 4)
    ib.safe_div(6, 2, 5)
    ib.tanh(7, 6)
    instrs = ib.build()

    iterations = 500
    t0 = time.perf_counter()
    for _ in range(iterations):
        _ = engine.execute(instrs, features)
    elapsed = time.perf_counter() - t0
    engine.close()

    evals_per_sec = (iterations * rows) / elapsed
    summary = (
        f"[bold green]Throughput:[/bold green] {evals_per_sec:,.0f} row-evaluations/sec\n"
        f"[bold cyan]Formula Rate:[/bold cyan] {(iterations / elapsed) * 60:,.0f} formulas/minute\n"
        f"Execution Time for {iterations} iterations: {elapsed:.4f}s"
    )
    console.print(Panel.fit(summary, border_style="green"))


@cli.command()
def audit():
    """Run automated Power of 10 static AST safety invariants audit."""
    from scripts.audit_safety_invariants import audit_cpp_file
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    target = os.path.join(base_dir, "csrc", "chimera_eval.cpp")
    errors = audit_cpp_file(target)
    if errors:
        for e in errors:
            console.print(f"[bold red]VIOLATION:[/bold red] {e}")
        sys.exit(1)
    console.print("[bold green][PASS][/bold green] All Power of 10 Invariants satisfied (0 violations).")


@cli.command()
def demo():
    """Run complete 1-second live demonstration."""
    console.print("[bold cyan]Running Symbolic Alpha Synthesizer Live Demo...[/bold cyan]")
    ctx = click.get_current_context()
    ctx.invoke(benchmark, rows=50000)
    ctx.invoke(audit)


if __name__ == "__main__":
    cli()
