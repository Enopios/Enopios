# Copyright (C) 2021 Radiotherapy AI Pty Ltd

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


def make_exe():
    dist = default_python_distribution(python_version="3.10")

    policy = dist.make_python_packaging_policy()
    policy.set_resource_handling_mode("files")

    # site-packages is required here so that streamlit doesn't boot in
    # development mode:
    # https://github.com/streamlit/streamlit/blob/953dfdbe/lib/streamlit/config.py#L255-L267
    policy.resources_location = "filesystem-relative:site-packages"

    python_config = dist.make_python_interpreter_config()
    python_config.module_search_paths = ["$ORIGIN/site-packages"]
    python_config.run_module = "enopios"

    python_config.filesystem_importer = True
    python_config.oxidized_importer = False
    python_config.sys_frozen = True

    exe = dist.to_python_executable(
        name="enopios",
        packaging_policy=policy,
        config=python_config,
    )
    exe.windows_runtime_dlls_mode = "always"
    exe.windows_subsystem = "console"

    exe.add_python_resources(exe.pip_install(["-r", "requirements.txt"]))
    exe.add_python_resources(exe.pip_install(["."]))

    return exe


def make_install(exe):
    files = FileManifest()
    files.add_python_resource(".", exe)
    files.install("dist", replace=True)

    return files


register_target("exe", make_exe)
register_target(
    "install", make_install, depends=["exe"], default=True, default_build_script=True
)

resolve_targets()
