import axios from 'axios';

// Base API configuration
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';
console.log('API_BASE_URL:', API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // withCredentials: true,  // Temporarily disabled to debug CORS issues
});

// Request interceptor to add auth tokens if needed
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Handle unauthorized access
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API Service Functions

// Attendance APIs
export const attendanceAPI = {
  // Get attendance records
  getAttendance: (date = null, classId = null) => {
    const params = new URLSearchParams();
    if (date) params.append('date', date);
    if (classId) params.append('class', classId);
    return api.get(`/api/attendance?${params}`);
  },

  // Mark attendance for a student
  markAttendance: (studentId, date, status) => {
    return api.post('/api/attendance', {
      student_id: studentId,
      date,
      status,
    });
  },

  // Bulk mark attendance
  bulkMarkAttendance: (attendanceData) => {
    return api.post('/api/attendance/bulk', { attendance: attendanceData });
  },

  // Get attendance summary
  getAttendanceSummary: (startDate, endDate) => {
    return api.get(`/api/attendance/summary?start_date=${startDate}&end_date=${endDate}`);
  },

  // Export attendance data
  exportAttendance: (format = 'csv', filters = {}) => {
    return api.post('/api/attendance/export', { format, filters }, {
      responseType: 'blob'
    });
  },
};

// Students APIs
export const studentsAPI = {
  // Get all students
  getStudents: (classId = null, searchTerm = null) => {
    const params = new URLSearchParams();
    if (classId && classId !== 'all') params.append('class', classId);
    if (searchTerm) params.append('search', searchTerm);
    return api.get(`/api/students?${params}`);
  },

  // Get student by ID
  getStudent: (studentId) => {
    return api.get(`/api/students/${studentId}`);
  },

  // Add new student
  addStudent: (studentData) => {
    return api.post('/api/students', studentData);
  },

  // Update student
  updateStudent: (studentId, studentData) => {
    return api.put(`/api/students/${studentId}`, studentData);
  },

  // Delete student
  deleteStudent: (studentId) => {
    return api.delete(`/api/students/${studentId}`);
  },

  // Get student attendance history
  getStudentAttendance: (studentId, startDate = null, endDate = null) => {
    const params = new URLSearchParams();
    if (startDate) params.append('start_date', startDate);
    if (endDate) params.append('end_date', endDate);
    return api.get(`/api/students/${studentId}/attendance?${params}`);
  },
};

// Reports APIs
export const reportsAPI = {
  // Get dashboard statistics
  getDashboardStats: () => {
    return api.get('/api/reports/dashboard');
  },

  // Get attendance reports
  getAttendanceReport: (reportType, params = {}) => {
    return api.post('/api/reports/attendance', { type: reportType, ...params });
  },

  // Get class-wise reports
  getClassWiseReport: (startDate, endDate) => {
    return api.get(`/api/reports/class-wise?start_date=${startDate}&end_date=${endDate}`);
  },

  // Get monthly trends
  getMonthlyTrends: (year = null) => {
    const currentYear = year || new Date().getFullYear();
    return api.get(`/api/reports/monthly-trends?year=${currentYear}`);
  },

  // Get absenteeism analysis
  getAbsenteeismAnalysis: (period = 'month') => {
    return api.get(`/api/reports/absenteeism?period=${period}`);
  },

  // Export report
  exportReport: (reportType, format, params = {}) => {
    return api.post('/api/reports/export', {
      type: reportType,
      format,
      ...params
    }, {
      responseType: 'blob'
    });
  },
};

// Trends APIs
export const trendsAPI = {
  // Get trend analysis data
  getTrendAnalysis: (type = 'monthly', period = 'current_year') => {
    return api.get(`/api/trends/${type}?period=${period}`);
  },

  // Get seasonal patterns
  getSeasonalPatterns: () => {
    return api.get('/api/trends/seasonal');
  },

  // Get AI predictions
  getPredictions: (months = 6) => {
    return api.get(`/api/trends/predictions?months=${months}`);
  },

  // Get weekly patterns
  getWeeklyPatterns: () => {
    return api.get('/api/trends/weekly');
  },

  // Get yearly comparison
  getYearlyComparison: (years = 5) => {
    return api.get(`/api/trends/yearly?years=${years}`);
  },
};

// Settings APIs
export const settingsAPI = {
  // Get school information
  getSchoolInfo: () => {
    return api.get('/api/settings/school');
  },

  // Update school information
  updateSchoolInfo: (schoolData) => {
    return api.put('/api/settings/school', schoolData);
  },

  // Get notification settings
  getNotificationSettings: () => {
    return api.get('/api/settings/notifications');
  },

  // Update notification settings
  updateNotificationSettings: (settings) => {
    return api.put('/api/settings/notifications', settings);
  },

  // Get sync settings
  getSyncSettings: () => {
    return api.get('/api/settings/sync');
  },

  // Update sync settings
  updateSyncSettings: (settings) => {
    return api.put('/api/settings/sync', settings);
  },

  // Trigger manual sync
  triggerSync: () => {
    return api.post('/api/settings/sync/trigger');
  },

  // Get system info
  getSystemInfo: () => {
    return api.get('/api/settings/system');
  },
};

// Authentication APIs
export const authAPI = {
  // Login
  login: (credentials) => {
    return api.post('/api/auth/login', credentials);
  },

  // Logout
  logout: () => {
    return api.post('/api/auth/logout');
  },

  // Get current user info
  getCurrentUser: () => {
    return api.get('/api/auth/me');
  },

  // Change password
  changePassword: (currentPassword, newPassword) => {
    return api.post('/api/auth/change-password', {
      current_password: currentPassword,
      new_password: newPassword,
    });
  },

  // Refresh token
  refreshToken: () => {
    return api.post('/api/auth/refresh');
  },
};

// RFID Scan APIs
export const rfidScanAPI = {
  // Get recent RFID scans
  getRecentScans: (limit = 10) => {
    const url = `/api/rfid/scans?limit=${limit}`;
    console.log('Making request to:', API_BASE_URL + url);
    return api.get(url);
  },
};

// Utility functions for error handling
export const handleAPIError = (error) => {
  if (error.response) {
    // Server responded with error status
    const { status, data } = error.response;
    
    switch (status) {
      case 400:
        return { message: data.message || 'Invalid request data' };
      case 401:
        return { message: 'Authentication required' };
      case 403:
        return { message: 'Access denied' };
      case 404:
        return { message: 'Resource not found' };
      case 500:
        return { message: 'Server error. Please try again later.' };
      default:
        return { message: data.message || 'An error occurred' };
    }
  } else if (error.request) {
    // Network error
    return { message: 'Network error. Please check your connection.' };
  } else {
    // Other error
    return { message: 'An unexpected error occurred' };
  }
};

// Check if API is available
export const checkAPIHealth = async () => {
  try {
    const response = await api.get('/api/health');
    return response.status === 200;
  } catch (error) {
    return false;
  }
};

export default api;
