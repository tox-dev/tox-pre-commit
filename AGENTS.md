# AGENTS.md

This file provides guidance to compatible agentic tools (Claude Code,
Codex, etc.) when working with code in this repository.

> [!note]
> This file is for AI assistant use only. Humans should follow the
> [contributing guide][CONTRIBUTING] and the
> [code of conduct][CoC] instead.

[CONTRIBUTING]: ./.github/CONTRIBUTING.md
[CoC]: ./.github/CODE_OF_CONDUCT.md


## ⚠️ Operating mode

> [!important]
> Bidirectional quizzing is mandatory. Surface every proposed change
> for human review before performing it; the operator will quiz you
> on rationale, diff, blast radius and rollback path. *In the same
> turn*, you quiz the operator back on the understanding of the
> change -- restate the goal in your own words, confirm scope
> boundaries, and ask for clarification on anything ambiguous. Do
> not assume implicit consent from previous turns; re-check,
> re-confirm.

Concretely:

* Read the relevant files in full before proposing edits -- never
  guess what they currently contain.
* Show diffs for non-trivial changes and pause for explicit
  approval.
* Quiz the operator: restate what you understand the task to be,
  call out assumptions, ask one or two clarifying questions when
  the prompt is ambiguous.
* Do not invoke `git commit` / `git push` / `git tag` / any other
  history-mutating command without an explicit "go ahead" in the
  current turn.
* Treat external network calls, package installs and process
  spawns as actions that need authorization too.
* When in doubt, ask. The operator prefers a clarifying question
  over an unwound mistake.


## ⚠️ Hard constraints

These are non-negotiable. Do not propose or implement changes that
violate any of them.

1. **No `setup.py`** at the repository root. The project relies
   exclusively on PEP 621 metadata in `pyproject.toml`.
2. **No `__init__.py`** under `src/tox_plugins/` or its
   sub-packages. The plugin lives in a PEP 420 implicit namespace
   package shared with other `tox_plugins.*` distributions.
3. **No `tests/__init__.py`.** Pytest must not promote the project
   root into `sys.path` via package discovery.
4. **MIT-NORUS license terms** remain in `LICENSE`. Do not strip or
   relicense without explicit maintainer approval.
5. **`shlex.join` only** for shell command composition. Never
   `shell=True`, never raw string concatenation into a subprocess.
6. **Sphinx-native docstrings** -- `:param X:`, `:returns:`,
   `:raises X:`. Not Google, not Napoleon, not Numpy.
7. **No `Co-Authored-By` trailer** generated automatically by
   tools. Maintainer adds attribution manually when warranted.


## Project layout

```
.
├── src/tox_plugins/<name>/_plugin.py   # the plugin itself
├── tests/
│   ├── conftest.py                     # loads tox.pytest
│   ├── smoke_test.py                   # importability
│   ├── importable_test.py              # entry-point exposure
│   └── integration_test.py             # tox.pytest behavioral tests
├── pyproject.toml                      # PEP 621 metadata
├── tox.ini                             # build / test envs
├── pytest.ini                          # pytest config
├── .pre-commit-config.yaml             # local lint orchestrator
├── .codecov.yml / .coveragerc          # coverage config
├── .github/
│   ├── workflows/                      # CI / cron
│   ├── reusables/tox-dev/workflow/     # tox-dev/workflow hook actions
│   ├── actions/cache-keys/             # composite action
│   ├── FUNDING.yml                     # sponsors
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── SECURITY.md
│   ├── THREAT_MODEL.md
│   ├── INCIDENT_RESPONSE.md
│   ├── ISSUE_TEMPLATE/                 # GitHub form templates
│   └── PULL_REQUEST_TEMPLATE.md
├── AGENTS.md / CLAUDE.md               # you are here
├── README.md / LICENSE                 # landing + legal
└── .gitignore / .editorconfig / ...    # local tooling configs
```


## Canonical commands

* **Discover what tox envs are available:** `tox list`
* **Run all lint hooks:** `pre-commit run --all-files`
* **Run the default tox env:** `tox run`
* **Run a specific env** (look it up via `tox list` first):
  `tox run -q -e <env-name>`

> [!note]
> Use the long subcommand forms in automation and documentation:
> `tox run`, `tox list`, etc. Single-letter shortcuts (`tox r`,
> `tox l`) are convenient for interactive development but are easy
> to misread in scripts and CI logs.
>
> Do *not* invent flags. `tox` accepts `-e` for env selection and
> `-q` for quiet output -- there are no `--env` / `--quiet` long
> forms.

The project tests itself via [`tox.pytest`][tox.pytest], so the test
suite spins up real `tox` projects in `tmp_path` -- behavioral,
not unit-mocking.

[tox.pytest]: https://tox.wiki/en/latest/plugin/howto.html#testing-plugins


## Conventions

### Commit messages

* Imperative-mood subject ≤ 50 characters.
* Body is *descriptive*, not imperative: explain why, not what (the
  diff already shows what).
* Wrap body at 72 columns.
* No conventional-commits prefixes (`feat:`, `fix:`, etc.).
* Must pass `gitlint`.

### Python style

* `typing` is aliased as `_t`, `collections.abc` is aliased as
  `_c`.
* Use tuples (`(...)`) for fixed-size command-arg sequences, lists
  for things consumed by tox's `MemoryLoader`.
* Single quotes for inline strings, triple-double quotes for
  multi-line strings.
* `from __future__ import annotations` in every module.

### Configuration files

* YAML uses no-indent sequences (`- foo` at the same indent as the
  key).
* Long lines in YAML use a leading `>-` or `|-` block rather than
  trailing-backslash continuation.
* GitHub Actions expression `if:` clauses starting with `!` use a
  `>-` block to keep them out of YAML's quoting rules.

### Markdown

* Admonitions use the GitHub-flavoured `> [!note]` / `> [!warning]`
  / `> [!caution]` / `> [!tip]` / `> [!important]` syntax.
* Inline code uses *single* backticks. Double backticks are RST,
  not Markdown.
* Link definitions are detached -- inline `[text](url)` is reserved
  for the rare case where the URL only appears once and the line
  is short enough to keep readable.
* Detached link definitions live in groups close to the paragraphs
  that reference them, not exclusively in a bottom-of-file dump.


## Where to look first

When picking up a task in this repo, read in this order:

1. `pyproject.toml` -- what the project is, what it depends on,
   what entry point it exposes.
2. `src/tox_plugins/<name>/_plugin.py` -- the entire plugin
   implementation lives here.
3. `tests/integration_test.py` -- the behavioral contract.
4. `tox.ini` + `.pre-commit-config.yaml` -- how things get run
   locally and in CI.
5. `.github/workflows/ci-cd.yml` -- the full CI/CD pipeline,
   delegates to `tox-dev/workflow`'s reusable workflow.


## Related projects

This project shares its philosophy, layout and tooling shape with
other tox plugins under the `tox_plugins.*` namespace -- and more
similar projects are expected to land over time. The repositories
are not formally coupled; cross-project drift is acceptable when
there is a deliberate reason for it.

Maintainer-side, that means: when changing shared tooling here
(configs, GitHub workflows, hook actions, this AGENTS.md), consider
whether the change is generic or project-specific. If it is generic,
propagating it to the other tox-plugin repositories keeps the
ecosystem coherent.
