// Handle chevron rotation on collapse toggle
document.addEventListener('DOMContentLoaded', function() {
    const collapseHeaders = document.querySelectorAll('[data-toggle="collapse"]');

    collapseHeaders.forEach(function(header) {
        const target = document.querySelector(header.getAttribute('data-target'));

        if (target) {
            target.addEventListener('show.bs.collapse', function() {
                header.setAttribute('aria-expanded', 'true');
            });

            target.addEventListener('hide.bs.collapse', function() {
                header.setAttribute('aria-expanded', 'false');
            });
        }
    });
});
