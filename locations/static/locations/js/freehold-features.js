document.addEventListener('DOMContentLoaded', function() {
    const balefire = document.querySelector('[name="balefire"]');
    const size = document.querySelector('[name="size"]');
    const sanctuary = document.querySelector('[name="sanctuary"]');
    const resources = document.querySelector('[name="resources"]');
    const passages = document.querySelector('[name="passages"]');

    function calculatePoints() {
        const b = parseInt(balefire.value) || 0;
        const si = parseInt(size.value) || 0;
        const sa = parseInt(sanctuary.value) || 0;
        const r = parseInt(resources.value) || 0;
        const p = parseInt(passages.value) || 1;

        let total = b + si + sa + r;
        if (p > 1) {
            total += (p - 1);
        }

        const holdings = Math.ceil(total / 3);

        document.getElementById('totalPoints').textContent = total;
        document.getElementById('holdingsRequired').textContent = holdings;
    }

    [balefire, size, sanctuary, resources, passages].forEach(field => {
        field.addEventListener('change', calculatePoints);
        field.addEventListener('input', calculatePoints);
    });

    calculatePoints();
});
