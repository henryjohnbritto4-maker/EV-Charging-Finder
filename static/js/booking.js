document.addEventListener("DOMContentLoaded", function () {

    // Extra confirmation safety net for all cancel-booking forms
    const cancelForms = document.querySelectorAll(".cancel-form");

    cancelForms.forEach(function (form) {
        form.addEventListener("submit", function (e) {
            const confirmed = confirm("Are you sure you want to cancel this booking? This cannot be undone.");
            if (!confirmed) {
                e.preventDefault();
            }
        });
    });

    // Prevent selecting a booking date in the past on the booking form
    const dateInput = document.querySelector('input[name="booking_date"]');
    if (dateInput) {
        const today = new Date().toISOString().split("T")[0];
        dateInput.setAttribute("min", today);
    }

    // Ensure end_time is after start_time on the booking form
    const startTime = document.querySelector('input[name="start_time"]');
    const endTime = document.querySelector('input[name="end_time"]');

    if (startTime && endTime) {
        endTime.addEventListener("change", function () {
            if (startTime.value && endTime.value && endTime.value <= startTime.value) {
                alert("End time must be after start time.");
                endTime.value = "";
            }
        });
    }

});