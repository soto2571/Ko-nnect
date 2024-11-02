document.addEventListener('DOMContentLoaded', () => {
    // Function to open the modal and populate the form with schedule data
    function editSchedule(scheduleId) {
        const scheduleElement = document.querySelector(`button[data-schedule-id="${scheduleId}"]`);
        const shiftStart = scheduleElement.getAttribute('data-shift-start');
        const shiftEnd = scheduleElement.getAttribute('data-shift-end');
        
        document.getElementById('schedule_id').value = scheduleId;
        document.getElementById('edit_shift_start').value = shiftStart;
        document.getElementById('edit_shift_end').value = shiftEnd;

        document.getElementById('editScheduleModal').style.display = 'block';
    }

    // Event listener for edit buttons
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', (e) => {
            const scheduleId = e.target.getAttribute('data-schedule-id');
            editSchedule(scheduleId);
        });
    });
    // Script para alternar la visibilidad del menú en pantallas móviles
        document.addEventListener('DOMContentLoaded', function() {
            const menuBtn = document.getElementById('menu-btn');
            const mobileMenu = document.getElementById('mobile-menu');

            menuBtn.addEventListener('click', function() {
                mobileMenu.classList.toggle('hidden');
            });
        });

    // Event listener for form submission
    document.getElementById('editScheduleForm').addEventListener('submit', (e) => {
        e.preventDefault();

        const scheduleId = document.getElementById('schedule_id').value;
        const shiftStart = document.getElementById('edit_shift_start').value;
        const shiftEnd = document.getElementById('edit_shift_end').value;

        fetch(`/admin/edit_schedule/${scheduleId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                shift_start: shiftStart,
                shift_end: shiftEnd
            })
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                alert('Schedule updated successfully');
                window.location.reload(); // Reload the page to see the changes
            } else {
                alert('Error updating schedule');
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});
