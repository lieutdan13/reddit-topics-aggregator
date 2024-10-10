# Reddit Topics Aggregator

[![badge_documentation][]][documentation] [![badge_pipeline][]][pipeline] [![badge_coverage][]][coverage] [![badge_maintainability][]][maintainability]

[documentation]: https://lieutdan13.github.io/reddit-topics-aggregator
[badge_documentation]: https://img.shields.io/badge/Documentation-main-blue
[coverage]: https://lieutdan13.github.io/reddit-topics-aggregator/coverage
[maintainability]: https://github.com/lieutdan13/reddit-topics-aggregator
[badge_coverage]: https://lieutdan13.github.io/reddit-topics-aggregator/badges/coverage.svg
[badge_pipeline]: https://github.com/lieutdan13/reddit-topics-aggregator/actions/workflows/ci.yaml/badge.svg
[pipeline]: https://github.com/lieutdan13/reddit-topics-aggregator/actions?query=branch%3Amain
[badge_maintainability]: https://lieutdan13.github.io/reddit-topics-aggregator/badges/maintainability.svg

<!-- TODO: extend readme template -->

## Installation

```console
pip install git+https://github.com/lieutdan13/reddit-topics-aggregator
```

## Usage

Call the `reddit-topics-aggregator` command line interface like this:

```console
$ reddit-topics-aggregator
Usage: reddit-topics-aggregator [OPTIONS] COMMAND [ARGS]...

  Reddit Topics Aggregator is a tool used to aggregate hot, new, top, and
  rising topics from multiple subreddits.

Options:
  --version  Show the version and exit.
  --help     Show this message and exit.

Commands:
  connect  Retrieve info about the authenticated Reddit user.
  topics   Retrieve Subreddit topic submissions
```

Provide the `--help` option to see supported options and arguments.

---
*This project was created using the [Project Template for Python](https://github.com/jannismain/python-project-template)*
