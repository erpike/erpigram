from datetime import datetime, timezone
from unittest import mock
from unittest.mock import Mock

import jwt
import pytest

from src.utils import create_access_token


@pytest.mark.parametrize("subject, expired, res_sub, res_exp", [
    ("token", None, "token", datetime(2022, 10, 10, 0, 30, tzinfo=timezone.utc)),
    ("token", 75, "token", datetime(2022, 10, 10, 1, 15, tzinfo=timezone.utc)),
    (
        {"token": "token"},
        None,
        "{'token': 'token'}",
        datetime(2022, 10, 10, 0, 30, tzinfo=timezone.utc)
    ),
])
@pytest.mark.nodb
def test_create_access_token(subject, expired, res_sub, res_exp):
    time = datetime(2022, 10, 10)

    class FakeDateTime(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime(2022, 10, 10, 0, 0)

    with mock.patch("src.utils.get_now_time", Mock(return_value=time)), \
            mock.patch("jwt.api_jwt.datetime", FakeDateTime):

        token = create_access_token(subject, expired)
        decoded = jwt.decode(token, "jwt_secret", "HS256")
        assert decoded["sub"] == res_sub
        assert (
            datetime.fromtimestamp(decoded["exp"]).astimezone(timezone.utc) ==
            res_exp
        )


@pytest.mark.parametrize("subject, expired, exp_token, exp_value", [
    ("token", None, "token", 30),
    ("token", 20, "token", 20),
    ("token", 65, "token", 65),
    (
        {"token": "token"},
        33,
        "{'token': 'token'}",
        33
    ),
])
@pytest.mark.nodb
def test_create_access_token_no_patch_datetime(subject, expired, exp_token, exp_value):
    nowtime = datetime.utcnow()
    token = create_access_token(subject, expired)
    decoded = jwt.decode(token, "jwt_secret", "HS256")
    exp = (
          datetime
          .fromtimestamp(decoded["exp"])  # 2023-04-01 15:52:01.003793          # local time
          .astimezone(timezone.utc)       # 2023-04-01 12:52:01.003793+00:00    # local time in utc
          .replace(tzinfo=None)           # 2023-04-01 12:52:01.003793          # remove tz info from utc time
    )

    assert decoded["sub"] == exp_token

    # include test execution time to final assertion
    # main goal: expired_time - nowtime should be equal default value of create_access_token function
    # or equal to expires value if it set
    # default = 30. but expired_time - nowtime can be less than 30 because some time spent for test execution
    assert exp_value - 1 <= int((exp - nowtime).total_seconds() / 60) <= exp_value + 1
