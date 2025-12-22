/**
 * Manage the upload of files.
 */
$(document).ready(function() {
    const dropBoxId = "#drop-box";
    const $fileInput = $("#id_file");

    $(document).on("dragover", dropBoxId, (event) => {
        event.preventDefault();
        $(dropBoxId).addClass("dragover");
    });

    $(document).on("dragleave", dropBoxId, () => {
        $(dropBoxId).removeClass("dragover");
    });

    $(document).on("drop", dropBoxId, (event) => {
        event.preventDefault();
        event.stopPropagation();
        $(dropBoxId).removeClass("dragover");

        uploadFileList(event.originalEvent.dataTransfer.files)
    });

    $fileInput.on("change", function (event) {
        event.preventDefault();
        uploadFileList(event.target.files)
    })

    function uploadFileList(fileList) {
        // Toggle the upload alert on.
        $(".upload-alert").addClass("hidden")
        $("#upload-data-alert-box").removeClass("hidden")

        // Ensure file list is an array and perform basic healthcheck.
        fileList = Array.from(fileList);
        if (!fileList || fileList.length === 0) return;

        // Create FormData and other variables.
        const $form = $("#file-upload-form");
        const formData = new FormData($form[0]);

        const inputName = $fileInput.attr('name');

        // Ensures the fileList variable is send and not what is currently selected in
        // the HTML input.
        if (formData.has(inputName)) {
            formData.delete(inputName);
        }

        // Append all files to the same input name and upload.
        fileList.forEach((file) => {
            formData.append(inputName, file);
        });
        uploadFile(formData);
    }

    /**
     * Initiates the file upload process using AJAX.
     */
    function uploadFile(uploadData) {
        $.ajax({
            url: uploadFileUrl,
            type: "POST",
            dataType: "json",
            processData: false,
            contentType: false,
            data: uploadData,
            success: function() {
                location.reload();
            },
            error: function (xhr, _text, _error) {
                let error_message;

                // Check for Nginx specific errors (413 = Too Large)
                if (xhr.status === 413) {
                    error_message = "The files are too large for the server.";
                }
                // Check for Nginx Gateway Timeouts (504)
                else if (xhr.status === 504) {
                    error_message = "The files took too long to upload.";
                }
                // Check for Django Bad Requests (400)
                else if (xhr.status === 400) {
                    try {
                        const response = JSON.parse(xhr.responseText);
                        // If the response is empty, the 400 is due to an upload error,
                        // with all info stored on the session. We just need to reload
                        // the page.
                        if (Object.keys(response).length === 0) {
                            location.reload(); // Reload the page
                            return;
                        } else {
                            error_message = response.message || "Bad request";
                        }
                    } catch (_) {
                        // Fallback if response isn't JSON or parsing fails
                        error_message = "An unexpected error occurred (" + xhr.status + ").";
                    }
                }
                else { // Parse any other Django JSON errors
                    try {
                        // Attempt to parse the response text as JSON
                        error_message = JSON.parse(xhr.responseText).message;
                    } catch (_) {
                        // Fallback if response isn't JSON
                        error_message = "An unexpected error occurred (" + xhr.status + ").";
                    }
                }

                $(".upload-alert").addClass("hidden")
                $.notify(error_message, "danger");
            },
        });
    }
});
