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
            handleFiles(e.dataTransfer.files);
        }
    });

    // Handle normal selection
    input.addEventListener('change', () => {
        handleFiles(input.files);
    });

    // Internal state for property gallery
    let galleryFiles = [];

    const renderGallery = () => {
        previewGrid.innerHTML = '';
        galleryFiles.forEach((fileObj, idx) => {
            const isHidden = idx > 2;
            const isLastVisible = idx === 2;
            const hasMore = galleryFiles.length > 3 && isLastVisible;
            const moreCount = galleryFiles.length - 3;

            const div = document.createElement('div');
            div.className = `preview-item card-look ${hasMore ? 'has-more lightbox-trigger' : ''}`;
            if (isHidden) div.style.display = 'none';
            if (hasMore) div.setAttribute('data-more', `+${moreCount} More`);

            div.innerHTML = `
                <img src="${fileObj.url}" class="lightbox-trigger" alt="Preview">
                <div class="preview-remove"><i class="fas fa-times"></i></div>
            `;

            div.querySelector('.preview-remove').onclick = (event) => {
                event.stopPropagation();
                galleryFiles.splice(idx, 1);
                renderGallery();
            };

            previewGrid.appendChild(div);
        });
    };

    const handleFiles = (files) => {
        Array.from(files).forEach(file => {
            if (!file.type.startsWith('image/')) return;
            galleryFiles.push({
                file: file,
                url: URL.createObjectURL(file)
            });
        });
        renderGallery();
    };
});
