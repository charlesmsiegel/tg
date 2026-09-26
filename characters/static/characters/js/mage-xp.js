document.addEventListener("DOMContentLoaded", function() {
    const categorySelectMenu = document.getElementById("id_category");
    const exampleElement = document.getElementById("example_wrap");
    const valueElement = document.getElementById("value_wrap");
    const resElement = document.getElementById("resonance_wrap");
    const noteElement = document.getElementById("note_wrap");
    const pooled_wrap = document.getElementById("pooled_wrap");
    const image_field_wrap = document.getElementById("image_field_wrap");
    const rote_wrap = document.getElementById("rote_wrap");

    var isGroupMember = document.getElementById("mage-xp-script").dataset.isGroupMember === "true";

    function updateVisibility() {
        const value = categorySelectMenu.value;

        // Reset all to hidden
        exampleElement.classList.add("d-none");
        valueElement.classList.add("d-none");
        resElement.classList.add("d-none");
        noteElement.classList.add("d-none");
        pooled_wrap.classList.add("d-none");
        image_field_wrap.classList.add("d-none");
        rote_wrap.classList.add("d-none");

        // Show fields based on category
        if (!["Willpower", "-----", "Rote Points", "Quintessence", "Rote", "Resonance", "Arete", "Image"].includes(value)) {
            exampleElement.classList.remove("d-none");
        }

        if (value === "Rote") {
            rote_wrap.classList.remove("d-none");
        }

        if (value === "MeritFlaw") {
            valueElement.classList.remove("d-none");
        }

        if (value === "Resonance") {
            resElement.classList.remove("d-none");
        }

        if (value === "Background") {
            noteElement.classList.remove("d-none");
            if (isGroupMember) {
                pooled_wrap.classList.remove("d-none");
            }
        }

        if (value === "Image") {
            image_field_wrap.classList.remove("d-none");
        }
    }

    categorySelectMenu.addEventListener("change", updateVisibility);

    // Initial visibility on page load
    updateVisibility();
});
