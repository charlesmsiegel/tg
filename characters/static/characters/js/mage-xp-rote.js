document.addEventListener('DOMContentLoaded', function() {
    const rote_creation_toggle = document.getElementById('id_select_or_create_rote');
    const effect_creation_toggle = document.getElementById('id_select_or_create_effect');
    const rote_creation = document.getElementById('rote creation');
    const rote_selection = document.getElementById('rote selection');
    const effect_creation = document.getElementById('effect creation');
    const effect_selection = document.getElementById('effect selection');

    rote_creation_toggle.addEventListener('change', function() {
        if (this.checked) {
            rote_selection.classList.add("d-none");
            rote_creation.classList.remove("d-none");
        } else {
            rote_creation.classList.add("d-none");
            rote_selection.classList.remove("d-none");
        }
    });

    effect_creation_toggle.addEventListener('change', function() {
        if (this.checked) {
            effect_selection.classList.add("d-none");
            effect_creation.classList.remove("d-none");
        } else {
            effect_creation.classList.add("d-none");
            effect_selection.classList.remove("d-none");
        }
    });
});
