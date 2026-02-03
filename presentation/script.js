/**
 * WorkHere Presentation — Crazy Designer Edition
 * Interactive slide navigation and animations
 */

class Presentation {
    constructor() {
        this.slides = document.querySelectorAll('.slide');
        this.currentSlide = 0;
        this.totalSlides = this.slides.length;
        this.isAnimating = false;
        
        this.init();
    }
    
    init() {
        // Update total slides counter
        document.getElementById('totalSlides').textContent = 
            this.totalSlides.toString().padStart(2, '0');
        
        // Navigation buttons
        document.getElementById('prevBtn').addEventListener('click', () => this.prev());
        document.getElementById('nextBtn').addEventListener('click', () => this.next());
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => this.handleKeyboard(e));
        
        // Scroll navigation
        this.setupScrollNavigation();
        
        // Touch navigation
        this.setupTouchNavigation();
        
        // Intersection Observer for animations
        this.setupIntersectionObserver();
        
        // Animate numbers on scroll
        this.setupNumberAnimations();
        
        // Initial state
        this.goToSlide(0);
    }
    
    setupScrollNavigation() {
        let lastScrollTime = 0;
        const scrollCooldown = 800;
        
        window.addEventListener('wheel', (e) => {
            const now = Date.now();
            if (now - lastScrollTime < scrollCooldown) return;
            
            if (e.deltaY > 50) {
                this.next();
                lastScrollTime = now;
            } else if (e.deltaY < -50) {
                this.prev();
                lastScrollTime = now;
            }
        }, { passive: true });
    }
    
    setupTouchNavigation() {
        let touchStartY = 0;
        let touchEndY = 0;
        
        document.addEventListener('touchstart', (e) => {
            touchStartY = e.changedTouches[0].screenY;
        }, { passive: true });
        
        document.addEventListener('touchend', (e) => {
            touchEndY = e.changedTouches[0].screenY;
            const diff = touchStartY - touchEndY;
            
            if (Math.abs(diff) > 50) {
                if (diff > 0) {
                    this.next();
                } else {
                    this.prev();
                }
            }
        }, { passive: true });
    }
    
    setupIntersectionObserver() {
        const options = {
            root: null,
            rootMargin: '0px',
            threshold: 0.5
        };
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const slideIndex = parseInt(entry.target.dataset.slide);
                    this.currentSlide = slideIndex;
                    this.updateUI();
                    
                    // Trigger animations
                    entry.target.classList.add('visible');
                    this.animateSlideElements(entry.target);
                }
            });
        }, options);
        
        this.slides.forEach(slide => observer.observe(slide));
    }
    
    setupNumberAnimations() {
        const numbers = document.querySelectorAll('.stat-number[data-target]');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    this.animateNumber(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        numbers.forEach(num => observer.observe(num));
    }
    
    animateNumber(element) {
        const target = parseInt(element.dataset.target);
        const duration = 2000;
        const start = 0;
        const startTime = performance.now();
        
        const animate = (currentTime) => {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            
            // Easing function
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(start + (target - start) * easeOutQuart);
            
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        requestAnimationFrame(animate);
    }
    
    animateSlideElements(slide) {
        // Animate cards with stagger
        const cards = slide.querySelectorAll('.problem-card, .audience-card, .ai-feature, .result-card, .case-card, .security-item, .custom-item, .module-card');
        cards.forEach((card, index) => {
            card.style.animationDelay = `${index * 0.1}s`;
        });
        
        // Animate funnel steps
        const funnelSteps = slide.querySelectorAll('.funnel-step');
        funnelSteps.forEach((step, index) => {
            setTimeout(() => {
                step.style.opacity = '1';
                step.style.transform = 'translateY(0)';
            }, index * 100);
        });
        
        // Animate kanban cards
        const kanbanCards = slide.querySelectorAll('.kanban-card');
        kanbanCards.forEach((card, index) => {
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateX(0)';
            }, index * 50);
        });
    }
    
    handleKeyboard(e) {
        switch(e.key) {
            case 'ArrowDown':
            case 'ArrowRight':
            case ' ':
            case 'PageDown':
                e.preventDefault();
                this.next();
                break;
            case 'ArrowUp':
            case 'ArrowLeft':
            case 'PageUp':
                e.preventDefault();
                this.prev();
                break;
            case 'Home':
                e.preventDefault();
                this.goToSlide(0);
                break;
            case 'End':
                e.preventDefault();
                this.goToSlide(this.totalSlides - 1);
                break;
        }
    }
    
    next() {
        if (this.currentSlide < this.totalSlides - 1) {
            this.goToSlide(this.currentSlide + 1);
        }
    }
    
    prev() {
        if (this.currentSlide > 0) {
            this.goToSlide(this.currentSlide - 1);
        }
    }
    
    goToSlide(index) {
        if (this.isAnimating || index < 0 || index >= this.totalSlides) return;
        
        this.isAnimating = true;
        this.currentSlide = index;
        
        // Smooth scroll to slide
        this.slides[index].scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
        
        this.updateUI();
        
        // Reset animation lock
        setTimeout(() => {
            this.isAnimating = false;
        }, 800);
    }
    
    updateUI() {
        // Update slide counter
        document.getElementById('currentSlide').textContent = 
            (this.currentSlide + 1).toString().padStart(2, '0');
        
        // Update progress bar
        const progress = ((this.currentSlide + 1) / this.totalSlides) * 100;
        document.getElementById('progressFill').style.width = `${progress}%`;
        
        // Update button states
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        prevBtn.style.opacity = this.currentSlide === 0 ? '0.3' : '1';
        nextBtn.style.opacity = this.currentSlide === this.totalSlides - 1 ? '0.3' : '1';
    }
}

// Parallax effect for hero blobs
function setupParallax() {
    const blobs = document.querySelectorAll('.blob');
    
    window.addEventListener('mousemove', (e) => {
        const x = (e.clientX / window.innerWidth - 0.5) * 30;
        const y = (e.clientY / window.innerHeight - 0.5) * 30;
        
        blobs.forEach((blob, index) => {
            const factor = (index + 1) * 0.5;
            blob.style.transform = `translate(${x * factor}px, ${y * factor}px)`;
        });
    });
}

// Glitch effect enhancement
function setupGlitchEffect() {
    const glitchElement = document.querySelector('.glitch');
    if (!glitchElement) return;
    
    setInterval(() => {
        glitchElement.classList.add('glitch-active');
        setTimeout(() => {
            glitchElement.classList.remove('glitch-active');
        }, 100);
    }, 3000);
}

// Typing effect for subtitle
function setupTypingEffect() {
    const subtitle = document.querySelector('.hero-subtitle');
    if (!subtitle) return;
    
    const originalText = subtitle.innerHTML;
    // Could add typing animation here if desired
}

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded', () => {
    new Presentation();
    setupParallax();
    setupGlitchEffect();
    setupTypingEffect();
    
    console.log('🚀 WorkHere Presentation Loaded');
    console.log('Use Arrow keys, Space, or Scroll to navigate');
});

// Easter egg
let konamiCode = [];
const konamiSequence = ['ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown', 'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight', 'b', 'a'];

document.addEventListener('keydown', (e) => {
    konamiCode.push(e.key);
    konamiCode = konamiCode.slice(-10);
    
    if (konamiCode.join(',') === konamiSequence.join(',')) {
        document.body.style.animation = 'rainbow 2s infinite';
        console.log('🎉 Konami Code activated!');
    }
});

// Add rainbow animation
const style = document.createElement('style');
style.textContent = `
@keyframes rainbow {
    0% { filter: hue-rotate(0deg); }
    100% { filter: hue-rotate(360deg); }
}
`;
document.head.appendChild(style);
