// onboarding_gallery.js
document.addEventListener('DOMContentLoaded', () => {
    const uploadZone = document.getElementById('galleryUploadZone');
    const input = document.getElementById('galleryInput');
    const previewGrid = document.getElementById('galleryPreviewContainer');

    if (!uploadZone || !input || !previewGrid) return;

    // Trigger input on zone click
    uploadZone.addEventListener('click', () => input.click());

    // Handle Drag & Drop
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('drag-active');
    });

    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('drag-active');
    });

    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('drag-active');
        if (e.dataTransfer.files.length) {
            input.files = e.dataTransfer.files;
            handleFiles(e.dataTransfer.files);
        }
    });

    // Handle normal selection
    input.addEventListener('change', () => {
        handleFiles(input.files);
    });

    const handleFiles = (files) => {
        Array.from(files).forEach(file => {
            if (!file.type.startsWith('image/')) return;

            const reader = new FileReader();
            reader.onload = (e) => {
                const div = document.createElement('div');
                div.className = 'preview-item card-look';
                div.innerHTML = `
                    <img src="${e.target.result}" alt="Preview">
                    <div class="preview-remove"><i class="fas fa-times"></i></div>
                `;

                div.querySelector('.preview-remove').onclick = (event) => {
                    event.stopPropagation();
                    div.remove();
                };

                previewGrid.appendChild(div);
            };
            reader.readAsDataURL(file);
        });
    };
});
