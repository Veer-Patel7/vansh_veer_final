// onboarding_rooms.js
document.addEventListener('DOMContentLoaded', () => {
    const roomList = document.getElementById('roomList');
    const addRoomBtn = document.getElementById('addRoomBtn');
    const template = document.getElementById('room-row-template');

    let roomIndex = 1; // Start at 1 to match views.py while loop

    const reorderRooms = () => {
        const rows = roomList.querySelectorAll('.room-row');
        console.group(`[Rooms] Re-indexing ${rows.length} categories`);

        rows.forEach((row, index) => {
            const newIdx = index + 1;

            // 1. Update Visual Title
            const display = row.querySelector('.room-num-display');
            if (display) display.textContent = newIdx;

            // 2. Update Row Tracking
            row.dataset.roomIndex = newIdx;

            // 3. Update Inputs/Selects/Targets
            const updateAttr = (el, attr) => {
                const val = el.getAttribute(attr);
                if (val) {
                    // Match numbers at the end of the string (e.g. room_name_1)
                    const newVal = val.replace(/\d+$/, newIdx);
                    el.setAttribute(attr, newVal);
                }
            };

            row.querySelectorAll('input, select, textarea').forEach(el => {
                updateAttr(el, 'name');
                updateAttr(el, 'id');
            });

            row.querySelectorAll('.custom-select-container').forEach(el => {
                const target = el.getAttribute('data-target');
                if (target) {
                    el.setAttribute('data-target', target.replace(/\d+$/, newIdx));
                }
            });
        });

        roomIndex = rows.length + 1;
        console.log(`[Rooms] Ready for next node at index: ${roomIndex}`);
        console.groupEnd();
    };

    const addRoom = () => {
        if (!template || !roomList) return;
        const content = template.innerHTML.replace(/__prefix__/g, roomIndex);
        const div = document.createElement('div');
        div.innerHTML = content;
        const row = div.firstElementChild;

        // Add to DOM first so we can find elements by ID/selection if needed
        roomList.appendChild(row);

        // Dropdown initialization is now handled globally by dropdown.js via event delegation
        console.log(`[Rooms] Row index ${roomIndex} added. Dropdown auto-wired.`);

        row.querySelector('.remove-room').addEventListener('click', () => {
            row.remove();
            console.log(`[Rooms] Removed category. Triggering re-index...`);
            reorderRooms();
        });

        // Add amenity logic
        const amenityInput = row.querySelector('.new-amenity-text');
        const amenityBtn = row.querySelector('.pill-add-btn');
        const amenityContainer = row.querySelector('.dynamic-pills-container');
        const hiddenAmenities = row.querySelector('input[type="hidden"]');

        const updateAmenities = () => {
            const pills = Array.from(amenityContainer.querySelectorAll('.dynamic-pill-item span')).map(s => s.textContent);
            hiddenAmenities.value = JSON.stringify(pills);
        };

        amenityBtn.addEventListener('click', () => {
            const val = amenityInput.value.trim();
            if (val) {
                const pill = document.createElement('div');
                pill.className = 'dynamic-pill-item';
                pill.innerHTML = `<span>${val}</span><i class="fas fa-times remove-icon"></i>`;
                pill.querySelector('.remove-icon').onclick = () => { pill.remove(); updateAmenities(); };
                amenityContainer.appendChild(pill);
                amenityInput.value = '';
                updateAmenities();
            }
        });

        // Photo upload logic
        const uploadBtn = row.querySelector('.room-upload-btn');
        const fileInput = row.querySelector('input[type="file"]');
        const previewBox = row.querySelector('.room-preview-box');

        uploadBtn.addEventListener('click', () => fileInput.click());
        fileInput.addEventListener('change', () => {
            const files = Array.from(fileInput.files);
            if (files.length === 0) return;

            // Enterprise Feedback: Pulse and Progress
            uploadBtn.classList.add('pulse-upload');
            let progressWrapper = row.querySelector('.upload-progress-wrapper');
            if (!progressWrapper) {
                progressWrapper = document.createElement('div');
                progressWrapper.className = 'upload-progress-wrapper active';
                progressWrapper.innerHTML = '<div class="upload-progress-fill"></div>';
                uploadBtn.parentNode.insertBefore(progressWrapper, uploadBtn.nextSibling);
            } else {
                progressWrapper.classList.add('active');
            }

            const progressFill = progressWrapper.querySelector('.upload-progress-fill');
            progressFill.style.width = '0%';

            let loadedCount = 0;
            files.forEach(file => {
                const reader = new FileReader();

                // Simulate progress for smooth enterprisey feel
                let simulatedProgress = 0;
                const progressInterval = setInterval(() => {
                    simulatedProgress += 5;
                    if (simulatedProgress <= 90) progressFill.style.width = `${simulatedProgress}%`;
                }, 50);

                reader.onload = (e) => {
                    clearInterval(progressInterval);
                    const preview = document.createElement('div');
                    preview.className = 'preview-item card-look';
                    preview.innerHTML = `<img src="${e.target.result}"><div class="preview-remove"><i class="fas fa-times"></i></div>`;
                    preview.querySelector('.preview-remove').onclick = () => preview.remove();
                    previewBox.appendChild(preview);

                    loadedCount++;
                    if (loadedCount === files.length) {
                        progressFill.style.width = '100%';
                        setTimeout(() => {
                            uploadBtn.classList.remove('pulse-upload');
                            progressWrapper.classList.remove('active');
                            progressFill.style.width = '0%';
                        }, 500);
                    }
                };
                reader.readAsDataURL(file);
            });
        });

        roomIndex++;
    };

    if (addRoomBtn) addRoomBtn.addEventListener('click', addRoom);

    // Add first room by default
    if (roomList && roomList.children.length === 0) addRoom();
});
