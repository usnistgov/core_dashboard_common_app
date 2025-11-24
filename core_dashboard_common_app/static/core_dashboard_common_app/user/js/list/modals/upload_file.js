/**
 * Manage the upload of files.
 */
$(document).ready(function() {
    const dropBoxId = "#drop-box";
    const $fileInput = $("#id_file");
    const $fileName = $("#file-name");

    $(document).on("dragover", dropBoxId, (event) => {
        event.preventDefault();
        $(dropBoxId).addClass("dragover");
    });

    $(document).on("dragleave", dropBoxId, () => {
        $(dropBoxId).removeClass("dragover");
    });

    $(document).on("drop", dropBoxId, (event) => {
        event.preventDefault();
        $(dropBoxId).removeClass("dragover");

        const transferedFiles = event.originalEvent.dataTransfer.files;

        // Iterate over the transferedFiles and upload each file
        Array.from(transferedFiles).forEach((file, index) => {
            const fileList = new DataTransfer();
            fileList.items.add(file);

            // Populate the form with the correct items
            $fileInput.prop("files", fileList.files);
            $fileName.text(file.name);

            // Upload the current file
            uploadFile(index === transferedFiles.length - 1);
        });
    });

    $fileInput.on("change", function (event) {
        uploadFile(true)
    })

    /**
     * Initiates the file upload process using AJAX.
     */
    function uploadFile(reload = false) {
        const formData = new FormData($("#file-upload-form")[0]);

        $.ajax({
            url: uploadFileUrl,
            type: "POST",
            dataType: "json",
            processData: false,
            contentType: false,
            data: formData,
            success: function() {
                if (reload) {
                    location.reload();
                }
            },
            error: function (data) {
                let error_message;
                try {
                    error_message = JSON.parse(data.responseText).message;
                } catch (e) {
                    error_message = "Unable to upload this file."
                }

                $.notify(error_message, "danger");
            }
        });
    }
});
