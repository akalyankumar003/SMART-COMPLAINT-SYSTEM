from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required

ai_bp = Blueprint('ai', __name__)

@ai_bp.route('/suggest-category', methods=['POST'])
@jwt_required()
def suggest_category():
    data = request.json
    desc = data.get('description', '').lower()
    
    # Simple keyword fallback mock
    results = []
    if 'bank' in desc or 'upi' in desc or 'pay' in desc or 'money' in desc:
        results.append({'category': 'UPI/Payment Fraud', 'confidence': 85})
    if 'job' in desc or 'offer' in desc or 'hire' in desc:
        results.append({'category': 'Online Job Scam', 'confidence': 90})
    if 'hack' in desc or 'password' in desc or 'account' in desc:
        results.append({'category': 'Account Hacking', 'confidence': 88})
        
    if not results:
        results = [
            {'category': 'Phishing Attack', 'confidence': 60},
            {'category': 'Social Media Crime', 'confidence': 45},
            {'category': 'Identity Theft', 'confidence': 40}
        ]
        
    return jsonify({'results': results[:3]})

@ai_bp.route('/generate-complaint', methods=['POST'])
@jwt_required()
def generate_complaint():
    data = request.json
    title = data.get('title', '')
    date = data.get('incidentDate', '')
    
    if not title:
        return jsonify({'error': 'Title is required'}), 400
        
    # Mock fallback logic since OpenAI API key might not be available
    lower_title = title.lower()
    
    severity = 'Medium'
    confidence = 85
    category = 'Other'
    sections = ['IPC 419', 'IPC 420', 'IT Act 66D']
    evidence = ['Screenshots of communication', 'Transaction receipts', 'Bank statement']
    
    if 'bank' in lower_title or 'upi' in lower_title or 'pay' in lower_title:
        severity = 'High'
        category = 'UPI/Payment Fraud'
        confidence = 94
        sections = ['IPC 420 (Cheating)', 'IT Act 66D (Cheating by personation)']
        evidence = ['Bank Account Statement', 'UPI Transaction ID Screenshot', 'SMS Alerts from Bank']
    elif 'hack' in lower_title or 'password' in lower_title:
        severity = 'Critical'
        category = 'Account Hacking'
        confidence = 91
        sections = ['IT Act 66 (Computer Related Offences)', 'IT Act 66C (Identity Theft)']
        evidence = ['Login Activity Logs', 'Password Change Notification Emails', 'Device IP Logs']
    elif 'job' in lower_title or 'offer' in lower_title:
        severity = 'Medium'
        category = 'Online Job Scam'
        confidence = 88
        sections = ['IPC 415 (Fraud)', 'IPC 420 (Cheating)']
        evidence = ['Offer Letter PDF', 'Email thread with recruiter', 'Payment receipt for registration fee']
        
    generated_desc = (
        f"On or around {date}, an incident involving '{title}' occurred. "
        f"The victim encountered a deceptive cyber activity falling under the category of {category}. "
        f"The perpetrator utilized digital mediums to execute the fraud, causing distress and potential financial/data loss to the victim. "
        f"Immediate intervention is required to trace the digital footprint and prevent further unauthorized access or financial drain."
    )
    
    response_data = {
        'description': generated_desc,
        'category': category,
        'applicableSections': sections,
        'suggestedEvidence': evidence,
        'severity': severity,
        'aiConfidenceScore': confidence
    }
    
    return jsonify(response_data)

@ai_bp.route('/analyse-sentiment', methods=['POST'])
@jwt_required()
def analyse_sentiment():
    data = request.json
    text = data.get('text', '').lower()
    
    # Heuristic sentiment analysis
    urgency = 'Medium'
    score = 0.5
    
    crisis_words = ['suicide', 'die', 'kill', 'emergency', 'blood', 'life', 'help me']
    angry_words = ['fraud', 'scam', 'cheated', 'lost', 'stole', 'angry', 'terrible', 'worst']
    
    if any(w in text for w in crisis_words):
        urgency = 'Critical'
        score = 0.1
    elif any(w in text for w in angry_words):
        urgency = 'High'
        score = 0.3
        
    return jsonify({
        'urgency': urgency,
        'sentimentScore': score,
        'sentiment': 'Negative' if score < 0.5 else 'Neutral'
    })

@ai_bp.route('/detect-fake', methods=['POST'])
@jwt_required()
def detect_fake():
    data = request.json
    text = data.get('text', '').lower()
    
    # Heuristic fake detection
    is_fake = False
    fake_score = 15 # out of 100
    
    spam_keywords = ['win money', 'lottery', 'inheritance', 'billionaire', 'nigerian prince', 'test complaint', 'asdf']
    if len(text) < 50: 
        fake_score += 30
    if any(w in text for w in spam_keywords):
        fake_score += 50
        is_fake = True
        
    return jsonify({
        'fakeScore': fake_score,
        'isLikelyFake': is_fake,
        'flaggedKeywords': [w for w in spam_keywords if w in text]
    })

@ai_bp.route('/predict-time', methods=['POST'])
@jwt_required()
def predict_time():
    data = request.json
    category = data.get('category', 'Other')
    
    # Regression-like heuristic
    base_hours = 48
    if category == 'UPI/Payment Fraud': base_hours = 24
    elif category == 'Ransomware': base_hours = 12
    elif category == 'Account Hacking': base_hours = 36
    
    return jsonify({
        'estimatedHours': base_hours,
        'confidence': 82
    })

@ai_bp.route('/chat', methods=['POST'])
@jwt_required()
def ai_chat():
    data = request.json
    query = data.get('query', '').lower()
    
    # Knowledge Base
    kb = {
        'file': 'To file a complaint, go to the "File Complaint" section in your dashboard. You can use our AI assistant to help generate the description.',
        'status': 'You can track your complaint status in the "My Complaints" section. Statuses include Pending, Under Review, In Progress, and Resolved.',
        'admin': 'Admin profiles can be updated in the Admin Settings. Admins can manage users, view crime heatmaps, and resolve complaints.',
        'heatmap': 'The Crime Heatmap shows crime density across various regions. Access it from the Admin Sidebar.',
        'aadhaar': 'Aadhaar card details are optional and are used only for identity verification.',
        'who are you': 'I am the SCS Intelligent Assistant, designed to help you navigate the Smart Complaint System.',
        'help': 'I can help you with filing complaints, checking status, understanding legal sections, and technical support.'
    }
    
    response = "I'm sorry, I don't have specific information on that. Please contact our support team for further assistance."
    
    for key in kb:
        if key in query:
            response = kb[key]
            break
            
    # Simulate thinking
    import time
    time.sleep(0.5)
    
    return jsonify({
        'response': response,
        'senderName': 'SCS Assistant Bot'
    })
