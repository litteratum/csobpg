"""Nox sessions."""

import nox


nox.options.sessions = ["lint", "tests"]


@nox.session(python=["3.9", "3.11", "3.12", "3.13"])
def tests(session):
    """Run tests."""
    session.run("make", "testdeps", external=True)
    session.run("make", "test", external=True)


@nox.session(python=["3.11"])
def lint(session):
    """Run linting."""
    session.run("make", "lintdeps", external=True)
    session.run("make", "lint", external=True)


@nox.session(python="3.12")
def coverage(session):
    """Run coverage."""
    session.run("make", "testdeps", external=True)
    session.run("pytest", "--cov=csobpg", "--cov-report=xml")
