# +--------------------------------------------------------------------+ #
# |      This file was originally written by Simon Biggs in 2022.      | #
# |             It as been adapted by Luc Vedrenne in 2022.            | #
# +--------------------------------------------------------------------+ #

# _________________________  Original License: _________________________ #

# Copyright (C) 2020 Simon Biggs

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# ______________________________________________________________________ #

import shutil
import subprocess
from pathlib import Path
from argparse import Namespace
from dataclasses import dataclass


# _______________________________ Paths datastructure _______________________________ #

@dataclass
class Paths:

    repo_root: Path
    library: Path = None
    pyoxidizer_build: Path = None
    pyoxidizer_dist: Path = None
    electron_app: Path = None
    python_app: Path = None

    def __post_init__(self) -> None:
        self.library = self.repo_root.joinpath("enopios")
        self.pyoxidizer_build = self.repo_root.joinpath("build")
        self.pyoxidizer_dist = self.pyoxidizer_build.joinpath("dist")
        self.electron_app = self.repo_root.joinpath("js", "app")
        self.python_app = self.electron_app.joinpath("python")


# ___________________________ Main build process function ___________________________ #

def build_binary(args: Namespace) -> None:
    """ Run `pyoxidizer` and `yarn build` sequentially, optionaly preceded by
        `yarn install`.
        The resulting python/ folder from pyoxidizer is copied from repo_root/ to
        repo_root/js/app in order to be available from `js/app/packages.json`.

    Args:
        args (Namespace): Parsed from build_cli(). Has a boolan parameter `install` to
            control wether or not `yarn install` should be called at the beginning.
    """
    paths = Paths(repo_root=Path(__file__).resolve().parent.parent)
    if args.install:
        subprocess.check_call(
            [shutil.which("yarn"), "install"], cwd=paths.electron_app
        )
    try:
        shutil.rmtree(paths.pyoxidizer_build)
    except FileNotFoundError:
        pass
    try:
        shutil.rmtree(paths.python_app)
    except FileNotFoundError:
        pass
    subprocess.check_call(
        ["poetry", "run", "pyoxidizer", "build", "install"], cwd=paths.repo_root
    )
    shutil.move(paths.pyoxidizer_dist, paths.python_app)
    subprocess.check_call([shutil.which("yarn"), "build"], cwd=paths.electron_app)

# ___________________________________________________________________________________ #


if __name__ == '__main__':
    build_binary()
