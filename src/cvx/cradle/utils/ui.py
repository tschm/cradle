#    Copyright 2025 Stanford University Convex Optimization Group
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.
from pathlib import Path

from copier import run_copy


def worker(template: str, dst_path: Path, vcs_ref="HEAD", user_defaults=None):
    """Run copier to copy the template to the destination path"""
    if user_defaults is None:
        _worker = run_copy(src_path=template, dst_path=dst_path, vcs_ref=vcs_ref)
        return _worker

    # important for testing
    _worker = run_copy(
        src_path=template,
        dst_path=dst_path,
        vcs_ref=vcs_ref,
        unsafe=True,
        defaults=True,
        user_defaults=user_defaults,
    )

    return _worker
