""" Unit tests on common dashboard views.
"""

from unittest import TestCase
from unittest.mock import patch, MagicMock

from django.contrib.sessions.backends.base import SessionBase
from django.test import override_settings
from rest_framework.test import APIRequestFactory

from core_dashboard_common_app.views.common import views as common_views
from core_main_app.components.data import api as data_api
from core_main_app.components.user import api as user_api
from core_main_app.components.workspace import api as workspace_api
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from core_main_app.utils.tests_tools.RequestMock import RequestMock


class TestDashboardWorkspaceRecordsGet(TestCase):
    @staticmethod
    def mock_render_only_context(
        request, template_name, modals=None, assets=None, context=None
    ):
        return context

    def setUp(self) -> None:
        self.workspace_records_view = common_views.DashboardWorkspaceRecords

    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_all_by_workspace")
    @patch.object(workspace_api, "can_user_read_workspace")
    @patch.object(workspace_api, "can_user_write_workspace")
    @patch.object(common_views, "ResultsPaginator")
    @patch.object(
        common_views.DashboardWorkspaceRecords, "_format_data_context"
    )
    @patch.object(common_views, "UserForm")
    @patch.object(common_views.DashboardWorkspaceRecords, "_get_modals")
    @patch.object(common_views.DashboardWorkspaceRecords, "_get_assets")
    @patch.object(user_api, "get_user_by_id")
    @patch.object(common_views.DashboardWorkspaceRecords, "common_render")
    def test_user_side_context_has_no_owner_info(
        self,
        mock_common_render,
        mock_get_user_by_id,
        mock_get_assts,
        mock_get_modals,
        mock_user_form,
        mock_format_data_context,
        mock_results_paginator,
        mock_can_user_write_workspace,
        mock_can_user_read_workspace,
        mock_get_all_by_workspace,
        mock_workspace_get_by_id,
    ):
        mock_common_render.side_effect = self.mock_render_only_context

        self.workspace_records_view.administration = False
        response = RequestMock.do_request_get(
            self.workspace_records_view.as_view(),
            None,
            param={"workspace_id": 42},
        )

        self.assertNotIn("owner", response.keys())
        self.assertNotIn("owner_change_url", response.keys())

    @patch.object(workspace_api, "get_by_id")
    @patch.object(data_api, "get_all_by_workspace")
    @patch.object(workspace_api, "can_user_read_workspace")
    @patch.object(workspace_api, "can_user_write_workspace")
    @patch.object(common_views, "ResultsPaginator")
    @patch.object(
        common_views.DashboardWorkspaceRecords, "_format_data_context"
    )
    @patch.object(common_views, "UserForm")
    @patch.object(common_views.DashboardWorkspaceRecords, "_get_modals")
    @patch.object(common_views.DashboardWorkspaceRecords, "_get_assets")
    @patch.object(user_api, "get_user_by_id")
    @patch.object(common_views, "reverse")
    @patch.object(common_views.DashboardWorkspaceRecords, "common_render")
    def test_admin_side_context_has_owner_info(
        self,
        mock_common_render,
        mock_reverse,
        mock_get_user_by_id,
        mock_get_assts,
        mock_get_modals,
        mock_user_form,
        mock_format_data_context,
        mock_results_paginator,
        mock_can_user_write_workspace,
        mock_can_user_read_workspace,
        mock_get_all_by_workspace,
        mock_workspace_get_by_id,
    ):
        mock_common_render.side_effect = self.mock_render_only_context

        self.workspace_records_view.administration = True
        response = RequestMock.do_request_get(
            self.workspace_records_view.as_view(),
            None,
            param={"workspace_id": 42},
        )

        self.assertIn("owner", response.keys())
        self.assertIn("owner_change_url", response.keys())


class TestDashboardFiles(TestCase):
    """Unit tests for DashboardFiles.get method."""

    @staticmethod
    def mock_render_only_context(
        request, template_name, modals=None, assets=None, context=None
    ):
        """mock_render_only_context"""
        return context

    def setUp(self) -> None:
        """setUp"""
        self.workspace_files_view = common_views.DashboardFiles

    @patch("core_main_app.components.user.api.get_active_users")
    @patch("core_main_app.components.blob.api.get_all_by_user")
    def test_dashboard_files_loads_blob_file_form(
        self, blob_get_all_by_user, user_get_active_users
    ):
        """test_dashboard_files_loads_blob_file_form"""
        files_qs = MagicMock()
        files_qs.count.return_value = 0
        blob_get_all_by_user.return_value = files_qs
        response = RequestMock.do_request_get(
            self.workspace_files_view.as_view(),
            create_mock_user("1"),
        )
        self.assertTrue(
            '<input type="file" name="file"' in response.content.decode()
        )

    @patch("core_main_app.components.user.api.get_active_users")
    @patch("core_main_app.components.blob.api.get_all_by_user")
    @override_settings(
        INSTALLED_APPS=[
            "core_main_app",
            "core_dashboard_common_app",
            "core_file_preview_app",
        ]
    )
    def test_dashboard_files_adds_file_preview_files_when_installed(
        self, blob_get_all_by_user, user_get_active_users
    ):
        """test_dashboard_files_adds_file_preview_files_when_installed"""
        files_qs = MagicMock()
        files_qs.count.return_value = 0
        blob_get_all_by_user.return_value = files_qs
        response = RequestMock.do_request_get(
            self.workspace_files_view.as_view(),
            create_mock_user("1"),
        )
        self.assertTrue("file_preview.js" in response.content.decode())

    @patch("core_main_app.components.user.api.get_active_users")
    @patch("core_main_app.components.blob.api.get_all_by_user")
    @override_settings(
        INSTALLED_APPS=["core_main_app", "core_dashboard_common_app"]
    )
    def test_dashboard_files_does_not_add_file_preview_files_when_not_installed(
        self, blob_get_all_by_user, user_get_active_users
    ):
        """test_dashboard_files_does_not_add_file_preview_files_when_not_installed"""
        files_qs = MagicMock()
        files_qs.count.return_value = 0
        blob_get_all_by_user.return_value = files_qs
        response = RequestMock.do_request_get(
            self.workspace_files_view.as_view(),
            create_mock_user("1"),
        )
        self.assertTrue("file_preview.js" not in response.content.decode())

    @patch.object(common_views.DashboardFiles, "common_render")
    def test_recently_uploaded_files_none_if_no_report_in_session(
        self, mock_common_render
    ):
        """test_recently_uploaded_files_none_if_no_report_in_session"""

        factory = APIRequestFactory()
        request = factory.get("/mock_url")
        request.user = create_mock_user("1")
        request.session = SessionBase(session_key="KEY")

        mock_common_render.side_effect = self.mock_render_only_context

        response = self.workspace_files_view.as_view()(request)

        self.assertIsNone(response["recently_uploaded_files"])

    @patch.object(common_views.DashboardFiles, "common_render")
    def test_recently_uploaded_files_is_report_from_session(
        self, mock_common_render
    ):
        """test_recently_uploaded_files_is_report_from_session"""

        factory = APIRequestFactory()
        request = factory.get("/mock_url")
        request.user = create_mock_user("1")
        request.session = SessionBase(session_key="KEY")

        mock_upload_report = {"status": "mock_report"}
        request.session["upload_report"] = mock_upload_report

        mock_common_render.side_effect = self.mock_render_only_context

        response = self.workspace_files_view.as_view()(request)

        self.assertEqual(
            response["recently_uploaded_files"], mock_upload_report
        )
