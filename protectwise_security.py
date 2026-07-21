# Copyright (c) 2016-2026 Splunk Inc.
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

import unicodedata
from datetime import datetime, timezone


def format_epoch_millis_utc(epoch_millis: object) -> str:
    """Render epoch milliseconds as the UTC instant claimed by the Z suffix."""
    return datetime.fromtimestamp(int(epoch_millis) / 1000.0, tz=timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")


def sanitize_external_value(value: object) -> object:
    """Remove NUL and Unicode format controls from externally sourced values."""
    if isinstance(value, str):
        return "".join(character for character in value if character != "\x00" and unicodedata.category(character) != "Cf")
    if isinstance(value, list):
        return [sanitize_external_value(item) for item in value]
    if isinstance(value, tuple):
        return tuple(sanitize_external_value(item) for item in value)
    if isinstance(value, dict):
        return {key: sanitize_external_value(item) for key, item in value.items()}
    return value
