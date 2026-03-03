/**
 * SummaryEngine - Professional Data Extraction & Modular Rendering
 * Standardizes Step 4 Dossier Generation with high maintainability.
 */
class SummaryEngine {
    constructor() {
        this.container = document.getElementById('summaryContainer');
        this.setupEventListeners();
    }

    /**
     * Extracts values from input fields by name
     */
    getVal(name, multiple = false) {
        if (multiple) {
            const checked = document.querySelectorAll(`input[name="${name}"]:checked`);
            return Array.from(checked).map(i => i.closest('label')?.textContent.trim() || i.value);
        }

        const input = document.querySelector(`[name="${name}"]`);
        if (!input) return 'Not Provided';

        if (input.type === 'radio') {
            const checked = document.querySelector(`input[name="${name}"]:checked`);
            return checked ? checked.closest('label')?.querySelector('span')?.textContent.trim() || checked.value : 'Not Provided';
        }

        if (input.tagName === 'SELECT') {
            return input.options[input.selectedIndex]?.text || '';
        }

        return input.value || '';
    }

    /**
     * Standardizes ID formatting
     */
    formatID(str) {
        if (!str || str === 'Not Provided') return str;
        return str.replace(/\s/g, '').match(/.{1,4}/g)?.join(' ') || str;
    }

    /**
     * Renders a standardized summary section
     */
    renderSection(id, title, items) {
        return `
            <div class="summary-module">
                <div class="module-header">
                    <div class="module-number">${id}</div>
                    <h4 style="font-weight: 800; text-transform: uppercase; letter-spacing: 1px;">${title}</h4>
                </div>
                <div class="dense-grid" style="gap: 30px;">
                    ${items}
                </div>
            </div>
        `;
    }

    /**
     * Renders the final Executive Dossier
     */
    render() {
        if (!this.container) return;

        const data = {
            hotelName: this.getVal('hotel_name'),
            hotelType: this.getVal('hotel_type'),
            address: this.getVal('address'),
            city: this.getVal('city'),
            pincode: this.getVal('pincode'),
            idType: this.getVal('id_type'),
            idNumber: this.getVal('id_number'),
            gstNumber: this.getVal('gst_number'),
            checkIn: this.getVal('check_in'),
            checkOut: this.getVal('check_out'),
            cancellation: this.getVal('cancellation_policy'),
            services: this.getVal('services', true),
            govtRegNumber: this.getVal('govt_reg_number')
        };

        const propertyPhotos = this.getAllFilePreviews('#galleryInput');
        const idDocs = this.getAllFilePreviews('input[name="doc_mandatory"]');
        const gstDocs = this.getAllFilePreviews('input[name="doc_gst"]');
        const regDocs = this.getAllFilePreviews('input[name="doc_certificate"]');

        this.container.innerHTML = `
            <div class="summary-dossier">
                <div class="summary-header">
                    <div class="holographic-seal"></div>
                    <div style="display: flex; justify-content: space-between; align-items: flex-end;">
                        <div>
                            <div style="display: flex; gap: 10px; margin-bottom: 15px;">
                                <span class="compliance-badge" style="background:var(--primary); color:white; border:none;">Partner Enrollment</span>
                                <span style="color:var(--text-muted); font-size: 0.7rem;">Ref: HP-${Math.floor(Math.random() * 900000 + 100000)}</span>
                            </div>
                            <h3 style="font-size: 2.8rem; font-weight: 800; color: var(--primary); line-height: 1;">${data.hotelName || 'Property Name'}</h3>
                            <div style="margin-top: 20px; color: var(--text-muted); display:flex; gap:10px; align-items:center;">
                                <i class="fas fa-location-dot" style="color:var(--secondary);"></i> 
                                ${this.extractCleanCity(data.city, data.address)} ${data.pincode ? `(${data.pincode})` : ''}
                            </div>
                        </div>
                        <div class="tier-badge" style="background: white; padding: 15px 25px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.05); border: 1px solid var(--border);">
                            <span style="display:block; font-size:0.65rem; font-weight:800; color:var(--text-muted); text-transform:uppercase; margin-bottom: 2px;">Property Tier</span>
                            <div style="font-size: 1.4rem; font-weight: 800; color: var(--primary); display: flex; align-items: center; gap: 10px;">
                                <i class="fas fa-crown" style="color:var(--secondary);"></i> 
                                ${data.hotelType}
                            </div>
                        </div>
                    </div>
                </div>

                <div style="padding: 60px;">
                    ${this.renderSection('01', 'Property Foundation', `
                        <div class="col-12">
                            <div class="summary-room-item" style="gap:40px; border-bottom: none; border-radius: 20px 20px 0 0;">
                                <div style="flex: 1;">
                                    <span style="font-size: 0.7rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">Legal Designation & Location</span>
                                    <h4 style="font-size: 1.8rem; font-weight: 800; color: var(--primary); margin-top: 8px;">${data.hotelName || 'Property Name'}</h4>
                                    <p style="font-size: 1rem; margin-top: 12px; color: var(--text-muted);"><i class="fas fa-map-location-dot" style="color:var(--secondary);"></i> ${data.address}</p>
                                </div>
                                <div class="tier-badge" style="background: white; padding: 12px 20px; border-radius: 15px; border: 1px solid var(--border); box-shadow: 0 10px 25px rgba(0,0,0,0.03);">
                                    <span style="display:block; font-size:0.6rem; font-weight:800; color:var(--text-muted); text-transform:uppercase;">Classification</span>
                                    <div style="font-size: 1.1rem; font-weight: 800; color: var(--primary);"><i class="fas fa-crown" style="color:var(--secondary); font-size:0.8rem;"></i> ${data.hotelType}</div>
                                </div>
                            </div>
                            
                            <div class="summary-portfolio-showcase" style="background: rgba(15, 23, 42, 0.02); padding: 30px; border: 1px solid var(--border); border-top: none; border-radius: 0 0 20px 20px;">
                                <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 20px;">
                                    <div>
                                        <h5 style="font-size: 0.8rem; font-weight: 800; color: var(--primary); text-transform: uppercase; letter-spacing: 2px;">Property Portfolio Showcase</h5>
                                        <p style="font-size: 0.7rem; color: var(--text-muted);">Displaying all ${propertyPhotos.length} verified physical assets</p>
                                    </div>
                                    <div style="font-size: 0.7rem; font-weight: 700; color: var(--secondary);"><i class="fas fa-expand-arrows-alt"></i> TAP TO INSPECT</div>
                                </div>
                                <div class="summary-media-grid" style="grid-template-columns: repeat(auto-fill, minmax(130px, 1fr));">
                                    ${propertyPhotos.map((fileObj, idx) => `
                                        <div class="summary-media-item lightbox-trigger">
                                            <img src="${fileObj.url}" class="lightbox-trigger">
                                        </div>
                                    `).join('')}
                                </div>
                            </div>
                        </div>
                    `)}

                    ${this.renderSection('02', 'Operational Inventory', `
                        <div class="col-12">
                            <div id="summary-room-list" style="display: grid; gap: 15px;">
                                ${this.renderRoomSummary()}
                            </div>
                        </div>
                    `)}

                    ${this.renderSection('03', 'Elite Service Registry', `
                        <div class="col-12">
                            <div class="elite-pills-container" style="margin-top: 0;">
                                ${data.services.length > 0
                ? data.services.map(s => `<div class="elite-pill-item"><i class="fas fa-check-double" style="color:var(--secondary); font-size:0.7rem;"></i> ${s}</div>`).join('')
                : '<p style="color:var(--text-muted);">No additional services selected.</p>'}
                            </div>
                        </div>
                    `)}

                    ${this.renderSection('04', 'Operational Standards', `
                        <div class="col-6">
                            <div class="summary-room-item">
                                <i class="fas fa-clock fa-2x" style="color:var(--secondary);"></i>
                                <div>
                                    <span style="font-size: 0.7rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Standard Schedule</span>
                                    <div style="font-size: 1.1rem; font-weight: 800;">IN: ${data.checkIn} | OUT: ${data.checkOut}</div>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="summary-room-item">
                                <i class="fas fa-shield-halved fa-2x" style="color:var(--secondary);"></i>
                                <div style="flex:1;">
                                    <span style="font-size: 0.7rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Policy Protocol</span>
                                    <div style="font-size: 0.85rem; font-weight: 600; line-height: 1.4;">${this.formatPolicy(data.cancellation)}</div>
                                </div>
                            </div>
                        </div>
                    `)}

                    ${this.renderSection('05', 'Identity Verification', `
                        <div class="col-12">
                            <div class="summary-room-item" style="border-color: var(--secondary-hover); background: var(--accent-soft);">
                                <div style="display:flex; gap:25px; width: 100%; align-items: center;">
                                    <div class="summary-media-item lightbox-trigger" style="width: 120px; height: 80px; flex-shrink: 0; border-radius: 12px; display:flex; align-items:center; justify-content:center; background: white; border: 1.5px solid var(--border-gold);">
                                        ${this.renderFilePreview(idDocs[0], 'fa-file-invoice')}
                                    </div>
                                    <div style="flex:1;">
                                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                                            <div>
                                                <span style="font-size: 0.75rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase; letter-spacing: 1px;">Primary Identification</span>
                                                <div style="font-size: 1.1rem; font-weight: 800; color: var(--secondary); margin: 4px 0;">${data.idType}</div>
                                                <div style="font-size: 1.8rem; font-weight: 800; letter-spacing: 2px; color: var(--primary);">${this.formatID(data.idNumber)}</div>
                                            </div>
                                            <div style="text-align: right;">
                                                <span class="compliance-badge" style="background: #22c55e; color: white; border: none; font-size: 0.6rem; padding: 4px 12px;">ACTIVE VALIDATION</span>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `)}

                    ${this.renderSection('06', 'Business Authentication', `
                        <div class="col-6">
                            <div class="summary-room-item" style="height: 100%; align-items: flex-start;">
                                <div style="display:flex; gap:15px; width: 100%;">
                                    <div class="summary-media-item lightbox-trigger" style="width: 70px; height: 70px; flex-shrink: 0; border-radius: 10px; display:flex; align-items:center; justify-content:center; background: #f8fafc;">
                                        ${this.renderFilePreview(gstDocs[0], 'fa-building-circle-check')}
                                    </div>
                                    <div style="flex:1;">
                                        <span style="font-size: 0.7rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Tax Authentication</span>
                                        <div style="font-size: 0.85rem; font-weight: 800; color: var(--secondary); margin-bottom: 2px;">GST CERTIFICATE</div>
                                        <div style="font-size: 1.1rem; font-weight: 800;">${data.gstNumber || 'Not Provided'}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="col-6">
                            <div class="summary-room-item" style="height: 100%; align-items: flex-start;">
                                <div style="display:flex; gap:15px; width: 100%;">
                                    <div class="summary-media-item lightbox-trigger" style="width: 70px; height: 70px; flex-shrink: 0; border-radius: 10px; display:flex; align-items:center; justify-content:center; background: #f8fafc;">
                                        ${this.renderFilePreview(regDocs[0], 'fa-gavel')}
                                    </div>
                                    <div style="flex:1;">
                                        <span style="font-size: 0.7rem; font-weight: 800; color: var(--text-muted); text-transform: uppercase;">Govt. Mandate</span>
                                        <div style="font-size: 0.85rem; font-weight: 800; color: var(--secondary); margin-bottom: 2px;">REGISTRATION</div>
                                        <div style="font-size: 1.1rem; font-weight: 800;">${data.govtRegNumber || 'Not Provided'}</div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `)}
                </div>

                <div class="summary-footer">
                    <div class="summary-footer-brand">
                        <i class="fas fa-shield-check fa-2x" style="color:var(--secondary);"></i>
                        <div>
                            <div style="font-size:0.7rem; opacity:0.6; text-transform:uppercase; font-weight:800;">Identity Authentication</div>
                            <div style="font-weight:800; font-size:1.1rem;">Secured by HotelPro Elite</div>
                        </div>
                    </div>
                    <div class="footer-timestamp">
                        Report Generated<br><strong>${new Date().toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })}</strong>
                    </div>
                </div>
            </div>
        `;
    }

    renderRoomSummary() {
        const roomRows = document.querySelectorAll('.room-card-elite');
        return Array.from(roomRows).map((row) => {
            const index = row.dataset.roomIndex;
            const name = row.querySelector(`[name="room_name_${index}"]`)?.value || 'Standard Category';
            const price = row.querySelector(`[name="room_price_${index}"]`)?.value || '0';
            const type = row.querySelector(`[name="room_class_${index}"]`)?.value || 'Room';
            const amenitiesJson = row.querySelector(`[name="room_amenities_${index}"]`)?.value || '[]';
            let amenities = [];
            try { amenities = JSON.parse(amenitiesJson); } catch (e) { amenities = []; }

            // Extract room-specific photos
            const roomPreviewBox = row.querySelector('.room-preview-box');
            const roomMediaUrls = Array.from(roomPreviewBox.querySelectorAll('img, video')).map(media => {
                if (media.tagName === 'IMG') return media.src;
                // For videos, we use a placeholder or thumbnail if possible, but for now, just the src
                return media.src;
            }).filter(src => src && !src.startsWith('blob:null'));

            return `
                <div class="summary-room-item" style="align-items: flex-start; gap: 25px;">
                    <div class="summary-media-grid" style="width: 220px; grid-template-columns: repeat(2, 1fr); flex-shrink: 0;">
                        ${roomMediaUrls.map((url, mIdx) => {
                const isVid = url.includes('video') || url.startsWith('data:video');
                return `
                                <div class="summary-media-item lightbox-trigger" style="border-radius: 12px;">
                                    ${isVid
                        ? `<div class="video-overlay"><i class="fas fa-play" style="font-size: 0.6rem;"></i></div><video src="${url}" style="width:100\%; height:100\%; object-fit:cover;"></video>`
                        : `<img src="${url}" class="lightbox-trigger">`
                    }
                                </div>
                            `;
            }).join('')}
                        ${roomMediaUrls.length === 0 ? '<div class="summary-media-item" style="display:flex; align-items:center; justify-content:center; background:#f8fafc; border: 1px dashed var(--border);"><i class="fas fa-image" style="color:var(--text-muted); opacity:0.3;"></i></div>' : ''}
                    </div>

                    <div style="flex: 1;">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <span style="font-size: 0.65rem; font-weight: 800; color: var(--secondary); text-transform: uppercase;">${type}</span>
                                <h5 style="font-size: 1.1rem; font-weight: 800; margin: 2px 0;">${name}</h5>
                                <div style="font-size: 0.9rem; font-weight: 700; color: var(--primary);">₹${parseFloat(price).toLocaleString('en-IN')} / night</div>
                            </div>
                            <div style="font-size: 0.75rem; font-weight: 800; color: #22c55e; background: rgba(34, 197, 94, 0.1); padding: 5px 12px; border-radius: 8px;">
                                <i class="fas fa-check-circle"></i> VERIFIED
                            </div>
                        </div>
                        
                        <div class="elite-pills-container" style="margin-top: 12px; gap: 6px;">
                            ${amenities.map(a => `<span style="font-size: 0.65rem; background: rgba(15, 23, 42, 0.05); padding: 4px 10px; border-radius: 50px; font-weight: 700; color: var(--primary);"><i class="fas fa-check" style="color:var(--secondary); font-size: 0.6rem;"></i> ${a}</span>`).join('')}
                        </div>
                    </div>
                </div>
            `;
        }).join('');
    }

    getAllFilePreviews(selector) {
        const input = document.querySelector(selector);
        if (!input?.files) return [];
        return Array.from(input.files).map(f => ({
            url: URL.createObjectURL(f),
            type: f.type,
            name: f.name
        }));
    }

    /**
     * Professional file preview renderer
     */
    renderFilePreview(fileObj, fallbackIcon) {
        if (!fileObj) return `<i class="fas ${fallbackIcon}" style="opacity:0.2; font-size:1.8rem;"></i>`;

        const viewerAttr = `data-document-url="${fileObj.url}" data-file-type="${fileObj.type}" title="Click to view full document"`;

        if (fileObj.type.startsWith('image/')) {
            return `<img src="${fileObj.url}" class="lightbox-trigger" ${viewerAttr} style="width:100\%; height:100\%; object-fit:cover;">`;
        }

        // Elite document icon for PDFs/other docs
        const icon = fileObj.type === 'application/pdf' ? 'fa-file-pdf' : 'fa-file-lines';
        const color = fileObj.type === 'application/pdf' ? '#ef4444' : 'var(--secondary)';

        return `
            <div class="document-view-trigger" ${viewerAttr} style="display:flex; flex-direction:column; align-items:center; gap:5px; cursor:pointer; width:100\%; height:100\%; justify-content:center;">
                <i class="fas ${icon}" style="color:${color}; font-size:2rem;"></i>
                <span style="font-size:0.5rem; font-weight:800; opacity:0.6; text-transform:uppercase;">DOCUMENT</span>
            </div>
        `;
    }

    /**
     * Set up global event listeners for the summary
     */
    setupEventListeners() {
        document.addEventListener('click', (e) => {
            const trigger = e.target.closest('[data-document-url]');
            if (!trigger) return;

            const url = trigger.getAttribute('data-document-url');
            const type = trigger.getAttribute('data-file-type');

            // If it's a PDF, we always open in a new tab
            if (type === 'application/pdf') {
                e.preventDefault();
                e.stopPropagation();
                window.open(url, '_blank');
            }
            // Images are usually handled by the lightbox, 
            // but we can add secondary handling here if needed.
        }, true); // Use capture phase to intercept before other handlers if necessary
    }

    /**
     * Professional policy text formatter
     */
    formatPolicy(text) {
        if (!text || text.toLowerCase() === 'no' || text.length < 5) {
            return '<span style="color:var(--text-muted); font-style:italic;">Standard Property Revocation & Refund Protocols Apply.</span>';
        }
        return text;
    }

    /**
     * Refined city extraction for header
     */
    extractCleanCity(city, address) {
        if (city && city !== 'Not Provided' && city.length > 2) return city;

        // Extract from address components
        const parts = address.split(',').map(p => p.trim());
        if (parts.length > 2) {
            // Usually the 2nd or 3rd part is most relevant for city/town
            return parts[1] || parts[0];
        }
        return parts[0] || 'Property Location';
    }
}

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    window.summaryEngine = new SummaryEngine();
});
