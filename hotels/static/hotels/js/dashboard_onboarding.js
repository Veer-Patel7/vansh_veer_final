let currentHotelId = null;
let currentCategory = null;
let currentData = null;

function getCsrfToken() {
    const cookie = document.cookie.split(';').find(c => c.trim().startsWith('csrftoken='));
    return cookie ? cookie.trim().split('=')[1] : '';
}

function handleOverlayClick(e) {
    if (e.target === document.getElementById('editModalOverlay')) closeModal();
}

function openEditInterface(hotelId, category) {
    currentHotelId = hotelId;
    currentCategory = category;
    document.getElementById('editModalOverlay').classList.add('active');

    const titles = { IDENTITY: 'Property Identity', INVENTORY: 'Room Inventory', GALLERY: 'Photo Gallery', OPS: 'Policies & Ops' };
    document.getElementById('modalTitle').textContent = titles[category] || category;

    document.getElementById('modalBody').innerHTML = `
    <div style="text-align: center; padding: 40px; color: var(--text-dim);">
        <i class="fas fa-spinner fa-spin" style="font-size: 2rem; margin-bottom: 15px;"></i>
        <p>Loading details...</p>
    </div>`;

    fetch(`/hotel/edit-detail/${hotelId}/${category}/`)
        .then(r => r.json())
        .then(res => {
            currentData = res.data;
            renderEditForm(category, res.data);
        })
        .catch(() => {
            document.getElementById('modalBody').innerHTML = `<p style="color:#ef4444; text-align:center;">Failed to load. Please try again.</p>`;
        });
}

function renderEditForm(category, data) {
    let html = '';

    if (category === 'IDENTITY') {
        html = `
    <div class="edit-field"><label>Hotel Name</label><input type="text" id="f_hotel_name" value="${data.hotel_name || ''}"></div>
    <div class="edit-field">
        <label>Property Type</label>
        <select id="f_hotel_type">
            <option value="HOTEL" ${data.hotel_type === 'HOTEL' ? 'selected' : ''}>Hotel</option>
            <option value="5_STAR" ${data.hotel_type === '5_STAR' ? 'selected' : ''}>5 Star Premium</option>
            <option value="4_STAR" ${data.hotel_type === '4_STAR' ? 'selected' : ''}>4 Star Luxury</option>
            <option value="3_STAR" ${data.hotel_type === '3_STAR' ? 'selected' : ''}>3 Star Business</option>
            <option value="RESORT" ${data.hotel_type === 'RESORT' ? 'selected' : ''}>Resort / Villa</option>
            <option value="VILLA" ${data.hotel_type === 'VILLA' ? 'selected' : ''}>Villa</option>
            <option value="GUESTHOUSE" ${data.hotel_type === 'GUESTHOUSE' ? 'selected' : ''}>Guest House</option>
            <option value="HOSTEL" ${data.hotel_type === 'HOSTEL' ? 'selected' : ''}>Hostel</option>
            <option value="OTHER" ${data.hotel_type === 'OTHER' ? 'selected' : ''}>Other</option>
        </select>
    </div>
    <div class="edit-field"><label>Description</label><textarea id="f_description" rows="3">${data.description || ''}</textarea></div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px;">
        <div class="edit-field"><label>City</label><input type="text" id="f_city" value="${data.city || ''}"></div>
        <div class="edit-field"><label>State</label><input type="text" id="f_state" value="${data.state || ''}"></div>
    </div>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px;">
        <div class="edit-field"><label>Pincode</label><input type="text" id="f_pincode" value="${data.pincode || ''}"></div>
    </div>
    <div class="edit-field"><label>Address</label><textarea id="f_address" rows="2">${data.address || ''}</textarea></div>
    <div style="background:#fefce8; border:1px solid #fde68a; border-radius:10px; padding:12px 16px; font-size:0.85rem; color:#92400e;">
        <i class="fas fa-info-circle"></i> Changes require Super Admin approval before going live.
    </div>`;
    } else if (category === 'INVENTORY') {
        if (!data.rooms || data.rooms.length === 0) {
            html = `<p style="text-align:center; color:var(--text-dim); padding:20px;">No rooms added yet.</p>`;
        } else {
            html = data.rooms.map((r, i) => `
            <div class="room-edit-card">
                <div style="font-weight:700; margin-bottom:12px; color:var(--primary);">
                    <i class="fas fa-bed" style="color:var(--secondary);"></i> ${r.name || r.type}
                </div>
                <div style="display:grid; grid-template-columns:1fr 1fr; gap:12px;">
                    <div class="edit-field"><label>Price / Night (₹)</label><input type="number" id="f_room_price_${i}" value="${r.price}" data-room-id="${r.id}"></div>
                    <div class="edit-field"><label>Max Guests</label><input type="number" id="f_room_guests_${i}" value="${r.guests}"></div>
                    <div class="edit-field"><label>Total Rooms</label><input type="number" id="f_room_count_${i}" value="${r.inventory}"></div>
                </div>
            </div>`).join('');
            html += `<div style="background:#fefce8; border:1px solid #fde68a; border-radius:10px; padding:12px 16px; font-size:0.85rem; color:#92400e;">
            <i class="fas fa-info-circle"></i> Changes require Super Admin approval before going live.
        </div>`;
        }
        document.getElementById('submitBtn').style.display = (!data.rooms || data.rooms.length === 0) ? 'none' : 'flex';
    } else if (category === 'GALLERY') {
        if (!data.images || data.images.length === 0) {
            html = `<p style="text-align:center; color:var(--text-dim); padding:20px;">No images uploaded yet.</p>`;
            document.getElementById('submitBtn').style.display = 'none';
        } else {
            html = `<p style="color:var(--text-dim); font-size:0.9rem; margin:0 0 15px;">Current gallery images (${data.images.length} total):</p>
        <div class="gallery-preview-grid">
            ${data.images.map(img => `<img src="${img.url}" class="${img.is_primary ? 'primary-img' : ''}" title="${img.is_primary ? 'Primary Image' : ''}">`).join('')}
        </div>
        <p style="margin-top:20px; color:var(--text-dim); font-size:0.85rem;"><i class="fas fa-info-circle"></i> To add/remove photos, submit a gallery change request via the form below.</p>
        <div class="edit-field" style="margin-top:10px;"><label>Change Request Description</label><textarea id="f_gallery_note" rows="3" placeholder="Describe what changes you'd like to make to the gallery..."></textarea></div>`;
        }
    } else if (category === 'OPS') {
        html = `
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:15px;">
        <div class="edit-field"><label>Check-In Time</label><input type="time" id="f_check_in" value="${data.check_in || '14:00'}"></div>
        <div class="edit-field"><label>Check-Out Time</label><input type="time" id="f_check_out" value="${data.check_out || '11:00'}"></div>
    </div>
    <div class="edit-field"><label>Cancellation Policy</label><textarea id="f_cancellation_policy" rows="4">${data.cancellation_policy || ''}</textarea></div>
    <div style="background:#fefce8; border:1px solid #fde68a; border-radius:10px; padding:12px 16px; font-size:0.85rem; color:#92400e;">
        <i class="fas fa-info-circle"></i> Changes require Super Admin approval before going live.
    </div>`;
    }

    document.getElementById('modalBody').innerHTML = html;
}

function collectFormData() {
    const d = {};
    if (currentCategory === 'IDENTITY') {
        d.hotel_name = document.getElementById('f_hotel_name').value;
        d.hotel_type = document.getElementById('f_hotel_type').value;
        d.description = document.getElementById('f_description').value;
        d.city = document.getElementById('f_city').value;
        d.state = document.getElementById('f_state').value;
        d.pincode = document.getElementById('f_pincode').value;
        d.address = document.getElementById('f_address').value;
    } else if (currentCategory === 'INVENTORY') {
        d.rooms = currentData.rooms.map((r, i) => ({
            id: r.id,
            price: document.getElementById(`f_room_price_${i}`)?.value,
            guests: document.getElementById(`f_room_guests_${i}`)?.value,
            inventory: document.getElementById(`f_room_count_${i}`)?.value,
        }));
    } else if (currentCategory === 'GALLERY') {
        d.note = document.getElementById('f_gallery_note')?.value;
    } else if (currentCategory === 'OPS') {
        d.check_in = document.getElementById('f_check_in').value;
        d.check_out = document.getElementById('f_check_out').value;
        d.cancellation_policy = document.getElementById('f_cancellation_policy').value;
    }
    return d;
}

function submitEditRequest() {
    const btn = document.getElementById('submitBtn');
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Submitting...';

    const payload = collectFormData();

    fetch(`/hotel/edit-submit/${currentHotelId}/${currentCategory}/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-CSRFToken': getCsrfToken() },
        body: JSON.stringify(payload)
    })
        .then(r => r.json())
        .then(res => {
            if (res.status === 'success') {
                document.getElementById('modalBody').innerHTML = `
            <div style="text-align:center; padding: 40px;">
                <div style="width:70px; height:70px; background:rgba(34,197,94,0.1); border-radius:50%; display:flex; align-items:center; justify-content:center; margin:0 auto 20px; font-size:2rem; color:#22c55e;">
                    <i class="fas fa-check"></i>
                </div>
                <h3 style="margin:0 0 10px;">Request Submitted!</h3>
                <p style="color:var(--text-dim);">Your change request has been sent to the Super Admin for review. You'll be notified once it's approved.</p>
            </div>`;
                document.getElementById('modalFooter').innerHTML = `
            <button onclick="closeModal()" class="btn btn-primary" style="padding: 12px 32px; border-radius: 8px; background: var(--secondary); border: none; color: var(--primary); cursor: pointer; font-weight: 700; font-family: inherit; width: 100%;">
                Done
            </button>`;
            } else {
                btn.disabled = false;
                btn.innerHTML = '<i class="fas fa-paper-plane"></i> Request Update';
                alert('Submission failed. Please try again.');
            }
        })
        .catch(() => {
            btn.disabled = false;
            btn.innerHTML = '<i class="fas fa-paper-plane"></i> Request Update';
            alert('Network error. Please try again.');
        });
}

function closeModal() {
    document.getElementById('editModalOverlay').classList.remove('active');
    currentHotelId = null;
    currentCategory = null;
    currentData = null;
    document.getElementById('submitBtn').style.display = 'flex';
    document.getElementById('submitBtn').disabled = false;
    document.getElementById('submitBtn').innerHTML = '<i class="fas fa-paper-plane"></i> Request Update';
}

document.addEventListener('DOMContentLoaded', () => {
    const fill = document.getElementById('progressFill');
    if (fill) {
        fill.style.width = fill.dataset.progress + '%';
    }
});
