document.addEventListener('DOMContentLoaded', function () {

    // Navbar background on scroll
    const navbar = document.querySelector('.navbar-custom');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        }, { passive: true });
    }

    // Animate elements on scroll
    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-fade-in');
            }
        });
    }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });

    document.querySelectorAll('.animate-fade').forEach(el => observer.observe(el));

    // Initialize Bootstrap tooltips lazily
    if (typeof bootstrap !== 'undefined') {
        const tooltips = document.querySelectorAll('[data-bs-toggle="tooltip"]');
        if (tooltips.length > 0) {
            [].slice.call(tooltips).map(el => new bootstrap.Tooltip(el));
        }
    }

    // Lite YouTube Embeds
    document.addEventListener('click', function (e) {
        const target = e.target.closest('.lite-youtube');
        if (target && !target.querySelector('iframe')) {
            const videoId = target.getAttribute('data-video-id');
            target.innerHTML = `
                <iframe 
                    src="https://www.youtube.com/embed/${videoId}?rel=0" 
                    frameborder="0" 
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" 
                    allowfullscreen 
                    referrerpolicy="no-referrer-when-downgrade"
                    title="${target.getAttribute('aria-label') || 'YouTube Video'}">
                </iframe>`;
        }
    });
});

// ========================================
// ACCESSIBILITY WIDGET (Merged from accessibility.js)
// ========================================
(function () {
    const STORAGE_KEY = 'suarez_accessibility_config';
    let state = { textLarge: false, highContrast: false, darkMode: false, grayscale: false, readableFont: false, highlightLinks: false };

    function applyState() {
        const b = document.body;
        b.classList.toggle('acc-text-large', state.textLarge);
        b.classList.toggle('acc-high-contrast', state.highContrast);
        b.classList.toggle('acc-dark-mode', state.darkMode);
        b.classList.toggle('acc-grayscale', state.grayscale);
        b.classList.toggle('acc-readable-font', state.readableFont);
        b.classList.toggle('acc-links', state.highlightLinks);
    }

    // Load initial state immediately to avoid flicker
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved) { state = JSON.parse(saved); applyState(); }

    function togglePanel() {
        let panel = document.getElementById('acc-panel');
        if (!panel) {
            const html = `
                <div id="acc-panel">
                    <div class="acc-panel-header"><h2 class="acc-panel-title">Accesibilidad</h2><button class="acc-close-btn">&times;</button></div>
                    <div class="acc-options">
                        <button class="acc-option-btn" id="btn-text-large">Texto+</button>
                        <button class="acc-option-btn" id="btn-dark-mode">Oscuro</button>
                        <button class="acc-option-btn" id="btn-high-contrast">Contraste</button>
                        <button class="acc-option-btn" id="btn-grayscale">Gris</button>
                        <button class="acc-option-btn" id="btn-readable-font">Fuente</button>
                        <button class="acc-option-btn" id="btn-links">Enlaces</button>
                    </div>
                    <button class="acc-reset-btn" id="btn-reset">Reset</button>
                </div>`;
            document.getElementById('acc-widget-container').insertAdjacentHTML('beforeend', html);
            setupListeners();
            panel = document.getElementById('acc-panel');
        }
        panel.classList.toggle('visible');
    }

    function setupListeners() {
        const opt = {
            'btn-text-large': 'textLarge', 'btn-dark-mode': 'darkMode', 'btn-high-contrast': 'highContrast',
            'btn-grayscale': 'grayscale', 'btn-readable-font': 'readableFont', 'btn-links': 'highlightLinks'
        };
        Object.keys(opt).forEach(id => {
            document.getElementById(id).addEventListener('click', () => {
                state[opt[id]] = !state[opt[id]];
                if (opt[id] === 'darkMode' && state.darkMode) state.highContrast = false;
                if (opt[id] === 'highContrast' && state.highContrast) state.darkMode = false;
                applyState();
                localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
            });
        });
        document.getElementById('btn-reset').addEventListener('click', () => {
            state = { textLarge: false, highContrast: false, darkMode: false, grayscale: false, readableFont: false, highlightLinks: false };
            applyState();
            localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
        });
        document.querySelector('.acc-close-btn').addEventListener('click', () => document.getElementById('acc-panel').classList.remove('visible'));
    }

    document.addEventListener('DOMContentLoaded', () => {
        const btn = document.createElement('div');
        btn.id = 'acc-widget-container';
        btn.innerHTML = `<button id="acc-widget-btn" aria-label="Accesibilidad"><svg viewBox="0 0 24 24" width="24" height="24"><path fill="currentColor" d="M12 2c1.1 0 2 .9 2 2s-.9 2-2 2-2-.9-2-2 .9-2 2-2zm9 7h-6v13h-2v-6h-2v6H9V9H3V7h18v2z"/></svg></button>`;
        document.body.appendChild(btn);
        btn.querySelector('button').addEventListener('click', togglePanel);
    });
})();
