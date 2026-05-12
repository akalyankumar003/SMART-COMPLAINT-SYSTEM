(function() {
    // Inject styles
    const style = document.createElement('style');
    style.innerHTML = `
        #ai-widget-panel {
            position: fixed; bottom: 100px; right: 30px; z-index: 9999;
            width: 360px; height: 480px; background: rgba(0,5,30,0.95);
            backdrop-filter: blur(20px); border: 1px solid rgba(0,212,255,0.3);
            border-radius: 16px; display: none; flex-direction: column;
            overflow: hidden; box-shadow: 0 10px 40px rgba(0,0,0,0.5);
            font-family: 'Inter', sans-serif;
        }
        .ai-msg { background: rgba(255,255,255,0.05); padding: 12px; border-radius: 12px; align-self: flex-start; max-width: 85%; color: #e2e8f0; line-height: 1.4; border: 1px solid rgba(255,255,255,0.1); }
        .user-msg { background: rgba(0,212,255,0.1); padding: 12px; border-radius: 12px; align-self: flex-end; max-width: 85%; color: white; line-height: 1.4; border: 1px solid rgba(0,212,255,0.3); }
        .typing-dot { display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: var(--neon-cyan); margin: 0 2px; animation: ai-typing 1.4s infinite both; }
        .typing-dot:nth-child(1) { animation-delay: -0.32s; }
        .typing-dot:nth-child(2) { animation-delay: -0.16s; }
        @keyframes ai-typing { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
        .quick-chip { background: rgba(0,212,255,0.1); color: var(--neon-cyan); border: 1px solid rgba(0,212,255,0.3); padding: 6px 12px; border-radius: 16px; font-size: 0.8rem; cursor: pointer; white-space: nowrap; transition: 0.2s; }
        .quick-chip:hover { background: rgba(0,212,255,0.2); }
        .chip-container { display: flex; gap: 8px; overflow-x: auto; padding: 10px 20px; padding-top: 0; }
        .chip-container::-webkit-scrollbar { display: none; }
    `;
    document.head.appendChild(style);

    const widget = document.createElement('div');
    widget.id = 'ai-support-widget';
    widget.style.cssText = `
        position: fixed; bottom: 30px; right: 30px; z-index: 9999;
        width: 60px; height: 60px; border-radius: 50%;
        background: linear-gradient(135deg, #00d4ff, #7b2fff);
        box-shadow: 0 0 20px rgba(0,212,255,0.5);
        display: flex; align-items: center; justify-content: center;
        cursor: pointer; transition: 0.3s; font-size: 1.8rem;
    `;
    widget.innerHTML = '🤖';
    
    const panel = document.createElement('div');
    panel.id = 'ai-widget-panel';
    panel.innerHTML = `
        <div style="padding: 16px 20px; background: rgba(0,212,255,0.1); border-bottom: 1px solid rgba(0,212,255,0.2); display: flex; justify-content: space-between; align-items: center;">
            <div style="display:flex; align-items:center; gap:8px;">
                <span style="font-size:1.5rem">🤖</span>
                <div>
                    <div style="font-weight: 700; color: #00d4ff; font-size:14px; letter-spacing:0.5px;">CYBER AI</div>
                    <div style="font-size:10px; color:#94a3b8; display:flex; align-items:center; gap:4px;"><span style="display:inline-block;width:6px;height:6px;background:#00ff88;border-radius:50%"></span> Online</div>
                </div>
            </div>
            <button id="close-widget" style="background:none; border:none; color:#94a3b8; cursor:pointer; font-size:1.2rem; padding:4px;">✕</button>
        </div>
        <div id="ai-widget-msgs" style="flex: 1; padding: 20px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; font-size: 0.9rem;">
            <div class="ai-msg">Hello! Welcome to Smart Complaint System. I can help you file a complaint, check status, escalate, or answer questions. What would you like to do?</div>
        </div>
        <div class="chip-container" id="ai-quick-replies">
            <div class="quick-chip" onclick="window.sendWidgetMsg('How to file a complaint?')">File Complaint</div>
            <div class="quick-chip" onclick="window.sendWidgetMsg('Check status')">Track Status</div>
            <div class="quick-chip" onclick="window.sendWidgetMsg('Escalate issue')">Escalate</div>
        </div>
        <div style="padding: 16px; border-top: 1px solid rgba(255,255,255,0.05); display: flex; gap: 8px; background: rgba(0,0,0,0.2);">
            <input type="text" id="ai-widget-input" placeholder="Type your message..." style="flex: 1; background: rgba(255,255,255,0.05); border: 1px solid rgba(0,212,255,0.2); border-radius: 20px; padding: 10px 16px; color: white; outline: none; font-family: inherit;">
            <button id="ai-widget-send" style="background: linear-gradient(135deg, #00d4ff, #7b2fff); border: none; border-radius: 50%; width: 40px; height: 40px; cursor: pointer; color: white; display:flex; align-items:center; justify-content:center;">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><line x1="22" y1="2" x2="11" y2="13"></line><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
            </button>
        </div>
    `;

    document.body.appendChild(widget);
    document.body.appendChild(panel);

    const trainingData = [
        [['hello','hi','hey','good morning','namaste'], "Hello! Welcome to Smart Complaint System. I can help you file a complaint, check status, escalate, or answer questions. What would you like to do?"],
        [['file','submit','new complaint','register','report','lodge'], "To file a complaint: 1. Click File New on dashboard. 2. Fill Title, Category, Description. 3. Upload evidence. 4. Select priority and Submit. You'll receive a complaint ID immediately."],
        [['status','track','where is','progress','update','my complaint'], "Check status via My Complaints → Live Tracker. Stages: Submitted → Under Review → In Progress → Resolved. You'll get email/push notifications on every update."],
        [['escalate','urgent','emergency','not resolved','ignored','supervisor'], "Click the red SOS Escalate button on your dashboard. Confirm escalation — it's marked Critical and a supervisor is notified within 15 minutes."],
        [['how long','when','resolve','time','eta','days'], "Resolution times: Infrastructure 3-5 days, Billing 1-2 days, Harassment within 24 hours, General 3-7 days. Your dashboard shows AI-predicted ETA."],
        [['evidence','attach','upload','photo','document','proof'], "Attach evidence when filing: JPG, PNG, PDF, MP4, MP3 supported. Max 10MB per file, up to 5 files. For existing complaints, open it and click Add Evidence."],
        [['anonymous','hide','identity','private','without name'], "Yes! Toggle Submit Anonymously on the complaint form. You'll get a Token ID to track status without logging in."],
        [['fake','false','fraud','detected','rejected','ai score','flagged'], "Our AI scans for fake keywords, incoherent text, and suspicious patterns. If genuine complaint was flagged, click Appeal and provide context. Admin reviews within 24 hours."],
        [['login','account','password','sign in','register','forgot'], "Forgot password: click Forgot Password on login page. New account: click Register. Locked account: contact support@scs.gov.in. Change password: Profile → Security."],
        [['contact','support','help','human','agent','phone','email'], "Reach us via: In-app Chat Support sidebar, Email: support@smartcomplaint.in, Phone: 1800-XXX-XXXX (Mon-Sat 9am-6pm), or SOS Escalate for urgent matters."],
        [['notification','alert','notify','sms','message'], "Notifications sent on: status change, agent reply, resolution. Manage preferences: Profile → Notifications → toggle channels."],
        [['category','type','kind','which category'], "Categories: Infrastructure, Billing & Financial, Harassment & Safety, Public Health, Corruption, Noise & Environment, Government Services, Other."],
        [['not satisfied','reopen','unsatisfied','wrong resolution'], "Unsatisfied? Open complaint → Rate Resolution (low rating) → click Request Reopen. Re-examined by supervisor within 48 hours."],
        [['bye','goodbye','thanks','thank you','done'], "You're welcome! Your complaint matters. Have a great day! 🙏"]
    ];

    function getResponse(input) {
        const q = input.toLowerCase().trim();
        for (const [keywords, response] of trainingData) {
            if (keywords.some(kw => q.includes(kw))) return response;
        }
        return "I couldn't find an exact answer. Try asking about filing a complaint, checking status, escalating, or contacting support.";
    }

    widget.onclick = () => {
        panel.style.display = panel.style.display === 'none' ? 'flex' : 'none';
        if(panel.style.display === 'flex') loadHistory();
    };
    
    document.getElementById('close-widget').onclick = () => panel.style.display = 'none';

    const sendBtn = document.getElementById('ai-widget-send');
    const input = document.getElementById('ai-widget-input');
    const msgBox = document.getElementById('ai-widget-msgs');
    
    function loadHistory() {
        const history = JSON.parse(localStorage.getItem('scs_chatlog') || '[]');
        if (history.length > 0) {
            msgBox.innerHTML = '';
            history.forEach(m => {
                const div = document.createElement('div');
                div.className = m.role === 'user' ? 'user-msg' : 'ai-msg';
                div.innerText = m.text;
                msgBox.appendChild(div);
            });
            msgBox.scrollTop = msgBox.scrollHeight;
        }
    }
    
    function saveHistory(role, text) {
        const history = JSON.parse(localStorage.getItem('scs_chatlog') || '[]');
        history.push({role, text});
        if(history.length > 50) history.shift();
        localStorage.setItem('scs_chatlog', JSON.stringify(history));
    }

    window.sendWidgetMsg = function(prefill) {
        const text = prefill || input.value.trim();
        if(!text) return;

        const uMsg = document.createElement('div');
        uMsg.className = 'user-msg';
        uMsg.innerText = text;
        msgBox.appendChild(uMsg);
        
        input.value = '';
        msgBox.scrollTop = msgBox.scrollHeight;
        saveHistory('user', text);

        // Typing indicator
        const typingId = 'typing-' + Date.now();
        const tMsg = document.createElement('div');
        tMsg.id = typingId;
        tMsg.className = 'ai-msg';
        tMsg.innerHTML = '<span class="typing-dot"></span><span class="typing-dot"></span><span class="typing-dot"></span>';
        msgBox.appendChild(tMsg);
        msgBox.scrollTop = msgBox.scrollHeight;

        setTimeout(() => {
            const el = document.getElementById(typingId);
            if(el) el.remove();
            
            const responseText = getResponse(text);
            const bMsg = document.createElement('div');
            bMsg.className = 'ai-msg';
            bMsg.innerText = responseText;
            msgBox.appendChild(bMsg);
            msgBox.scrollTop = msgBox.scrollHeight;
            saveHistory('ai', responseText);
        }, 800);
    }

    sendBtn.onclick = () => window.sendWidgetMsg();
    input.addEventListener('keydown', (e) => {
        if(e.key === 'Enter') {
            e.preventDefault();
            window.sendWidgetMsg();
        }
    });
})();
