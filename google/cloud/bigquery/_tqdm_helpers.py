# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Shared helper functions for tqdm progress bar."""

import warnings

try:
    import tqdm
except ImportError:  # pragma: NO COVER
    tqdm = None

_NO_TQDM_ERROR = (
    "A progress bar was requested, but there was an error loading the tqdm "
    "library. Please install tqdm to use the progress bar functionality."
)


def _get_progress_bar(progress_bar_type, description, total, unit):
    """Construct a tqdm progress bar object, if tqdm is installed."""
    if tqdm is None:
        if progress_bar_type is not None:
            warnings.warn(_NO_TQDM_ERROR, UserWarning, stacklevel=3)
        return None

    try:
        if progress_bar_type == "tqdm":
            return tqdm.tqdm(desc=description, total=total, unit=unit)
        elif progress_bar_type == "tqdm_notebook":
            return tqdm.tqdm_notebook(desc=description, total=total, unit=unit)
        elif progress_bar_type == "tqdm_gui":
            return tqdm.tqdm_gui(desc=description, total=total, unit=unit)
    except (KeyError, TypeError):
        # Protect ourselves from any tqdm errors. In case of
        # unexpected tqdm behavior, just fall back to showing
        # no progress bar.
        warnings.warn(_NO_TQDM_ERROR, UserWarning, stacklevel=3)
    return None
