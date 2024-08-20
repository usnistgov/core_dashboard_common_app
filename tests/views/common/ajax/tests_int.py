""" Test ajax views
"""

from unittest.case import TestCase
from unittest.mock import patch

from core_main_app.components.data.models import Data
from django.http import HttpResponse
from django.test import RequestFactory
from core_dashboard_common_app.views.common.ajax import edit_record
from core_curate_app.components.curate_data_structure.models import (
    CurateDataStructure,
)
from core_main_app.components.template.models import Template

from core_main_app.utils.tests_tools.MockUser import create_mock_user


class TestEditRecord(TestCase):
    """Test Edit Record"""

    def setUp(self):
        """setUp
        Returns:
        """
        self.factory = RequestFactory()
        self.user1 = create_mock_user(
            user_id="1", is_staff=True, is_superuser=True
        )

    @patch("core_curate_app.components.curate_data_structure.api.upsert")
    @patch(
        "core_curate_app.components.curate_data_structure.api.get_by_data_id_and_user"
    )
    @patch("core_main_app.components.data.api.get_by_id")
    def test_edit_xml_record_returns_http_response(
        self, mock_data_get_by_id, mock_get_by_data_id_and_user, mock_upsert
    ):
        """test_edit_record_returns_http_response


        Returns:


        """
        mock_data_get_by_id.return_value = Data(template=Template())
        mock_get_by_data_id_and_user.return_value = CurateDataStructure()
        mock_upsert.return_value = None
        data = {
            "id": "1",
        }
        request = self.factory.post("core_dashboard_edit_record", data)

        request.user = self.user1
        response = edit_record(request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch("core_curate_app.components.curate_data_structure.api.upsert")
    @patch(
        "core_curate_app.components.curate_data_structure.api.get_by_data_id_and_user"
    )
    @patch("core_main_app.components.data.api.get_by_id")
    def test_edit_json_record_returns_http_response(
        self, mock_data_get_by_id, mock_get_by_data_id_and_user, mock_upsert
    ):
        """test_edit_json_record_returns_http_response


        Returns:


        """
        mock_data_get_by_id.return_value = Data(
            template=Template(format=Template.JSON)
        )
        mock_get_by_data_id_and_user.return_value = CurateDataStructure()
        mock_upsert.return_value = None
        data = {
            "id": "1",
        }
        request = self.factory.post("core_dashboard_edit_record", data)

        request.user = self.user1
        response = edit_record(request)

        self.assertTrue(isinstance(response, HttpResponse))

    @patch("core_curate_app.components.curate_data_structure.api.upsert")
    @patch(
        "core_curate_app.components.curate_data_structure.api.get_by_data_id_and_user"
    )
    @patch("core_main_app.components.data.api.get_by_id")
    def test_edit_other_format_record_returns_http_response_bad_request(
        self, mock_data_get_by_id, mock_get_by_data_id_and_user, mock_upsert
    ):
        """test_edit_other_format_record_returns_http_response_bad_request


        Returns:


        """
        mock_data_get_by_id.return_value = Data(
            template=Template(format="BAD_FORMAT")
        )
        mock_get_by_data_id_and_user.return_value = CurateDataStructure()
        mock_upsert.return_value = None
        data = {
            "id": "1",
        }
        request = self.factory.post("core_dashboard_edit_record", data)

        request.user = self.user1
        response = edit_record(request)

        self.assertTrue(isinstance(response, HttpResponse))
        self.assertTrue("Unable to edit" in response.content.decode("utf-8"))
