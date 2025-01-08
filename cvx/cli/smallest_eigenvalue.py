#    Copyright 2023 Stanford University Convex Optimization Group
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
from typing import Dict

import fire  # type: ignore
import numpy as np

from cvx.bson.file import read_bson


def smallest_ev(bson_file) -> Dict[str, float]:
    """
    Compute the smallest eigenvalue of matrices stored in a bson file.

    There are faster methods to compute the smallest eigenvalue, e.g. an inverse power iteration.
    Here, we only use this as an example to work with the bson interface.

    On the command line

    poetry run smallest-eigenvalue cli/data/test.bson
    """

    eigenvalues = {key: np.min(np.linalg.eigh(matrix)[0]) for key, matrix in read_bson(bson_file).items()}

    for key, ev in eigenvalues.items():
        print(key, ev)

    return eigenvalues


def main():  # pragma: no cover
    fire.Fire(smallest_ev)
