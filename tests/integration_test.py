"""Behavioral tests for the tox-pre-commit plugin."""

from __future__ import annotations

import typing as _t


if _t.TYPE_CHECKING:
    from tox.pytest import ToxProjectCreator


def test_pre_commit_env_registered(tox_project: ToxProjectCreator) -> None:
    """The plugin contributes a ``pre-commit`` env to the env list.

    :param tox_project: Tox-provided project factory fixture.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run('list')
    tox_invocation_result.assert_success()
    assert 'pre-commit' in tox_invocation_result.out


def test_pre_commit_default_command(tox_project: ToxProjectCreator) -> None:
    """The ``pre-commit`` env runs ``pre_commit run --all-files`` by default.

    :param tox_project: Tox-provided project factory fixture.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run(
        'config',
        '-e',
        'pre-commit',
        '-k',
        'commands',
    )
    tox_invocation_result.assert_success()
    assert '-m pre_commit run' in tox_invocation_result.out
    assert '--all-files' in tox_invocation_result.out


def test_pre_commit_posargs_replace_default(
    tox_project: ToxProjectCreator,
) -> None:
    """User-provided posargs replace the default ``--all-files``.

    :param tox_project: Tox-provided project factory fixture.
    """
    project = tox_project({'tox.ini': '[tox]\n'})
    tox_invocation_result = project.run(
        'config',
        '-e',
        'pre-commit',
        '-k',
        'commands',
        '--',
        'sentinel',
        '--stub',
    )
    tox_invocation_result.assert_success()
    assert 'sentinel --stub' in tox_invocation_result.out
