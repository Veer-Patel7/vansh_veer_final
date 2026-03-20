document.addEventListener("DOMContentLoaded", function () {

    const searchInput = document.getElementById("ownerSearch");

    if (!searchInput) return;

    searchInput.addEventListener("keyup", function () {

        const value = this.value.toLowerCase();
        const rows = document.querySelectorAll(".sa-table tbody tr");

        rows.forEach(row => {

            const cols = row.querySelectorAll("td");

            if (cols.length < 3) return;

            const id = cols[0].innerText.toLowerCase();
            const name = cols[1].innerText.toLowerCase();
            const email = cols[2].innerText.toLowerCase();

            if (
                id.includes(value) ||
                name.includes(value) ||
                email.includes(value)
            ) {
                row.style.display = "";
            } else {
                row.style.display = "none";
            }

        });

    });

});