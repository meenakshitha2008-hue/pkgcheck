# pkgcheck-cli

A learning project: a command that checks a Python package **name** for risk before you install it.

    pip install pkgcheck-cli
    pkgcheck requests

Example output:

    requests   SAFE
    reqeusts   RISKY - name is very similar to popular package 'requests'

## How it works

The command sends the package name to a small web server (FastAPI). The server runs a Random Forest model and answers SAFE or RISKY, with a plain-English reason.

## Important limits (please read)

- **This is a learning project, not a security tool.** Do not rely on it to decide what is safe to install.
- The model uses **name-only clues**: name length, digits, dashes, and similarity to popular package names.
- On held-out test data it finds about **63%** of bad packages, and when it says RISKY it is right about **51%** of the time. The test data had far more bad packages than real PyPI has, so real-world precision would be lower.
- The 500 most popular packages are always answered SAFE.
- Bad examples come from the DataDog malicious-software-packages dataset. Safe examples are popular PyPI packages, which is not a perfect picture of the real world.
- The server runs on a free plan. The first request after a quiet period can take up to a minute, and the server may go offline.

## Privacy

Only the package name you type is sent to the server. The server stores the name and its answer in a database.

## Source code

https://github.com/meenakshitha2008-hue/pkgcheck