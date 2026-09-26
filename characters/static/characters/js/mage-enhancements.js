document.addEventListener("DOMContentLoaded", function() {
    const styleSelectMenu = document.getElementById("id_enhancement_style");
    const typeSelectMenu = document.getElementById("id_enhancement_type");
    const effectSelectMenu = document.getElementById("id_new_device_new_power_option");

    const attributeElements = document.getElementById("attributes");
    const deviceElements = document.getElementById("device");
    const ndeviceElements = document.getElementById("new_device");
    const powerSelectElements = document.getElementById("new_device_power_select");
    const newPowerElements = document.getElementById("new_device_new_power");



    typeSelectMenu.addEventListener("change", function() {
        const selectedValue = this.value;
        // Update the class of the element
        if(selectedValue == "Attributes"){
            attributeElements.classList.remove("d-none");
        }
        else {
            attributeElements.classList.add("d-none");
        }

        if(selectedValue == "Existing Device"){
            deviceElements.classList.remove("d-none");
        }
        else {
            deviceElements.classList.add("d-none");
        }

        if(selectedValue == "New Device"){
            ndeviceElements.classList.remove("d-none");
        }
        else {
            ndeviceElements.classList.add("d-none");
        }

    });

    effectSelectMenu.addEventListener("change", function() {
        const selectedValue = this.value;
        // Update the class of the element
        if(selectedValue == "New Effect"){
            newPowerElements.classList.remove("d-none");
            powerSelectElements.classList.add("d-none");
        }
        else {
            newPowerElements.classList.add("d-none");
            powerSelectElements.classList.remove("d-none");
        }

    });
});
