from __future__ import annotations

import os
import platform
import shutil

from devenv.constants import root
from devenv.constants import shell
from devenv.lib import archive
from devenv.lib import fs
from devenv.lib import proc

_version = "2.32.3"

_sha256 = {
    "direnv.darwin-amd64": "6ff42606edb38ffce5e1a3f4a1c69401e42a7c49b8bdc4ddafd705bc770bd15c",  # noqa: E501
    "direnv.darwin-arm64": "dd053025ecae958118b3db2292721464e68da4fb319b80905a4cebba5ba9f069",  # noqa: E501
}


def install() -> None:
    direnv_path = f"{root}/bin/direnv"

    if shutil.which("direnv") == direnv_path:
        return

    suffix = "arm64" if platform.machine() == "arm64" else "amd64"
    name = f"direnv.darwin-{suffix}"
    url = "https://github.com/direnv/direnv/releases/download" f"/v{_version}/{name}"

    archive.download(url, _sha256[name], dest=direnv_path)
    os.chmod(direnv_path, 0o775)

    proc.run((direnv_path, "version"))

    fs.idempotent_add(
        fs.shellrc(),
        f"""
eval "$(direnv hook {shell})"
""",
    )