document.addEventListener("DOMContentLoaded", function () {
    const addButton = document.getElementById("openAddRow");
    const form = document.getElementById("addComponentForm");
    const cancelBtn = document.getElementById("cancelForm");

    // Show form when Add button clicked
    addButton.addEventListener("click", function () {
        form.style.display = "block";
        addButton.style.display = "none";
    });

    // Hide form when Cancel clicked
    cancelBtn.addEventListener("click", function () {
        form.reset(); // optional
        form.style.display = "none";
        addButton.style.display = "inline-block";
    });


//Edit button for project
    document.querySelectorAll(".edit-icon").forEach(icon => {
        icon.addEventListener("click", function () {
            const card = icon.closest(".project-card");
            const editForm = card.querySelector(".card-edit");

            editForm.style.display = "block";
        });
    });

    document.querySelectorAll(".cancel-edit").forEach(btn => {
        btn.addEventListener("click", function () {
            const card = btn.closest(".project-card");
            const editForm = card.querySelector(".card-edit");

            editForm.style.display = "none";
        });
    });

});