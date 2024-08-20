""" Mock object for core_dashboard_common_app
"""

from unittest.mock import Mock


class MockSession(Mock):
    """MockSession"""

    session_key = "mock_session"


class MockRequest(Mock):
    """Mock Request"""

    user = None
    session = MockSession()
