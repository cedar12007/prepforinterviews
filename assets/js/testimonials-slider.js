/**
 * Testimonials Slider
 * Automatically rotates testimonials every 5 seconds
 * User interaction extends pause to 10 seconds
 */

(function () {
    'use strict';

    // Configuration
    const AUTO_SLIDE_INTERVAL = 5000; // 5 seconds
    const USER_INTERACTION_PAUSE = 10000; // 10 seconds after user interaction

    // State
    let currentSlide = 0;
    let autoSlideTimer = null;
    let isUserInteraction = false;
    let isManualPaused = false;

    // DOM Elements
    const slides = document.querySelectorAll('.testimonial-slide');
    const dots = document.querySelectorAll('.slider-dots .dot');
    const prevBtn = document.querySelector('.slider-btn.prev');
    const nextBtn = document.querySelector('.slider-btn.next');
    const pauseBtn = document.querySelector('.slider-btn.toggle-pause');
    const pauseIcon = document.querySelector('.pause-icon');
    const playIcon = document.querySelector('.play-icon');

    if (!slides.length) {
        console.warn('No testimonial slides found');
        return;
    }

    /**
     * Show a specific slide
     */
    function showSlide(index) {
        // Wrap around if needed
        if (index >= slides.length) {
            currentSlide = 0;
        } else if (index < 0) {
            currentSlide = slides.length - 1;
        } else {
            currentSlide = index;
        }

        // Update slides
        slides.forEach((slide, i) => {
            slide.classList.toggle('active', i === currentSlide);
        });

        // Update dots
        dots.forEach((dot, i) => {
            dot.classList.toggle('active', i === currentSlide);
        });
    }

    /**
     * Go to next slide
     */
    function nextSlide() {
        showSlide(currentSlide + 1);
    }

    /**
     * Go to previous slide
     */
    function prevSlide() {
        showSlide(currentSlide - 1);
    }

    /**
     * Start automatic sliding
     */
    function startAutoSlide(interval = AUTO_SLIDE_INTERVAL) {
        stopAutoSlide();
        if (!isManualPaused) {
            autoSlideTimer = setInterval(nextSlide, interval);
        }
    }

    /**
     * Stop automatic sliding
     */
    function stopAutoSlide() {
        if (autoSlideTimer) {
            clearInterval(autoSlideTimer);
            autoSlideTimer = null;
        }
    }

    /**
     * Toggle Pause/Play
     */
    function togglePause() {
        isManualPaused = !isManualPaused;

        if (isManualPaused) {
            stopAutoSlide();
            pauseIcon.style.display = 'none';
            playIcon.style.display = 'inline';
            pauseBtn.setAttribute('aria-label', 'Play testimonials');
        } else {
            pauseIcon.style.display = 'inline';
            playIcon.style.display = 'none';
            pauseBtn.setAttribute('aria-label', 'Pause testimonials');
            startAutoSlide(AUTO_SLIDE_INTERVAL);
        }
    }

    /**
     * Handle user interaction
     * Pauses auto-slide for longer duration
     */
    function handleUserInteraction(callback) {
        return function () {
            callback();

            if (!isManualPaused) {
                isUserInteraction = true;

                // Restart with longer pause after user interaction
                startAutoSlide(USER_INTERACTION_PAUSE);

                // After the first auto-slide following user interaction,
                // return to normal interval
                setTimeout(() => {
                    if (isUserInteraction && !isManualPaused) {
                        isUserInteraction = false;
                        startAutoSlide(AUTO_SLIDE_INTERVAL);
                    }
                }, USER_INTERACTION_PAUSE);
            }
        };
    }

    /**
     * Initialize slider
     */
    function init() {
        // Set up event listeners for navigation buttons
        if (prevBtn) {
            prevBtn.addEventListener('click', handleUserInteraction(prevSlide));
        }

        if (nextBtn) {
            nextBtn.addEventListener('click', handleUserInteraction(nextSlide));
        }

        if (pauseBtn) {
            pauseBtn.addEventListener('click', togglePause);
        }

        // Set up event listeners for dots
        dots.forEach((dot, index) => {
            dot.addEventListener('click', handleUserInteraction(() => {
                showSlide(index);
            }));
        });

        // Add keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (e.key === 'ArrowLeft') {
                handleUserInteraction(prevSlide)();
            } else if (e.key === 'ArrowRight') {
                handleUserInteraction(nextSlide)();
            } else if (e.key === ' ') { // Space bar to toggle pause
                // Prevent scrolling if user is not in a form
                if (document.activeElement.tagName !== 'INPUT' &&
                    document.activeElement.tagName !== 'TEXTAREA') {
                    e.preventDefault();
                    togglePause();
                }
            }
        });

        // Add touch/swipe support
        let touchStartX = 0;
        let touchEndX = 0;

        const sliderContainer = document.querySelector('.testimonials-slider');
        if (sliderContainer) {
            sliderContainer.addEventListener('touchstart', (e) => {
                touchStartX = e.changedTouches[0].screenX;
            }, { passive: true });

            sliderContainer.addEventListener('touchend', (e) => {
                touchEndX = e.changedTouches[0].screenX;
                handleSwipe();
            }, { passive: true });
        }

        function handleSwipe() {
            const swipeThreshold = 50;
            const diff = touchStartX - touchEndX;

            if (Math.abs(diff) > swipeThreshold) {
                if (diff > 0) {
                    // Swiped left - next slide
                    handleUserInteraction(nextSlide)();
                } else {
                    // Swiped right - previous slide
                    handleUserInteraction(prevSlide)();
                }
            }
        }

        // Pause on hover
        if (sliderContainer) {
            sliderContainer.addEventListener('mouseenter', () => {
                if (!isManualPaused) stopAutoSlide();
            });
            sliderContainer.addEventListener('mouseleave', () => {
                if (!isManualPaused) {
                    startAutoSlide(isUserInteraction ? USER_INTERACTION_PAUSE : AUTO_SLIDE_INTERVAL);
                }
            });
        }

        // Start automatic sliding
        startAutoSlide();
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
