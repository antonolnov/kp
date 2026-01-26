// WorkHere Presentation - Clean Navigation & Animations

document.addEventListener('DOMContentLoaded', () => {
    const slides = document.querySelectorAll('.slide');
    const totalSlides = slides.length;
    const currentSlideEl = document.getElementById('currentSlide');
    const totalSlidesEl = document.getElementById('totalSlides');
    const progressFill = document.getElementById('progressFill');
    const prevBtn = document.getElementById('prevBtn');
    const nextBtn = document.getElementById('nextBtn');
    
    let currentSlide = 0;
    
    // Initialize
    totalSlidesEl.textContent = String(totalSlides).padStart(2, '0');
    updateUI();
    
    // Navigation functions
    function goToSlide(index) {
        if (index < 0) index = 0;
        if (index >= totalSlides) index = totalSlides - 1;
        
        currentSlide = index;
        slides[index].scrollIntoView({ behavior: 'smooth' });
        updateUI();
    }
    
    function updateUI() {
        currentSlideEl.textContent = String(currentSlide + 1).padStart(2, '0');
        
        const progress = ((currentSlide + 1) / totalSlides) * 100;
        progressFill.style.width = `${progress}%`;
    }
    
    // Button navigation
    prevBtn.addEventListener('click', () => goToSlide(currentSlide - 1));
    nextBtn.addEventListener('click', () => goToSlide(currentSlide + 1));
    
    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        switch(e.key) {
            case 'ArrowDown':
            case 'ArrowRight':
            case ' ':
            case 'PageDown':
                e.preventDefault();
                goToSlide(currentSlide + 1);
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
            case 'PageUp':
                e.preventDefault();
                goToSlide(currentSlide - 1);
                break;
            case 'Home':
                e.preventDefault();
                goToSlide(0);
                break;
            case 'End':
                e.preventDefault();
                goToSlide(totalSlides - 1);
                break;
        }
    });
    
    // Scroll detection
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                currentSlide = parseInt(entry.target.dataset.slide);
                updateUI();
                
                // Trigger animations for this slide
                animateSlide(entry.target);
            }
        });
    }, { threshold: 0.5 });
    
    slides.forEach(slide => observer.observe(slide));
    
    // Touch navigation
    let touchStartY = 0;
    
    document.addEventListener('touchstart', (e) => {
        touchStartY = e.changedTouches[0].screenY;
    }, { passive: true });
    
    document.addEventListener('touchend', (e) => {
        const touchEndY = e.changedTouches[0].screenY;
        const diff = touchStartY - touchEndY;
        
        if (Math.abs(diff) > 50) {
            if (diff > 0) {
                goToSlide(currentSlide + 1);
            } else {
                goToSlide(currentSlide - 1);
            }
        }
    }, { passive: true });
    
    // Animate slide elements
    function animateSlide(slide) {
        // Animate stat numbers
        const statNumbers = slide.querySelectorAll('.stat-number[data-target]');
        statNumbers.forEach(num => {
            animateNumber(num, parseInt(num.dataset.target));
        });
        
        // Animate stat bars
        const statBars = slide.querySelectorAll('.stat-bar-fill');
        statBars.forEach(bar => {
            bar.style.width = '0%';
            setTimeout(() => {
                bar.style.width = bar.style.getPropertyValue('--width');
            }, 100);
        });
        
        // Add visible class to cards for staggered animation
        const cards = slide.querySelectorAll('.value-item, .feature-card, .metric-card, .capability-row, .pipeline-item');
        cards.forEach((card, i) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(20px)';
            setTimeout(() => {
                card.style.transition = 'all 0.5s ease';
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 + i * 80);
        });
    }
    
    // Animate number counting
    function animateNumber(element, target) {
        const duration = 2000;
        const start = 0;
        const startTime = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOut = 1 - Math.pow(1 - progress, 3);
            
            const current = Math.round(start + (target - start) * easeOut);
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        requestAnimationFrame(update);
    }
    
    // Parallax effect on hero cards
    const heroVisual = document.querySelector('.hero-visual');
    if (heroVisual) {
        document.addEventListener('mousemove', (e) => {
            const cards = heroVisual.querySelectorAll('.hero-card');
            const x = (e.clientX / window.innerWidth - 0.5) * 20;
            const y = (e.clientY / window.innerHeight - 0.5) * 20;
            
            cards.forEach((card, i) => {
                const factor = (i + 1) * 0.5;
                card.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
            });
        });
    }
    
    // Initial animation for first slide
    setTimeout(() => {
        animateSlide(slides[0]);
    }, 300);
    
    // Fade in body
    document.body.style.opacity = '0';
    document.body.style.transition = 'opacity 0.4s ease';
    
    window.addEventListener('load', () => {
        document.body.style.opacity = '1';
    });
});
