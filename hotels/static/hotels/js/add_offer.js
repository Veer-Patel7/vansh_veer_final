const pills = document.querySelectorAll('.premium-pill');
const typeInput = document.getElementById('offer_type_input');

pills.forEach(pill => {
    pill.addEventListener('click', () => {
        pills.forEach(p => p.classList.remove('active'));
        pill.classList.add('active');
        typeInput.value = pill.dataset.value;

        // Visual feedback for archetype switch
        pill.style.transform = 'scale(1.1)';
        setTimeout(() => pill.style.transform = '', 200);

        runCalc();
    });
});

const hSelect = document.getElementById('hotel_select');
const dVal = document.getElementById('discount_value');
const dType = document.getElementById('discount_type');
const rChecks = document.querySelectorAll('input[name="room_categories"]');

function formatCurrency(val) {
    return '₹' + Math.round(val).toLocaleString('en-IN');
}

function runCalc() {
    let maxBase = 0;
    const hotelId = hSelect.value;
    const allRows = document.querySelectorAll('.selection-row');

    allRows.forEach(row => {
        const isMatch = row.dataset.hotel === hotelId;
        row.style.display = isMatch ? 'flex' : 'none';
        if (isMatch) {
            row.style.animation = 'fadeIn 0.4s ease forwards';
        }
    });

    const checked = Array.from(rChecks).filter(c => c.checked && c.closest('.selection-row').style.display !== 'none');

    if (checked.length > 0) {
        maxBase = Math.max(...checked.map(c => parseFloat(c.closest('.selection-row').dataset.price)));
    } else {
        const visibleRows = Array.from(allRows).filter(r => r.style.display !== 'none');
        if (visibleRows.length > 0) {
            maxBase = Math.max(...visibleRows.map(r => parseFloat(r.dataset.price)));
        }
    }

    const discount = parseFloat(dVal.value) || 0;
    let final = maxBase;
    let savings = 0;

    if (dType.value === 'PERCENT') {
        final = maxBase * (1 - discount / 100);
        savings = discount;
    } else {
        final = maxBase - discount;
        savings = maxBase > 0 ? (discount / maxBase) * 100 : 0;
    }

    final = Math.max(0, final);

    // Dynamic Updates with micro-transitions
    const prevOld = document.getElementById('prev-old');
    const prevNew = document.getElementById('prev-new');
    const prevSavings = document.getElementById('prev-savings');

    prevOld.innerText = formatCurrency(maxBase);
    prevNew.innerText = formatCurrency(final);
    prevSavings.innerText = Math.round(savings) + '% REDUCTION';

    document.getElementById('prev-base').innerText = formatCurrency(maxBase);
    document.getElementById('prev-burn').innerText = '-' + formatCurrency(maxBase - final);
    document.getElementById('prev-net').innerText = formatCurrency(final);

    // Impact Animation
    prevNew.style.transform = 'scale(1.05)';
    prevNew.style.transition = 'transform 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275)';
    setTimeout(() => prevNew.style.transform = 'scale(1)', 200);
}

[hSelect, dVal, dType, ...rChecks].forEach(el => {
    el.addEventListener('input', runCalc);
    el.addEventListener('change', runCalc);
});

runCalc();

document.getElementById('strategyForm').onsubmit = function () {
    const b = document.querySelector('.btn-deploy');
    b.innerHTML = '<i class="fa-regular fa-spinner-third fa-spin"></i> SYNCING...';
    b.style.opacity = '0.7';
    b.style.pointerEvents = 'none';
};
