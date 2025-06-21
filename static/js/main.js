document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide flash messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.style.display = 'none';
            }, 300);
        }, 5000);
    });

    // Close button for alerts
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('close')) {
            const alert = e.target.closest('.alert');
            if (alert) {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.style.display = 'none';
                }, 300);
            }
        }
    });

    // Toggle task completion
    document.querySelectorAll('.task-checkbox').forEach(checkbox => {
        checkbox.addEventListener('change', function() {
            const taskId = this.dataset.taskId;
            const isCompleted = this.checked;
            const taskItem = this.closest('.task-item');
            
            // Get CSRF token from meta tag
            const csrfToken = document.querySelector('meta[name="csrf-token"]').getAttribute('content');
            
            // Show loading state
            this.disabled = true;
            
            fetch(`/toggle/${taskId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrfToken
                },
                body: JSON.stringify({
                    completed: isCompleted
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    // Update UI
                    taskItem.classList.toggle('completed', isCompleted);
                    const taskTitle = taskItem.querySelector('.task-title');
                    if (taskTitle) {
                        taskTitle.style.textDecoration = isCompleted ? 'line-through' : 'none';
                        taskTitle.style.opacity = isCompleted ? '0.7' : '1';
                    }
                } else {
                    // Revert checkbox if there was an error
                    this.checked = !isCompleted;
                    console.error('Error toggling task:', data.error);
                }
            })
            .catch(error => {
                console.error('Error:', error);
                this.checked = !isCompleted;
            })
            .finally(() => {
                this.disabled = false;
            });
        });
    });

    // Confirm before deleting a task
    document.querySelectorAll('.delete-task').forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this task?')) {
                e.preventDefault();
            }
        });
    });

    // Update filters on change
    const filterForm = document.getElementById('filter-form');
    if (filterForm) {
        const filterSelects = filterForm.querySelectorAll('select');
        filterSelects.forEach(select => {
            select.addEventListener('change', function() {
                filterForm.submit();
            });
        });
    }

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
});
