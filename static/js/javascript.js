
document.addEventListener("DOMContentLoaded", function () {

    const fileInput = document.querySelector(
        'input[type="file"]'
    );

    if (fileInput) {

        fileInput.addEventListener(
            "change",
            function () {

                if (fileInput.files.length > 0) {

                    console.log(
                        "Resume selected:",
                        fileInput.files[0].name
                    );

                }

            }
        );

    }

});