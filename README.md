[![SWUbanner]][SWUdocs]

[![tox-dev badge]][tox-dev]
[![pre-commit.ci status badge]][pre-commit.ci results page]
[![GH Sponsors badge]][GH Sponsors URL]

[SWUbanner]:
https://raw.githubusercontent.com/vshymanskyy/StandWithUkraine/main/banner-direct-single.svg
[SWUdocs]:
https://github.com/vshymanskyy/StandWithUkraine/blob/main/docs/README.md

[tox-dev]: https://github.com/tox-dev
[tox-dev badge]:
https://img.shields.io/badge/project-yellow?label=tox-dev&labelColor=c3cc39&color=7f833e

[pre-commit.ci status badge]:
https://results.pre-commit.ci/badge/github/tox-dev/tox-pre-commit/main.svg
[pre-commit.ci results page]:
https://results.pre-commit.ci/latest/github/tox-dev/tox-pre-commit/main

[GH Sponsors badge]:
https://img.shields.io/badge/%40webknjaz-transparent?logo=githubsponsors&logoColor=%23EA4AAA&label=Sponsor&color=2a313c
[GH Sponsors URL]:
https://github.com/sponsors/webknjaz


# tox-pre-commit

A tox plugin providing a pre-commit environment.


## Usage

Add `tox-pre-commit` to your project's `tox` requirements -- either
in `tox.toml`:

```toml
requires = [
  "tox-pre-commit",
]
```

...or in `tox.ini`:

```ini
[tox]
requires =
  tox-pre-commit
```

Then invoke the `pre-commit` env that the plugin exposes:

```console
$ tox run -q -e pre-commit
$ tox run -q -e pre-commit -- ruff --all-files  # narrow with posargs
$ SKIP=mypy,ruff tox run -q -e pre-commit       # skip specific hooks
```
