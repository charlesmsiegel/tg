document.addEventListener('DOMContentLoaded', function() {
    const nameFilter = document.getElementById('nameFilter');
    const typeFilter = document.getElementById('typeFilter');
    const costFilter = document.getElementById('costFilter');
    const clearButton = document.getElementById('clearFilters');
    const resultCount = document.getElementById('resultCount');
    const thornItems = document.querySelectorAll('.thorn-item');

    function filterThorns() {
        const nameValue = nameFilter.value.toLowerCase();
        const typeValue = typeFilter.value;
        const costValue = costFilter.value;

        let visibleCount = 0;

        thornItems.forEach(function(item) {
            const itemName = item.getAttribute('data-name');
            const itemType = item.getAttribute('data-type');
            const itemCost = item.getAttribute('data-cost');

            let showItem = true;

            // Filter by name
            if (nameValue && !itemName.includes(nameValue)) {
                showItem = false;
            }

            // Filter by type
            if (typeValue && itemType !== typeValue) {
                showItem = false;
            }

            // Filter by cost
            if (costValue && itemCost !== costValue) {
                showItem = false;
            }

            item.style.display = showItem ? '' : 'none';
            if (showItem) visibleCount++;
        });

        // Update result count
        resultCount.textContent = `Showing ${visibleCount} of ${thornItems.length} thorns`;
    }

    // Add event listeners
    nameFilter.addEventListener('input', filterThorns);
    typeFilter.addEventListener('change', filterThorns);
    costFilter.addEventListener('change', filterThorns);

    clearButton.addEventListener('click', function() {
        nameFilter.value = '';
        typeFilter.value = '';
        costFilter.value = '';
        filterThorns();
    });

    // Initial count
    filterThorns();
});
