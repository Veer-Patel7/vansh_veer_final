/**
 * StepperManager - Professional Multi-Step Navigation & Validation
 */
class StepperManager {
    constructor() {
        this.currentStep = 1;
        this.steps = document.querySelectorAll('.onboarding-step');
        this.stepperIcons = document.querySelectorAll('.step');
        this.toast = this.initToast();

        this.init();
    }

    init() {
        this.setupNavigation();
        this.showStep(1);
    }

    initToast() {
        let toast = document.getElementById('onboarding-toast');
        if (!toast) {
            toast = document.createElement('div');
            toast.id = 'onboarding-toast';
            toast.className = 'onboarding-toast';
            document.body.appendChild(toast);
        }
        return toast;
    }

    showToast(message, type = 'error') {
        const icon = type === 'error' ? 'fa-exclamation-circle' : 'fa-check-circle';
        this.toast.innerHTML = `<i class="fas ${icon}"></i> <span>${message}</span>`;
        this.toast.classList.add('show');
        setTimeout(() => this.toast.classList.remove('show'), 4000);
    }

    showStep(step) {
        const activeStep = document.getElementById(`step-${step}`);
        if (!activeStep) return;

        // Transitions
        this.steps.forEach(s => s.classList.remove('active'));
        activeStep.classList.add('active');

        // Stepper Breadcrumbs
        this.stepperIcons.forEach((s, idx) => {
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

        this.currentStep = step;
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    validateStep() {
        const stepContainer = document.getElementById(`step-${this.currentStep}`);
        if (!stepContainer) return true;

        const inputs = Array.from(stepContainer.querySelectorAll('input[required], select[required], textarea[required]'))
            .filter(el => this.isVisible(el));

        let isValid = true;
        let firstErr = null;

        // Reset errors
        stepContainer.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));

        // Basic Validity
        inputs.forEach(input => {
            if (!input.checkValidity()) {
                input.classList.add('input-error');
                isValid = false;
                if (!firstErr) firstErr = input;
            }
        });

        // Custom Media Audits
        if (this.currentStep === 2) {
            const gallery = document.getElementById('galleryPreviewContainer');
            if (gallery && gallery.children.length < 5) {
                this.showToast('Property Gallery requires at least 5 photos.');
                isValid = false;
            }
        }

        if (!isValid) {
            this.showToast('Please complete all mandatory fields.');
            if (firstErr) firstErr.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }

        return isValid;
    }

    isVisible(el) {
        if (!el || el.type === 'hidden') return false;
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden' && el.offsetParent !== null;
    }

    setupNavigation() {
        document.addEventListener('click', (e) => {
            const nextBtn = e.target.closest('.next-step');
            const prevBtn = e.target.closest('.prev-step');

            if (nextBtn) {
                e.preventDefault();
                if (this.validateStep()) {
                    const nextStep = this.currentStep + 1;
                    this.showStep(nextStep);
                    if (nextStep === 4 && window.summaryEngine) {
                        window.summaryEngine.render();
                    }
                }
            }

            if (prevBtn) {
                e.preventDefault();
                this.showStep(this.currentStep - 1);
            }
        });
    }
}

// Global instance
document.addEventListener('DOMContentLoaded', () => {
    window.stepperManager = new StepperManager();
});
