function showRejection() {
    const box = document.getElementById('rejection-box');
    const trigger = document.getElementById('reject-trigger');
    const submit = document.getElementById('reject-submit');
    if (box) box.style.display = 'block';
    if (trigger) trigger.style.display = 'none';
    if (submit) submit.style.display = 'block';
}
