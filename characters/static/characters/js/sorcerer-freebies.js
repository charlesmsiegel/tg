document.addEventListener("DOMContentLoaded", function() {
    const categorySelectMenu = document.getElementById("id_category");
    const exampleElement = document.getElementById("example_wrap");
    const valueElement = document.getElementById("value_wrap");
    const noteElement = document.getElementById("note_wrap");
    const practiceElement = document.getElementById("practice_wrap");
    const abilityElement = document.getElementById("ability_wrap");
    const createritualformElement = document.getElementById("id_create_ritual_form");

    function updateVisibility() {
        const value = categorySelectMenu.value;

        // Reset all to hidden
        exampleElement.classList.add("d-none");
        valueElement.classList.add("d-none");
        noteElement.classList.add("d-none");
        practiceElement.classList.add("d-none");
        abilityElement.classList.add("d-none");
        createritualformElement.classList.add("d-none");

        // Show fields based on category
        if (!["Willpower", "-----", "Create Ritual"].includes(value)) {
            exampleElement.classList.remove("d-none");
        }

        if (value === "MeritFlaw" || value === "Advantage") {
            valueElement.classList.remove("d-none");
        }

        if (value === "Background") {
            noteElement.classList.remove("d-none");
        }

        if (value === "New Path" && document.getElementById("sorcerer-freebies-script").dataset.sorcererType === "hedge_mage") {
            practiceElement.classList.remove("d-none");
            abilityElement.classList.remove("d-none");
        }

        if (value === "Create Ritual") {
            createritualformElement.classList.remove("d-none");
        }
    }

    categorySelectMenu.addEventListener("change", updateVisibility);

    // Initial visibility on page load
    updateVisibility();
});
