/**
 * Strip the trailing ", Draft" label from a table row's name cell.
 *
 * @param {jQuery} btnObject - The button element containing the record.
 * @param {boolean} isAdminView - Zero-based index of the name cell within the row.
 */
removeDraftStatus = function(btnObject, isAdminView) {
    const columnIdx = isAdminView ? 1 : 0;

    const $recordNameCol = btnObject.parents("tr").children("td").eq(columnIdx);
    const filename = $recordNameCol.text().replace(/,\s*Draft\s*$/i, "").trim();
    $recordNameCol.text(filename);
};
