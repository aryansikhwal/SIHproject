import React, { useState, useEffect } from 'react';
import { Calendar, Download, Search, Filter, CheckCircle, XCircle, WifiOff } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import offlineAPI from '../services/offlineAPI';

const Attendance = () => {
  const { t } = useLanguage();
  const [selectedDate, setSelectedDate] = useState(new Date().toISOString().split('T')[0]);
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedClass, setSelectedClass] = useState('all');
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isOffline, setIsOffline] = useState(false);

  // Load students with attendance data
  useEffect(() => {
    loadStudentsWithAttendance();
    
    // Listen for online/offline events
    const handleOnline = () => {
      setIsOffline(false);
      loadStudentsWithAttendance(); // Refresh data when back online
    };
    const handleOffline = () => setIsOffline(true);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [selectedDate, selectedClass]);

  const loadStudentsWithAttendance = async () => {
    setLoading(true);
    try {
      const studentsWithAttendance = await offlineAPI.getStudentsWithAttendance(
        selectedDate, 
        selectedClass === 'all' ? null : selectedClass
      );
      setStudents(studentsWithAttendance);
      setIsOffline(offlineAPI.isOffline());
    } catch (error) {
      console.error('Error loading students:', error);
      // Fallback to empty array on error
      setStudents([]);
    } finally {
      setLoading(false);
    }
  };

  const filteredStudents = students.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesClass = selectedClass === 'all' || student.class === selectedClass;
    return matchesSearch && matchesClass;
  });

  const toggleAttendance = async (studentId) => {
    const student = students.find(s => s.id === studentId);
    const newStatus = student.status === 'present' ? 'absent' : 'present';
    
    try {
      // Update in database/indexedDB
      await offlineAPI.markAttendance(studentId, selectedDate, newStatus);
      
      // Update local state
      setStudents(students.map(s => 
        s.id === studentId ? { ...s, status: newStatus } : s
      ));
    } catch (error) {
      console.error('Error updating attendance:', error);
      // Could show a toast notification here
    }
  };

  const markAllPresent = async () => {
    try {
      const attendanceData = students.map(student => ({
        studentId: student.id,
        date: selectedDate,
        status: 'present'
      }));
      
      // Bulk update in database/indexedDB
      await offlineAPI.bulkMarkAttendance(attendanceData);
      
      // Update local state
      setStudents(students.map(student => ({ ...student, status: 'present' })));
    } catch (error) {
      console.error('Error marking all present:', error);
    }
  };

  const exportAttendance = () => {
    // Mock export functionality
    alert('Attendance exported successfully!');
  };

  const classes = ['all', '5A', '5B', '6A', '6B', '7A', '7B'];

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-neutral-dark mb-2">{t('attendance')}</h1>
            <p className="text-gray-600">{t('markManageAttendance')}</p>
            {isOffline && (
              <div className="flex items-center gap-2 mt-2 text-yellow-600">
                <WifiOff className="h-4 w-4" />
                <span className="text-sm">Working offline - changes will sync when online</span>
              </div>
            )}
          </div>
          <div className="mt-4 lg:mt-0 flex flex-col sm:flex-row gap-3">
            <button
              onClick={markAllPresent}
              className="px-6 py-2 bg-primary-light text-white rounded-2xl hover:bg-primary transition-colors"
            >
              {t('markAllPresent')}
            </button>
            <button
              onClick={exportAttendance}
              className="px-6 py-2 bg-primary text-white rounded-2xl hover:bg-green-700 transition-colors flex items-center gap-2"
            >
              <Download className="h-4 w-4" />
              {t('exportCsv')}
            </button>
          </div>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Date Picker */}
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">
              <Calendar className="inline h-4 w-4 mr-1" />
              {t('selectDate')}
            </label>
            <input
              type="date"
              value={selectedDate}
              onChange={(e) => setSelectedDate(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">
              <Search className="inline h-4 w-4 mr-1" />
              {t('searchStudent')}
            </label>
            <input
              type="text"
              placeholder={t('searchByNameOrId')}
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent"
            />
          </div>

          {/* Class Filter */}
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">
              <Filter className="inline h-4 w-4 mr-1" />
              {t('filterByClass')}
            </label>
            <select
              value={selectedClass}
              onChange={(e) => setSelectedClass(e.target.value)}
              className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              {classes.map(cls => (
                <option key={cls} value={cls}>
                  {cls === 'all' ? t('allClasses') : `${t('class')} ${cls}`}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      {/* Attendance Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-dark text-sm font-medium">{t('totalStudents')}</p>
              <p className="text-2xl font-bold text-neutral-dark">{filteredStudents.length}</p>
            </div>
            <div className="p-3 bg-blue-100 rounded-2xl">
              <Calendar className="h-6 w-6 text-blue-600" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-dark text-sm font-medium">{t('present')}</p>
              <p className="text-2xl font-bold text-primary">
                {filteredStudents.filter(s => s.status === 'present').length}
              </p>
            </div>
            <div className="p-3 bg-green-100 rounded-2xl">
              <CheckCircle className="h-6 w-6 text-primary" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-neutral-dark text-sm font-medium">{t('absent')}</p>
              <p className="text-2xl font-bold text-red-500">
                {filteredStudents.filter(s => s.status === 'absent').length}
              </p>
            </div>
            <div className="p-3 bg-red-100 rounded-2xl">
              <XCircle className="h-6 w-6 text-red-500" />
            </div>
          </div>
        </div>
      </div>

      {/* Attendance Table */}
      <div className="bg-white rounded-2xl shadow-lg overflow-hidden">
        {loading ? (
          <div className="flex items-center justify-center py-12">
            <div className="text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary mx-auto mb-4"></div>
              <p className="text-gray-600">Loading students...</p>
            </div>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('studentId')}
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('name')}
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('class')}
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('status')}
                  </th>
                  <th className="px-6 py-4 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                    {t('action')}
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {filteredStudents.length === 0 ? (
                  <tr>
                    <td colSpan="5" className="px-6 py-12 text-center text-gray-500">
                      No students found
                    </td>
                  </tr>
                ) : (
                  filteredStudents.map((student) => (
                    <tr key={student.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-neutral-dark">
                        {student.id}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-dark">
                        {student.name}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-neutral-dark">
                        {student.class}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className={`px-3 py-1 inline-flex text-xs leading-5 font-semibold rounded-full ${
                          student.status === 'present' 
                            ? 'bg-green-100 text-green-800' 
                            : student.status === 'absent'
                            ? 'bg-red-100 text-red-800'
                            : 'bg-gray-100 text-gray-800'
                        }`}>
                          {student.status === 'not_marked' ? 'Not Marked' : t(student.status)}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <button
                          onClick={() => toggleAttendance(student.id)}
                          className={`px-4 py-2 text-xs font-medium rounded-2xl transition-colors ${
                            student.status === 'present'
                              ? 'bg-red-100 text-red-700 hover:bg-red-200'
                              : 'bg-green-100 text-green-700 hover:bg-green-200'
                          }`}
                        >
                          {t('mark')} {student.status === 'present' ? t('absent') : t('present')}
                        </button>
                      </td>
                    </tr>
                  ))
                )}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};

export default Attendance;
