# Copyright (c) 2016-2026 Splunk Inc.

import os
import sys
import time
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from protectwise_security import format_epoch_millis_utc, sanitize_external_value


def test_format_epoch_millis_utc_is_independent_of_host_timezone():
    previous_timezone = os.environ.get("TZ")
    try:
        os.environ["TZ"] = "America/New_York"
        time.tzset()
        assert format_epoch_millis_utc(0) == "1970-01-01T00:00:00.000000Z"
    finally:
        if previous_timezone is None:
            os.environ.pop("TZ", None)
        else:
            os.environ["TZ"] = previous_timezone
        time.tzset()


def test_sanitize_external_value_removes_nul_and_format_controls_recursively():
    value = {
        "name": "invoice\u200b_\u202efdp.scr\x00",
        "nested": ["safe", {"description": "zero\ufeffwidth"}],
        "count": 1,
    }

    assert sanitize_external_value(value) == {
        "name": "invoice_fdp.scr",
        "nested": ["safe", {"description": "zerowidth"}],
        "count": 1,
    }
