# Incident Response Playbook

This document captures how the maintainer triages, fixes and discloses
confirmed security incidents covering this plugin. The path is
written down here so it is decided in calm waters, not in the middle
of a live disclosure.

> [!note]
> Reporters should follow [`SECURITY.md`][SECURITY] to reach the
> maintainer. This file is for the maintainer's response side.

[SECURITY]: ./SECURITY.md


## Severity Classes

| Class | Definition |
|-------|------------|
| **Critical** | Arbitrary code execution from default plugin behavior, or any vulnerability that compromises the integrity of the published distribution. |
| **High** | Information disclosure or denial of service that the plugin can cause without explicit user opt-in. |
| **Medium** | Broken builds for legitimate users; CI hangs; spurious data leaks limited to the user's own machine. |
| **Low** | Cosmetic, non-exploitable bugs incorrectly classified as security. |


## Triage Timeline

| Step | Target turnaround |
|------|-------------------|
| Initial acknowledgment to the reporter | **≤ 72 hours** from receipt |
| Severity-class assignment | **≤ 72 hours** |
| Impact assessment + remediation plan | **≤ 7 days** |
| Fix-or-yank decision | **≤ 14 days** |
| Coordinated disclosure window for **Critical** / **High** | **≤ 45 days** from initial report by default; extendable on reporter request |

These are targets, not hard SLAs -- this is unpaid maintenance on an
open-source project.


## Coordination

* For **Critical** and **High**: open a GitHub Security Advisory
  draft as soon as the issue is reproduced. The draft serves as the
  shared workspace between the maintainer and the reporter.
* Cross-link the advisory to the `tox-dev` maintainer chat for severe
  cross-project impact (e.g. if the bug originates in `tox` itself
  rather than the plugin).
* CVE assignment is requested via GitHub's GHSA flow when CVSS
  v4.0 base score ≥ 7.0 (High or Critical).


## Disclosure Philosophy

* Coordinated disclosure is preferred.
* The advisory is **published after** the fix release reaches PyPI
  so users have a remediation available immediately.
* Embargo only when downstream coordination warrants it (e.g.
  affected downstream packagers have not yet shipped the fix).


## Remediation Playbook

1. Cut a hot-fix branch from the latest released tag.
2. Land the minimal fix + a regression test under `tests/`.
3. Bump the patch component of the version.
4. Release via Trusted Publishing on PyPI (the existing
   `ci-cd.yml` release flow does this).
5. If older versions are confirmed affected and not in active use,
   `pip` yank them (PyPI maintainer console). Yanking does not
   delete; it warns installers off.
6. Publish the GHSA advisory.
7. Open a public GitHub Discussion announcing the fix.


## Post-Incident

* A short public post-mortem is published within **30 days** after
  disclosure for any **Critical** / **High** incident.
* The [threat model][threat-model] is updated to reflect any new
  mitigations added.
* Regression coverage is verified to be in place under `tests/`.

[threat-model]: ./THREAT_MODEL.md


## Drills

Incident response drills are not currently scheduled. Revisit if user
base or attack surface grows substantially.
