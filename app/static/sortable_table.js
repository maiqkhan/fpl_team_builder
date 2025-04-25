document.addEventListener("DOMContentLoaded", () => {
    const table = document.getElementById("sortable-table");
    const headers = table.querySelectorAll("th");
    const tbody = table.querySelector("tbody");
    const positionFilter = document.getElementById("position-filter");
    const teamFilter = document.getElementById("team-filter");
    const gameweekFilter = document.getElementById("gameweek-filter");
    const applyFiltersButton = document.getElementById("apply-filters");

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

    // Function to apply filters
    function applyFilters() {
        const positionValue = positionFilter.value.toLowerCase();
        const teamValue = teamFilter.value.toLowerCase();
        // const gameweekValue = gameweekFilter.value;

        Array.from(tbody.querySelectorAll("tr")).forEach(row => {
            const positionText = row.children[1].textContent.toLowerCase();
            const teamText = row.children[2].textContent.toLowerCase();
            // const gameweekText = row.dataset.gameweek; // Assuming gameweek data is stored in a data attribute

            const matchesPosition = positionValue === "all" || !positionValue || positionText === positionValue;
            const matchesTeam = teamValue === "all" || !teamValue || teamText === teamValue;
            //const matchesGameweek = !gameweekValue || parseInt(gameweekText) <= parseInt(gameweekValue);
            //console.log(gameweekValue, row.dataset.gameweek, matchesGameweek);
            row.style.display = matchesPosition && matchesTeam ? "" : "none"; // && matchesGameweek 
        });
    }

    // Add event listener to the "Apply Filters" button
    applyFiltersButton.addEventListener("click", applyFilters);
});