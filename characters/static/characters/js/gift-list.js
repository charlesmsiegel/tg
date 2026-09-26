document.addEventListener('DOMContentLoaded', function() {
    const nameFilter = document.getElementById('nameFilter');
    const rankFilter = document.getElementById('rankFilter');
    const typeFilter = document.getElementById('typeFilter');
    const clearButton = document.getElementById('clearFilters');
    const resultCount = document.getElementById('resultCount');
    const giftItems = document.querySelectorAll('.gift-item');

    function filterGifts() {
        const nameValue = nameFilter.value.toLowerCase();
        const rankValue = rankFilter.value;
        const typeValue = typeFilter.value;

        let visibleCount = 0;

        giftItems.forEach(function(item) {
            const itemName = item.getAttribute('data-name');
            const itemRank = item.getAttribute('data-rank');
            const itemAllowed = item.getAttribute('data-allowed');

            let showItem = true;

            // Filter by name
            if (nameValue && !itemName.includes(nameValue)) {
                showItem = false;
            }

            // Filter by rank/level
            if (rankValue && itemRank !== rankValue) {
                showItem = false;
            }

            // Filter by allowed type
            if (typeValue) {
                const allowedIds = itemAllowed.split(',').filter(id => id !== '');
                if (!allowedIds.includes(typeValue)) {
                    showItem = false;
                }
            }

            item.style.display = showItem ? '' : 'none';
            if (showItem) visibleCount++;
        });

        // Update result count
        resultCount.textContent = `Showing ${visibleCount} of ${giftItems.length} gifts`;
    }

    // Add event listeners
    nameFilter.addEventListener('input', filterGifts);
    rankFilter.addEventListener('change', filterGifts);
    typeFilter.addEventListener('change', filterGifts);

    clearButton.addEventListener('click', function() {
        nameFilter.value = '';
        rankFilter.value = '';
        typeFilter.value = '';
        filterGifts();
    });

    // Initial count
    filterGifts();
});
