// Tailwind CSS Configuration
tailwind.config = {
    darkMode: 'class',
    theme: {
        extend: {
            colors: {
                primary: {
                    50: '#f0f9ff',
                    100: '#e0f2fe',
                    600: '#2563eb',
                    700: '#1d4ed8',
                    800: '#1e40af',
                    900: '#1e3a8a',
                    950: '#020617',
                }
            },
            fontFamily: {
                display: ['Outfit', 'sans-serif'],
                sans: ['Inter', 'sans-serif'],
            },
            borderRadius: {
                'large': '2.5rem',
            },
            animation: {
                'premium-slide': 'premiumSlide 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards',
            },
            keyframes: {
                premiumSlide: {
                    '0%': { opacity: '0', transform: 'translateY(20px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                }
            }
        }
    }
}

// Real-time booking notifications
let lastRef = null;

async function checkNewBookings() {
    try {
        // The API URL should be provided in data attribute of body
        const url = document.body.dataset.apiLatestBooking;
        if (!url) return;

        const res = await fetch(url);
        if (res.ok) {
            const data = await res.json();
            if (data.status === 'new' && data.ref !== lastRef) {
                lastRef = data.ref;
                showNotification(data);
            }
        }
    } catch (e) { /* silent fail */ }
}

function showNotification(booking) {
    const toast = document.createElement('div');
    toast.className = "fixed bottom-10 right-10 z-[100]";
    toast.style.background = "rgba(255, 255, 255, 0.95)";
    toast.style.backdropFilter = "blur(20px)";
    toast.style.padding = "2rem";
    toast.style.borderRadius = "2rem";
    toast.style.boxShadow = "0 25px 50px -12px rgba(0, 0, 0, 0.2)";
    toast.style.border = "1px solid rgba(0, 0, 0, 0.05)";
    toast.style.display = "flex";
    toast.style.alignItems = "center";
    toast.style.gap = "1.5rem";
    toast.innerHTML = `
        <div style="width: 3.5rem; height: 3.5rem; border-radius: 1rem; background: #2563eb; color: white; display: flex; align-items: center; justify-content: center; font-size: 1.25rem;">
            <i class="fas fa-bell"></i>
        </div>
        <div style="display: flex; flex-direction: column;">
            <span style="font-size: 0.625rem; font-weight: 900; color: #2563eb; text-transform: uppercase; letter-spacing: 0.1em; line-height: 1;">New Booking Received</span>
            <span style="font-size: 1rem; font-weight: 700; color: #0f172a; margin-top: 0.25rem;">${booking.guest} – ${booking.room}</span>
            <span style="font-size: 0.625rem; font-weight: 700; color: #94a3b8; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 0.25rem;">Ref: #${booking.ref}</span>
        </div>
        <button onclick="this.parentElement.remove()" style="width: 2.5rem; height: 2.5rem; border: none; background: transparent; color: #cbd5e1; cursor: pointer;">
            <i class="fas fa-times"></i>
        </button>
    `;
    document.body.appendChild(toast);
    setTimeout(() => toast.remove(), 10000);
}

document.addEventListener('DOMContentLoaded', () => {
    setInterval(checkNewBookings, 45000);

    // Global Delete Confirmation
    document.addEventListener('submit', (e) => {
        if (e.target && e.target.classList.contains('delete-confirm')) {
            const message = e.target.dataset.confirmMessage || 'Are you sure you want to delete this?';
            if (!confirm(message)) {
                e.preventDefault();
            }
        }
    });
});