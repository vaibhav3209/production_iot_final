// To close the sidebar in mobile view
document.addEventListener("DOMContentLoaded", function () {
    const openToggle = document.getElementById("mobilesidebarToggle");   // header IoT
    const closeToggle = document.getElementById("sidebarClose");        // sidebar h2
    const sidebar = document.querySelector(".sidebar");

    function toggleSidebar() {
        sidebar.classList.toggle("active");
    }

    openToggle.addEventListener("click", function (e) {
        e.stopPropagation();
        toggleSidebar();
    });

    closeToggle.addEventListener("click", function () {
        toggleSidebar();
    });
});