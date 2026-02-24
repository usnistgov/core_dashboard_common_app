""" Unit tests for views.common.ajax file
"""

from unittest import TestCase
from unittest.mock import patch, Mock, MagicMock

from django.http import (
    HttpResponse,
    HttpResponseBadRequest,
    HttpResponseServerError,
    QueryDict,
)

from core_dashboard_common_app import constants
from core_dashboard_common_app.views.common import ajax as common_ajax
from core_main_app.access_control.exceptions import AccessControlError
from core_main_app.commons.exceptions import DoesNotExist, NotUniqueError
from core_main_app.utils.tests_tools.MockUser import create_mock_user
from tests.mocks import MockRequest


class TestDeleteWorkspace(TestCase):
    """Unit tests for _delete_workspace method"""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)
        self.kwargs = {"request": mock_request, "workspace_ids": [1, 2, 3]}

    @patch.object(common_ajax, "_get_workspaces")
    def test_get_worspaces_is_called(self, mock_get_workspaces):
        """test_get_worspaces_is_called"""
        mock_get_workspaces.side_effect = Exception(
            "mock_get_workspaces_exception"
        )
        common_ajax._delete_workspace(**self.kwargs)

        mock_user = self.kwargs["request"].user
        mock_get_workspaces.assert_called_with(
            self.kwargs["workspace_ids"], mock_user.is_superuser, mock_user.id
        )

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "_get_workspaces")
    def test_get_workspaces_exception_calls_add_message(
        self, mock_get_workspaces, mock_messages
    ):
        """test_get_workspaces_exception_calls_add_message"""
        mock_get_workspaces.side_effect = Exception(
            "mock_get_workspaces_exception"
        )
        common_ajax._delete_workspace(**self.kwargs)

        self.assertTrue(mock_messages.add_message.assert_called)

    @patch.object(common_ajax, "_get_workspaces")
    def test_get_workspaces_exception_returns_http_response(
        self, mock_get_workspaces
    ):
        """test_get_workspaces_exception_returns_http_response"""
        mock_get_workspaces.side_effect = Exception(
            "mock_get_workspaces_exception"
        )
        response = common_ajax._delete_workspace(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "workspace_api")
    @patch.object(common_ajax, "_get_workspaces")
    def test_workspace_api_delete_is_called(
        self, mock_get_workspaces, mock_workspace_api
    ):
        """test_workspace_api_delete_is_called"""
        mock_get_workspaces.return_value = ["mock_workspace" for _ in range(3)]
        common_ajax._delete_workspace(**self.kwargs)

        self.assertTrue(mock_workspace_api.delete.called)

    @patch.object(common_ajax, "workspace_api")
    @patch.object(common_ajax, "_get_workspaces")
    def test_workspace_api_delete_call_count_is_correct(
        self, mock_get_workspaces, mock_workspace_api
    ):
        """test_workspace_api_delete_is_called"""
        mock_get_workspaces.return_value = ["mock_workspace" for _ in range(3)]
        common_ajax._delete_workspace(**self.kwargs)

        self.assertEqual(mock_workspace_api.delete.call_count, 3)

    @patch.object(common_ajax, "workspace_api")
    @patch.object(common_ajax, "_get_workspaces")
    def test_workspace_api_delete_exception_returns_http_response_bad_request(
        self, mock_get_workspaces, mock_workspace_api
    ):
        """test_workspace_api_delete_exception_returns_http_response_bad_request"""
        mock_get_workspaces.return_value = ["mock_workspace" for _ in range(3)]
        mock_workspace_api.delete.side_effect = AccessControlError(
            "mock_workspace_api_delete_error"
        )
        response = common_ajax._delete_workspace(**self.kwargs)

        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(common_ajax, "workspace_api")
    @patch.object(common_ajax, "_get_workspaces")
    def test_returns_http_response(
        self, mock_get_workspaces, mock_workspace_api
    ):
        """test_returns_http_response"""
        mock_get_workspaces.return_value = ["mock_workspace" for _ in range(3)]
        mock_workspace_api.delete.return_value = None
        response = common_ajax._delete_workspace(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)


class TestDeleteFile(TestCase):
    """Unit tests for _delete_file method"""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)
        self.kwargs = {"request": mock_request, "blob_ids": [1, 2, 3]}

    @patch.object(common_ajax, "_get_blobs")
    def test_get_blobs_is_called(self, mock_get_blobs):
        """test_get_blobs_is_called"""
        mock_get_blobs.side_effect = Exception("mock_get_blobs_exception")
        common_ajax._delete_file(**self.kwargs)

        mock_get_blobs.assert_called_with(
            self.kwargs["blob_ids"], self.kwargs["request"].user
        )

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "_get_blobs")
    def test_get_blobs_exception_calls_add_message(
        self, mock_get_blobs, mock_messages
    ):
        """test_get_blobs_exception_calls_add_message"""
        mock_get_blobs.side_effect = Exception("mock_get_blobs_exception")
        common_ajax._delete_file(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "_get_blobs")
    def test_get_blobs_exception_returns_http_response(self, mock_get_blobs):
        """test_get_blobs_exception_returns_http_response"""
        mock_get_blobs.side_effect = Exception("mock_get_blobs_exception")
        response = common_ajax._delete_file(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "blob_api")
    @patch.object(common_ajax, "_get_blobs")
    def test_blob_api_delete_is_called(self, mock_get_blobs, mock_blob_api):
        """test_blob_api_delete_is_called"""
        mock_get_blobs.return_value = ["mock_blob" for _ in range(3)]
        common_ajax._delete_file(**self.kwargs)

        self.assertTrue(mock_blob_api.delete.called)

    @patch.object(common_ajax, "blob_api")
    @patch.object(common_ajax, "_get_blobs")
    def test_blob_api_delete_call_count_is_correct(
        self, mock_get_blobs, mock_blob_api
    ):
        """test_blob_api_delete_is_called"""
        mock_get_blobs.return_value = ["mock_blob" for _ in range(3)]
        common_ajax._delete_file(**self.kwargs)

        self.assertEqual(mock_blob_api.delete.call_count, 3)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "blob_api")
    @patch.object(common_ajax, "_get_blobs")
    def test_blob_api_delete_exception_calls_add_message(
        self, mock_get_blobs, mock_blob_api, mock_messages
    ):
        """test_blob_api_delete_exception_calls_add_message"""
        mock_get_blobs.return_value = ["mock_blob" for _ in range(3)]
        mock_blob_api.delete.side_effect = Exception(
            "mock_blob_api_delete_exception"
        )
        common_ajax._delete_file(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "blob_api")
    @patch.object(common_ajax, "_get_blobs")
    def test_blob_api_delete_exception_returns_http_response(
        self, mock_get_blobs, mock_blob_api
    ):
        """test_blob_api_delete_exception_returns_http_response"""
        mock_get_blobs.return_value = ["mock_blob" for _ in range(3)]
        mock_blob_api.delete.side_effect = Exception(
            "mock_blob_api_delete_exception"
        )
        response = common_ajax._delete_file(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "blob_api")
    @patch.object(common_ajax, "_get_blobs")
    def test_blob_api_delete_success_calls_add_message(
        self, mock_get_blobs, mock_blob_api, mock_messages
    ):
        """test_blob_api_delete_success_calls_add_message"""
        mock_get_blobs.return_value = ["mock_blob" for _ in range(3)]
        mock_blob_api.delete.return_value = None
        common_ajax._delete_file(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "blob_api")
    @patch.object(common_ajax, "_get_blobs")
    def test_blob_api_delete_success_returns_http_response(
        self, mock_get_blobs, mock_blob_api
    ):
        """test_blob_api_delete_success_returns_http_response"""
        mock_get_blobs.return_value = ["mock_blob" for _ in range(3)]
        mock_blob_api.delete.return_value = None
        response = common_ajax._delete_file(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)


class TestDeleteForm(TestCase):
    """Unit tests for _delete_form method"""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)
        self.kwargs = {"request": mock_request, "form_ids": [1, 2, 3]}

    @patch.object(common_ajax, "_get_forms")
    def test_get_forms_is_called(self, mock_get_forms):
        """test_get_forms_is_called"""
        mock_get_forms.side_effect = Exception("mock_get_forms_exception")
        common_ajax._delete_form(**self.kwargs)

        mock_get_forms.assert_called_with(
            self.kwargs["form_ids"], self.kwargs["request"].user
        )

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "_get_forms")
    def test_get_forms_exception_calls_add_message(
        self, mock_get_forms, mock_messages
    ):
        """test_get_forms_exception_calls_add_message"""
        mock_get_forms.side_effect = Exception("mock_get_forms_exception")
        common_ajax._delete_form(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "_get_forms")
    def test_get_forms_exception_returns_http_response(self, mock_get_forms):
        """test_get_forms_exception_returns_http_response"""
        mock_get_forms.side_effect = Exception("mock_get_forms_exception")
        response = common_ajax._delete_form(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "_get_forms")
    def test_curate_data_structure_api_delete_is_called(
        self, mock_get_forms, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_api_delete_is_called"""
        mock_get_forms.return_value = ["mock_form" for _ in range(3)]
        common_ajax._delete_form(**self.kwargs)

        self.assertTrue(mock_curate_data_structure_api.delete.called)

    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "_get_forms")
    def test_curate_data_structure_api_delete_call_count_is_correct(
        self, mock_get_forms, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_api_delete_is_called"""
        mock_get_forms.return_value = ["mock_form" for _ in range(3)]
        common_ajax._delete_form(**self.kwargs)

        self.assertEqual(mock_curate_data_structure_api.delete.call_count, 3)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "_get_forms")
    def test_curate_data_structure_api_delete_exception_calls_add_message(
        self, mock_get_forms, mock_curate_data_structure_api, mock_messages
    ):
        """test_curate_data_structure_api_delete_exception_calls_add_message"""
        mock_get_forms.return_value = ["mock_form" for _ in range(3)]
        mock_curate_data_structure_api.delete.side_effect = Exception(
            "mock_curate_data_structure_api_delete_exception"
        )
        common_ajax._delete_form(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "_get_forms")
    def test_curate_data_structure_api_delete_exception_returns_http_response(
        self, mock_get_forms, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_api_delete_exception_returns_http_response"""
        mock_get_forms.return_value = ["mock_form" for _ in range(3)]
        mock_curate_data_structure_api.delete.side_effect = Exception(
            "mock_curate_data_structure_api_delete_exception"
        )
        response = common_ajax._delete_form(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "_get_forms")
    def test_curate_data_structure_api_delete_success_calls_add_message(
        self, mock_get_forms, mock_curate_data_structure_api, mock_messages
    ):
        """test_curate_data_structure_api_delete_success_calls_add_message"""
        mock_get_forms.return_value = ["mock_form" for _ in range(3)]
        mock_curate_data_structure_api.delete.return_value = None
        common_ajax._delete_form(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "_get_forms")
    def test_curate_data_structure_api_delete_success_returns_http_response(
        self, mock_get_forms, mock_curate_data_structure_api
    ):
        """test_curate_data_structure_api_delete_success_returns_http_response"""
        mock_get_forms.return_value = ["mock_form" for _ in range(3)]
        mock_curate_data_structure_api.delete.return_value = None
        response = common_ajax._delete_form(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)


class TestDeleteRecord(TestCase):
    """Unit tests for _delete_record method"""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)
        self.kwargs = {"request": mock_request, "data_ids": [1, 2, 3]}

    @patch.object(common_ajax, "_get_data")
    def test_get_data_is_called(self, mock_get_data):
        """test_get_forms_is_called"""
        mock_get_data.side_effect = Exception("mock_get_data_exception")
        common_ajax._delete_record(**self.kwargs)

        mock_get_data.assert_called_with(
            self.kwargs["data_ids"], self.kwargs["request"].user
        )

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "_get_data")
    def test_get_data_exception_calls_add_message(
        self, mock_get_data, mock_messages
    ):
        """test_get_forms_exception_calls_add_message"""
        mock_get_data.side_effect = Exception("mock_get_data_exception")
        common_ajax._delete_record(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "_get_data")
    def test_get_data_exception_returns_http_response(self, mock_get_data):
        """test_get_forms_exception_returns_http_response"""
        mock_get_data.side_effect = Exception("mock_get_data_exception")
        response = common_ajax._delete_record(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_is_object_locked_called(self, mock_get_data, mock_lock_api):
        """test_is_object_locked_called"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        common_ajax._delete_record(**self.kwargs)

        self.assertTrue(mock_lock_api.is_object_locked.called)

    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_is_object_locked_call_count_correct_when_object_is_locked(
        self, mock_get_data, mock_lock_api, mock_data_api
    ):
        """test_is_object_locked_call_count_correct_when_object_is_locked"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        # Method `is_object_locked` will return True after the second call
        mock_lock_api.is_object_locked.side_effect = (
            lambda data_id, user: mock_lock_api.is_object_locked.call_count
            == 2
        )
        mock_data_api.delete.return_value = None
        common_ajax._delete_record(**self.kwargs)

        self.assertEqual(mock_lock_api.is_object_locked.call_count, 2)

    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_is_object_locked_call_count_correct_when_nothing_is_locked(
        self, mock_get_data, mock_lock_api, mock_data_api
    ):
        """test_is_object_locked_call_count_correct_when_nothing_is_locked"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.delete.return_value = None
        common_ajax._delete_record(**self.kwargs)

        self.assertEqual(mock_lock_api.is_object_locked.call_count, 3)

    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_is_object_locked_true_returns_http_response_bad_request(
        self, mock_get_data, mock_lock_api
    ):
        """test_is_object_locked_true_returns_http_response_bad_request"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        mock_lock_api.is_object_locked.return_value = True
        response = common_ajax._delete_record(**self.kwargs)

        self.assertIsInstance(response, HttpResponseBadRequest)

    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_data_api_delete_is_called(
        self, mock_get_data, mock_lock_api, mock_data_api
    ):
        """test_data_api_delete_is_called"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.delete.return_value = None
        common_ajax._delete_record(**self.kwargs)

        self.assertTrue(mock_data_api.delete.called)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_data_api_delete_exception_calls_add_message(
        self, mock_get_data, mock_lock_api, mock_data_api, mock_messages
    ):
        """test_data_api_delete_exception_calls_add_message"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.delete.side_effect = Exception(
            "mock_data_api_delete_exception"
        )
        common_ajax._delete_record(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_data_api_delete_exception_returns_http_response(
        self, mock_get_data, mock_lock_api, mock_data_api
    ):
        """test_data_api_delete_exception_returns_http_response"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.delete.side_effect = Exception(
            "mock_data_api_delete_exception"
        )
        response = common_ajax._delete_record(**self.kwargs)

        self.assertTrue(response, HttpResponse)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_data_api_success_exception_calls_add_message(
        self, mock_get_data, mock_lock_api, mock_data_api, mock_messages
    ):
        """test_data_api_success_exception_calls_add_message"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.delete.return_value = None
        common_ajax._delete_record(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    @patch.object(common_ajax, "_get_data")
    def test_data_api_success_exception_returns_http_response(
        self, mock_get_data, mock_lock_api, mock_data_api
    ):
        """test_data_api_success_exception_returns_http_response"""
        mock_get_data.return_value = [Mock() for _ in range(3)]
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.delete.return_value = None
        response = common_ajax._delete_record(**self.kwargs)

        self.assertTrue(response, HttpResponse)


class TestDeleteQuery(TestCase):
    """Unit tests for _delete_query method"""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)
        mock_request.POST = {"document_type": "mock_document_type"}
        self.kwargs = {"request": mock_request, "query_ids": [1, 2, 3]}

    @patch.object(common_ajax, "_get_query")
    def test_get_query_is_called(self, mock_get_query):
        """test_get_query_is_called"""
        mock_get_query.side_effect = Exception("mock_get_query_exception")
        common_ajax._delete_query(**self.kwargs)

        mock_get_query.assert_called_with(
            None, self.kwargs["query_ids"], self.kwargs["request"].user
        )

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "_get_query")
    def test_get_query_exception_calls_add_message(
        self, mock_get_query, mock_messages
    ):
        """test_get_query_exception_calls_add_message"""
        mock_get_query.side_effect = Exception("mock_get_query_exception")
        common_ajax._delete_query(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "_get_query")
    def test_get_query_exception_returns_http_response(self, mock_get_query):
        """test_get_query_exception_returns_http_response"""
        mock_get_query.side_effect = Exception("mock_get_query_exception")
        response = common_ajax._delete_query(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "persistent_query_api")
    @patch.object(common_ajax, "_get_query")
    def test_persistent_query_api_delete_is_called(
        self, mock_get_query, mock_persistent_query_api
    ):
        """test_persistent_query_api_delete_is_called"""
        mock_get_query.return_value = ["mock_query" for _ in range(3)]
        common_ajax._delete_query(**self.kwargs)

        self.assertTrue(mock_persistent_query_api.delete.called)

    @patch.object(common_ajax, "persistent_query_api")
    @patch.object(common_ajax, "_get_query")
    def test_persistent_query_api_delete_call_count_is_correct(
        self, mock_get_query, mock_persistent_query_api
    ):
        """test_persistent_query_api_delete_is_called"""
        mock_get_query.return_value = ["mock_query" for _ in range(3)]
        common_ajax._delete_query(**self.kwargs)

        self.assertEqual(mock_persistent_query_api.delete.call_count, 3)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "persistent_query_api")
    @patch.object(common_ajax, "_get_query")
    def test_persistent_query_api_delete_exception_calls_add_message(
        self, mock_get_query, mock_persistent_query_api, mock_messages
    ):
        """test_persistent_query_api_delete_exception_calls_add_message"""
        mock_get_query.return_value = ["mock_query" for _ in range(3)]
        mock_persistent_query_api.delete.side_effect = Exception(
            "mock_persistent_query_api_delete_exception"
        )
        common_ajax._delete_query(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "persistent_query_api")
    @patch.object(common_ajax, "_get_query")
    def test_persistent_query_api_delete_exception_returns_http_response(
        self, mock_get_query, mock_persistent_query_api
    ):
        """test_persistent_query_api_delete_exception_returns_http_response"""
        mock_get_query.return_value = ["mock_query" for _ in range(3)]
        mock_persistent_query_api.delete.side_effect = Exception(
            "mock_persistent_query_api_delete_exception"
        )
        response = common_ajax._delete_query(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)

    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "persistent_query_api")
    @patch.object(common_ajax, "_get_query")
    def test_persistent_query_api_delete_success_calls_add_message(
        self, mock_get_query, mock_persistent_query_api, mock_messages
    ):
        """test_persistent_query_api_delete_success_calls_add_message"""
        mock_get_query.return_value = ["mock_query" for _ in range(3)]
        mock_persistent_query_api.delete.return_value = None
        common_ajax._delete_query(**self.kwargs)

        self.assertTrue(mock_messages.add_message.called)

    @patch.object(common_ajax, "persistent_query_api")
    @patch.object(common_ajax, "_get_query")
    def test_persistent_query_api_delete_success_returns_http_response(
        self, mock_get_query, mock_persistent_query_api
    ):
        """test_persistent_query_api_delete_success_returns_http_response"""
        mock_get_query.return_value = ["mock_query" for _ in range(3)]
        mock_persistent_query_api.delete.return_value = None
        response = common_ajax._delete_query(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)


class TestDeleteDocument(TestCase):
    """Unit tests for delete_document view"""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)
        mock_request.POST = MagicMock()
        mock_request.POST.__getitem__ = Mock(
            return_value=constants.FUNCTIONAL_OBJECT_ENUM.RECORD.name
        )

        self.mock_document_id_list = ["1"]
        mock_request.POST.getlist.return_value = self.mock_document_id_list
        self.kwargs = {"request": mock_request}

    def test_multiple_document_ids_non_superuser_returns_http_server_error(
        self,
    ):
        """test_multiple_document_ids_non_superuser_returns_http_server_error"""
        self.kwargs["request"].POST.getlist.return_value = ["1", "2"]
        response = common_ajax.delete_document(**self.kwargs)

        self.assertIsInstance(response, HttpResponseServerError)

    @patch.object(common_ajax, "_delete_record")
    def test_record_document_calls_delete_record(self, mock_delete_record):
        """test_record_document_calls_delete_record"""
        common_ajax.delete_document(**self.kwargs)

        mock_delete_record.assert_called_with(
            self.kwargs["request"], self.mock_document_id_list
        )

    @patch.object(common_ajax, "_delete_form")
    def test_form_document_calls_delete_form(self, mock_delete_form):
        """test_form_document_calls_delete_form"""
        self.kwargs["request"].POST.__getitem__ = Mock(
            return_value=constants.FUNCTIONAL_OBJECT_ENUM.FORM.name
        )
        common_ajax.delete_document(**self.kwargs)

        mock_delete_form.assert_called_with(
            self.kwargs["request"], self.mock_document_id_list
        )

    @patch.object(common_ajax, "_delete_file")
    def test_file_document_calls_delete_file(self, mock_delete_file):
        """test_file_document_calls_delete_file"""
        self.kwargs["request"].POST.__getitem__ = Mock(
            return_value=constants.FUNCTIONAL_OBJECT_ENUM.FILE.name
        )
        common_ajax.delete_document(**self.kwargs)

        mock_delete_file.assert_called_with(
            self.kwargs["request"], self.mock_document_id_list
        )

    @patch.object(common_ajax, "_delete_query")
    def test_query_document_calls_delete_query(self, mock_delete_query):
        """test_query_document_calls_delete_query"""
        self.kwargs["request"].POST.__getitem__ = Mock(
            return_value=constants.FUNCTIONAL_OBJECT_ENUM.QUERY.name
        )
        common_ajax.delete_document(**self.kwargs)

        mock_delete_query.assert_called_with(
            self.kwargs["request"], self.mock_document_id_list
        )

    @patch.object(common_ajax, "_delete_workspace")
    def test_workspace_document_calls_delete_workspace(
        self, mock_delete_workspace
    ):
        """test_workspace_document_calls_delete_workspace"""
        self.kwargs["request"].POST.__getitem__ = Mock(
            return_value=constants.FUNCTIONAL_OBJECT_ENUM.WORKSPACE.name
        )
        common_ajax.delete_document(**self.kwargs)

        mock_delete_workspace.assert_called_with(
            self.kwargs["request"], self.mock_document_id_list
        )

    def test_unknown_document_type_returns_http_bad_request(self):
        """test_unknown_document_type_returns_http_bad_request"""
        self.kwargs["request"].POST.__getitem__ = Mock(
            return_value="unknown_type"
        )
        response = common_ajax.delete_document(**self.kwargs)

        self.assertIsInstance(response, HttpResponseBadRequest)


class TestChangeOwnerDocument(TestCase):
    """Unit tests for change_owner_document view"""

    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)

        mock_request_data = {
            "document_id[]": ["1"],
            "user_id": "1",
            "functional_object": None,
        }

        mock_request.POST = QueryDict(mutable=True)
        mock_request.POST.update(mock_request_data)
        mock_request.POST._mutable = False

        self.kwargs = {"request": mock_request}

    def test_missing_post_params_returns_http_bad_request(self):
        """test_missing_post_params_returns_http_bad_request"""
        self.kwargs["request"].POST = QueryDict(mutable=False)  # noqa
        response = common_ajax.change_owner_document(**self.kwargs)

        self.assertIsInstance(response, HttpResponseBadRequest)

    def test_multiple_document_ids_non_superuser_returns_http_server_error(
        self,
    ):
        """test_multiple_document_ids_non_superuser_returns_http_server_error"""
        self.kwargs["request"].POST._mutable = True
        self.kwargs["request"].POST.setlist("document_id[]", ["1", "2"])
        self.kwargs["request"].POST._mutable = False
        response = common_ajax.change_owner_document(**self.kwargs)

        self.assertIsInstance(response, HttpResponseServerError)

    @patch.object(common_ajax, "_change_owner_record")
    def test_record_document_calls_change_owner_record(
        self, mock_change_owner_record
    ):
        """test_record_document_calls_change_owner_record"""
        self.kwargs["request"].POST._mutable = True
        self.kwargs["request"].POST[
            "functional_object"
        ] = constants.FUNCTIONAL_OBJECT_ENUM.RECORD.name
        self.kwargs["request"].POST._mutable = False
        common_ajax.change_owner_document(**self.kwargs)

        self.assertTrue(mock_change_owner_record.called)

    @patch.object(common_ajax, "_change_owner_form")
    def test_form_document_calls_change_owner_form(
        self, mock_change_owner_form
    ):
        """test_form_document_calls_change_owner_form"""
        self.kwargs["request"].POST._mutable = True
        self.kwargs["request"].POST[
            "functional_object"
        ] = constants.FUNCTIONAL_OBJECT_ENUM.FORM.name
        self.kwargs["request"].POST._mutable = False
        common_ajax.change_owner_document(**self.kwargs)

        self.assertTrue(mock_change_owner_form.called)

    @patch.object(common_ajax, "_change_owner_file")
    def test_file_document_calls_change_owner_file(
        self, mock_change_owner_file
    ):
        """test_file_document_calls_change_owner_file"""

        self.kwargs["request"].POST._mutable = True
        self.kwargs["request"].POST[
            "functional_object"
        ] = constants.FUNCTIONAL_OBJECT_ENUM.FILE.name
        self.kwargs["request"].POST._mutable = False
        common_ajax.change_owner_document(**self.kwargs)

        self.assertTrue(mock_change_owner_file.called)

    def test_unknown_document_type_returns_http_response(self):
        """test_unknown_document_type_returns_http_response"""
        self.kwargs["request"].POST._mutable = True
        self.kwargs["request"].POST["functional_object"] = "n/a"
        self.kwargs["request"].POST._mutable = False
        response = common_ajax.change_owner_document(**self.kwargs)

        self.assertIsInstance(response, HttpResponse)


class TestEditRecord(TestCase):
    def setUp(self) -> None:
        """setUp"""
        mock_request = MockRequest()
        mock_request.user = create_mock_user(1)
        mock_request.POST = {"id": "1"}
        self.kwargs = {"request": mock_request}

    @patch(
        "core_curate_app.components.curate_data_structure.models.CurateDataStructure.__init__"
    )
    @patch.object(common_ajax, "template_api")
    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    def test_edit_record_not_unique_error_return_http_bad_response(
        self,
        mock_lock_api,
        mock_data_api,
        mock_messages,
        mock_curate_data_structure_api,
        mock_template_api,
        mock_cds,
    ):
        """test_edit_record_not_unique_error_return_http_bad_response"""
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.get_by_id.return_value = MagicMock()
        mock_curate_data_structure_api.get_by_data_id_and_user.side_effect = (
            DoesNotExist("error")
        )
        mock_template_api.get_by_id.return_value = MagicMock()
        mock_cds.return_value = None

        mock_curate_data_structure_api.upsert.side_effect = NotUniqueError(
            "error"
        )
        response = common_ajax.edit_record(**self.kwargs)

        self.assertTrue(isinstance(response, HttpResponseBadRequest))

    @patch(
        "core_curate_app.components.curate_data_structure.models.CurateDataStructure.__init__"
    )
    @patch.object(common_ajax, "template_api")
    @patch.object(common_ajax, "curate_data_structure_api")
    @patch.object(common_ajax, "messages")
    @patch.object(common_ajax, "data_api")
    @patch.object(common_ajax, "lock_api")
    def test_edit_record_exception_return_http_bad_response(
        self,
        mock_lock_api,
        mock_data_api,
        mock_messages,
        mock_curate_data_structure_api,
        mock_template_api,
        mock_cds,
    ):
        """test_edit_record_exception_return_http_bad_response"""
        mock_lock_api.is_object_locked.return_value = False
        mock_data_api.get_by_id.return_value = MagicMock()
        mock_curate_data_structure_api.get_by_data_id_and_user.side_effect = (
            DoesNotExist("error")
        )
        mock_template_api.get_by_id.return_value = MagicMock()
        mock_cds.return_value = None

        mock_curate_data_structure_api.upsert.side_effect = Exception("")
        response = common_ajax.edit_record(**self.kwargs)

        self.assertTrue(isinstance(response, HttpResponseBadRequest))
