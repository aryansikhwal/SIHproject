"""
Fresh API Service Layer for AttenSync Frontend
Clean implementation for backend communication
"""
import axios from 'axios';

// Configuration
const API_CONFIG = {
    baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
    timeout: 10000,
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
};

// Create axios instance
const apiClient = axios.create(API_CONFIG);

// Request interceptor for logging and auth
apiClient.interceptors.request.use(
    (config) => {
        console.log(`🌐 API Request: ${config.method?.toUpperCase()} ${config.url}`);
        return config;
    },
    (error) => {
        console.error('❌ Request error:', error);
        return Promise.reject(error);
    }
);

// Response interceptor for error handling
apiClient.interceptors.response.use(
    (response) => {
        console.log(`✅ API Response: ${response.status} ${response.config.url}`);
        return response;
    },
    (error) => {
        console.error(`❌ API Error: ${error.response?.status || 'Network'} ${error.config?.url}`);
        
        // Handle specific error cases
        if (error.response?.status === 401) {
            // Unauthorized - redirect to login
            window.location.href = '/login';
        } else if (error.response?.status === 403) {
            console.warn('⚠️ Access forbidden');
        } else if (error.response?.status >= 500) {
            console.error('🔥 Server error');
        }
        
        return Promise.reject(error);
    }
);

// ==================== API SERVICE CLASS ====================

class AttenSyncAPI {
    
    // ==================== HEALTH & SYSTEM ====================
    
    async healthCheck() {
        try {
            const response = await apiClient.get('/api/health');
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Health check failed');
        }
    }
    
    async getDashboardStats() {
        try {
            const response = await apiClient.get('/api/stats/dashboard');
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to fetch dashboard statistics');
        }
    }
    
    // ==================== AUTHENTICATION ====================
    
    async login(username, password) {
        try {
            const response = await apiClient.post('/api/auth/login', {
                username,
                password
            });
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Login failed');
        }
    }
    
    async logout() {
        try {
            const response = await apiClient.post('/api/auth/logout');
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Logout failed');
        }
    }
    
    async getCurrentUser() {
        try {
            const response = await apiClient.get('/api/auth/me');
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to fetch user information');
        }
    }
    
    // ==================== STUDENTS ====================
    
    async getStudents(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            if (filters.class_id) params.append('class_id', filters.class_id);
            if (filters.search) params.append('search', filters.search);
            if (filters.page) params.append('page', filters.page);
            if (filters.per_page) params.append('per_page', filters.per_page);
            
            const response = await apiClient.get(`/api/students?${params.toString()}`);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to fetch students');
        }
    }
    
    async getStudent(studentId) {
        try {
            const response = await apiClient.get(`/api/students/${studentId}`);
            return response.data;
        } catch (error) {
            throw this._handleError(error, `Failed to fetch student ${studentId}`);
        }
    }
    
    async createStudent(studentData) {
        try {
            const response = await apiClient.post('/api/students', studentData);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to create student');
        }
    }
    
    async updateStudent(studentId, studentData) {
        try {
            const response = await apiClient.put(`/api/students/${studentId}`, studentData);
            return response.data;
        } catch (error) {
            throw this._handleError(error, `Failed to update student ${studentId}`);
        }
    }
    
    async deleteStudent(studentId) {
        try {
            const response = await apiClient.delete(`/api/students/${studentId}`);
            return response.data;
        } catch (error) {
            throw this._handleError(error, `Failed to delete student ${studentId}`);
        }
    }
    
    // ==================== ATTENDANCE ====================
    
    async getAttendance(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            if (filters.class_id) params.append('class_id', filters.class_id);
            if (filters.student_id) params.append('student_id', filters.student_id);
            if (filters.start_date) params.append('start_date', filters.start_date);
            if (filters.end_date) params.append('end_date', filters.end_date);
            if (filters.status) params.append('status', filters.status);
            if (filters.page) params.append('page', filters.page);
            if (filters.per_page) params.append('per_page', filters.per_page);
            
            const response = await apiClient.get(`/api/attendance?${params.toString()}`);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to fetch attendance records');
        }
    }
    
    async markAttendance(attendanceData) {
        try {
            const response = await apiClient.post('/api/attendance/mark', attendanceData);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to mark attendance');
        }
    }
    
    async bulkMarkAttendance(bulkData) {
        try {
            const response = await apiClient.post('/api/attendance/bulk', bulkData);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to bulk mark attendance');
        }
    }
    
    // ==================== CLASSES ====================
    
    async getClasses() {
        try {
            const response = await apiClient.get('/api/classes');
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to fetch classes');
        }
    }
    
    async createClass(classData) {
        try {
            const response = await apiClient.post('/api/classes', classData);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to create class');
        }
    }
    
    // ==================== RFID OPERATIONS ====================
    
    async getRFIDScans(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            if (filters.limit) params.append('limit', filters.limit);
            if (filters.status) params.append('status', filters.status);
            
            const response = await apiClient.get(`/api/rfid/scans?${params.toString()}`);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to fetch RFID scans');
        }
    }
    
    // ==================== REPORTS & ANALYTICS ====================
    
    async getAttendanceReport(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            if (filters.class_id) params.append('class_id', filters.class_id);
            if (filters.start_date) params.append('start_date', filters.start_date);
            if (filters.end_date) params.append('end_date', filters.end_date);
            if (filters.report_type) params.append('report_type', filters.report_type);
            
            const response = await apiClient.get(`/api/reports/attendance?${params.toString()}`);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to generate attendance report');
        }
    }
    
    async getAttendanceTrends(filters = {}) {
        try {
            const params = new URLSearchParams();
            
            if (filters.period) params.append('period', filters.period);
            if (filters.class_id) params.append('class_id', filters.class_id);
            
            const response = await apiClient.get(`/api/reports/trends?${params.toString()}`);
            return response.data;
        } catch (error) {
            throw this._handleError(error, 'Failed to fetch attendance trends');
        }
    }
    
    // ==================== UTILITY METHODS ====================
    
    _handleError(error, defaultMessage = 'An error occurred') {
        const errorMessage = error.response?.data?.error || 
                           error.response?.data?.message || 
                           error.message || 
                           defaultMessage;
        
        const errorCode = error.response?.status;
        
        console.error(`❌ API Error [${errorCode}]: ${errorMessage}`);
        
        return {
            message: errorMessage,
            code: errorCode,
            details: error.response?.data
        };
    }
    
    // ==================== MOCK DATA HELPERS (for development) ====================
    
    async getMockDashboardData() {
        return {
            total_students: 150,
            total_classes: 8,
            present_today: 142,
            absent_today: 8,
            weekly_average: 89.5,
            attendance_percentage: 94.7,
            recent_rfid_scans: [
                {
                    id: 1,
                    rfid_tag: "ABCD1234",
                    student_name: "John Doe",
                    status: "success",
                    scan_time: new Date().toISOString()
                }
            ]
        };
    }
    
    async getMockStudentData() {
        return {
            students: [
                {
                    id: 1,
                    full_name: "John Doe",
                    roll_number: "001",
                    class_name: "Class 5A",
                    attendance_percentage: 95.5,
                    rfid_tag: "ABCD1234",
                    is_active: true
                },
                {
                    id: 2,
                    full_name: "Jane Smith",
                    roll_number: "002",
                    class_name: "Class 5A",
                    attendance_percentage: 88.2,
                    rfid_tag: "EFGH5678",
                    is_active: true
                }
            ],
            total: 2
        };
    }
    
    async getMockAttendanceData() {
        return {
            attendance: [
                {
                    id: 1,
                    student_name: "John Doe",
                    student_roll: "001",
                    class_name: "Class 5A",
                    attendance_date: new Date().toISOString().split('T')[0],
                    time_marked: new Date().toISOString(),
                    status: "present",
                    method: "rfid"
                }
            ],
            total: 1
        };
    }
    
    // ==================== CONNECTION TESTING ====================
    
    async testConnection() {
        try {
            console.log('🧪 Testing API connection...');
            const health = await this.healthCheck();
            console.log('✅ API connection successful:', health);
            return true;
        } catch (error) {
            console.error('❌ API connection failed:', error);
            return false;
        }
    }
}

// ==================== EXPORT ====================

// Create and export singleton instance
const attenSyncAPI = new AttenSyncAPI();

// Export both the instance and the class
export default attenSyncAPI;
export { AttenSyncAPI };

// Export specific method groups for convenience
export const authAPI = {
    login: attenSyncAPI.login.bind(attenSyncAPI),
    logout: attenSyncAPI.logout.bind(attenSyncAPI),
    getCurrentUser: attenSyncAPI.getCurrentUser.bind(attenSyncAPI)
};

export const studentAPI = {
    getAll: attenSyncAPI.getStudents.bind(attenSyncAPI),
    getById: attenSyncAPI.getStudent.bind(attenSyncAPI),
    create: attenSyncAPI.createStudent.bind(attenSyncAPI),
    update: attenSyncAPI.updateStudent.bind(attenSyncAPI),
    delete: attenSyncAPI.deleteStudent.bind(attenSyncAPI)
};

export const attendanceAPI = {
    getAll: attenSyncAPI.getAttendance.bind(attenSyncAPI),
    mark: attenSyncAPI.markAttendance.bind(attenSyncAPI),
    bulkMark: attenSyncAPI.bulkMarkAttendance.bind(attenSyncAPI)
};

export const classAPI = {
    getAll: attenSyncAPI.getClasses.bind(attenSyncAPI),
    create: attenSyncAPI.createClass.bind(attenSyncAPI)
};

export const rfidAPI = {
    getScans: attenSyncAPI.getRFIDScans.bind(attenSyncAPI)
};

export const dashboardAPI = {
    getStats: attenSyncAPI.getDashboardStats.bind(attenSyncAPI)
};

// Test the connection on module load in development
if (process.env.NODE_ENV === 'development') {
    attenSyncAPI.testConnection().then(success => {
        if (success) {
            console.log('🎉 AttenSync API service initialized successfully');
        } else {
            console.warn('⚠️ AttenSync API service failed to connect - using mock data');
        }
    });
}

console.log('📡 AttenSync API service loaded');