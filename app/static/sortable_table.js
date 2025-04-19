document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("sortable-table");
    const headers = table.querySelectorAll("th");
    const tbody = table.querySelector("tbody");
    const positionFilter = document.getElementById("position-filter");
    const teamFilter = document.getElementById("team-filter");

    // Sort table by column
    headers.forEach((header, index) => {
        header.addEventListener("click", () => {
            const rows = Array.from(tbody.querySelectorAll("tr"));
            const isAscending = header.classList.contains("asc");

            rows.sort((a, b) => {
                const aText = a.children[index].textContent.trim();
                const bText = b.children[index].textContent.trim();

                // Check if the column contains numeric values
                const aValue = isNaN(aText) ? aText : parseFloat(aText);
                const bValue = isNaN(bText) ? bText : parseFloat(bText);

                if (typeof aValue === "number" && typeof bValue === "number") {
                    return isAscending ? aValue - bValue : bValue - aValue;
                }

                return isAscending
                    ? aValue.toString().localeCompare(bValue.toString())
                    : bValue.toString().localeCompare(aValue.toString());
            });

            // Update the table with sorted rows
            tbody.innerHTML = "";
            rows.forEach(row => tbody.appendChild(row));

            // Update header classes for sorting direction
            headers.forEach(h => h.classList.remove("asc", "desc"));
            header.classList.toggle("asc", !isAscending);
            header.classList.toggle("desc", isAscending);
        });
    });

    // Filter table by position and team
    function filterTable() {
        const positionValue = positionFilter.value.toLowerCase();
        const teamValue = teamFilter.value.toLowerCase();

        Array.from(tbody.querySelectorAll("tr")).forEach(row => {
            const positionText = row.children[1].textContent.toLowerCase();
            const teamText = row.children[2].textContent.toLowerCase();

            const matchesPosition = !positionValue || positionText === positionValue;
            const matchesTeam = !teamValue || teamText === teamValue;

            row.style.display = matchesPosition && matchesTeam ? "" : "none";
        });
    }

    positionFilter.addEventListener("change", filterTable);
    teamFilter.addEventListener("change", filterTable);
});