// WorkHere Presentation Navigation
document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const navDots = document.querySelectorAll('.nav-dot');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    let currentSlide = 0;

    // Navigate to specific slide
    function goToSlide(index) {
        if (index < 0) index = 0;
        if (index >= slides.length) index = slides.length - 1;
        
        currentSlide = index;
        slides[index].scrollIntoView({ behavior: 'smooth' });
        updateNavDots();
    }

    // Update navigation dots
    function updateNavDots() {
        navDots.forEach((dot, index) => {
            dot.classList.toggle('active', index === currentSlide);
        });
    }

    // Navigation dot clicks
    navDots.forEach((dot, index) => {
        dot.addEventListener('click', () => goToSlide(index));
    });

    // Arrow navigation
    prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
            e.preventDefault();
            goToSlide(currentSlide + 1);
        } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft' || e.key === 'PageUp') {
            e.preventDefault();
            goToSlide(currentSlide - 1);
        } else if (e.key === 'Home') {
            e.preventDefault();
            goToSlide(0);
        } else if (e.key === 'End') {
            e.preventDefault();
            goToSlide(slides.length - 1);
        }
    });

    // Scroll detection to update current slide
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const slideIndex = parseInt(entry.target.dataset.slide);
                currentSlide = slideIndex;
                updateNavDots();
            }
        });
    }, {
        threshold: 0.5
    });

    slides.forEach(slide => observer.observe(slide));

    // Animate metrics on scroll
    const metricCards = document.querySelectorAll('.metric-card');
    const metricObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const fill = entry.target.querySelector('.metric-fill');
                if (fill) {
                    const width = fill.style.width;
                    fill.style.width = '0%';
                    setTimeout(() => {
                        fill.style.width = width;
                    }, 100);
                }
            }
        });
    }, { threshold: 0.5 });

    metricCards.forEach(card => metricObserver.observe(card));

    // Add hover effect to stat numbers
    const statNumbers = document.querySelectorAll('.stat-number, .metric-number, .geo-number');
    statNumbers.forEach(num => {
        num.addEventListener('mouseenter', () => {
            num.style.transform = 'scale(1.05)';
            num.style.transition = 'transform 0.3s ease';
        });
        num.addEventListener('mouseleave', () => {
            num.style.transform = 'scale(1)';
        });
    });

    // Parallax effect on mascot
    const mascot = document.querySelector('.mascot');
    if (mascot) {
        document.addEventListener('mousemove', (e) => {
            const x = (e.clientX / window.innerWidth - 0.5) * 20;
            const y = (e.clientY / window.innerHeight - 0.5) * 20;
            mascot.style.transform = `translate(${x}px, ${y}px)`;
        });
    }

    // Touch swipe support
    let touchStartY = 0;
    let touchEndY = 0;

    document.addEventListener('touchstart', (e) => {
        touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });

    document.addEventListener('touchend', (e) => {
        touchEndY = e.changedTouches[0].screenY;
        handleSwipe();
    }, { passive: true });

    function handleSwipe() {
        const swipeThreshold = 50;
        const diff = touchStartY - touchEndY;
        
        if (Math.abs(diff) > swipeThreshold) {
            if (diff > 0) {
                goToSlide(currentSlide + 1);
            } else {
                goToSlide(currentSlide - 1);
            }
        }
    }

    // Preload animation
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.5s ease';
    
    window.addEventListener('load', () => {
        document.body.style.opacity = '1';
    });
});
