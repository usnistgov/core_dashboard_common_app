"""
Url router for the dashboard common
"""

from django.conf.urls import include
from django.contrib import admin
from django.urls import re_path

from core_dashboard_common_app.views.common import ajax
from core_file_preview_app.views.user.ajax import get_blob_preview
from core_main_app.admin import core_admin_site

urlpatterns = [
    re_path(r"^admin/", admin.site.urls),
    re_path(r"^core-admin/", core_admin_site.urls),
    re_path(r"^", include("core_main_app.urls")),
    re_path(r"^", include("core_curate_app.urls")),
    re_path(
        r"^edit-record", ajax.edit_record, name="core_dashboard_edit_record"
    ),
    re_path(
        r"^delete-document",
        ajax.delete_document,
        name="core_dashboard_delete_document",
    ),
    re_path(
        r"^change-owner",
        ajax.change_owner_document,
        name="core_dashboard_change_owner_document",
    ),
    re_path(
        r"^get_blob_preview",
        get_blob_preview,
        name="core_file_preview_app_get_blob_preview",
    ),
]
