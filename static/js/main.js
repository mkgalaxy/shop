// static/js/main.js
(function () {
    const toPersianNum = (n) => {
        const pNums = ['۰', '۱', '۲', '۳', '۴', '۵', '۶', '۷', '۸', '۹'];
        return n.toString().padStart(2, '0').split('').map(d => pNums[parseInt(d)] || d).join('');
    };

    // تاریخ امروز
    const dateEl = document.getElementById('current-jalali-date');
    if (dateEl) {
        dateEl.textContent = '۱۸ مهر ۱۴۰۵';
    }

    // تایمر معکوس
    let seconds = 42;
    let minutes = 38;
    let hours = 7;

    const secEl = document.getElementById('timer-sec');
    const minEl = document.getElementById('timer-min');
    const hourEl = document.getElementById('timer-hour');

    if (secEl && minEl && hourEl) {
        setInterval(() => {
            seconds--;
            if (seconds < 0) {
                seconds = 59;
                minutes--;
                if (minutes < 0) {
                    minutes = 59;
                    hours--;
                    if (hours < 0) {
                        hours = 23;
                    }
                    hourEl.textContent = toPersianNum(hours);
                }
                minEl.textContent = toPersianNum(minutes);
            }
            secEl.textContent = toPersianNum(seconds);
        }, 1000);
    }

    // منوی همبرگری موبایل
    const menuBtn = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');

    if (menuBtn && mobileMenu) {
        menuBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            mobileMenu.classList.toggle('hidden');
        });

        document.addEventListener('click', (e) => {
            if (!mobileMenu.contains(e.target) && !menuBtn.contains(e.target)) {
                mobileMenu.classList.add('hidden');
            }
        });
    }

    // سوییچ تم دارک و روشن
    const themeToggleBtn = document.getElementById('theme-toggle');
    const htmlEl = document.documentElement;

    if (localStorage.getItem('theme') === 'dark') {
        htmlEl.classList.add('dark');
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener('click', () => {
            htmlEl.classList.toggle('dark');
            if (htmlEl.classList.contains('dark')) {
                localStorage.setItem('theme', 'dark');
            } else {
                localStorage.setItem('theme', 'light');
            }
        });
    }
})();
// توابع پاپ‌آپ ورود و ثبت‌نام
window.openAuthModal = function() {
    const modal = document.getElementById('auth-modal');
    if (modal) modal.classList.remove('hidden');
};

window.closeAuthModal = function() {
    const modal = document.getElementById('auth-modal');
    if (modal) modal.classList.add('hidden');
};

window.flipToRegister = function() {
    const card = document.getElementById('auth-card');
    if (card) {
        card.style.transform = 'rotateY(180deg)';
    }
};

window.flipToLogin = function() {
    const card = document.getElementById('auth-card');
    if (card) {
        card.style.transform = 'rotateY(0deg)';
    }
};

// بستن پاپ‌آپ با کلیک روی بیرون از کادر
window.addEventListener('click', (e) => {
    const modal = document.getElementById('auth-modal');
    if (e.target === modal) {
        closeAuthModal();
    }
});