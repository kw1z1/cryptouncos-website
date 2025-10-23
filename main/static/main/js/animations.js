// main/static/main/js/animations.js

// Анимация чисел в статистике
function animateNumbers() {
    const statNumbers = document.querySelectorAll('.stat-number');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.getAttribute('data-target'));
        const duration = 2000; // 2 секунды
        const step = target / (duration / 16); // 60 FPS
        let current = 0;
        
        const timer = setInterval(() => {
            current += step;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            stat.textContent = Math.floor(current) + (target > 100 ? '+' : '');
        }, 16);
    });
}

// Запуск анимации при скролле
function isElementInViewport(el) {
    const rect = el.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

function checkAnimation() {
    const statsSection = document.querySelector('.statistics');
    if (statsSection && isElementInViewport(statsSection)) {
        animateNumbers();
        window.removeEventListener('scroll', checkAnimation);
    }
}

// Инициализация при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    window.addEventListener('scroll', checkAnimation);
    // Проверяем сразу, если секция уже в viewport
    checkAnimation();
});