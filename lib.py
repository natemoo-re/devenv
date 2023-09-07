from __future__ import annotations

import os
from functools import cache
from subprocess import CalledProcessError
from subprocess import run


@cache
def gitroot(cd: str) -> str:
    from os.path import normpath, join

    try:
        proc = run(
            ("git", "-C", cd, "rev-parse", "--show-cdup"),
            check=True,
            capture_output=True,
        )
        root = normpath(join(cd, proc.stdout.decode().strip()))
    except CalledProcessError as e:
        raise SystemExit(f"git failed: {e.stderr}")
    return root


def brew_packages() -> list[str]:
    # note: brew leaves will not print out top-level casks unfortunately
    try:
        proc = run(
            ("brew", "list"),
            check=True,
            capture_output=True,
            env={
                **os.environ,
                "HOMEBREW_NO_AUTO_UPDATE": "1",
                "HOMEBREW_NO_INSTALLED_DEPENDENTS_CHECK": "1",
                "HOMEBREW_NO_INSTALL_CLEANUP": "1",
                "HOMEBREW_NO_ANALYTICS": "1",
            },
        )
        leaves = proc.stdout.decode().split()
    except CalledProcessError as e:
        raise SystemExit(f"brew failed: {e.stderr}")
    return leaves
