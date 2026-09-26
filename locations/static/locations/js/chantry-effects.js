document.addEventListener('DOMContentLoaded', function() {
    // Select all elements with data-toggle="toggle"
    const effect_creation_toggle = document.getElementById('id_select_or_create');
    const effect_creation = document.getElementById('effect creation');
    const effect_selection = document.getElementById('effect selection');

    effect_creation_toggle.addEventListener('change', function() {
        if ($(this).prop('checked')) {
            effect_selection.classList.add("d-none");
            effect_creation.classList.remove("d-none");
        } else {
            effect_selection.classList.add("d-none")
            effect_creation.classList.remove("d-none")
        }
    });
});
