document.addEventListener('DOMContentLoaded', () => {
    console.log('[Dropdown] Global listener initialized.');

    document.addEventListener('click', (e) => {
        const container = e.target.closest('.custom-select-container');
        const selected = e.target.closest('.select-selected');
        const item = e.target.closest('.select-item');

        // Close dropdowns when clicking outside
        if (!container) {
            const openDropdowns = document.querySelectorAll('.select-items.show');
            if (openDropdowns.length > 0) {
                console.log(`[Dropdown] Closing ${openDropdowns.length} open dropdowns (click outside).`);
                openDropdowns.forEach(items => items.classList.remove('show'));
                document.querySelectorAll('.select-selected.active').forEach(s => s.classList.remove('active'));
            }
            return;
        }

        // Toggle dropdown
        if (selected) {
            const items = container.querySelector('.select-items');
            const isActive = items.classList.contains('show');

            console.log(`[Dropdown] Toggling: ${container.dataset.target || 'unknown'} | Current: ${isActive ? 'OPEN' : 'CLOSED'}`);

            // Close all other dropdowns
            document.querySelectorAll('.select-items.show').forEach(i => {
                if (i !== items) i.classList.remove('show');
            });
            document.querySelectorAll('.select-selected.active').forEach(s => {
                if (s !== selected) s.classList.remove('active');
            });

            // Toggle current
            items.classList.toggle('show');
            selected.classList.toggle('active');

            console.log(`[Dropdown] New status: ${items.classList.contains('show') ? 'OPEN' : 'CLOSED'}`);
        }

        // Handle item selection
        if (item) {
            const val = item.dataset.value;
            const text = item.innerHTML;
            const targetId = container.dataset.target;

            console.log(`[Dropdown] Item clicked: ${val} for target: ${targetId}`);

            // Search within the same parent row first for dynamic contexts
            const row = container.closest('.room-row');
            const hidden = row ? row.querySelector('#' + targetId) : document.getElementById(targetId);

            const selectedBox = container.querySelector('.select-selected');
            if (selectedBox) {
                const textEl = selectedBox.querySelector('.selected-text');
                if (textEl) textEl.innerHTML = text;
            }

            if (hidden) {
                hidden.value = val;
                hidden.dispatchEvent(new Event('change'));
            }

            // Close
            container.querySelector('.select-items').classList.remove('show');
            selectedBox.classList.remove('active');
        }
    });

    // Keyboard Accessibility
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.select-items').forEach(items => items.classList.remove('show'));
            document.querySelectorAll('.select-selected').forEach(s => s.classList.remove('active'));
        }
    });
});
