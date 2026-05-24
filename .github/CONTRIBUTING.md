# Contributing

<!-- sphinx-inclusion-post-this-line -->

This project is part of the [tox-dev] ecosystem. By contributing, you
agree to abide by the [Contributor Code of Conduct][coc] and follow the
conventions outlined below.

## Project Contribution Guidelines

The following apply to contributions in this repository:

- Use [`tox`] to invoke the testing, linting and packaging environments
  declared in `tox.ini`.
- Local code-style and static-analysis checks run under [`pre-commit`].
  Run `pre-commit run --all-files` before pushing.
- Add tests for behavioral changes. The test suite uses [`tox.pytest`]
  to exercise the plugin against a real `tox` runtime.
- Give a clear one-line description in the pull request title.
- Wait for review from at least one other contributor before merging,
  even if you have write access.

The only exception to these guidelines is for trivial changes, such as
documentation corrections or contributions that do not change the
plugin itself.

Contributions following these guidelines are always welcomed, encouraged
and appreciated.

[`pre-commit`]: https://pre-commit.com
[`tox`]: https://tox.wiki
[`tox.pytest`]:
https://tox.wiki/en/latest/plugin/howto.html#testing-plugins
[coc]: ./CODE_OF_CONDUCT.md
[tox-dev]: https://github.com/tox-dev

### LLM Generated Contributions

Contributors are free to use whatever tools they like, but we have some
additional guidance for LLM-assisted contributions.

When interacting in this project's spaces (issues, pull requests,
discussions, etc.), do not use LLMs to speak for you, except for
translation or grammar edits. This includes the creation of change
logs and pull request descriptions. Human-to-human communication is
foundational to open source communities.

> [!CAUTION]
> In extreme cases, low quality PRs may be closed as spam.

#### Responsibility

Remember that you, not the LLM, are responsible for your contributions.
Be ready to discuss your changes.
Do not submit code you have not reviewed.

Do your best to follow the conventions and standards of the project.
Make sure your code really works.
Be thoughtful about testing and documentation.

Try to make your code brief, and recognize when less is more.

#### Autonomous Code Submissions

The use of agents which write code and submit pull requests without
human review is not permitted.

We can already run these tools ourselves, if we want to. Contributions
should provide value beyond running a tool.

#### Pull Request Templates

Please do not replace the pull request template, which is part of the
maintainers' process.

### The `good first issue` label

The [`good first issue` label] is used to designate items which are
being left for new contributors.
They're a great way to get onboarded into the project and learn.

Having an LLM resolve one of these issues does not help anyone learn.
Therefore, please be considerate of those who may benefit from these
opportunities, and refrain from asking an LLM to produce a complete
solution.

[`good first issue` label]:
https://github.com/search?q=org%3Atox-dev+label%3A%22good+first+issue%22&type=issues
