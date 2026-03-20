document.addEventListener('DOMContentLoaded', () => {

    const modal = document.getElementById('rejectModal');
    const openBtn = document.getElementById('openRejectModal');
    const closeBtn = document.getElementById('closeRejectModal');

    if (openBtn) {
        openBtn.addEventListener('click', () => {
            modal.style.display = 'flex';
        });
    }

    if (closeBtn) {
        closeBtn.addEventListener('click', () => {
            modal.style.display = 'none';
        });
    }

    // Close on outside click
    window.addEventListener('click', (e) => {
        if (e.target === modal) modal.style.display = 'none';
    });

});

// Smart Back Function
function smartBack(){
    const ref = document.referrer;

    if(ref.includes("/super/dashboard")){
        window.location.href = "/super/dashboard/";
    }
    else if(ref.includes("/super/hotels")){
        window.location.href = "/super/hotels/";
    }
    else{
        window.history.back();
    }
}