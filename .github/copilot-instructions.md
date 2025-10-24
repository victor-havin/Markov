<!-- .github/copilot-instructions.md - guidance for AI coding agents working on this repository -->
# Repo snapshot: Markov random-walk experiments

This repository contains a small experimental Python project that simulates a random walk and fits a curve to the resulting histogram. The single main script is `Markov.py` (under the repo root). Use the guidance below to make targeted code changes, fix bugs, and add features reliably.

Key facts (what an agent needs to know immediately):
- Entry point: `Markov.py` — the script runs a simulation loop at module import time (the bottom `for i in range(ITERATIONS): walk(10, LENGTH)` block). Edits that change top-level runtime behavior will execute on import.
- Primary dependencies: `numpy`, `matplotlib`, and `scipy` (for `curve_fit`). Ensure these are available when running or testing.
- Platform: developer uses Windows with PowerShell; prefer PowerShell command examples.

Quick run (PowerShell):
```powershell
# from repository root
python .\Markov.py
```

What to watch for (bugs & patterns found):
- Global mutable state: `space`, `result`, `time`, and `grid` are module-level arrays mutated by `walk()` and `step()`. Prefer converting simulation state into function-local data structures or encapsulating in a class when adding features or tests.
- Potential infinite-loop / index errors:
  - `step(pos, time)` returns `pos+1` or `pos-1` but `walk()` calls `space[position-1]` after `step()`. If `position` becomes 0 this writes `space[-1]` unexpectedly (wraps to last element). Also, `while position < length:` with position increasing can still get stuck if `position` decreases or oscillates. Be careful when changing logic.
- Unused variables / typos: variable `time` is both a module-level array and passed as an argument name in `step(pos, time)`; this is okay but confusing. `plot_results()` title says "Time Dillation" (typo).

Suggested, safe-first edits for AI agents:
- Low-risk: Fix typos, add an explicit `if __name__ == '__main__':` guard so the script doesn't run on import, and wrap simulation in a function `run_simulation(iterations=ITERATIONS)` that returns results. These are minimal, backwards-compatible changes.
- Medium-risk: Refactor to avoid module-level mutable arrays — return arrays from `run_simulation()` and pass them into plotting and fitting functions. Add simple CLI args (start, length, iterations) using `argparse`.
- Higher-risk: Rework the random walk semantics (e.g., boundary conditions, time-dependent probability function). Add unit tests that validate step behavior and deterministic runs by seeding `numpy.random`.

Examples and local patterns to follow when modifying code:
- Keep numerical constants near the top (`LENGTH`, `ITERATIONS`) so experiments are easy to change.
- Small functions: `step()`, `walk()`, `plot_results()`, and `match_results()` are the main units. When adding features, keep changes localized: e.g., modify `step()` and add tests for its outputs rather than sweeping changes across the script.
- When adding tests, prefer pure functions (no global state). If you must test the current script, run with `python -c "import Markov; ..."` only after adding `if __name__ == '__main__'` guard.

Run & debug tips:
- To run quickly and avoid plots blocking automated runs, set `matplotlib` to a non-interactive backend or conditionally call `plot_results()` only when a `--plot` flag is present.
  Example: set environment variable for headless runs: `set MPLBACKEND=Agg; python .\Markov.py` in PowerShell.
- To reproduce runs, seed numpy: `np.random.seed(42)` at the start of `run_simulation()` or in tests.

Files to inspect for context and examples:
- `Markov.py` — single-file implementation; most code will be changed here.
- (No other modules detected in repository root.)

When editing, be explicit about intent in commit messages and PR descriptions: mention if you are moving execution out of module import, adding CLI flags, or making the simulation deterministic.

If you refactor into multiple modules, maintain the same top-level script behavior behind an `if __name__ == '__main__'` guard so existing experimental workflows continue to work.

Questions for the author (if clarification is needed):
- Should the script be runnable as a library (importable without side effects)? Recommended: yes — add `if __name__ == '__main__'`.
- Intended boundary handling: what should happen when the walker reaches 0 or LENGTH-1? (current code resets to 0 on negative but may index `-1`.)

If this is helpful, I can implement the low-risk changes (add main guard, fix typos, return results from a `run_simulation` function) and add a short README and a `requirements.txt` listing the dependencies.
