async function apiCall(endpoint, options = {}) {
  // If there's a backend call, try it. If it fails, rely on localStorage mock.
  try {
      const token = localStorage.getItem('scs_token');
      const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const response = await fetch(`/api/v1${endpoint}`, {
        ...options,
        headers
      });
      if (response.status === 401) {
        localStorage.removeItem('scs_user');
        localStorage.removeItem('scs_session');
        localStorage.removeItem('scs_token');
        window.location.href = 'login.html';
        return null;
      }
      if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      return data;
  } catch (error) {
      console.warn("API Call fallback to mock data due to:", error);
      // Fallback for mocked environment
      if (endpoint.includes('/complaints')) {
          if (options.method === 'POST') {
              const complaints = JSON.parse(localStorage.getItem('scs_complaints') || '[]');
              let newComplaint = {};
              if (options.body instanceof FormData) {
                  const fd = options.body;
                  const cId = 'C' + Math.floor(Math.random() * 9000 + 1000);
                  const sessionUser = JSON.parse(localStorage.getItem('scs_user') || '{}');
                  newComplaint = {
                      id: cId,
                      _id: cId,
                      complaintId: cId,
                      userId: sessionUser.id || 'U000',
                      userName: sessionUser.fullName || 'User',
                      category: fd.get('category') || 'Other',
                      title: fd.get('title') || 'New Complaint',
                      status: 'Under Review',
                      priority: fd.get('priority') || 'Medium',
                      aiScore: fd.get('aiConfidenceScore') || Math.floor(Math.random() * 50 + 50),
                      fraudRisk: 'Low',
                      createdAt: new Date().toISOString(),
                      escalated: false
                  };
              }
              complaints.unshift(newComplaint);
              localStorage.setItem('scs_complaints', JSON.stringify(complaints));
              return newComplaint;
          }
          return JSON.parse(localStorage.getItem('scs_complaints') || '[]');
      }
      if (endpoint.includes('/users')) {
          return JSON.parse(localStorage.getItem('scs_users') || '[]');
      }
      throw error;
  }
}

function guardPage(requiredRole) {
  const sessionStr = localStorage.getItem('scs_user') || localStorage.getItem('scs_session');
  if (!sessionStr) {
    if (window.location.pathname.indexOf('login.html') === -1 && window.location.pathname.indexOf('index.html') === -1) {
        window.location.href = 'login.html';
    }
    return false;
  }
  
  try {
      const session = JSON.parse(sessionStr);
      if (requiredRole === 'admin' && session.role !== 'admin' && session.role !== 'SUPER ADMIN') {
        window.location.href = 'login.html';
        return false;
      }
      if (requiredRole === 'user' && (session.role === 'admin' || session.role === 'SUPER ADMIN')) {
        window.location.href = 'admin-dashboard.html';
        return false;
      }
      return true;
  } catch(e) {
      localStorage.removeItem('scs_user');
      localStorage.removeItem('scs_session');
      window.location.href = 'login.html';
      return false;
  }
}

function getCurrentUserRole() {
    const sessionStr = localStorage.getItem('scs_user') || localStorage.getItem('scs_session');
    if (!sessionStr) return null;
    try {
        return JSON.parse(sessionStr).role;
    } catch(e) { return null; }
}

function getCurrentUserId() {
    const sessionStr = localStorage.getItem('scs_user') || localStorage.getItem('scs_session');
    if (!sessionStr) return null;
    try {
        return JSON.parse(sessionStr).id;
    } catch(e) { return null; }
}
