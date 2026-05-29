# Threat Model

This document captures the threat surface of `tox-pre-commit` and the
mitigations already in place. It exists so future reviewers,
downstream packagers and security auditors can reason about the
plugin without reverse-engineering the workflow files.


## Assets

* **The plugin distribution** -- the wheel and sdist published to
  PyPI under the `tox-pre-commit` project name.
* **The plugin source repository** on GitHub, including the CI/CD
  workflows that publish releases.
* **The user's tox project** -- *trusted by the user, but the plugin
  must not amplify any trust the user has placed in the plugin code
  onto the user's project*.
* **Transitive dependencies** -- `pre-commit` itself, and the hooks
  that `pre-commit` loads from the user's
  `.pre-commit-config.yaml`. These are pulled in by the user's own
  environment and are not redistributed by this project.


## Trust Boundaries

1. **PyPI &rarr; end user** -- the user runs `pip install` over the
   network. Trusted Publishing, in-toto attestations and Sigstore
   signing on PyPI provide cryptographic proof of provenance.
2. **Plugin entry point &rarr; tox runtime** -- when tox loads the
   plugin, plugin code runs in the user's Python process with the
   user's privileges. There is no privilege escalation; the plugin
   does not request more capabilities than `tox` itself.
3. **User's `pyproject.toml` / `tox.ini` &rarr; the plugin** -- the
   plugin reads tox state (positional arguments, config keys) and
   forwards them to `pre_commit run` subprocesses. All forwarded
   values pass through `shlex.join` over native Python tuples;
   `shell=True` is never used.
4. **The plugin &rarr; pre-commit** -- the plugin invokes
   `python -Im pre_commit run --color=always --show-diff-on-failure
   ...` in a tox env. The user's `.pre-commit-config.yaml` and the
   hooks it references operate under pre-commit's own trust model;
   the plugin neither validates nor sandboxes them.


## Threats In Scope

* **Supply-chain substitution** -- a malicious actor publishes a
  same-or-similar-named package to PyPI. Mitigated by Trusted
  Publishing + Sigstore + SLSA-3 provenance + in-toto attestations
  on this project's releases. *Downstream users must verify
  signatures to benefit; this project provides the signatures.*
* **Plugin tampering at install time** -- a man-in-the-middle
  attacker replaces dist contents during install. Mitigated by
  HTTPS-only PyPI and the same signing/attestation chain above.
* **Namespace squatting** -- another distribution publishes a module
  under `tox_plugins.pre_commit` that collides with this plugin's
  namespace. Out of scope (PyPI's responsibility); this project pins
  its name on PyPI and uses the implicit-namespace layout
  intentionally so co-located siblings under `tox_plugins.*` work.
* **Shell injection via `posargs`** -- an attacker tricks the user
  into pasting a malicious `tox run -e pre-commit -- ...` line.
  Mitigated: positional arguments are joined exclusively via
  `shlex.join`, preventing shell-metacharacter escape; `shell=True`
  is never used.
* **Downgrade attacks against the release artifact** -- mitigated by
  PEP 740 build attestations published alongside every PyPI release.


## Threats Out Of Scope

* Compromise of GitHub or PyPI infrastructure itself.
* Compromise of the user's machine, IDE or credentials.
* Compromise of `pre-commit` upstream releases (downstream of the
  user's package selection).
* The security of the user's own `.pre-commit-config.yaml` and the
  pre-commit hooks it references -- pre-commit's own hook trust
  model applies, not this plugin's.


## Existing Mitigations Checklist

* [x] Trusted Publishing on PyPI (OIDC, no long-lived tokens)
* [x] Sigstore signing of dists
* [x] SLSA-3 provenance generation via
      `slsa-framework/slsa-github-generator`
* [x] In-toto build attestations via
      `actions/attest-build-provenance`
* [x] GitHub Actions pinned by SHA where third-party
* [x] `tox-dev/workflow` reusable workflow pinned by SHA
* [x] `forbidden-files` pre-commit hook -- enforces no `setup.py`,
      no `__init__.py` under `src/`, no `tests/__init__.py`
* [x] Ruff's `namespace-packages` config so static analysis sees the
      PEP 420 layout correctly
* [x] `shlex.join` used exclusively for subprocess command
      composition; `shell=True` is never used in the codebase
* [ ] CodeQL static analysis -- deferred
* [ ] Per-dependency SBOM publication -- deferred


## Review Cadence

This threat model is re-evaluated when any of the following land:

* A new `@tox.plugin.impl` entry point is added.
* A new shell-out invocation is introduced (any new `subprocess.run`
  / `shlex.join` call site).
* The CI runner platform changes (new OS, new release channel).
* A new transitive dependency is added to the runtime requirements.
* A vulnerability report is received and triaged per the
  [incident response playbook][incident-response].

[incident-response]: ./INCIDENT_RESPONSE.md
