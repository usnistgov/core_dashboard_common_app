/**
 * Send a DELETE request and return the jQuery XHR deferred.
 *
 * @param {string} deleteUrl - URL for the DELETE endpoint.
 * @returns {jqXHR}
 */
const deleteDraft = function(deleteUrl) {
    return $.ajax({
        url: deleteUrl,
        type: "DELETE",
        dataType: "json",
    });
};

/**
 * Handle clicks on draft-delete buttons (.delete-draft-btn and
 * .delete-data-draft-list-btn). Optimistically removes the "Draft" label
 * and the button, then fires the DELETE request.
 *
 * Expects globals injected by the Django template:
 *   deleteRecordDraftUrl, deleteRecordDraftListUrl  (with "pk" placeholder)
 */
$(".delete-draft-btn, .delete-data-draft-list-btn").on("click", function() {
    const $btn = $(this);
    const objectId = $btn.attr("objectid");
    const isAdminView = $btn.hasClass("delete-data-draft-list-btn");
    const deleteUrl = isAdminView
        ? deleteRecordDraftListUrl.replace("pk", objectId)
        : deleteRecordDraftUrl.replace("pk", objectId);

    removeDraftStatus($btn, isAdminView);
    $btn.remove();

    deleteDraft(deleteUrl)
        .done(function() {
            $.notify("Draft is being deleted!", "success");
        })
        .fail(function(xhr) {
            const response = JSON.parse(xhr.responseText);
            $.notify("Draft deletion failed: " + response.message, "danger");
        });
});
