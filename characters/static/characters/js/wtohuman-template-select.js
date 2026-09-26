// Highlight selected template
document.querySelectorAll('.template-option').forEach(option => {
    option.addEventListener('click', function(e) {
        // Remove previous selection
        document.querySelectorAll('.template-card').forEach(card => {
            card.style.borderColor = 'rgba(0,0,0,0.1)';
            card.style.boxShadow = 'none';
        });

        // Highlight this one
        const card = this.querySelector('.template-card');
        card.style.borderColor = 'var(--wto-primary, #4B0082)';
        card.style.boxShadow = '0 4px 12px rgba(75, 0, 130, 0.15)';

        // Check the radio button
        this.querySelector('input[type="radio"]').checked = true;
    });

    // Add hover effect
    const card = option.querySelector('.template-card');
    option.addEventListener('mouseenter', function() {
        if (!this.querySelector('input[type="radio"]').checked) {
            card.style.borderColor = 'rgba(75, 0, 130, 0.3)';
        }
    });
    option.addEventListener('mouseleave', function() {
        if (!this.querySelector('input[type="radio"]').checked) {
            card.style.borderColor = 'rgba(0,0,0,0.1)';
        }
    });
});

// Select "Build from Scratch" by default
document.querySelector('input[type="radio"][value=""]').checked = true;
document.querySelector('input[type="radio"][value=""]').closest('.template-option').click();
