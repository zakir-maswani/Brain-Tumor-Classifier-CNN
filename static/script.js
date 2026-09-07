const imageInput = document.getElementById("imageInput");

const preview = document.getElementById("preview");

const previewContainer =
    document.getElementById("previewContainer");

const predictBtn =
    document.getElementById("predictBtn");

const loading =
    document.getElementById("loading");

const result =
    document.getElementById("result");

const prediction =
    document.getElementById("prediction");

const confidence =
    document.getElementById("confidence");


// ---------------------------------------------
// Image Selection
// ---------------------------------------------

imageInput.addEventListener("change", function () {

    const file = imageInput.files[0];

    if (!file) {
        return;
    }


    // Show preview

    const imageURL =
        URL.createObjectURL(file);

    preview.src = imageURL;

    previewContainer.classList.remove("hidden");


    // Enable button

    predictBtn.disabled = false;


    // Hide previous result

    result.classList.add("hidden");

});


// ---------------------------------------------
// Prediction
// ---------------------------------------------

predictBtn.addEventListener("click", async function () {

    const file = imageInput.files[0];

    if (!file) {
        return;
    }


    // FormData

    const formData = new FormData();

    formData.append("file", file);


    // UI

    predictBtn.disabled = true;

    loading.classList.remove("hidden");

    result.classList.add("hidden");


    try {

        const response = await fetch(
            "/predict",
            {
                method: "POST",
                body: formData
            }
        );


        if (!response.ok) {

            throw new Error(
                "Prediction failed"
            );

        }


        const data =
            await response.json();


        // Display result

        prediction.textContent =
            data.prediction;

        confidence.textContent =
            data.confidence + "%";


        result.classList.remove(
            "hidden"
        );


    } catch (error) {

        alert(
            "Something went wrong while predicting."
        );

        console.error(error);

    }


    // UI reset

    loading.classList.add("hidden");

    predictBtn.disabled = false;

});