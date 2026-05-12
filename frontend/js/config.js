// API Configuration
const API_CONFIG = {
  BASE_URL: 'http://localhost:5000/api/v1',
  SOCKET_URL: 'http://localhost:5000',
  TIMEOUT: 30000, // 30 seconds
  RETRY_ATTEMPTS: 3
};

// Storage Keys
const STORAGE_KEYS = {
  TOKEN: 'scs_token',
  USER: 'scs_user',
  THEME: 'scs_theme',
  LANGUAGE: 'scs_language',
  LOGIN_ATTEMPTS: 'scs_login_attempts'
};

// Complaint Categories with Icons
const COMPLAINT_CATEGORIES = [
  { id: 1, name: 'UPI/Payment Fraud', icon: '💳', severity: 'critical', color: '#ff006e' },
  { id: 2, name: 'Account Hacking', icon: '🔓', severity: 'high', color: '#ff5a00' },
  { id: 3, name: 'Online Job Scam', icon: '💼', severity: 'medium', color: '#ffaa00' },
  { id: 4, name: 'Phishing Attack', icon: '🎣', severity: 'high', color: '#ff5a00' },
  { id: 5, name: 'Ransomware', icon: '🔒', severity: 'critical', color: '#ff006e' },
  { id: 6, name: 'Identity Theft', icon: '👤', severity: 'critical', color: '#ff006e' },
  { id: 7, name: 'Social Media Crime', icon: '📱', severity: 'medium', color: '#ffaa00' },
  { id: 8, name: 'E-Commerce Fraud', icon: '🛒', severity: 'medium', color: '#ffaa00' },
  { id: 9, name: 'Cyberbullying', icon: '😢', severity: 'high', color: '#ff5a00' },
  { id: 10, name: 'Child Exploitation (CSAM)', icon: '🛡️', severity: 'critical', color: '#ff006e' },
  { id: 11, name: 'Dark Web Activity', icon: '🕸️', severity: 'critical', color: '#ff006e' },
  { id: 12, name: 'Cryptocurrency Scam', icon: '₿', severity: 'high', color: '#ff5a00' },
  { id: 13, name: 'Email Fraud', icon: '📧', severity: 'medium', color: '#ffaa00' },
  { id: 14, name: 'Fake News/Deepfakes', icon: '🎭', severity: 'high', color: '#ff5a00' },
  { id: 15, name: 'Data Breach', icon: '💾', severity: 'critical', color: '#ff006e' },
  { id: 16, name: 'Mobile App Fraud', icon: '📲', severity: 'medium', color: '#ffaa00' },
  { id: 17, name: 'Banking Cyber Fraud', icon: '🏦', severity: 'critical', color: '#ff006e' },
  { id: 18, name: 'Sexual Harassment Online', icon: '⚠️', severity: 'critical', color: '#ff006e' },
  { id: 19, name: 'Corporate Espionage', icon: '🕵️', severity: 'high', color: '#ff5a00' },
  { id: 20, name: 'Illegal Content', icon: '🚫', severity: 'critical', color: '#ff006e' }
];

// Export for use in other files
window.API_CONFIG = API_CONFIG;
window.STORAGE_KEYS = STORAGE_KEYS;
window.COMPLAINT_CATEGORIES = COMPLAINT_CATEGORIES;
