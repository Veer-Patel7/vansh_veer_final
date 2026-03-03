function handleDelete(id) {
    if (!id) return;

    // Get CSRF token from HTML data attribute or global variable
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value ||
        document.documentElement.dataset.csrf;

    if (confirm('Are you sure you want to terminate this strategy permanently? This action cannot be undone.')) {
        fetch(`/hotels/offers/delete/${id}/`, {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken }
        })
            .then(res => res.json())
            .then(data => { if (data.status === 'success') location.reload(); });
    }
}
