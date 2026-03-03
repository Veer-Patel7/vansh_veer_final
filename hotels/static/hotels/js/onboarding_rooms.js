/**
 * RoomManager - Professional Room Category Management
 * Handles dynamic addition, removal, media uploads, and amenities for room categories.
 */
class RoomManager {
    constructor() {
        this.roomList = document.getElementById('roomList');
        this.addRoomBtn = document.getElementById('addRoomBtn');
        this.template = document.getElementById('room-row-template');
        this.roomIndex = 1;
        this.rooms = new Map(); // Store room-specific state

        this.init();
    }

    init() {
        if (this.addRoomBtn) {
            this.addRoomBtn.addEventListener('click', () => this.addRoom());
        }

        // Add first room by default if empty
        if (this.roomList && this.roomList.children.length === 0) {
            this.addRoom();
        }

        this.setupLightbox();
    }

    /**
     * Re-indexes all room cards to ensure form name consistency
     */
    reorderRooms() {
        const rows = this.roomList.querySelectorAll('.room-card-elite');
        rows.forEach((row, index) => {
            const newIdx = index + 1;
            row.dataset.roomIndex = newIdx;

            const display = row.querySelector('.room-num-display');
            if (display) display.textContent = newIdx;

            row.querySelectorAll('input, select, textarea').forEach(el => {
                ['name', 'id'].forEach(attr => {
                    const val = el.getAttribute(attr);
                    if (val) el.setAttribute(attr, val.replace(/\d+$/, newIdx));
                });
            });

            row.querySelectorAll('.custom-select-container').forEach(el => {
                const target = el.getAttribute('data-target');
                if (target) el.setAttribute('data-target', target.replace(/\d+$/, newIdx));
            });
        });
        this.roomIndex = rows.length + 1;
    }

    /**
     * Adds a new room category row
     */
    addRoom() {
        if (!this.template || !this.roomList) return;

        const content = this.template.innerHTML.replace(/__prefix__/g, this.roomIndex);
        const div = document.createElement('div');
        div.innerHTML = content;
        const row = div.firstElementChild;

        this.roomList.appendChild(row);
        this.setupRoomInteractions(row);
        this.roomIndex++;
    }

    /**
     * Wire up listeners for a specific room row
     */
    setupRoomInteractions(row) {
        // 1. Remove Logic
        row.querySelector('.remove-room').addEventListener('click', () => {
            row.remove();
            this.reorderRooms();
        });

        // 2. Dropdown Logic
        const classContainer = row.querySelector('.room-class-select-container');
        if (classContainer && window.updateRoomClassOptions) {
            window.updateRoomClassOptions(classContainer);
        }
        if (window.updateRoomCategoryOptions) {
            window.updateRoomCategoryOptions(row);
        }

        // 3. Amenity Logic
        this.setupAmenities(row);

        // 4. Media Logic
        this.setupMedia(row);
    }

    setupAmenities(row) {
        const input = row.querySelector('.new-amenity-text');
        const btn = row.querySelector('.pill-add-btn');
        const container = row.querySelector('.dynamic-pills-container');
        const hidden = row.querySelector('input[name^="room_amenities"]');

        const sync = () => {
            const checked = Array.from(container.querySelectorAll('.pill-label input:checked'))
                .map(i => i.value.trim());
            hidden.value = JSON.stringify(checked);
        };

        container.addEventListener('change', (e) => {
            if (e.target.type === 'checkbox') sync();
        });

        btn.addEventListener('click', () => {
            const val = input.value.trim();
            if (val) {
                const label = document.createElement('label');
                label.className = 'pill-label';
                label.innerHTML = `
                    <input type="checkbox" value="${val}" checked style="display:none;">
                    <i class="fas fa-check-circle" style="color:var(--secondary);"></i>
                    ${val}
                `;
                container.appendChild(label);
                input.value = '';
                sync();
            }
        });
        sync();
    }

    setupMedia(row) {
        const uploadBtn = row.querySelector('.room-upload-btn');
        const fileInput = row.querySelector('input[name^="room_photos"]');
        const previewBox = row.querySelector('.room-preview-box');
        let currentMedia = [];

        const renderGallery = () => {
            previewBox.innerHTML = '';
            currentMedia.forEach((fileObj, idx) => {
                const isHidden = idx > 2; // Show only 3 items
                const isLastVisible = idx === 2;
                const hasMore = currentMedia.length > 3 && isLastVisible;
                const moreCount = currentMedia.length - 3;

                const preview = document.createElement('div');
                preview.className = `preview-item card-look ${hasMore ? 'has-more lightbox-trigger' : ''}`;
                if (isHidden) preview.style.display = 'none';
                if (hasMore) preview.setAttribute('data-more', `+${moreCount} More`);

                if (fileObj.type.startsWith('image/')) {
                    preview.innerHTML = `
                        <img src="${fileObj.url}" class="lightbox-trigger">
                        <div class="preview-remove"><i class="fas fa-times"></i></div>
                    `;
                } else {
                    preview.innerHTML = `
                        <video src="${fileObj.url}"></video>
                        <div class="video-overlay lightbox-trigger"><i class="fas fa-play"></i></div>
                        <div class="preview-remove"><i class="fas fa-times"></i></div>
                    `;
                }

                preview.querySelector('.preview-remove').onclick = (ex) => {
                    ex.stopPropagation();
                    currentMedia.splice(idx, 1);
                    renderGallery();
                };

                previewBox.appendChild(preview);
            });
        };

        uploadBtn.addEventListener('click', (e) => {
            if (!e.target.closest('.preview-item')) fileInput.click();
        });

        fileInput.addEventListener('change', () => {
            const files = Array.from(fileInput.files);
            let photoCount = currentMedia.filter(m => m.type.startsWith('image/')).length;
            let videoCount = currentMedia.filter(m => m.type.startsWith('video/')).length;

            files.forEach(file => {
                const isImg = file.type.startsWith('image/');
                const isVid = file.type.startsWith('video/');

                if (isImg && photoCount >= 3) return;
                if (isVid && videoCount >= 1) return;

                currentMedia.push({
                    file: file,
                    url: URL.createObjectURL(file),
                    type: file.type
                });
                if (isImg) photoCount++;
                if (isVid) videoCount++;
            });
            renderGallery();
        });
    }

    setupLightbox() {
        const lightbox = document.getElementById('lightboxModal');
        const img = document.getElementById('lightboxImage');
        const vid = document.getElementById('lightboxVideo');
        const pdf = document.getElementById('lightboxPDF');
        const caption = document.getElementById('lightboxCaption');
        let gallery = [];
        let cursor = 0;

        const show = () => {
            const media = gallery[cursor];
            if (!media || !lightbox) return;

            // Reset all stage elements
            if (img) { img.style.display = 'none'; img.src = ''; }
            if (vid) { vid.style.display = 'none'; vid.pause(); vid.src = ''; }
            if (pdf) { pdf.style.display = 'none'; pdf.src = 'about:blank'; }

            // Handle direct blobs/URL objects (from single file preview)
            if (media.isBlob) {
                if (media.type === 'pdf' && pdf) {
                    pdf.src = media.src;
                    pdf.style.display = 'block';
                } else if (media.type === 'video' && vid) {
                    vid.src = media.src;
                    vid.style.display = 'block';
                    vid.play().catch(e => console.warn("Blob Video Autoplay prevented:", e));
                } else if (img) {
                    img.src = media.src;
                    img.style.display = 'block';
                }

                // Update professional header metadata
                if (caption) caption.textContent = media.filename || 'verification_dossier.pdf';
                const tokenEl = document.getElementById('viewer-token');
                if (tokenEl) {
                    const randomToken = 'AUTH-' + Math.floor(1000 + Math.random() * 9000) + '-' + Math.random().toString(36).substring(2, 4).toUpperCase();
                    tokenEl.textContent = `TOKEN: ${randomToken}`;
                }
                return;
            }

            // Handle DOM elements (gallery)
            if (media.tagName === 'IMG' && img) {
                img.src = media.src;
                img.style.display = 'block';
            } else if ((media.tagName === 'VIDEO' || media.classList.contains('video-trigger')) && vid) {
                let videoSrc = media.src || media.querySelector('source')?.src;
                if (!videoSrc) {
                    const parent = media.closest('.preview-item') || media.closest('.summary-media-item');
                    videoSrc = parent?.querySelector('video')?.src;
                }
                vid.src = videoSrc || '';
                vid.style.display = 'block';
                vid.play().catch(e => console.warn("Gallery Video Autoplay prevented:", e));
            }

            // Update header for Gallery Mode
            const filenameEl = document.getElementById('lightboxCaption');
            if (filenameEl) {
                const isRoom = media.closest('.room-preview-box') || media.closest('.summary-room-item');
                filenameEl.textContent = isRoom ? `Room Gallery [${cursor + 1} / ${gallery.length}]` : `Property Gallery [${cursor + 1} / ${gallery.length}]`;
            }
            const tokenEl = document.getElementById('viewer-token');
            if (tokenEl) {
                const tokenType = (media.closest('.room-preview-box') || media.closest('.summary-room-item')) ? 'RM-GAL' : 'PROP-GAL';
                const randomToken = `${tokenType}-${Math.floor(1000 + Math.random() * 9000)}-${(cursor + 1).toString().padStart(2, '0')}`;
                tokenEl.textContent = `REF: ${randomToken}`;
            }

            const iconBox = document.querySelector('.viewer-icon-box i');
            if (iconBox) {
                iconBox.className = 'fas fa-images';
            }
        };

        window.openLightbox = (sources, start = 0) => {
            if (!lightbox) return console.error("Lightbox: #lightboxModal not found in DOM.");
            gallery = sources;
            cursor = start;
            show();
            lightbox.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Lock scrolling
        };

        window.closeLightbox = () => {
            if (lightbox) lightbox.style.display = 'none';
            if (vid) { vid.pause(); vid.src = ''; }
            if (img) img.src = '';
            if (pdf) pdf.src = 'about:blank';
            document.body.style.overflow = ''; // Unlock scrolling

            // Clean up any blob URLs if necessary
            if (gallery.some(m => m.isBlob)) {
                gallery.forEach(m => { if (m.isBlob && m.src.startsWith('blob:')) URL.revokeObjectURL(m.src); });
            }
        };

        // Professional Single File Preview Helper
        window.previewSingleFile = (url, filename, ext) => {
            const previewObj = {
                src: url,
                filename: filename,
                type: (['jpg', 'jpeg', 'png', 'webp'].includes(ext) ? 'image' : (ext === 'pdf' ? 'pdf' : (['mp4', 'webm'].includes(ext) ? 'video' : 'image'))),
                isBlob: true
            };

            // Reset header for Document Mode before opening
            const iconBox = document.querySelector('.viewer-icon-box i');
            if (iconBox) iconBox.className = 'fas fa-file-shield';

            window.openLightbox([previewObj], 0);
        };

        window.changeSlide = (n) => {
            cursor = (cursor + n + gallery.length) % gallery.length;
            show();
        };

        document.addEventListener('click', (e) => {
            const trigger = e.target.closest('.lightbox-trigger');
            if (trigger) {
                const box = trigger.closest('.room-preview-box') ||
                    trigger.closest('.gallery-preview-grid') ||
                    trigger.closest('.summary-media-grid');

                if (box) {
                    // Collect all media sources in the box
                    const images = Array.from(box.querySelectorAll('img')).map(el => ({
                        tagName: 'IMG',
                        src: el.src,
                        closest: (sel) => el.closest(sel)
                    }));
                    const videos = Array.from(box.querySelectorAll('video')).map(el => ({
                        tagName: 'VIDEO',
                        src: el.src,
                        closest: (sel) => el.closest(sel),
                        classList: { contains: (c) => el.classList.contains(c) }
                    }));

                    const allMedia = [...images, ...videos];

                    // Find target index
                    let targetSrc = trigger.tagName === 'IMG' || trigger.tagName === 'VIDEO' ? trigger.src : trigger.querySelector('img, video')?.src;
                    const index = allMedia.findIndex(m => m.src === targetSrc);

                    if (allMedia.length > 0) {
                        window.openLightbox(allMedia, index > -1 ? index : 0);
                    }
                }
            }
        });
    }
}

// Initialize on DOM Load
document.addEventListener('DOMContentLoaded', () => {
    window.roomManager = new RoomManager();
});
