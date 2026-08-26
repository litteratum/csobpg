"""Nox sessions.

The sessions below are the single source of truth for the project commands
(tests, lint, coverage). Dependencies are installed by nox-uv, which pins
them to the versions locked in uv.lock.
"""

import nox
from nox import Session
from nox_uv import session

nox.options.default_venv_backend = "uv"
nox.options.sessions = ["lint", "tests"]
# Run sessions marked with allow_parallel=True concurrently (one subprocess
# per CPU). Override with "nox -j 1" to force a sequential run.
nox.options.parallel = "auto"

PACKAGE = "csobpg"
LOCATIONS = (PACKAGE, "tests")

# Pinned: a release must not depend on whatever uvx resolves today.
BUMP_MY_VERSION = "bump-my-version@1.5.1"
VERSION_PARTS = ("major", "minor", "patch")


@session(
    python=["3.9", "3.10", "3.11", "3.12", "3.13", "3.14"],
    uv_groups=["test"],
    allow_parallel=True,
)
def tests(s: Session) -> None:
    """Run tests."""
    s.run("pytest", "-svvv", "tests", *s.posargs)


@session(python="3.11", uv_only_groups=["lint"], allow_parallel=True)
def lint(s: Session) -> None:
    """Check the code with ruff."""
    s.run("ruff", "check", *LOCATIONS)
    s.run("ruff", "format", "--check", *LOCATIONS)


@session(python="3.11", uv_only_groups=["lint"])
def fmt(s: Session) -> None:
    """Format the code with ruff and apply lint autofixes."""
    s.run("ruff", "check", "--fix", *LOCATIONS)
    s.run("ruff", "format", *LOCATIONS)


@session(python="3.12", uv_groups=["test"])
def coverage(s: Session) -> None:
    """Run tests and report coverage to stdout, XML and HTML."""
    s.run(
        "pytest",
        f"--cov={PACKAGE}",
        "--cov-report=term-missing",
        "--cov-report=xml",
        "--cov-report=html",
        "tests",
    )


@nox.session(venv_backend="none")
def release(s: Session) -> None:
    """Bump the version, update the CHANGELOG, commit and tag.

    Usage: nox -s release -- {major|minor|patch} [extra bump-my-version args]
    """
    if not s.posargs or s.posargs[0] not in VERSION_PARTS:
        parts = "|".join(VERSION_PARTS)
        s.error(f"usage: nox -s release -- {{{parts}}} [args]")
    s.run("uvx", BUMP_MY_VERSION, "bump", *s.posargs, external=True)
