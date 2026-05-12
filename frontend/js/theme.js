function toggleTheme() {
    const currentTheme = localStorage.getItem('scs_theme') || 'dark';
    const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
    
    localStorage.setItem('scs_theme', newTheme);
    applyTheme(newTheme);
}

function applyTheme(theme) {
    if (theme === 'light') {
        document.documentElement.style.setProperty('--bg-primary', '#f5f7fa');
        document.documentElement.style.setProperty('--bg-secondary', '#ffffff');
        document.documentElement.style.setProperty('--bg-card', 'rgba(0,0,0,0.05)');
        document.documentElement.style.setProperty('--text-primary', '#111827');
        document.documentElement.style.setProperty('--text-secondary', '#4b5563');
        document.documentElement.style.setProperty('--text-muted', '#9ca3af');
        document.documentElement.style.setProperty('--border-neon', 'rgba(0,200,255,0.4)');
    } else {
        document.documentElement.style.setProperty('--bg-primary', '#000000');
        document.documentElement.style.setProperty('--bg-secondary', '#0a0a1a');
        document.documentElement.style.setProperty('--bg-card', 'rgba(255,255,255,0.05)');
        document.documentElement.style.setProperty('--text-primary', '#ffffff');
        document.documentElement.style.setProperty('--text-secondary', 'rgba(255,255,255,0.7)');
        document.documentElement.style.setProperty('--text-muted', 'rgba(255,255,255,0.4)');
        document.documentElement.style.setProperty('--border-neon', 'rgba(0,200,255,0.2)');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('scs_theme') || 'dark';
    applyTheme(savedTheme);
});
