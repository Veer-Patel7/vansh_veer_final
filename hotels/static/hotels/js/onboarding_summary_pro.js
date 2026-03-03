/**
 * Onboarding Summary Logic (Pro Version)
 * Gathers data from Steps 1, 2, and 3 and populates Step 4.
 */

window.populateSummary = function () {
    const summaryContainer = document.getElementById('summaryContainer');
    if (!summaryContainer) return;

    // Helper to get value or 'Not Provided'
    const getVal = (name) => {
        const input = document.querySelector(`[name="${name}"]`);
        if (!input) return 'Not Provided';
        // Handle radio buttons
        if (input.type === 'radio') {
            const checked = document.querySelector(`input[name="${name}"]:checked`);
            return checked ? checked.value : 'Not Provided';
        }
        // Handle select text
        if (input.tagName === 'SELECT') {
            return input.options[input.selectedIndex]?.text || 'Not Selected';
        }
        return input.value || 'Not Provided';
    };

    // Helper to get checked labels (e.g. for services)
    const getCheckedLabels = (name) => {
        const checked = Array.from(document.querySelectorAll(`input[name="${name}"]:checked`));
        return checked.map(el => {
            const label = el.closest('label');
            return label ? label.textContent.trim() : el.value;
        }).join(', ') || 'None selected';
    };

    // 1. Hotel Identity Data
    const hotelName = getVal('hotel_name');
    const hotelType = getVal('hotel_type');
    const address = getVal('address');

    // 2. Compliance Data
    const idTypeRaw = getVal('id_type');
    let idType = idTypeRaw.charAt(0).toUpperCase() + idTypeRaw.slice(1).toLowerCase();
    if (idTypeRaw.toUpperCase() === 'PAN') idType = 'PAN';
    const idNumber = getVal('id_number');
    const govtNumber = getVal('govt_reg_number');
    const gstNumber = getVal('gst_number');

    // Helper for ID Formatting: Groups of 4 with space
    const formatID = (str) => {
        if (!str || str === 'Not Provided') return str;
        return str.replace(/\s/g, '').match(/.{1,4}/g)?.join(' ') || str;
    };

    // 3. Media Logic
    const getFilePreview = (inputSelector) => {
        const input = document.querySelector(inputSelector);
        if (input && input.files && input.files[0]) {
            return URL.createObjectURL(input.files[0]);
        }
        return null;
    };

    const getAllFilePreviews = (inputSelector) => {
        const input = document.querySelector(inputSelector);
        if (input && input.files) {
            return Array.from(input.files).map(file => URL.createObjectURL(file));
        }
        return [];
    };

    const propertyPhotos = getAllFilePreviews('#galleryInput');
    const propertyPreview = propertyPhotos[0] || null;
    const docMandatoryPreview = getFilePreview('[name="doc_mandatory"]');
    const docCertificatePreview = getFilePreview('[name="doc_certificate"]');
    const docGstPreview = getFilePreview('[name="doc_gst"]');

    // 4. Inventory Module Logic
    const roomRows = document.querySelectorAll('.room-row');
    let roomsHtml = '';
    roomRows.forEach((row, idx) => {
        const rIdx = row.dataset.roomIndex;
        const type = row.querySelector(`[name="room_name_${rIdx}"]`)?.value || 'Unnamed Category';
        const rClass = row.querySelector(`[name="room_class_${rIdx}"]`)?.value || 'Standard';
        const price = parseFloat(row.querySelector(`[name="room_price_${rIdx}"]`)?.value || '0').toLocaleString('en-IN');
        const guests = row.querySelector(`[name="room_guests_${rIdx}"]`)?.value || '0';
        const count = row.querySelector(`[name="room_count_${rIdx}"]`)?.value || '0';

        const rInput = row.querySelector(`input[type="file"]`);
        let rPreviewUrl = (rInput && rInput.files && rInput.files[0]) ? URL.createObjectURL(rInput.files[0]) : null;

        const pillAmens = Array.from(row.querySelectorAll('.dynamic-pill-item span')).map(s => s.textContent);
        const allAmens = pillAmens.join(', ') || 'Standard executive amenities';

        roomsHtml += `
            <div class="summary-room-item" style="padding: 24px; background: #f8fafc; border: 1px solid var(--border); border-radius: 20px; display: flex; gap: 20px; align-items: flex-start; transition: transform 0.3s ease;">
                <div style="width: 80px; height: 80px; border-radius: 12px; overflow: hidden; flex-shrink: 0; background: #f1f5f9; border: 1px solid var(--border);">
                    ${rPreviewUrl ? `<img src="${rPreviewUrl}" style="width: 100%; height: 100%; object-fit: cover;">` : '<div style="width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; color: #cbd5e1;"><i class="fas fa-image fa-2x"></i></div>'}
                </div>
                <div style="flex: 1; min-width: 0;">
                    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 8px;">
                        <div>
                            <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 2px;">
                                <span style="font-size: 0.65rem; text-transform: uppercase; letter-spacing: 1px; color: var(--secondary); font-weight: 700;">${rClass}</span>
                                <span style="color: var(--text-muted); font-size: 0.65rem; font-weight: 600;">• Category ${idx + 1}</span>
                            </div>
                            <strong style="font-size: 1.1rem; color: var(--text-main); font-weight: 700;">${type}</strong>
                        </div>
                    </div>
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 10px;">
                        <div style="display: flex; align-items: baseline; gap: 4px;">
                            <span style="font-size: 0.7rem; color: var(--text-muted);">₹</span>
                            <span style="font-size: 1.1rem; font-weight: 700; color: var(--text-main);">${price}</span>
                        </div>
                        <div style="display: flex; gap: 8px;">
                            <span style="font-size: 0.75rem; color: var(--text-muted); background: white; padding: 2px 8px; border-radius: 6px; border: 1px solid var(--border);"><i class="fas fa-users" style="font-size: 0.65rem;"></i> ${guests}</span>
                            <span style="font-size: 0.75rem; color: var(--text-muted); background: white; padding: 2px 8px; border-radius: 6px; border: 1px solid var(--border);"><i class="fas fa-door-open" style="font-size: 0.65rem;"></i> ${count}</span>
                        </div>
                    </div>
                    <div style="font-size: 0.75rem; color: var(--text-muted); line-height: 1.4; display: flex; gap: 6px;">
                        <i class="fas fa-check-circle" style="color: #22c55e; margin-top: 3px;"></i> 
                        <span>${allAmens}</span>
                    </div>
                </div>
            </div>
        `;
    });

    // 5. Build Final "Executive Dossier"
    summaryContainer.innerHTML = `
        <div class="summary-dossier" style="background: white; border-radius: 32px; overflow: hidden; box-shadow: var(--shadow-lg); border: 1px solid var(--border);">
            
            <!-- HEADER: Executive Summary -->
            <div class="summary-header" style="background: #f8fafc; padding: 60px; border-bottom: 2px solid var(--secondary); position: relative;">
                <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                    <div style="flex: 1;">
                        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                            <span style="background: var(--primary); color: white; padding: 4px 12px; border-radius: 100px; font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Partner Enrollment</span>
                            <span style="color: var(--text-muted); font-size: 0.7rem; font-family: monospace;">Ref: HP-${Math.floor(Math.random() * 900000 + 100000)}</span>
                        </div>
                        <h3 style="font-size: 3rem; margin: 0; font-weight: 800; color: var(--text-main); letter-spacing: -0.04em; line-height: 1;">${hotelName}</h3>
                        <div style="margin-top: 20px; display: flex; align-items: center; gap: 8px;">
                            <i class="fas fa-map-marker-alt" style="color: var(--secondary);"></i>
                            <p style="margin: 0; color: var(--text-muted); font-size: 1.1rem; font-weight: 500;">${address}</p>
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="background: white; padding: 24px; border-radius: 20px; border: 1px solid var(--border); box-shadow: var(--shadow-sm);">
                            <span style="display:block; font-size: 0.7rem; text-transform: uppercase; letter-spacing: 1px; color: var(--text-muted); margin-bottom: 8px; font-weight: 700;">Property Tier</span>
                            <div style="font-size: 1.5rem; color: var(--text-main); font-weight: 800;">
                                <i class="fas fa-crown" style="color: var(--secondary);"></i> ${hotelType}
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div class="summary-content" style="padding: 60px; display: flex; flex-direction: column; gap: 50px;">
                
                <!-- PHASE 01: Property Foundation -->
                <div class="summary-module">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px; border-bottom: 1px solid #f1f5f9; padding-bottom: 20px;">
                        <div style="width: 40px; height: 40px; background: var(--primary); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800;">01</div>
                        <h4 style="color: var(--text-main); font-size: 1.2rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 800; margin: 0;">Property Foundation</h4>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1.5fr; gap: 40px;">
                        <div style="background: #f8fafc; border-radius: 20px; padding: 30px; border: 1px solid var(--border);">
                            <label style="display:block; font-size: 0.7rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 15px; font-weight: 700;">Identity Blueprint</label>
                            <div style="display: flex; flex-direction: column; gap: 15px;">
                                <div>
                                    <span style="font-size: 0.65rem; color: var(--text-muted); display: block; text-transform: uppercase; font-weight: 700;">Designation</span>
                                    <strong style="color: var(--text-main); font-size: 1.1rem; font-weight: 700;">${hotelName}</strong>
                                </div>
                                <div style="padding-top: 15px; border-top: 1px dashed var(--border);">
                                    <span style="font-size: 0.65rem; color: var(--text-muted); display: block; text-transform: uppercase; font-weight: 700;">Location</span>
                                    <span style="color: var(--text-main); font-size: 0.95rem; font-weight: 600;">${address}</span>
                                </div>
                            </div>
                        </div>
                        <div>
                            <label style="display:block; font-size: 0.7rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 15px; font-weight: 700;">Media Portfolio</label>
                            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
                                ${propertyPhotos.slice(0, 4).map((url) => `
                                    <div style="aspect-ratio: 1; border-radius: 10px; overflow: hidden; border: 1px solid var(--border);">
                                        <img src="${url}" style="width: 100%; height: 100%; object-fit: cover;">
                                    </div>
                                `).join('') || '<div style="grid-column: span 4; padding: 20px; text-align: center; color: var(--text-muted); border: 2px dashed var(--border); border-radius: 12px;">No images uploaded</div>'}
                            </div>
                        </div>
                    </div>
                </div>

                <!-- PHASE 02: Inventory & Operations -->
                <div class="summary-module">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px; border-bottom: 1px solid #f1f5f9; padding-bottom: 20px;">
                        <div style="width: 40px; height: 40px; background: var(--primary); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800;">02</div>
                        <h4 style="color: var(--text-main); font-size: 1.2rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 800; margin: 0;">Inventory & Operations</h4>
                    </div>
                    
                    <div style="display: flex; flex-direction: column; gap: 40px;">
                        <div>
                            <label style="display:block; font-size: 0.7rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 20px; font-weight: 700;">Room Categories</label>
                            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px;">
                                ${roomsHtml}
                            </div>
                        </div>

                        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                            <div style="background: white; border-radius: 20px; padding: 30px; border: 1px solid var(--border);">
                                <label style="display:block; font-size: 0.7rem; text-transform: uppercase; color: var(--text-muted); margin-bottom: 15px; font-weight: 700;">Services & Protocols</label>
                                <div style="display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 20px;">
                                    ${getCheckedLabels('services').split(', ').map(s => `
                                        <span style="background: #f1f5f9; padding: 6px 14px; border-radius: 100px; font-size: 0.75rem; font-weight: 700; color: var(--text-main); border: 1px solid var(--border);">${s}</span>
                                    `).join('')}
                                </div>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                    <div style="background: #f8fafc; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid var(--border);">
                                        <span style="font-size: 0.6rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; display: block;">Check-In</span>
                                        <strong style="font-size: 1.1rem; color: var(--text-main);">${getVal('check_in')}</strong>
                                    </div>
                                    <div style="background: #f8fafc; padding: 15px; border-radius: 12px; text-align: center; border: 1px solid var(--border);">
                                        <span style="font-size: 0.6rem; color: var(--text-muted); font-weight: 700; text-transform: uppercase; display: block;">Check-Out</span>
                                        <strong style="font-size: 1.1rem; color: var(--text-main);">${getVal('check_out')}</strong>
                                    </div>
                                </div>
                            </div>
                            <div style="background: var(--primary); border-radius: 20px; padding: 30px; color: white;">
                                <label style="display:block; font-size: 0.7rem; text-transform: uppercase; color: rgba(255,255,255,0.6); margin-bottom: 15px; font-weight: 700;">Policies</label>
                                <p style="font-size: 0.95rem; line-height: 1.6; color: white; margin: 0; font-style: italic;">"${getVal('cancellation_policy')}"</p>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- PHASE 03: Compliance -->
                <div class="summary-module">
                    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px; border-bottom: 1px solid #f1f5f9; padding-bottom: 20px;">
                        <div style="width: 40px; height: 40px; background: var(--primary); border-radius: 10px; display: flex; align-items: center; justify-content: center; color: white; font-weight: 800;">03</div>
                        <h4 style="color: var(--text-main); font-size: 1.2rem; text-transform: uppercase; letter-spacing: 1px; font-weight: 800; margin: 0;">Identity & Compliance</h4>
                    </div>
                    
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                        <!-- Mandatory ID -->
                        <div style="background: #f8fafc; border: 1px solid var(--border); padding: 25px; border-radius: 20px; display: flex; align-items: center; gap: 20px;">
                            <div style="width: 50px; height: 50px; background: white; border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border);">
                                <i class="fas fa-id-card" style="color: var(--secondary); font-size: 1.5rem;"></i>
                            </div>
                            <div style="flex: 1;">
                                <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 2px;">${idType} Number</span>
                                <strong style="font-size: 1.1rem; color: var(--text-main); letter-spacing: 1px;">${formatID(idNumber)}</strong>
                            </div>
                            ${docMandatoryPreview ? `<a href="${docMandatoryPreview}" target="_blank" style="color: var(--primary); font-size: 1.2rem;"><i class="fas fa-external-link-alt"></i></a>` : ''}
                        </div>

                        <!-- Govt ID -->
                        <div style="background: #f8fafc; border: 1px solid var(--border); padding: 25px; border-radius: 20px; display: flex; align-items: center; gap: 20px;">
                            <div style="width: 50px; height: 50px; background: white; border-radius: 12px; display: flex; align-items: center; justify-content: center; border: 1px solid var(--border);">
                                <i class="fas fa-landmark" style="color: var(--secondary); font-size: 1.5rem;"></i>
                            </div>
                            <div style="flex: 1;">
                                <span style="font-size: 0.65rem; color: var(--text-muted); text-transform: uppercase; font-weight: 700; display: block; margin-bottom: 2px;">Govt Registry</span>
                                <strong style="font-size: 1.1rem; color: var(--text-main); letter-spacing: 1px;">${formatID(govtNumber)}</strong>
                            </div>
                            ${docCertificatePreview ? `<a href="${docCertificatePreview}" target="_blank" style="color: var(--primary); font-size: 1.2rem;"><i class="fas fa-external-link-alt"></i></a>` : ''}
                        </div>
                    </div>
                </div>

            </div>
            
            <!-- FOOTER -->
            <div style="background: #0f172a; padding: 40px 60px; color: white; display: flex; justify-content: space-between; align-items: center;">
                <div style="display: flex; gap: 30px; align-items: center;">
                    <i class="fas fa-shield-check" style="font-size: 2rem; color: var(--secondary);"></i>
                    <div>
                        <div style="font-size: 0.7rem; opacity: 0.6; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 5px;">Data Authentication</div>
                        <div style="font-weight: 700; font-size: 1.2rem;">Secured by HotelPro Global</div>
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.7rem; opacity: 0.6; margin-bottom: 5px;">Report Generated</div>
                    <div style="font-weight: 700;">${new Date().toLocaleDateString('en-US', { day: '2-digit', month: 'short', year: 'numeric' })}</div>
                </div>
            </div>
        </div>
        <style>
            .summary-room-item:hover {
                transform: translateY(-5px);
                border-color: var(--secondary);
                background: white !important;
                box-shadow: var(--shadow-md);
            }
        </style>
    `;
};

// Auto-populate Step 4
document.addEventListener('click', (e) => {
    if (e.target.closest('.next-step') && e.target.closest('.next-step').dataset.target === '4') {
        window.populateSummary();
    }
});
