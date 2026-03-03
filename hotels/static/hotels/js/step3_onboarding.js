/**
 * ComplianceManager - Professional Identity Verification Logic
 * Handles ID type switching, masking, and validation patterns.
 */
class ComplianceManager {
    constructor() {
        this.idInput = document.getElementById('id_number_input');
        this.idLabel = document.getElementById('idNumberLabel');
        this.config = {
            'AADHAAR': {
                label: 'Aadhaar Number',
                placeholder: 'XXXX-XXXX-XXXX',
                pattern: '\\d{4}-\\d{4}-\\d{4}',
                icon: 'fa-id-card-clip'
            },
            'PAN': {
                label: 'PAN Card Number',
                placeholder: 'ABCDE1234F',
                pattern: '[A-Z]{5}[0-9]{4}[A-Z]{1}',
                icon: 'fa-address-card'
            }
        };

        this.init();
        this.initFileUploads();
    }

    init() {
        if (!this.idInput) return;

        // Use event delegation for identity type radios
        document.addEventListener('change', (e) => {
            if (e.target.name === 'id_type') {
                this.updateUI(e.target.value);
            }
        });

        // Add real-time masking/formatting
        this.idInput.addEventListener('input', (e) => this.handleInput(e));

        // Match initial state
        const initialType = document.querySelector('input[name="id_type"]:checked')?.value || 'AADHAAR';
        this.updateUI(initialType);
    }

    updateUI(type) {
        const settings = this.config[type];
        if (!settings) return;

        if (this.idLabel) this.idLabel.textContent = settings.label;

        // Dynamic Icon Switching
        const iconEl = document.getElementById('id_input_icon');
        if (iconEl) {
            iconEl.className = `fas ${settings.icon}`;
        }

        if (this.idInput) {
            // Professional Reset: Clear previous value when switching types
            this.idInput.value = '';
            this.idInput.placeholder = settings.placeholder;

            // Re-trigger masking logic for empty state
            this.handleInput({ target: this.idInput });

            // Add a subtle animation feedback
            this.idInput.classList.add('pulse-highlight');
            setTimeout(() => this.idInput.classList.remove('pulse-highlight'), 500);
        }

        // Also reset the associated file upload for the primary ID
        const mandatoryDocInput = document.querySelector('input[name="doc_mandatory"]');
        if (mandatoryDocInput) {
            this.resetFileUpload(mandatoryDocInput.id);
        }
    }

    handleInput(e) {
        const type = document.querySelector('input[name="id_type"]:checked')?.value;
        let val = e.target.value.toUpperCase().replace(/\s/g, '');

        if (type === 'AADHAAR') {
            // Format Aadhaar: XXXX-XXXX-XXXX
            val = val.replace(/\D/g, '').substring(0, 12);
            const matches = val.match(/.{1,4}/g);
            e.target.value = matches ? matches.join('-') : val;
        } else {
            // PAN: Upper case only
            e.target.value = val.substring(0, 10);
        }
    }

    initFileUploads() {
        const fileInputs = document.querySelectorAll('.upload-dossier-zone input[type="file"]');
        fileInputs.forEach(input => {
            // Force strict browser filtering for professional UX
            input.setAttribute('accept', '.pdf,image/*');
            input.addEventListener('change', (e) => this.handleFileChange(e));
        });

        // Delegate clicks for remove and view buttons
        document.addEventListener('click', (e) => {
            const removeBtn = e.target.closest('.remove-file-btn');
            const viewBtn = e.target.closest('.view-document-btn');

            if (removeBtn) {
                const targetId = removeBtn.getAttribute('data-target');
                this.resetFileUpload(targetId);
            }

            if (viewBtn) {
                const targetId = viewBtn.getAttribute('data-target');
                this.handlePreview(targetId);
            }
        });
    }

    handlePreview(inputId) {
        const input = document.getElementById(inputId);

        // Robustness: If input.files[0] is missing, maybe it was a pre-existing file or error
        if (!input || !input.files[0]) {
            console.warn("ComplianceManager: No file found in input to preview.", inputId);
            return;
        }

        const file = input.files[0];
        const url = URL.createObjectURL(file);
        const ext = file.name.split('.').pop().toLowerCase();

        // Call the professional global preview system
        if (typeof window.previewSingleFile === 'function') {
            window.previewSingleFile(url, file.name, ext);
        } else {
            console.error("ComplianceManager: Global preview system not initialized. Opening in new tab.");
            window.open(url, '_blank');
        }
    }

    handleFileChange(e) {
        const input = e.target;
        const file = input.files[0];
        if (!file) return;

        // Strict Enterprise Validation: Only PDF and Images
        const ext = file.name.split('.').pop().toLowerCase();
        const validExtensions = ['pdf', 'jpg', 'jpeg', 'png', 'webp'];

        if (!validExtensions.includes(ext)) {
            // Professional error feedback
            this.showUploadError(input, "Invalid Format: Highly-secure verification only supports PDF or High-Res Images.");
            this.resetFileUpload(input.id);
            return;
        }

        const id = input.id;
        const statusBadge = document.getElementById(`status-${id}`);
        const placeholder = document.getElementById(`placeholder-${id}`);

        if (statusBadge && placeholder) {
            // Update metadata
            const nameEl = statusBadge.querySelector('.file-name-text');
            const metaEl = statusBadge.querySelector('.file-meta-text');
            const iconEl = statusBadge.querySelector('.file-icon-box i');

            if (nameEl) nameEl.textContent = file.name;
            if (metaEl) {
                const size = (file.size / (1024 * 1024)).toFixed(2);
                const extUpper = ext.toUpperCase();
                metaEl.textContent = `${size} MB • ${extUpper} DOCUMENT`;
            }

            // Update icon based on extension
            if (iconEl) {
                let iconClass = 'fa-file-lines';
                if (['jpg', 'jpeg', 'png', 'webp'].includes(ext)) iconClass = 'fa-file-image';
                if (ext === 'pdf') iconClass = 'fa-file-pdf';
                iconEl.className = `fas ${iconClass}`;
            }

            // Toggle visibility
            placeholder.style.display = 'none';
            statusBadge.classList.add('active');

            // Success feedback and State Management
            const zone = input.closest('.upload-dossier-zone');
            zone.classList.add('has-file'); // NEW: Add state class
            zone.classList.remove('upload-error');
            zone.classList.add('upload-success-glow');
            zone.style.borderColor = 'var(--secondary)';
            zone.style.background = 'rgba(212, 175, 55, 0.05)';
        }
    }

    showUploadError(input, msg) {
        const zone = input.closest('.upload-dossier-zone');
        if (zone) {
            zone.classList.add('upload-error');
            // Trigger a shake animation if available in common.css
            zone.style.borderColor = '#ef4444';
            zone.style.background = 'rgba(239, 68, 68, 0.05)';

            // Professional alert
            alert(msg);
        }
    }

    resetFileUpload(inputId) {
        const input = document.getElementById(inputId);
        if (!input) return;

        input.value = ''; // Clear file
        const statusBadge = document.getElementById(`status-${inputId}`);
        const placeholder = document.getElementById(`placeholder-${inputId}`);

        if (statusBadge && placeholder) {
            statusBadge.classList.remove('active');
            placeholder.style.display = 'flex';

            const zone = input.closest('.upload-dossier-zone');
            zone.classList.remove('has-file'); // NEW: Remove state class
            zone.classList.remove('upload-success-glow');
            zone.style.borderColor = '';
            zone.style.background = '';
        }
    }
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
    window.complianceManager = new ComplianceManager();
});
