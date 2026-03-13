document.addEventListener('DOMContentLoaded', () => {
    console.log('[Dropdown] Global listener initialized.');

    // --- Updated Property Categories (Step 1) ---
    const INITIAL_TYPES = [
        // Standard Classifications
        { id: '5_STAR', label: '5 Star Premium', icon: 'fas fa-star', color: '#fbbf24' },
        { id: '4_STAR', label: '4 Star Luxury', icon: 'fas fa-star', color: '#fbbf24' },
        { id: '3_STAR', label: '3 Star Business', icon: 'fas fa-star', color: '#fbbf24' },
        { id: 'RESORT', label: 'Resort / Villa', icon: 'fas fa-umbrella-beach', color: 'var(--secondary)' },
        // Common
        { id: 'HOTEL', label: 'Hotel', icon: 'fas fa-hotel' },
        { id: 'BOUTIQUE', label: 'Boutique Hotel', icon: 'fas fa-gem' },
        { id: 'BUSINESS', label: 'Business Hotel', icon: 'fas fa-briefcase' },
        { id: 'BUDGET', label: 'Budget Hotel', icon: 'fas fa-wallet' },
        { id: 'LUXURY', label: 'Luxury Hotel', icon: 'fas fa-crown' },
        { id: 'HERITAGE', label: 'Heritage Hotel', icon: 'fas fa-landmark' },
        { id: 'AIRPORT', label: 'Airport Hotel', icon: 'fas fa-plane-arrival' },
        { id: 'BEACH_RESORT', label: 'Beach Resort', icon: 'fas fa-sun' },
        { id: 'HILL_RESORT', label: 'Hill Resort', icon: 'fas fa-mountain' },
        { id: 'SERVICED_APT', label: 'Serviced Apartments', icon: 'fas fa-building-user' },
        { id: 'VACATION_RENTAL', label: 'Vacation Rentals', icon: 'fas fa-house-chimney-window' },
        { id: 'HOMESTAY', label: 'Homestay', icon: 'fas fa-house-user' },
        { id: 'GUEST_HOUSE', label: 'Guest House', icon: 'fas fa-bed' },
        { id: 'HOSTEL', label: 'Hostel', icon: 'fas fa-users-rectangle' },
        { id: 'LODGE', label: 'Lodge', icon: 'fas fa-tree' },
        { id: 'MOTEL', label: 'Motel', icon: 'fas fa-car' },
        { id: 'VILLA', label: 'Villa', icon: 'fas fa-house-chimney' },
        { id: 'ECO_RESORT', label: 'Eco Resort', icon: 'fas fa-leaf' },
        { id: 'WELLNESS', label: 'Wellness Retreat', icon: 'fas fa-spa' },
        // Premium
        { id: 'PALACE', label: 'Palace Hotel', icon: 'fas fa-university' },
        { id: 'CASINO', label: 'Casino Resort', icon: 'fas fa-dice' },
        { id: 'SPA_RESORT', label: 'Spa Resort', icon: 'fas fa-hot-tub-person' },
        { id: 'GOLF_RESORT', label: 'Golf Resort', icon: 'fas fa-golf-ball-tee' },
        { id: 'SKI_RESORT', label: 'Ski Resort', icon: 'fas fa-person-skiing' },
        { id: 'DESERT_CAMP', label: 'Desert Camp', icon: 'fas fa-tent' },
        { id: 'HOUSEBOAT', label: 'Houseboat', icon: 'fas fa-ship' },
        { id: 'FARM_STAY', label: 'Farm Stay', icon: 'fas fa-tractor' }
    ];

    // --- Room Class & Category Mappings (Step 2) ---
    const ROOM_VARIANTS = {
        'STANDARD': ['Standard Room', 'Standard City View', 'Standard Garden View', 'Standard Pool View', 'Standard Twin Room', 'Standard Double Room'],
        'DELUXE': ['Deluxe Room', 'Deluxe Garden View', 'Deluxe Sea View', 'Deluxe Pool View', 'Deluxe Balcony Room', 'Deluxe King Room', 'Deluxe Twin Room'],
        'SUITE': ['Junior Suite', 'Executive Suite', 'Family Suite', 'Honeymoon Suite', 'Duplex Suite', 'Penthouse Suite'],
        'LUXURY': ['Luxury Room', 'Luxury Suite', 'Presidential Suite', 'Royal Suite', 'Maharaja Suite', 'Imperial Suite'],
        'ECONOMY': ['Economy Room', 'Single Room', 'Small Double'],
        'PREMIUM': ['Premium Room', 'Premium City View', 'Premium Balcony'],
        'EXECUTIVE': ['Executive Room', 'Executive Club Room', 'Business Suite'],
        'CLUB': ['Club Room', 'Club Deluxe', 'Executive Club'],
        'PRESIDENTIAL': ['Presidential Suite', 'Grand Presidential', 'Penthouse Presidential'],
        'ROYAL': ['Royal Suite', 'Royal King Suite', 'Palace Suite'],
        'FAMILY': ['Family Room', 'Family Suite', 'Family Interconnecting'],
        'SPECIALTY': ['Studio Room', 'Connecting Rooms', 'Accessible Room', 'Pet-Friendly Room', 'Smoking Room', 'Non-Smoking Room']
    };

    const GUEST_DEFAULTS = {
        'STANDARD': 2, 'DELUXE': 3, 'SUITE': 4, 'LUXURY': 4, 'ECONOMY': 1,
        'PREMIUM': 2, 'EXECUTIVE': 2, 'CLUB': 2, 'PRESIDENTIAL': 6, 'ROYAL': 6, 'FAMILY': 6
    };

    const AMENITY_SUGGESTIONS = {
        'STANDARD': ['Free WiFi', 'Air Conditioning', 'Smart TV', 'Mini Fridge', 'Work Desk', 'Tea/Coffee Maker'],
        'DELUXE': ['Bathtub', 'Balcony', 'Sea View', 'Rain Shower', 'Premium Toiletries', 'Sofa Seating'],
        'LUXURY': ['Private Pool', 'Jacuzzi', 'Butler Service', 'Private Lounge Access', 'Walk-in Closet', 'Dining Area'],
        'SUITE': ['Living Room', 'Powder Room', 'Pantry', 'Walk-in Closet', 'City View']
    };

    const CLASS_METADATA = {
        'STANDARD': { icon: 'fas fa-bed', color: '#fbbf24' },
        'DELUXE': { icon: 'fas fa-crown', color: '#fbbf24' },
        'SUITE': { icon: 'fas fa-couch', color: '#fbbf24' },
        'LUXURY': { icon: 'fas fa-gem', color: '#fbbf24' },
        'ECONOMY': { icon: 'fas fa-wallet', color: 'var(--text-muted)' },
        'PREMIUM': { icon: 'fas fa-star', color: '#fbbf24' },
        'EXECUTIVE': { icon: 'fas fa-briefcase', color: '#fbbf24' },
        'CLUB': { icon: 'fas fa-key', color: '#fbbf24' },
        'PRESIDENTIAL': { icon: 'fas fa-medal', color: '#fbbf24' },
        'ROYAL': { icon: 'fas fa-landmark', color: '#fbbf24' },
        'FAMILY': { icon: 'fas fa-people-roof', color: '#fbbf24' },
        'SPECIALTY': { icon: 'fas fa-shapes', color: '#fbbf24' },
        'CUSTOM': { icon: 'fas fa-plus-circle', color: '#fbbf24' }
    };

    // Load from storage or initialize with defaults
    let allTypes = JSON.parse(localStorage.getItem('hotepro_property_types'));
    // Always force defaults to be available, but keep custom ones?
    // Let's just reset to defaults if it's the first time we're seeing this expanded list
    if (!allTypes || allTypes.length < 34) {
        allTypes = INITIAL_TYPES;
        localStorage.setItem('hotepro_property_types', JSON.stringify(allTypes));
    }

    const renderDropdownItems = () => {
        const list = document.getElementById('property-type-items');
        if (!list) return;

        let html = '';
        allTypes.forEach((t, index) => {
            const isDefault = INITIAL_TYPES.some(it => it.id === t.id);
            const color = t.color || 'var(--secondary)';

            // Group items into a wrapper
            html += `
                <div class="select-item-wrapper">
                    <div class="select-item" data-value="${t.id}">
                        <div class="item-icon-box">
                            <i class="${t.icon}" style="color:${color};"></i>
                        </div>
                        <span class="item-text">${t.label}</span>
                    </div>
                    ${!isDefault ? `
                        <div class="inline-actions">
                            <button class="inline-edit-btn property-type-edit" data-index="${index}" title="Edit"><i class="fas fa-pen"></i></button>
                            <button class="inline-delete-btn property-type-delete" data-index="${index}" title="Remove"><i class="fas fa-times"></i></button>
                        </div>
                    ` : ''}
                </div>`;
        });

        html += `
            <div class="select-item manage-types-btn" id="manage-types-trigger" data-value="OTHER">
                <div class="item-icon-box">
                    <i class="fas fa-ellipsis" style="color:var(--text-muted);"></i>
                </div>
                <span class="item-text">Other Property</span>
            </div>`;

        list.innerHTML = html;

        // Synchronize display text
        const customTypeSelect = document.getElementById('customTypeSelect');
        if (customTypeSelect) {
            const targetId = customTypeSelect.dataset.target;
            const hidden = document.getElementById(targetId);
            if (hidden && hidden.value) {
                const selectedType = allTypes.find(t => t.id === hidden.value);
                const textEl = customTypeSelect.querySelector('.selected-text');

                if (selectedType) {
                    const color = selectedType.color || 'var(--secondary)';
                    if (textEl) {
                        textEl.innerHTML = `
                            <div class="item-icon-box">
                                <i class="${selectedType.icon}" style="color:${color};"></i>
                            </div>
                            <span class="item-text text-truncate">${selectedType.label}</span>
                        `;
                    }
                } else {
                    if (textEl) textEl.innerHTML = 'Select Category';
                    hidden.value = '';
                    hidden.dispatchEvent(new Event('change'));
                }
            }
        }
    };

    // --- Room Custom Management ---
    let customRoomClasses = JSON.parse(localStorage.getItem('hotepro_custom_classes')) || [];
    let customRoomVariants = JSON.parse(localStorage.getItem('hotepro_custom_variants')) || {};

    window.updateRoomCategoryOptions = (row) => {
        const classVal = row.querySelector('input[name^="room_type"], select[name^="room_type"]').value;
        const catSelectContainer = row.querySelector('.category-name-select-container');
        if (!catSelectContainer) return;

        const baseVariants = ROOM_VARIANTS[classVal] || ROOM_VARIANTS['STANDARD'] || [];
        const customVariants = customRoomVariants[classVal] || [];
        const list = catSelectContainer.querySelector('.select-items');
        const meta = CLASS_METADATA[classVal] || CLASS_METADATA['STANDARD'];

        let html = '';
        baseVariants.forEach((v, idx) => {
            const isBase = idx === 0;
            const extraStyle = isBase ? `color: ${meta.color}; font-weight: 800;` : '';
            html += `
                <div class="select-item" data-value="${v}" style="${extraStyle}">
                    <div class="item-icon-box">
                        <i class="${meta.icon}" style="color:${meta.color};"></i>
                    </div>
                    <span class="item-text">${v}</span>
                </div>`;
        });

        customVariants.forEach((v, idx) => {
            html += `
                <div class="select-item-wrapper">
                    <div class="select-item" data-value="${v}">
                        <div class="item-icon-box">
                            <i class="${meta.icon}" style="color:${meta.color};"></i>
                        </div>
                        <span class="item-text">${v}</span>
                    </div>
                    <div class="inline-actions">
                        <button class="inline-edit-btn room-variant-edit" data-class="${classVal}" data-index="${idx}" title="Edit"><i class="fas fa-pen"></i></button>
                        <button class="inline-delete-btn room-variant-delete" data-class="${classVal}" data-index="${idx}" title="Remove"><i class="fas fa-times"></i></button>
                    </div>
                </div>`;
        });

        // Add "Other Category..." trigger with manage-types-btn style
        html += `
            <div class="select-item manage-types-btn custom-cat-trigger" data-value="OTHER">
                <div class="item-icon-box">
                    <i class="fas fa-ellipsis" style="color:var(--text-muted);"></i>
                </div>
                <span class="item-text">+ Other Category...</span>
            </div>`;
        list.innerHTML = html;

        // Auto-populate Max Guests if not manually changed
        const guestInput = row.querySelector('input[name^="room_guests"]');
        if (guestInput) {
            guestInput.value = GUEST_DEFAULTS[classVal] || 2;
        }

        // Auto-suggest Amenities (Elite Feature)
        const amenityContainer = row.querySelector('.dynamic-pills-container');
        if (amenityContainer && AMENITY_SUGGESTIONS[classVal]) {
            // Only add if container is empty or we want to overwrite
            const currentPills = amenityContainer.querySelectorAll('.pill-label');
            if (currentPills.length === 0) {
                AMENITY_SUGGESTIONS[classVal].forEach(amenity => {
                    const label = document.createElement('label');
                    label.className = 'pill-label';
                    label.innerHTML = `
                        <input type="checkbox" value="${amenity}" checked style="display:none;">
                        <i class="fas fa-check-circle" style="color:var(--secondary);"></i>
                        ${amenity}
                    `;
                    amenityContainer.appendChild(label);
                });
                // Trigger hidden field update if available
                const hiddenAmenities = row.querySelector('input[name^="room_amenities"]');
                if (hiddenAmenities) {
                    const pills = AMENITY_SUGGESTIONS[classVal];
                    hiddenAmenities.value = JSON.stringify(pills);
                }
            }
        }
    };

    window.updateRoomClassOptions = (container) => {
        const list = container.querySelector('.select-items');
        if (!list) return;

        const standardClasses = Object.keys(CLASS_METADATA).filter(k => k !== 'CUSTOM');

        let html = '';
        standardClasses.forEach(c => {
            const meta = CLASS_METADATA[c];
            html += `
                <div class="select-item" data-value="${c}">
                    <div class="item-icon-box">
                        <i class="${meta.icon}" style="color:${meta.color};"></i>
                    </div>
                    <span class="item-text">${c.charAt(0) + c.slice(1).toLowerCase()}</span>
                </div>`;
        });

        customRoomClasses.forEach((c, idx) => {
            const meta = CLASS_METADATA['CUSTOM'];
            html += `
                <div class="select-item-wrapper">
                    <div class="select-item" data-value="${c}">
                        <div class="item-icon-box">
                            <i class="${meta.icon}" style="color:${meta.color};"></i>
                        </div>
                        <span class="item-text">${c}</span>
                    </div>
                    <div class="inline-actions">
                        <button class="inline-edit-btn room-class-edit" data-index="${idx}" title="Edit"><i class="fas fa-pen"></i></button>
                        <button class="inline-delete-btn room-class-delete" data-index="${idx}" title="Remove"><i class="fas fa-times"></i></button>
                    </div>
                </div>`;
        });

        html += `
            <div class="select-item manage-types-btn custom-class-trigger" data-value="CUSTOM">
                <div class="item-icon-box">
                    <i class="fas fa-ellipsis" style="color:var(--text-muted);"></i>
                </div>
                <span class="item-text">+ Add Custom Class...</span>
            </div>`;
        list.innerHTML = html;
    };

    // --- Room Manager Modal Logic ---
    let currentRoomContext = null; // { type: 'class' | 'category', classVal?: string, container?: element }
    let editingRoomIndex = null; // Tracks index of the custom entry being edited

    window.openRoomManager = (type, classVal = null, container = null) => {
        currentRoomContext = { type, classVal, container };
        editingRoomIndex = null; // Reset edit mode
        const popup = document.getElementById('roomManagerPopup');
        const title = document.getElementById('roomManagerTitle');
        const formTitle = document.getElementById('roomFormTitle');
        const listTitle = document.getElementById('roomManagerListTitle');
        const saveBtn = document.getElementById('save-room-type-btn');
        const labelInput = document.getElementById('room-type-label');

        if (!popup) return;
        if (labelInput) labelInput.value = ''; // Clear input

        if (type === 'class') {
            title.innerHTML = '<i class="fas fa-layer-group"></i> Room Tier Registry';
            formTitle.innerText = 'Add New Room Tier';
            listTitle.innerHTML = '<i class="fas fa-list-check"></i> Current Tiers';
            saveBtn.innerHTML = 'Save Room Classification <i class="fas fa-check-circle"></i>';
        } else {
            title.innerHTML = `<i class="fas fa-tag"></i> ${classVal} Categories`;
            formTitle.innerText = `New ${classVal} Category`;
            listTitle.innerHTML = '<i class="fas fa-list-check"></i> Existing Variants';
            saveBtn.innerHTML = 'Save Category Variant <i class="fas fa-check-circle"></i>';
        }

        renderRoomManagerList();
        popup.style.display = 'flex';
    };

    const renderRoomManagerList = () => {
        const list = document.getElementById('room-manager-list');
        if (!list || !currentRoomContext) return;

        const { type, classVal } = currentRoomContext;
        let html = '';

        if (type === 'class') {
            // Show Standard Classes first
            const standardClasses = Object.keys(CLASS_METADATA).filter(k => k !== 'CUSTOM');
            standardClasses.forEach(c => {
                const meta = CLASS_METADATA[c];
                html += `
                    <div class="management-item is-default">
                        <div class="icon-plate">
                            <i class="${meta.icon}" style="color:${meta.color};"></i>
                        </div>
                        <div class="item-info">
                            <span>${c.charAt(0) + c.slice(1).toLowerCase()}</span>
                        </div>
                    </div>`;
            });

            // Show Custom Classes
            customRoomClasses.forEach((c, index) => {
                const meta = CLASS_METADATA['CUSTOM'];
                html += `
                    <div class="management-item">
                        <div class="item-actions">
                            <button class="action-btn edit-btn" onclick="editRoomCustom(${index})" title="Edit"><i class="fas fa-pen"></i></button>
                            <button class="action-btn delete-btn" onclick="deleteRoomCustom(${index})" title="Delete"><i class="fas fa-trash"></i></button>
                        </div>
                        <div class="icon-plate">
                            <i class="${meta.icon}" style="color:${meta.color};"></i>
                        </div>
                        <div class="item-info">
                            <span>${c}</span>
                        </div>
                    </div>`;
            });
        } else {
            // Show Standard Variants
            const standardVariants = ROOM_VARIANTS[classVal] || ROOM_VARIANTS['STANDARD'] || [];
            const meta = CLASS_METADATA[classVal] || CLASS_METADATA['STANDARD'];
            standardVariants.forEach(v => {
                html += `
                    <div class="management-item is-default">
                        <div class="icon-plate">
                            <i class="${meta.icon}" style="color:${meta.color};"></i>
                        </div>
                        <div class="item-info">
                            <span>${v}</span>
                        </div>
                    </div>`;
            });

            // Show Custom Variants
            const customVariants = customRoomVariants[classVal] || [];
            customVariants.forEach((v, index) => {
                html += `
                    <div class="management-item">
                        <div class="item-actions">
                            <button class="action-btn edit-btn" onclick="editRoomCustom(${index})" title="Edit"><i class="fas fa-pen"></i></button>
                            <button class="action-btn delete-btn" onclick="deleteRoomCustom(${index})" title="Delete"><i class="fas fa-trash"></i></button>
                        </div>
                        <div class="icon-plate">
                            <i class="${meta.icon}" style="color:${meta.color};"></i>
                        </div>
                        <div class="item-info">
                            <span>${v}</span>
                        </div>
                    </div>`;
            });
        }

        list.innerHTML = html;
    };

    window.editRoomCustom = (index) => {
        editingRoomIndex = index;
        const items = (currentRoomContext.type === 'class') ? customRoomClasses : (customRoomVariants[currentRoomContext.classVal] || []);
        const labelInput = document.getElementById('room-type-label');
        const saveBtn = document.getElementById('save-room-type-btn');
        if (labelInput) labelInput.value = items[index];
        if (saveBtn) saveBtn.innerHTML = 'Update Entry <i class="fas fa-check-circle"></i>';
    };

    window.deleteRoomCustom = (index) => {
        if (!currentRoomContext) return;
        if (confirm('Permanently remove this custom entry?')) {
            if (currentRoomContext.type === 'class') {
                customRoomClasses.splice(index, 1);
                localStorage.setItem('hotepro_custom_classes', JSON.stringify(customRoomClasses));
            } else {
                customRoomVariants[currentRoomContext.classVal].splice(index, 1);
                localStorage.setItem('hotepro_custom_variants', JSON.stringify(customRoomVariants));
            }
            renderRoomManagerList();
            // Refresh relevant dropdowns
            if (currentRoomContext.container) {
                if (currentRoomContext.type === 'class') window.updateRoomClassOptions(currentRoomContext.container);
                else {
                    const row = currentRoomContext.container.closest('.room-card-elite');
                    if (row) window.updateRoomCategoryOptions(row);
                }
            }
        }
    };

    const renderManagementList = () => {
        const list = document.getElementById('type-list');
        if (!list) return;

        let html = '';
        allTypes.forEach((t, index) => {
            // Harder check for default items: check ID against initial list IDs
            const isDefault = INITIAL_TYPES.some(it => it.id === t.id);
            const color = t.color || 'var(--secondary)';
            html += `
                <div class="management-item ${isDefault ? 'is-default' : ''}">
                    ${!isDefault ? `
                    <div class="item-actions">
                        <button class="action-btn edit-btn" onclick="editType(${index})" title="Edit"><i class="fas fa-pen"></i></button>
                        <button class="action-btn delete-btn" onclick="deleteType(${index})" title="Delete"><i class="fas fa-trash"></i></button>
                    </div>` : ''}
                    <div class="icon-plate">
                        <i class="${t.icon}" style="color:${color};"></i>
                    </div>
                    <div class="item-info">
                        <span>${t.label}</span>
                    </div>
                </div>
            `;
        });
        list.innerHTML = html;
    };

    window.saveTypes = () => {
        localStorage.setItem('hotepro_property_types', JSON.stringify(allTypes));
        renderDropdownItems();
        renderManagementList();
    };

    window.editType = (index) => {
        const type = allTypes[index];
        const labelInput = document.getElementById('new-type-label');
        const iconInput = document.getElementById('new-type-icon');
        const addBtn = document.getElementById('add-type-btn');

        if (labelInput) labelInput.value = type.label;
        if (iconInput) iconInput.value = type.icon;
        if (addBtn) {
            addBtn.innerText = 'Update Classification';
            addBtn.dataset.editIndex = index;
        }

        // Scroll to form
        if (labelInput) labelInput.focus();
    };

    window.deleteType = (index) => {
        if (confirm('Permanently remove this classification?')) {
            allTypes.splice(index, 1);
            saveTypes();
        }
    };

    // Initial Render
    renderDropdownItems();

    // --- Event Listeners ---
    document.addEventListener('click', (e) => {
        const container = e.target.closest('.custom-select-container');
        const selected = e.target.closest('.select-selected');
        const item = e.target.closest('.select-item');
        const deleteBtn = e.target.closest('.inline-delete-btn');
        const editBtn = e.target.closest('.inline-edit-btn');

        // Handle inline editing
        if (editBtn) {
            e.stopPropagation();
            const index = parseInt(editBtn.dataset.index);
            if (editBtn.classList.contains('room-class-edit')) {
                window.openRoomManager('class', null, container);
                window.editRoomCustom(index);
            } else if (editBtn.classList.contains('room-variant-edit')) {
                const classVal = editBtn.dataset.class;
                window.openRoomManager('category', classVal, container);
                window.editRoomCustom(index);
            } else if (editBtn.classList.contains('property-type-edit')) {
                const popup = document.getElementById('typeManagerPopup');
                if (popup) {
                    popup.style.display = 'flex';
                    renderManagementList();
                    window.editType(index);
                }
            }
            return;
        }

        // Handle inline deletion
        if (deleteBtn) {
            e.stopPropagation();
            const index = deleteBtn.dataset.index;

            if (deleteBtn.classList.contains('room-class-delete')) {
                if (confirm('Remove this custom room class?')) {
                    customRoomClasses.splice(index, 1);
                    localStorage.setItem('hotepro_custom_classes', JSON.stringify(customRoomClasses));
                    window.updateRoomClassOptions(container);
                }
            } else if (deleteBtn.classList.contains('room-variant-delete')) {
                const classVal = deleteBtn.dataset.class;
                if (confirm('Remove this custom category?')) {
                    customRoomVariants[classVal].splice(index, 1);
                    localStorage.setItem('hotepro_custom_variants', JSON.stringify(customRoomVariants));
                    const row = container.closest('.room-card-elite') || container.closest('.room-row');
                    if (row) window.updateRoomCategoryOptions(row);
                }
            } else if (confirm('Remove this custom classification?')) {
                allTypes.splice(index, 1);
                window.saveTypes();
            }
            return;
        }

        // Toggle Type Manager Modal (Step 1)
        if (item && item.id === 'manage-types-trigger') {
            const popup = document.getElementById('typeManagerPopup');
            if (popup) {
                popup.style.display = 'flex';
                renderManagementList();
            }
            if (container) {
                const items = container.querySelector('.select-items');
                if (items) items.classList.remove('show');
            }
            return;
        }

        // Toggle Room Manager Modal (Step 2)
        if (item && item.classList.contains('custom-cat-trigger')) {
            const row = container.closest('.room-card-elite') || container.closest('.room-row');
            const classVal = row ? row.querySelector('input[name^="room_type"], select[name^="room_type"]').value : 'STANDARD';
            window.openRoomManager('category', classVal, container);
            if (container.querySelector('.select-items')) container.querySelector('.select-items').classList.remove('show');
            return;
        }

        if (item && item.classList.contains('custom-class-trigger')) {
            window.openRoomManager('class', null, container);
            if (container.querySelector('.select-items')) container.querySelector('.select-items').classList.remove('show');
            return;
        }

        // Close dropdowns
        if (!container) {
            document.querySelectorAll('.select-items.show').forEach(items => items.classList.remove('show'));
            document.querySelectorAll('.select-selected.active').forEach(s => s.classList.remove('active'));
            return;
        }

        // Toggle dropdown
        if (selected) {
            const items = container.querySelector('.select-items');
            if (items) {
                // Pre-populate room class options if it's a room-class container
                if (container.classList.contains('room-class-select-container')) {
                    window.updateRoomClassOptions(container);
                }
                items.classList.toggle('show');
            }
            selected.classList.toggle('active');
        }

        // Handle selection
        if (item && !item.classList.contains('manage-types-btn')) {
            const val = item.dataset.value;
            const text = item.innerHTML;

            const targetId = container.dataset.target;
            const hidden = document.getElementById(targetId);
            const textEl = container.querySelector('.selected-text');

            // If it's a room category or class, try to preserve icon in selection display
            if (container.classList.contains('category-name-select-container') || container.classList.contains('room-class-select-container')) {
                if (textEl) textEl.innerHTML = text; // 'text' already contains the <i> from item.innerHTML
            } else {
                if (textEl) textEl.innerHTML = text;
            }

            if (hidden) { hidden.value = val; hidden.dispatchEvent(new Event('change')); }

            if (container.querySelector('.select-items')) container.querySelector('.select-items').classList.remove('show');
            if (container.querySelector('.select-selected')) container.querySelector('.select-selected').classList.remove('active');

            // Trigger dependency updates (like Max Guests)
            const row = container.closest('.room-card-elite') || container.closest('.room-row');
            if (row && container.dataset.target.includes('room_type')) {
                window.updateRoomCategoryOptions(row);
            }
        }
    });

    // Add/Update Type (Step 1)
    const addBtn = document.getElementById('add-type-btn');
    if (addBtn) {
        addBtn.addEventListener('click', () => {
            const labelInput = document.getElementById('new-type-label');
            const iconInput = document.getElementById('new-type-icon');
            const label = labelInput.value.trim();
            const icon = iconInput.value.trim() || 'fas fa-hotel';
            const editIndex = addBtn.dataset.editIndex;

            if (!label) return alert('Please enter a classification label.');

            if (editIndex !== undefined) {
                allTypes[editIndex] = { id: label.toUpperCase().replace(/\s/g, '_'), label, icon, color: allTypes[editIndex].color };
                delete addBtn.dataset.editIndex;
                addBtn.innerText = 'Save Classification';
            } else {
                allTypes.push({ id: label.toUpperCase().replace(/\s/g, '_'), label, icon });
            }

            labelInput.value = ''; iconInput.value = ''; saveTypes();
        });
    }

    // Room Save Classification (Step 2)
    const saveRoomBtn = document.getElementById('save-room-type-btn');
    if (saveRoomBtn) {
        saveRoomBtn.addEventListener('click', () => {
            const labelInput = document.getElementById('room-type-label');
            const label = labelInput.value.trim();
            if (!label || !currentRoomContext) return alert('Please enter a label.');

            if (editingRoomIndex !== null) {
                // Update existing
                if (currentRoomContext.type === 'class') {
                    customRoomClasses[editingRoomIndex] = label;
                    localStorage.setItem('hotepro_custom_classes', JSON.stringify(customRoomClasses));
                    if (currentRoomContext.container) window.updateRoomClassOptions(currentRoomContext.container);
                } else {
                    const cv = currentRoomContext.classVal;
                    customRoomVariants[cv][editingRoomIndex] = label;
                    localStorage.setItem('hotepro_custom_variants', JSON.stringify(customRoomVariants));
                    if (currentRoomContext.container) {
                        const row = currentRoomContext.container.closest('.room-card-elite') || currentRoomContext.container.closest('.room-row');
                        if (row) window.updateRoomCategoryOptions(row);
                    }
                }
                editingRoomIndex = null;
                saveRoomBtn.innerHTML = (currentRoomContext.type === 'class') ? 'Save Room Classification <i class="fas fa-check-circle"></i>' : 'Save Category Variant <i class="fas fa-check-circle"></i>';
            } else {
                // Add new
                if (currentRoomContext.type === 'class') {
                    if (!customRoomClasses.includes(label)) {
                        customRoomClasses.push(label);
                        localStorage.setItem('hotepro_custom_classes', JSON.stringify(customRoomClasses));
                    }
                    if (currentRoomContext.container) window.updateRoomClassOptions(currentRoomContext.container);
                } else {
                    const cv = currentRoomContext.classVal;
                    if (!customRoomVariants[cv]) customRoomVariants[cv] = [];
                    if (!customRoomVariants[cv].includes(label)) {
                        customRoomVariants[cv].push(label);
                        localStorage.setItem('hotepro_custom_variants', JSON.stringify(customRoomVariants));
                    }
                    if (currentRoomContext.container) {
                        const row = currentRoomContext.container.closest('.room-card-elite') || currentRoomContext.container.closest('.room-row');
                        if (row) window.updateRoomCategoryOptions(row);
                    }
                }
            }

            labelInput.value = '';
            renderRoomManagerList();
        });
    }

    // Modal Closing
    const closeBtn = document.getElementById('close-type-manager-btn');
    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            const popup = document.getElementById('typeManagerPopup');
            if (popup) popup.style.display = 'none';
        });
    }

    const closeRoomBtn = document.getElementById('close-room-manager-btn');
    if (closeRoomBtn) {
        closeRoomBtn.addEventListener('click', () => {
            const popup = document.getElementById('roomManagerPopup');
            if (popup) popup.style.display = 'none';
        });
    }

    // Keyboard Accessibility
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            document.querySelectorAll('.select-items').forEach(items => items.classList.remove('show'));
            document.querySelectorAll('.select-selected').forEach(s => s.classList.remove('active'));
            const p1 = document.getElementById('typeManagerPopup'); if (p1) p1.style.display = 'none';
            const p2 = document.getElementById('roomManagerPopup'); if (p2) p2.style.display = 'none';
        }
    });
});
