document.addEventListener('DOMContentLoaded', function() {
    const selectAllCheckbox = document.getElementById('select-all-checkbox');
    const selectAllBtn = document.getElementById('select-all-btn');
    const batchApproveBtn = document.getElementById('batch-approve-btn');
    const selectedCountSpan = document.getElementById('selected-count');
    const checkboxes = document.querySelectorAll('.request-checkbox');

    function updateSelectedCount() {
        const checked = document.querySelectorAll('.request-checkbox:checked').length;
        selectedCountSpan.textContent = checked;
        batchApproveBtn.disabled = checked === 0;
        selectAllCheckbox.checked = checked === checkboxes.length && checkboxes.length > 0;
        selectAllCheckbox.indeterminate = checked > 0 && checked < checkboxes.length;
    }

    selectAllCheckbox.addEventListener('change', function() {
        checkboxes.forEach(cb => cb.checked = this.checked);
        updateSelectedCount();
    });

    selectAllBtn.addEventListener('click', function() {
        const allChecked = document.querySelectorAll('.request-checkbox:checked').length === checkboxes.length;
        checkboxes.forEach(cb => cb.checked = !allChecked);
        updateSelectedCount();
        this.textContent = allChecked ? 'Select All' : 'Deselect All';
    });

    checkboxes.forEach(cb => cb.addEventListener('change', updateSelectedCount));
});
