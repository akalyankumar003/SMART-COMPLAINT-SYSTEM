// Global Chart Registry to fix Bug 6
window.chartRegistry = window.chartRegistry || {};

// Global Toast function
function showToast(message, type = 'info', duration = 4000) {
  const colors = {
    success: { border: '#00ff88', icon: '✓', bg: 'rgba(0,255,136,0.1)' },
    error: { border: '#ff006e', icon: '✕', bg: 'rgba(255,0,110,0.1)' },
    warning: { border: '#ffaa00', icon: '⚠', bg: 'rgba(255,170,0,0.1)' },
    info: { border: '#00d4ff', icon: 'ℹ', bg: 'rgba(0,212,255,0.1)' }
  };
  const c = colors[type] || colors.info;
  
  const toast = document.createElement('div');
  toast.style.cssText = `
    position: fixed; bottom: 20px; right: 20px; z-index: 9999;
    background: rgba(0,5,30,0.95); border: 1px solid ${c.border};
    border-left: 4px solid ${c.border}; border-radius: 12px;
    padding: 16px 20px; min-width: 280px; max-width: 400px;
    display: flex; align-items: center; gap: 12px;
    backdrop-filter: blur(20px);
    box-shadow: 0 10px 40px rgba(0,0,0,0.5), 0 0 20px ${c.border}33;
    transform: translateX(120%); transition: transform 0.3s ease;
    font-family: 'Inter', system-ui, sans-serif; color: white;
  `;
  toast.innerHTML = `
    <span style="font-size: 1.2rem; color: ${c.border}">${c.icon}</span>
    <span style="flex: 1; font-size: 0.9rem">${message}</span>
    <button onclick="this.parentElement.remove()" style="background:none;border:none;color:rgba(255,255,255,0.5);cursor:pointer;font-size:1.2rem;padding:0">×</button>
  `;
  document.body.appendChild(toast);
  
  requestAnimationFrame(() => {
    requestAnimationFrame(() => { toast.style.transform = 'translateX(0)'; });
  });
  
  setTimeout(() => {
    toast.style.transform = 'translateX(120%)';
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// Data Seeding Function
function initSeedData() {
    const users = JSON.parse(localStorage.getItem('scs_users') || '[]');
    if (users.length === 0) {
        const seedUsers = [
            {id:'U001',name:'Ravi Kumar',email:'ravi@mail.com',role:'User',status:'Active',joined:'2026-03-10',complaints:4,riskScore:'Low',lastLogin:'2026-05-05T08:30:00',avatar:'RK'},
            {id:'U002',name:'Priya Singh',email:'priya@mail.com',role:'User',status:'Active',joined:'2026-04-01',complaints:2,riskScore:'Low',lastLogin:'2026-05-04T14:00:00',avatar:'PS'},
            {id:'U003',name:'Arjun Nair',email:'arjun@mail.com',role:'Agent',status:'Active',joined:'2026-02-15',complaints:0,riskScore:'Low',lastLogin:'2026-05-05T07:55:00',avatar:'AN'},
            {id:'U004',name:'Meena Patel',email:'meena@mail.com',role:'User',status:'Suspended',joined:'2026-01-20',complaints:7,riskScore:'High',lastLogin:'2026-04-30T12:00:00',avatar:'MP'},
            {id:'U005',name:'Suresh Babu',email:'suresh@mail.com',role:'User',status:'Pending',joined:'2026-05-03',complaints:1,riskScore:'Medium',lastLogin:'2026-05-03T10:10:00',avatar:'SB'}
        ];
        localStorage.setItem('scs_users', JSON.stringify(seedUsers));
    }

    const complaints = JSON.parse(localStorage.getItem('scs_complaints') || '[]');
    if (complaints.length === 0) {
        const seedComplaints = [
            {id:'C4821',userId:'U001',userName:'Ravi Kumar',category:'Infrastructure',title:'Broken streetlight on MG Road',status:'Under Review',priority:'High',aiScore:87,fraudRisk:'Low',createdAt:'2026-05-04',escalated:false},
            {id:'C4820',userId:'U004',userName:'Meena Patel',category:'Billing',title:'Double charge on utility bill',status:'Flagged',priority:'Medium',aiScore:18,fraudRisk:'High',createdAt:'2026-05-03',escalated:false},
            {id:'C4819',userId:'U002',userName:'Priya Singh',category:'Harassment',title:'Workplace harassment by supervisor',status:'In Progress',priority:'Critical',aiScore:92,fraudRisk:'Low',createdAt:'2026-05-02',escalated:true},
            {id:'C4818',userId:'U001',userName:'Ravi Kumar',category:'Infrastructure',title:'Pothole on Station Road',status:'Resolved',priority:'Low',aiScore:95,fraudRisk:'Low',createdAt:'2026-04-28',resolvedAt:'2026-05-03',rating:4},
            {id:'C4817',userId:'U005',userName:'Suresh Babu',category:'Corruption',title:'Bribe demanded for ration card',status:'Under Review',priority:'High',aiScore:78,fraudRisk:'Medium',createdAt:'2026-05-01',escalated:false}
        ];
        localStorage.setItem('scs_complaints', JSON.stringify(seedComplaints));
    }

    const agents = JSON.parse(localStorage.getItem('scs_agents') || '[]');
    if (agents.length === 0) {
        const seedAgents = [
            {id:'A001',name:'Sneha Rao',avatar:'SR',assigned:12,capacity:20,resolved:89,avgTime:'2.4 days',rating:4.6,status:'Online'},
            {id:'A002',name:'Kiran Mehta',avatar:'KM',assigned:19,capacity:20,resolved:134,avgTime:'1.8 days',rating:4.8,status:'Online'},
            {id:'A003',name:'Deepa Verma',avatar:'DV',assigned:20,capacity:20,resolved:67,avgTime:'3.1 days',rating:4.2,status:'Busy'}
        ];
        localStorage.setItem('scs_agents', JSON.stringify(seedAgents));
    }
}

function createSkeletonCard(lines = 3) {
  const card = document.createElement('div');
  card.className = 'skeleton-card';
  card.style.cssText = 'background: rgba(255,255,255,0.05); border-radius: 12px; padding: 20px; border: 1px solid rgba(0,200,255,0.1);';
  for (let i = 0; i < lines; i++) {
    const line = document.createElement('div');
    line.style.cssText = `
      height: ${i === 0 ? '20px' : '14px'};
      width: ${i === lines - 1 ? '60%' : '100%'};
      border-radius: 6px;
      margin-bottom: 12px;
      background: linear-gradient(90deg, rgba(255,255,255,0.05) 25%, rgba(255,255,255,0.1) 50%, rgba(255,255,255,0.05) 75%);
      background-size: 1000px 100%;
      animation: shimmer 1.5s infinite;
    `;
    card.appendChild(line);
  }
  return card;
}

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe.toString()
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

function comingSoon(feature) {
    showToast(`🚧 ${feature} — Coming Soon`, 'info');
}

function loadUserProfile() {
    try {
        const sessionData = localStorage.getItem('scs_user') || localStorage.getItem('scs_session');
        if (sessionData) {
            const sessionUser = JSON.parse(sessionData);
            const fullName = sessionUser.name || sessionUser.fullName || 'User';
            const firstName = fullName.split(' ')[0];
            const initials = fullName.substring(0,2).toUpperCase();
            
            if (document.getElementById('welcomeName')) document.getElementById('welcomeName').innerText = firstName;
            if (document.getElementById('userNameDisplay')) document.getElementById('userNameDisplay').innerText = fullName;
            if (document.getElementById('userInitials')) document.getElementById('userInitials').innerText = initials;
            if (document.getElementById('userInitialsSmall')) document.getElementById('userInitialsSmall').innerText = initials;
        }
    } catch(e) {
        console.warn('Failed to load user profile elements', e);
    }
}

// Global hook to populate profile on any page that uses it
document.addEventListener('DOMContentLoaded', loadUserProfile);

// Call initSeedData instantly
initSeedData();
