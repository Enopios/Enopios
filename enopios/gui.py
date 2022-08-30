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

import json
import shutil
import sys
from pathlib import Path
from argparse import Namespace
import streamlit as st
from streamlit.web.bootstrap import _print_url
from enopios.app.start import start_streamlit_server


def main(args: Namespace) -> None:
    """ Boot up the enopios GUI. Triggered by enopios/cli.py:gui_cli(). """
    here = Path(__file__).parent.resolve()
    app_dir = here.joinpath("app")
    _fill_streamlit_credentials(app_dir)
    streamlit_script_path = str(here.joinpath("app.py"))
    config = {}
    if args.port:
        config["server.port"] = args.port
    if args.electron:
        _patch_streamlit_print_url()
        config["server.headless"] = True
    start_streamlit_server(streamlit_script_path, config)


def _patch_streamlit_print_url() -> None:
    """ Monkey patching to dump the port into a json once the server is running to
        fullfill the promise declared in js/app/main.ts#L64.
    """
    def _new_print_url(is_running_hello: bool) -> None:
        port = int(st.config.get_option("browser.serverPort"))
        sys.stdout.flush()
        print(json.dumps({"port": port}))
        sys.stdout.flush()
        _print_url(is_running_hello)

    st.web.bootstrap._print_url = _new_print_url


def _fill_streamlit_credentials(app_dir: Path) -> None:
    """ Write app/credendials.toml into $HOME/.streamlit (required to start the
        server).
    """
    streamlit_config_file = Path.home().joinpath(".streamlit", "credentials.toml")
    if streamlit_config_file.exists():
        return
    streamlit_config_dir = streamlit_config_file.parent
    streamlit_config_dir.mkdir(exist_ok=True)
    template_streamlit_config_file = app_dir.joinpath("credentials.toml")
    try:
        shutil.copy2(template_streamlit_config_file, streamlit_config_file)
    except FileExistsError:
        pass
