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


""" This file defines the whole CLI. It is organized as follows:

- There is one main command, namely `enopios` (see __main__.py).
  Every command should thus starts with:
    > poetry run enopios

- There are 3 subcommands: `build`, `gui`, `streamlit`:
  Each can be launched by running:
    > poetry run enopios subcommand --params values

    - `build`: launches the full Python+Electron app build process (see build.py).

    - `gui`: launches the streamlit app whithin this project. It can be uses to launch
      it like any normal streamlit app, or embedded inside Electron with the.
      That's what is done in the built version, see js/app/src/main.ts#L32.

    - `streamlit`: is a simple wrapper around the base streamlit command. It takes a
      path and allows to execute any live application inside the browser. It is usefull
      for development purposes.
"""

import argparse
from enopios.build import build_binary
from enopios.gui import main as client_main
from enopios.app.start import main as server_main


# _______________________ Subparsers (build / cli / streamlit) ______________________ #

def build_cli(subparsers: argparse._SubParsersAction) -> None:
    """ Add `build` subcommand to the main parser. Acts inplace. """
    parser = subparsers.add_parser("build")
    parser.add_argument(
        "--install",
        help="Run yarn install first.",
        action="store_true",
    )
    parser.set_defaults(func=build_binary)


def gui_cli(subparsers: argparse._SubParsersAction) -> None:
    """ Add `gui` subcommand to the main parser. Acts inplace. """
    parser: argparse.ArgumentParser = subparsers.add_parser(
        "gui", help="Run the Enopios GUI.",
    )
    parser.add_argument("--port")
    parser.add_argument("--electron", action="store_true")
    parser.set_defaults(func=client_main)


def streamlit_cli(subparsers: argparse._SubParsersAction) -> None:
    """ Add `streamlit` subcommand to the main parser. Acts inplace. """
    streamlit_parser = subparsers.add_parser(
        "streamlit", help="Wrapper for streamlit CLI"
    )
    streamlit_subparser = streamlit_parser.add_subparsers()
    streamlit_run = streamlit_subparser.add_parser("run")
    streamlit_run.add_argument("path")
    streamlit_run.set_defaults(func=server_main)


# ___________________________________ Main parser ___________________________________ #

def define_parser():
    """ Create the main parser, and adds the three subparsers:
        `build`, `gui`, `streamlit`.
    """
    parser = argparse.ArgumentParser(prog="enopios")
    subparsers = parser.add_subparsers()
    build_cli(subparsers)
    gui_cli(subparsers)
    streamlit_cli(subparsers)
    return parser


def enopios_cli() -> None:
    """ Creates the main parser, parse it, and execute the required function if any.
    """
    parser = define_parser()
    args, remaining = parser.parse_known_args()
    if hasattr(args, "func"):
        try:
            args.func(args, remaining)
            return
        except TypeError:
            pass
        parser.parse_args()
        args.func(args)
        return
    subparser_names = list(filter(lambda x: not x.startswith('_'), dir(args)))
    if not subparser_names:
        parser.print_help()
    else:
        assert len(subparser_names) == 1
        subparser_name = subparser_names[0]
        assert getattr(args, subparser_name) is None
        parser.parse_args([subparser_name, "--help"])
