// ===============================
// EV Charging Finder
// script.js
// ===============================

document.addEventListener("DOMContentLoaded", function () {

    console.log("EV Charging Finder Loaded");

    // Auto-close alerts after 3 seconds
    const alerts = document.querySelectorAll(".alert");

    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.classList.remove("show");
            alert.classList.add("fade");
        }, 3000);
    });

    // Confirm before deleting
    const deleteButtons = document.querySelectorAll(".delete-btn");

    deleteButtons.forEach(function (button) {

        button.addEventListener("click", function (e) {

            if (!confirm("Are you sure you want to delete this record?")) {

                e.preventDefault();

            }

        });

    });

    // Highlight active navigation link
    const currentPage = window.location.pathname;

    document.querySelectorAll(".navbar a").forEach(function (link) {

        if (link.getAttribute("href") === currentPage) {

            link.classList.add("active");

        }

    });

});