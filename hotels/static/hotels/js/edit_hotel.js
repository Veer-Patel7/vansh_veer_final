/**
 * Master Editor Intelligence Protocol
 */

document.addEventListener('DOMContentLoaded', () => {

    try {

        /* ---------------- MAP SETUP ---------------- */
        const latInput = document.getElementById('lat');
        const lngInput = document.getElementById('lng');
        if (latInput && lngInput && typeof L !== "undefined") {
            const lat = parseFloat(latInput.value) || 20.5937;
            const lng = parseFloat(lngInput.value) || 78.9629;

            const map = L.map('edit-map').setView([lat, lng], 13);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '© OpenStreetMap'
            }).addTo(map);

            let marker = L.marker([lat, lng], { draggable: true }).addTo(map);

            marker.on('dragend', () => {
                const p = marker.getLatLng();
                latInput.value = p.lat.toFixed(6);
                lngInput.value = p.lng.toFixed(6);
            });
        }

        /* ---------------- SERVICES TOGGLE ---------------- */
        const servicesGrid = document.getElementById('servicesGrid');
        const servicesInput = document.getElementById('id_services');

        if (servicesGrid && servicesInput) {
            servicesGrid.addEventListener('click', (e) => {
                const item = e.target.closest('.pill-item');
                if (!item) return;

                item.classList.toggle('active');

                const active = Array.from(
                    servicesGrid.querySelectorAll('.pill-item.active')
                ).map(i => i.dataset.val);

                servicesInput.value = JSON.stringify(active);
            });
        }

        /* ---------------- MEDIA DELETE ---------------- */
        document.body.addEventListener('click', (e) => {

            const btn = e.target.closest('.photo-del-btn');
            if (!btn) return;

            try {
                const type = btn.dataset.type;
                const photoId = btn.dataset.id;
                const roomIdx = btn.dataset.roomIdx;

                const card = btn.closest('.media-item');
                const overlay = card?.querySelector('.photo-deleted-overlay');

                let targetInput;

                if (type === 'gallery') {
                    targetInput = document.getElementById('id_deleted_gallery_photos');
                } else {
                    targetInput = document.getElementById(`id_deleted_room_photos_${roomIdx}`);
                }

                if (!targetInput) return;

                let deletedIds = JSON.parse(targetInput.value || '[]');

                if (deletedIds.includes(parseInt(photoId))) {
                    deletedIds = deletedIds.filter(id => id !== parseInt(photoId));
                    if (overlay) overlay.style.opacity = '0';
                } else {
                    deletedIds.push(parseInt(photoId));
                    if (overlay) overlay.style.opacity = '1';
                }

                targetInput.value = JSON.stringify(deletedIds);

            } catch (err) {
                console.log("Media delete error:", err);
            }

        });

        /* ---------------- ADD ROOM CATEGORY ---------------- */
        const roomContainer = document.getElementById('roomContainer');

        window.addRoomCategory = () => {

            if (!roomContainer) return;

            const index = Date.now();

            const template = `
            <div class="room-card" data-idx="${index}">
                <div class="room-badge">New Category</div>
                <button type="button"
                class="remove-room-btn"
                onclick="this.closest('.room-card').remove()">✕</button>

                <div class="grid-12">

                    <div class="col-8 input-group">
                        <label>Room Name</label>
                        <input type="text" name="room_name_${index}" class="input-field" required>
                    </div>

                    <div class="col-4 input-group">
                        <label>Room Class</label>
                        <select name="room_type_${index}" class="input-field">
                            <option value="STANDARD">Standard</option>
                            <option value="DELUXE">Deluxe</option>
                            <option value="SUITE">Suite</option>
                            <option value="LUXURY">Luxury</option>
                        </select>
                    </div>

                    <div class="col-4 input-group">
                        <label>Guests</label>
                        <input type="number" name="room_guests_${index}" value="2" class="input-field">
                    </div>

                    <div class="col-4 input-group">
                        <label>Price</label>
                        <input type="number" name="room_price_${index}" value="2500" class="input-field">
                    </div>

                    <div class="col-4 input-group">
                        <label>Total Rooms</label>
                        <input type="number" name="room_count_${index}" value="5" class="input-field">
                    </div>

                </div>
            </div>
            `;

            roomContainer.insertAdjacentHTML('beforeend', template);

        };

        /* ---------------- AMENITY TOGGLE ---------------- */
        document.body.addEventListener('click', (e) => {

            const item = e.target.closest('.pill-item');
            if (!item) return;

            const parent = item.closest('.pill-box');
            const targetName = parent?.dataset.target;

            if (parent?.id === 'servicesGrid') return;

            if (targetName) {

                item.classList.toggle('active');

                const targetEl =
                    document.getElementById(`id_${targetName}`) ||
                    document.getElementsByName(targetName)[0];

                const activePills =
                    Array.from(parent.querySelectorAll('.pill-item.active'))
                        .map(i => i.dataset.val);

                if (targetEl)
                    targetEl.value = JSON.stringify(activePills);
            }

        });

        /* ---------------- SIDEBAR FINAL WORKING ---------------- */

        const container = document.querySelector('.master-editor-container');
        const navItems = document.querySelectorAll(".sidebar-nav-item");

        // CLICK
        navItems.forEach(item => {
            item.addEventListener("click", function () {

                const id = this.getAttribute("data-id");
                const section = document.getElementById(id);

                if (section && container) {
                    container.scrollTo({
                        top: section.offsetTop - 40,
                        behavior: "smooth"
                    });
                }

                navItems.forEach(i => i.classList.remove("active"));
                this.classList.add("active");
            });
        });

        // SCROLL (IMPORTANT FIX)
        if (container) {
            container.addEventListener("scroll", function () {

                let current = "";

                document.querySelectorAll(".editor-section").forEach(section => {

                    const sectionTop = section.offsetTop - 120;
                    const sectionHeight = section.offsetHeight;

                    if (
                        container.scrollTop >= sectionTop &&
                        container.scrollTop < sectionTop + sectionHeight
                    ) {
                        current = section.id;
                    }

                });

                navItems.forEach(item => {
                    item.classList.remove("active");

                    if (item.getAttribute("data-id") === current) {
                        item.classList.add("active");
                    }
                });

            });
        }
        

    } catch (e) {
        console.log("GLOBAL ERROR:", e);
    }

});