// IndexedDB service for offline functionality
const DB_NAME = 'AttenSyncDB';
const DB_VERSION = 1;

// Store names
const STORES = {
  STUDENTS: 'students',
  ATTENDANCE: 'attendance',
  SYNC_QUEUE: 'syncQueue'
};

class IndexedDBService {
  constructor() {
    this.db = null;
    this.isOnline = navigator.onLine;
    this.initializeDB();
    this.setupOnlineListener();
  }

  async initializeDB() {
    return new Promise((resolve, reject) => {
      const request = indexedDB.open(DB_NAME, DB_VERSION);

      request.onerror = () => {
        console.error('Error opening IndexedDB:', request.error);
        reject(request.error);
      };

      request.onsuccess = () => {
        this.db = request.result;
        console.log('IndexedDB opened successfully');
        resolve(this.db);
      };

      request.onupgradeneeded = (event) => {
        const db = event.target.result;

        // Students store
        if (!db.objectStoreNames.contains(STORES.STUDENTS)) {
          const studentsStore = db.createObjectStore(STORES.STUDENTS, { keyPath: 'id' });
          studentsStore.createIndex('class', 'class', { unique: false });
          studentsStore.createIndex('name', 'name', { unique: false });
        }

        // Attendance store
        if (!db.objectStoreNames.contains(STORES.ATTENDANCE)) {
          const attendanceStore = db.createObjectStore(STORES.ATTENDANCE, { keyPath: 'id' });
          attendanceStore.createIndex('studentId', 'studentId', { unique: false });
          attendanceStore.createIndex('date', 'date', { unique: false });
          attendanceStore.createIndex('studentDate', ['studentId', 'date'], { unique: true });
        }

        // Sync queue for offline operations
        if (!db.objectStoreNames.contains(STORES.SYNC_QUEUE)) {
          const syncStore = db.createObjectStore(STORES.SYNC_QUEUE, { keyPath: 'id', autoIncrement: true });
          syncStore.createIndex('timestamp', 'timestamp', { unique: false });
          syncStore.createIndex('operation', 'operation', { unique: false });
        }
      };
    });
  }

  setupOnlineListener() {
    window.addEventListener('online', () => {
      this.isOnline = true;
      this.syncOfflineData();
    });

    window.addEventListener('offline', () => {
      this.isOnline = false;
    });
  }

  // Students operations
  async addStudent(student) {
    const transaction = this.db.transaction([STORES.STUDENTS], 'readwrite');
    const store = transaction.objectStore(STORES.STUDENTS);
    
    try {
      await store.add(student);
      
      if (!this.isOnline) {
        await this.addToSyncQueue('ADD_STUDENT', student);
      }
      
      return student;
    } catch (error) {
      console.error('Error adding student to IndexedDB:', error);
      throw error;
    }
  }

  async updateStudent(studentId, studentData) {
    const transaction = this.db.transaction([STORES.STUDENTS], 'readwrite');
    const store = transaction.objectStore(STORES.STUDENTS);
    
    try {
      const student = { ...studentData, id: studentId };
      await store.put(student);
      
      if (!this.isOnline) {
        await this.addToSyncQueue('UPDATE_STUDENT', student);
      }
      
      return student;
    } catch (error) {
      console.error('Error updating student in IndexedDB:', error);
      throw error;
    }
  }

  async getStudents(classFilter = null) {
    const transaction = this.db.transaction([STORES.STUDENTS], 'readonly');
    const store = transaction.objectStore(STORES.STUDENTS);
    
    try {
      let request;
      if (classFilter && classFilter !== 'all') {
        const index = store.index('class');
        request = index.getAll(classFilter);
      } else {
        request = store.getAll();
      }
      
      return new Promise((resolve, reject) => {
        request.onsuccess = () => resolve(request.result);
        request.onerror = () => reject(request.error);
      });
    } catch (error) {
      console.error('Error getting students from IndexedDB:', error);
      throw error;
    }
  }

  async deleteStudent(studentId) {
    const transaction = this.db.transaction([STORES.STUDENTS], 'readwrite');
    const store = transaction.objectStore(STORES.STUDENTS);
    
    try {
      await store.delete(studentId);
      
      if (!this.isOnline) {
        await this.addToSyncQueue('DELETE_STUDENT', { id: studentId });
      }
    } catch (error) {
      console.error('Error deleting student from IndexedDB:', error);
      throw error;
    }
  }

  // Attendance operations
  async markAttendance(studentId, date, status) {
    const transaction = this.db.transaction([STORES.ATTENDANCE], 'readwrite');
    const store = transaction.objectStore(STORES.ATTENDANCE);
    
    const attendanceRecord = {
      id: `${studentId}_${date}`,
      studentId,
      date,
      status,
      timestamp: new Date().toISOString(),
      synced: this.isOnline
    };
    
    try {
      await store.put(attendanceRecord);
      
      if (!this.isOnline) {
        await this.addToSyncQueue('MARK_ATTENDANCE', attendanceRecord);
      }
      
      return attendanceRecord;
    } catch (error) {
      console.error('Error marking attendance in IndexedDB:', error);
      throw error;
    }
  }

  async getAttendance(date = null, studentId = null) {
    const transaction = this.db.transaction([STORES.ATTENDANCE], 'readonly');
    const store = transaction.objectStore(STORES.ATTENDANCE);
    
    try {
      if (date && studentId) {
        const index = store.index('studentDate');
        const request = index.get([studentId, date]);
        return new Promise((resolve, reject) => {
          request.onsuccess = () => resolve(request.result);
          request.onerror = () => reject(request.error);
        });
      } else if (date) {
        const index = store.index('date');
        const request = index.getAll(date);
        return new Promise((resolve, reject) => {
          request.onsuccess = () => resolve(request.result);
          request.onerror = () => reject(request.error);
        });
      } else if (studentId) {
        const index = store.index('studentId');
        const request = index.getAll(studentId);
        return new Promise((resolve, reject) => {
          request.onsuccess = () => resolve(request.result);
          request.onerror = () => reject(request.error);
        });
      } else {
        const request = store.getAll();
        return new Promise((resolve, reject) => {
          request.onsuccess = () => resolve(request.result);
          request.onerror = () => reject(request.error);
        });
      }
    } catch (error) {
      console.error('Error getting attendance from IndexedDB:', error);
      throw error;
    }
  }

  async bulkMarkAttendance(attendanceData) {
    const transaction = this.db.transaction([STORES.ATTENDANCE], 'readwrite');
    const store = transaction.objectStore(STORES.ATTENDANCE);
    
    try {
      const promises = attendanceData.map(async (record) => {
        const attendanceRecord = {
          id: `${record.studentId}_${record.date}`,
          studentId: record.studentId,
          date: record.date,
          status: record.status,
          timestamp: new Date().toISOString(),
          synced: this.isOnline
        };
        
        return store.put(attendanceRecord);
      });
      
      await Promise.all(promises);
      
      if (!this.isOnline) {
        await this.addToSyncQueue('BULK_ATTENDANCE', attendanceData);
      }
      
      return attendanceData;
    } catch (error) {
      console.error('Error bulk marking attendance in IndexedDB:', error);
      throw error;
    }
  }

  // Sync queue operations
  async addToSyncQueue(operation, data) {
    const transaction = this.db.transaction([STORES.SYNC_QUEUE], 'readwrite');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);
    
    const syncItem = {
      operation,
      data,
      timestamp: new Date().toISOString()
    };
    
    try {
      await store.add(syncItem);
    } catch (error) {
      console.error('Error adding to sync queue:', error);
      throw error;
    }
  }

  async getSyncQueue() {
    const transaction = this.db.transaction([STORES.SYNC_QUEUE], 'readonly');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);
    
    return new Promise((resolve, reject) => {
      const request = store.getAll();
      request.onsuccess = () => resolve(request.result);
      request.onerror = () => reject(request.error);
    });
  }

  async clearSyncQueue() {
    const transaction = this.db.transaction([STORES.SYNC_QUEUE], 'readwrite');
    const store = transaction.objectStore(STORES.SYNC_QUEUE);
    
    return new Promise((resolve, reject) => {
      const request = store.clear();
      request.onsuccess = () => resolve();
      request.onerror = () => reject(request.error);
    });
  }

  // Sync offline data when online
  async syncOfflineData() {
    if (!this.isOnline) return;
    
    try {
      const syncQueue = await this.getSyncQueue();
      
      for (const item of syncQueue) {
        try {
          // Here you would call the actual API endpoints
          // This is a placeholder for the actual sync logic
          console.log('Syncing:', item.operation, item.data);
          
          // Mark as synced in the respective stores
          await this.markAsSynced(item);
        } catch (error) {
          console.error('Error syncing item:', error);
        }
      }
      
      await this.clearSyncQueue();
      console.log('Offline data synced successfully');
    } catch (error) {
      console.error('Error syncing offline data:', error);
    }
  }

  async markAsSynced(syncItem) {
    // Mark attendance records as synced
    if (syncItem.operation.includes('ATTENDANCE')) {
      const transaction = this.db.transaction([STORES.ATTENDANCE], 'readwrite');
      const store = transaction.objectStore(STORES.ATTENDANCE);
      
      if (Array.isArray(syncItem.data)) {
        // Bulk attendance
        for (const record of syncItem.data) {
          const existing = await store.get(`${record.studentId}_${record.date}`);
          if (existing) {
            existing.synced = true;
            await store.put(existing);
          }
        }
      } else {
        // Single attendance
        const existing = await store.get(syncItem.data.id);
        if (existing) {
          existing.synced = true;
          await store.put(existing);
        }
      }
    }
  }

  // Initialize with fake student data
  async initializeFakeData() {
    const fakeStudents = [
      { id: 'S001', name: 'Aarav Sharma', class: '5A', attendanceRate: 94, lastAttendance: '2025-09-16', parentContact: '+91 9876543210', rollNo: '001' },
      { id: 'S002', name: 'Diya Patel', class: '5A', attendanceRate: 98, lastAttendance: '2025-09-16', parentContact: '+91 9876543211', rollNo: '002' },
      { id: 'S003', name: 'Arjun Kumar', class: '5A', attendanceRate: 87, lastAttendance: '2025-09-15', parentContact: '+91 9876543212', rollNo: '003' },
      { id: 'S004', name: 'Priya Singh', class: '5B', attendanceRate: 92, lastAttendance: '2025-09-16', parentContact: '+91 9876543213', rollNo: '004' },
      { id: 'S005', name: 'Rahul Verma', class: '5B', attendanceRate: 89, lastAttendance: '2025-09-15', parentContact: '+91 9876543214', rollNo: '005' },
      { id: 'S006', name: 'Sneha Gupta', class: '5B', attendanceRate: 96, lastAttendance: '2025-09-16', parentContact: '+91 9876543215', rollNo: '006' },
      { id: 'S007', name: 'Karan Joshi', class: '6A', attendanceRate: 91, lastAttendance: '2025-09-16', parentContact: '+91 9876543216', rollNo: '007' },
      { id: 'S008', name: 'Anisha Reddy', class: '6A', attendanceRate: 95, lastAttendance: '2025-09-16', parentContact: '+91 9876543217', rollNo: '008' },
      { id: 'S009', name: 'Vikram Singh', class: '6A', attendanceRate: 88, lastAttendance: '2025-09-15', parentContact: '+91 9876543218', rollNo: '009' },
      { id: 'S010', name: 'Kavya Nair', class: '6B', attendanceRate: 97, lastAttendance: '2025-09-16', parentContact: '+91 9876543219', rollNo: '010' }
    ];

    try {
      // Check if data already exists
      const existingStudents = await this.getStudents();
      if (existingStudents.length === 0) {
        // Add fake students
        for (const student of fakeStudents) {
          await this.addStudent(student);
        }
        console.log('Fake student data initialized');
      }
    } catch (error) {
      console.error('Error initializing fake data:', error);
    }
  }

  // Check connection status
  isOffline() {
    return !this.isOnline;
  }
}

// Create singleton instance
const indexedDBService = new IndexedDBService();

export default indexedDBService;
