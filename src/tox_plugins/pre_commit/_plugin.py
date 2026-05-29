"""A tox plugin providing a pre-commit environment."""

from __future__ import annotations

import typing as _t
from shlex import join as shlex_join
from textwrap import dedent

from tox.config.loader.memory import MemoryLoader
from tox.plugin import impl


if _t.TYPE_CHECKING:
    from collections import abc as _c  # noqa: WPS347

    from tox.config.sets import ConfigSet
    from tox.session.state import State


_PYTHON_CLI_OPTIONS = (
    'python',
    '-bb',
    '-E',
    '-s',
    '-I',
    '-Werror',
)


@impl
def tox_extend_envs() -> _c.Iterable[str]:
    """Declare the pre-commit environment.

    :returns: The names of the tox environments this plugin provides.
    """
    return ('pre-commit',)


@impl
def tox_add_core_config(
    core_conf: ConfigSet,  # noqa: ARG001  # pylint: disable=unused-argument
    state: State,
) -> None:
    """Inject default configuration for the pre-commit environment.

    :param core_conf: The core tox configuration set (unused).
    :param state: The tox session state to inject environments into.
    """
    pos_args = state.conf.pos_args(to_path=None)
    pre_commit_args = ('--all-files',) if pos_args is None else pos_args

    pre_commit_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-m',
        'pre_commit',
        'run',
        '--color=always',
        '--show-diff-on-failure',
        *pre_commit_args,
    )

    install_advice_cmd = (
        *_PYTHON_CLI_OPTIONS,
        '-c',
        dedent("""\
            cmd = "python -Im pre_commit install"
            scr_width = max(len(cmd) + 10, 80)
            sep = "=" * scr_width
            cmd_str = "    $ " + cmd
            print()
            print(sep)
            print("To install pre-commit hooks into the Git repo, run:")
            print()
            print(cmd_str)
            print()
            print(sep)
        """),
    )

    state.conf.memory_seed_loaders['pre-commit'].append(
        MemoryLoader(
            base=[],
            description=(
                '[tox-pre-commit] Run the quality checks; '
                'use `SKIP=id1,id2 tox r -e pre-commit` to skip checks; '
                'use `tox r -e pre-commit -- id1 --all-files` to select checks'
            ),
            deps=['pre-commit'],
            commands_pre=[],
            commands=[shlex_join(pre_commit_cmd)],
            commands_post=[f'-{shlex_join(install_advice_cmd)}'],
            package='skip',
            pass_env=['SKIP'],
        ),
    )
