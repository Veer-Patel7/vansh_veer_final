document.addEventListener("DOMContentLoaded", function () {

    const tabs = document.querySelectorAll("#hotelTabs .nav-link");
    const input = document.getElementById("activeTabInput");

    // Tab click handle
    tabs.forEach(tab => {
        tab.addEventListener("click", function () {
            const tabName = this.getAttribute("data-tab");

            if (tabName && input) {
                input.value = tabName;
            }
        });
    });

    // URL se tab open karna
    const params = new URLSearchParams(window.location.search);
    const activeTab = params.get("tab");

    if (activeTab) {
        const tabBtn = document.querySelector(`#hotelTabs [data-tab="${activeTab}"]`);

        if (tabBtn) {
            tabBtn.click();

            if (input) {
                input.value = activeTab;
            }
        }
    }

});