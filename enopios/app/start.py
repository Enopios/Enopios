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

import streamlit as st
from streamlit.web.bootstrap import load_config_options, run


def main(args):
    start_streamlit_server(args.path, {})


def start_streamlit_server(script_path, config):
    load_config_options(flag_options=config)
    # apply_streamlit_server_patches()
    st._is_running_with_streamlit = True
    run(script_path, "", [], flag_options={})
