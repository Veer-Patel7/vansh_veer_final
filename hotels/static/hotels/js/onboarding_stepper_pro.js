// onboarding_stepper_pro.js
document.addEventListener('DOMContentLoaded', () => {
    let currentStep = 1;

    /**
     * Professional Toast Notification System
     */
    const showToast = (message, type = 'error') => {
        let toast = document.getElementById('onboarding-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'onboarding-toast';
            toast.className = 'onboarding-toast';
            document.body.appendChild(toast);
        }

        const icon = type === 'error' ? 'fa-exclamation-circle' : 'fa-check-circle';
        toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;

        toast.classList.add('show');
        setTimeout(() => toast.classList.remove('show'), 4000);
    };

    /**
     * Navigation: Transitions between steps
     */
    const showStep = (step) => {
        const steps = document.querySelectorAll('.onboarding-step');
        const activeStep = document.getElementById(`step-${step}`);

        if (!activeStep) return;

        // Visual Hide/Show
        steps.forEach(s => s.classList.remove('active'));
        activeStep.classList.add('active');

        // Update Stepper UI
        document.querySelectorAll('.step').forEach((s, idx) => {
            const stepIdx = idx + 1;
            const num = s.querySelector('.step-number');

            if (stepIdx === step) {
                s.className = 'step active';
                if (num) num.innerHTML = stepIdx;
            } else if (stepIdx < step) {
                s.className = 'step completed';
                if (num) num.innerHTML = '<i class="fas fa-check"></i>';
            } else {
                s.className = 'step';
                if (num) num.innerHTML = stepIdx;
            }
        });

        currentStep = step;
        console.log(`[Stepper] Transitioned to Step: ${step}`);
        window.scrollTo({ top: 0, behavior: 'smooth' });
    };

    /**
     * Professional Validation Interceptor
     */
    const isVisible = (el) => {
        if (!el || el.type === 'hidden') return false;
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden' && el.offsetParent !== null;
    };

    const validateCurrentStep = () => {
        console.group(`[Validation] Step ${currentStep}`);
        const stepContainer = document.getElementById(`step-${currentStep}`);
        if (!stepContainer) {
            console.groupEnd();
            return true;
        }

        const allRequired = stepContainer.querySelectorAll('input[required], select[required], textarea[required]');
        const inputs = Array.from(allRequired).filter(isVisible);

        console.log(`Analyzing ${inputs.length} visible required fields...`);

        let isValid = true;
        let firstErrorElement = null;

        stepContainer.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));

        inputs.forEach(input => {
            const fieldValid = input.checkValidity();
            console.log(`Field: ${input.name || input.id} | Valid: ${fieldValid} | Value: "${input.value}"`);
            if (!fieldValid) {
                input.classList.add('input-error');
                isValid = false;
                if (!firstErrorElement) firstErrorElement = input;
            }
        });

        const customSelects = stepContainer.querySelectorAll('.custom-select-container');
        customSelects.forEach(container => {
            const targetId = container.dataset.target;
            const hiddenSelect = document.getElementById(targetId);
            const selectBox = container.querySelector('.select-selected');

            if (hiddenSelect && hiddenSelect.required) {
                const hasValue = !!hiddenSelect.value;
                console.log(`Custom Select: ${targetId} | Has Value: ${hasValue} | Value: "${hiddenSelect.value}"`);
                if (!hasValue) {
                    if (selectBox) {
                        selectBox.classList.add('input-error', 'shake');
                        setTimeout(() => selectBox.classList.remove('shake'), 500);
                    }
                    isValid = false;
                    if (!firstErrorElement) firstErrorElement = container;
                }
            }
        });

        if (currentStep === 2) {
            console.log("[Validation] Running Step 2 Media Audit...");

            // 1. Property Gallery Audit
            const galleryPreviews = document.getElementById('galleryPreviewContainer');
            if (galleryPreviews && galleryPreviews.children.length < 5) {
                showToast(`Property Gallery requires at least 5 photos (Current: ${galleryPreviews.children.length})`);
                isValid = false;
                if (!firstErrorElement) firstErrorElement = document.getElementById('galleryUploadZone');
            }

            // 2. Room Inventory Media Audit
            const roomRows = document.querySelectorAll('.room-row');
            roomRows.forEach((row, idx) => {
                const previewBox = row.querySelector('.room-preview-box');
                const rowNum = idx + 1;
                if (previewBox && previewBox.children.length < 1) {
                    showToast(`Room Category #${rowNum} must have at least one photo.`);
                    isValid = false;
                    if (!firstErrorElement) firstErrorElement = row.querySelector('.room-upload-btn');
                }
            });
        }

        if (!isValid) {
            showToast('Please complete all mandatory fields and media requirements.');
            console.warn(`[Stepper] Navigation blocked by validation errors.`);
            if (firstErrorElement) firstErrorElement.scrollIntoView({ behavior: 'smooth', block: 'center' });
        } else {
            console.log(`[Stepper] Step ${currentStep} is fully validated.`);
        }

        console.groupEnd();
        return isValid;
    };

    /**
     * Reliable Event Delegation
     */
    document.addEventListener('click', (e) => {
        const target = e.target;
        const nextBtn = target.closest('.next-step');
        const prevBtn = target.closest('.prev-step');

        if (nextBtn) {
            e.preventDefault();
            e.stopPropagation();
            console.log(`[Click] Next button clicked. Current Step: ${currentStep}`);
            if (validateCurrentStep()) {
                showStep(currentStep + 1);
            }
        }

        if (prevBtn) {
            e.preventDefault();
            e.stopPropagation();
            console.log(`[Click] Prev button clicked. Target Step: ${currentStep - 1}`);
            showStep(currentStep - 1);
        }
    });

    window.nextStep = () => validateCurrentStep() && showStep(currentStep + 1);
    window.prevStep = () => showStep(currentStep - 1);

    // Initial show
    console.log('[Stepper] Initializing Step 1');
    showStep(1);
});
