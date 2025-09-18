import indexedDBService from './indexedDB';
import { attendanceAPI, studentsAPI } from './api';

// Offline-aware API service that falls back to IndexedDB when offline
class OfflineAwareAPI {
  constructor() {
    this.isOnline = navigator.onLine;
    this.setupOnlineListener();
  }

  setupOnlineListener() {
    window.addEventListener('online', () => {
      this.isOnline = true;
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
  }

  // Students API with offline support
  async getStudents(classFilter = null, searchTerm = null) {
    try {
      if (this.isOnline) {
        // Try to fetch from server first
        const response = await studentsAPI.getStudents(classFilter, searchTerm);
        const students = response.data;
        
        // Update local storage
        for (const student of students) {
          await indexedDBService.updateStudent(student.id, student);
        }
        
        return students;
      } else {
        // Fallback to IndexedDB
        let students = await indexedDBService.getStudents(classFilter);
        
        // Apply search filter locally if needed
        if (searchTerm) {
          students = students.filter(student => 
            student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
            student.id.toLowerCase().includes(searchTerm.toLowerCase())
          );
        }
        
        return students;
      }
    } catch (error) {
      console.warn('API call failed, falling back to IndexedDB:', error);
      // Fallback to IndexedDB on API failure
      let students = await indexedDBService.getStudents(classFilter);
      
      if (searchTerm) {
        students = students.filter(student => 
          student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
          student.id.toLowerCase().includes(searchTerm.toLowerCase())
        );
      }
      
      return students;
    }
  }

  async addStudent(studentData) {
    try {
      if (this.isOnline) {
        const response = await studentsAPI.addStudent(studentData);
        const student = response.data;
        
        // Also save to IndexedDB
        await indexedDBService.addStudent(student);
        
        return student;
      } else {
        // Save to IndexedDB only (will sync later)
        return await indexedDBService.addStudent(studentData);
      }
    } catch (error) {
      console.warn('API call failed, saving to IndexedDB only:', error);
      return await indexedDBService.addStudent(studentData);
    }
  }

  async updateStudent(studentId, studentData) {
    try {
      if (this.isOnline) {
        const response = await studentsAPI.updateStudent(studentId, studentData);
        const student = response.data;
        
        // Also save to IndexedDB
        await indexedDBService.updateStudent(studentId, student);
        
        return student;
      } else {
        // Save to IndexedDB only (will sync later)
        return await indexedDBService.updateStudent(studentId, studentData);
      }
    } catch (error) {
      console.warn('API call failed, saving to IndexedDB only:', error);
      return await indexedDBService.updateStudent(studentId, studentData);
    }
  }

  async deleteStudent(studentId) {
    try {
      if (this.isOnline) {
        await studentsAPI.deleteStudent(studentId);
        // Also remove from IndexedDB
        await indexedDBService.deleteStudent(studentId);
      } else {
        // Mark for deletion in IndexedDB (will sync later)
        await indexedDBService.deleteStudent(studentId);
      }
    } catch (error) {
      console.warn('API call failed, marking for deletion in IndexedDB:', error);
      await indexedDBService.deleteStudent(studentId);
    }
  }

  // Attendance API with offline support
  async getAttendance(date = null, classId = null) {
    try {
      if (this.isOnline) {
        const response = await attendanceAPI.getAttendance(date, classId);
        const attendance = response.data;
        
        // Update local storage
        for (const record of attendance) {
          await indexedDBService.markAttendance(record.student_id, record.date, record.status);
        }
        
        return attendance;
      } else {
        // Fallback to IndexedDB
        const attendance = await indexedDBService.getAttendance(date);
        
        // Filter by class if needed
        if (classId && classId !== 'all') {
          const students = await indexedDBService.getStudents(classId);
          const studentIds = students.map(s => s.id);
          return attendance.filter(record => studentIds.includes(record.studentId));
        }
        
        return attendance;
      }
    } catch (error) {
      console.warn('API call failed, falling back to IndexedDB:', error);
      const attendance = await indexedDBService.getAttendance(date);
      
      if (classId && classId !== 'all') {
        const students = await indexedDBService.getStudents(classId);
        const studentIds = students.map(s => s.id);
        return attendance.filter(record => studentIds.includes(record.studentId));
      }
      
      return attendance;
    }
  }

  async markAttendance(studentId, date, status) {
    try {
      if (this.isOnline) {
        const response = await attendanceAPI.markAttendance(studentId, date, status);
        const record = response.data;
        
        // Also save to IndexedDB
        await indexedDBService.markAttendance(studentId, date, status);
        
        return record;
      } else {
        // Save to IndexedDB only (will sync later)
        return await indexedDBService.markAttendance(studentId, date, status);
      }
    } catch (error) {
      console.warn('API call failed, saving to IndexedDB only:', error);
      return await indexedDBService.markAttendance(studentId, date, status);
    }
  }

  async bulkMarkAttendance(attendanceData) {
    try {
      if (this.isOnline) {
        const response = await attendanceAPI.bulkMarkAttendance(attendanceData);
        const records = response.data;
        
        // Also save to IndexedDB
        await indexedDBService.bulkMarkAttendance(attendanceData);
        
        return records;
      } else {
        // Save to IndexedDB only (will sync later)
        return await indexedDBService.bulkMarkAttendance(attendanceData);
      }
    } catch (error) {
      console.warn('API call failed, saving to IndexedDB only:', error);
      return await indexedDBService.bulkMarkAttendance(attendanceData);
    }
  }

  // Get attendance for specific students (for display purposes)
  async getStudentsWithAttendance(date, classFilter = null) {
    try {
      const students = await this.getStudents(classFilter);
      const attendance = await this.getAttendance(date);
      
      // Create a map of student attendance
      const attendanceMap = {};
      attendance.forEach(record => {
        attendanceMap[record.studentId || record.student_id] = record.status;
      });
      
      // Merge students with their attendance status
      return students.map(student => ({
        ...student,
        status: attendanceMap[student.id] || 'not_marked'
      }));
    } catch (error) {
      console.error('Error getting students with attendance:', error);
      throw error;
    }
  }

  // Check if offline
  isOffline() {
    return !this.isOnline;
  }

  // Get sync status
  async getSyncStatus() {
    const syncQueue = await indexedDBService.getSyncQueue();
    return {
      isOffline: this.isOffline(),
      pendingSync: syncQueue.length,
      lastSync: localStorage.getItem('lastSyncTime') || 'Never'
    };
  }

  // Force sync when online
  async forceSync() {
    if (this.isOnline) {
      await indexedDBService.syncOfflineData();
      localStorage.setItem('lastSyncTime', new Date().toISOString());
    }
  }
}

// Create singleton instance
const offlineAPI = new OfflineAwareAPI();

export default offlineAPI;
