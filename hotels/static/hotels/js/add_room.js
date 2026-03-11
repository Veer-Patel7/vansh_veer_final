document.addEventListener('DOMContentLoaded', () => {
    // 1. Selector Handshake
    const form = document.getElementById('room_form');
    const amenitiesHidden = document.getElementById('amenities_hidden');
    const uploadZone = document.getElementById('roomUploadZone');
    const mediaInput = document.getElementById('roomMediaInput');
    const previewContainer = document.getElementById('roomMediaPreview');
    
    const customInput = document.getElementById('custom_amenity_input');
    const addBtn = document.getElementById('add_custom_amenity_btn');
    const tagsContainer = document.getElementById('custom_tags_container');
    const tagsCountDisplay = document.getElementById('custom_tags_count');

    // 2. State & Persistence
    let customAmenities = [];

    // 3. Central Amenities Controller
    const addTag = (text) => {
        if (typeof text !== 'string') return;
        text = text.trim();
        
        // Validation: Empty or Duplicate
        if (!text || customAmenities.includes(text)) return;

        customAmenities.push(text);
        syncAndRender();
    };

    const removeTag = (text) => {
        customAmenities = customAmenities.filter(t => t !== text);
        syncAndRender();
    };

    const syncAndRender = () => {
        // Update Counter
        if (tagsCountDisplay) {
            tagsCountDisplay.textContent = `${customAmenities.length} ADDED`;
            tagsCountDisplay.classList.add('animate-pulse');
            setTimeout(() => tagsCountDisplay.classList.remove('animate-pulse'), 1000);
        }

        // Render Tags UI
        if (!tagsContainer) return;
        
        if (customAmenities.length === 0) {
            tagsContainer.innerHTML = '<div class="text-[11px] font-medium text-slate-400 italic">No custom amenities added yet...</div>';
        } else {
            tagsContainer.innerHTML = '';
            customAmenities.forEach(text => {
                const tag = document.createElement('div');
                tag.className = 'elite-tag group';
                tag.innerHTML = `
                    <span>${text}</span>
                    <i class="fas fa-times remove-tag ml-2 opacity-30 group-hover:opacity-100 hover:text-red-500 cursor-pointer transition-all" data-value="${text}"></i>
                `;
                tagsContainer.appendChild(tag);
            });
        }

        // Deep Sync with Hidden Input
        gatherAllAmenities();
    };

    const gatherAllAmenities = () => {
        const checked = document.querySelectorAll('input[name="amenity_check"]:checked');
        const standard = Array.from(checked).map(cb => cb.value);
        const all = [...standard, ...customAmenities];
        
        if (amenitiesHidden) {
            amenitiesHidden.value = JSON.stringify(all);
        }
    };

    // 4. Interaction Engine
    if (addBtn) {
        addBtn.onclick = (e) => {
            e.preventDefault();
            if (customInput) {
                addTag(customInput.value);
                customInput.value = '';
                customInput.focus();
            }
        };
    }

    if (customInput) {
        customInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                addTag(customInput.value);
                customInput.value = '';
            }
        });
    }

    if (tagsContainer) {
        tagsContainer.addEventListener('click', (e) => {
            if (e.target.classList.contains('remove-tag')) {
                removeTag(e.target.dataset.value);
            }
        });
    }

    // 5. Initial Lifecycle
    const init = () => {
        try {
            const initial = window.INITIAL_AMENITIES || [];
            const predefined = window.PREDEFINED_AMENITIES || [];
            
            if (Array.isArray(initial)) {
                initial.forEach(item => {
                    if (item && !predefined.includes(item)) {
                        // Push to array first to avoid multiple render cycles
                        if (!customAmenities.includes(item)) customAmenities.push(item);
                    }
                });
                syncAndRender();
            }
        } catch (err) {
            console.error("Init failure:", err);
        }
    };

    // 6. Media Logistics (Preserved)
    if (uploadZone && mediaInput) {
        uploadZone.addEventListener('click', () => mediaInput.click());

        mediaInput.addEventListener('change', (e) => {
            const files = Array.from(e.target.files);
            files.forEach(file => {
                const reader = new FileReader();
                reader.onload = (ev) => {
                    if (!previewContainer) return;
                    const div = document.createElement('div');
                    div.className = "relative group aspect-square rounded-2xl overflow-hidden border-2 border-primary-100 shadow-md animate-in zoom-in duration-300";
                    div.innerHTML = `
                        <img src="${ev.target.result}" class="w-full h-full object-cover">
                        <div class="absolute inset-0 bg-primary-600/20 opacity-0 group-hover:opacity-100 transition-opacity flex items-center justify-center">
                             <i class="fas fa-check-circle text-white text-3xl"></i>
                        </div>
                    `;
                    previewContainer.appendChild(div);
                };
                reader.readAsDataURL(file);
            });
        });

        uploadZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            uploadZone.style.borderColor = '#0d24c8';
            uploadZone.style.background = 'white';
        });

        uploadZone.addEventListener('dragleave', () => {
            uploadZone.style.borderColor = 'rgba(13, 36, 200, 0.1)';
            uploadZone.style.background = 'rgba(248, 250, 252, 0.5)';
        });

        uploadZone.addEventListener('drop', (e) => {
            e.preventDefault();
            mediaInput.files = e.dataTransfer.files;
            mediaInput.dispatchEvent(new Event('change'));
        });
    }

    // 7. Global Form Interceptor
    if (form) {
        form.addEventListener('submit', () => {
            gatherAllAmenities();
        });
    }

    // Execute Lifecycle
    init();
});