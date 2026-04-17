/**
 * Strip the trailing ", Draft" label from a table row's name cell.
 *
 * @param {jQuery} recordRow - The <tr> element containing the record.
 * @param {number} columnIdx - Zero-based index of the name cell within the row.
 */
const removeDraftStatus = function(recordRow, columnIdx) {
    const $recordNameCol = recordRow.children("td").eq(columnIdx);
    const filename = $recordNameCol.text().replace(/,\s*Draft\s*$/i, "").trim();
    $recordNameCol.text(filename);
};

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
    const $recordRow = $btn.parents("tr");
    const objectId = $btn.attr("objectid");
    const isDraftList = $btn.hasClass("delete-data-draft-list-btn");

    // Admin view has a checkbox column, shifting the name to index 1.
    const columnIdx = isDraftList ? 1 : 0;
    const deleteUrl = isDraftList
        ? deleteRecordDraftListUrl.replace("pk", objectId)
        : deleteRecordDraftUrl.replace("pk", objectId);

    removeDraftStatus($recordRow, columnIdx);
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
