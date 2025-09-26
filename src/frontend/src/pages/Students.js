import React, { useState, useEffect } from 'react';
import { Search, Filter, Plus, Edit, Trash2, User, WifiOff } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import { useTranslateObjects } from '../hooks/useTranslation';
import LoadingSpinner from '../components/LoadingSpinner';
import offlineAPI from '../services/offlineAPI';

const Students = () => {
  const { t } = useLanguage();
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedClass, setSelectedClass] = useState('all');
  const [showAddModal, setShowAddModal] = useState(false);
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isOffline, setIsOffline] = useState(false);

  // Load students data
  useEffect(() => {
    loadStudents();
    
    // Listen for online/offline events
    const handleOnline = () => {
      setIsOffline(false);
      loadStudents(); // Refresh data when back online
    };
    const handleOffline = () => setIsOffline(true);
    
    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);
    
    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
    };
  }, [selectedClass]);

  const loadStudents = async () => {
    setLoading(true);
    try {
      const studentsData = await offlineAPI.getStudents(
        selectedClass === 'all' ? null : selectedClass,
        searchTerm
      );
      setStudents(studentsData);
      setIsOffline(offlineAPI.isOffline());
    } catch (error) {
      console.error('Error loading students:', error);
      setStudents([]);
    } finally {
      setLoading(false);
    }
  };

  // Reload when search term changes (with debounce)
  useEffect(() => {
    const timer = setTimeout(() => {
      if (!loading) loadStudents();
    }, 300);
    
    return () => clearTimeout(timer);
  }, [searchTerm]);

  // Auto-translate student names and other text fields
  const { translatedObjects: translatedStudents, loading: studentsLoading } = useTranslateObjects(
    students, 
    ['name'] // Translate only the name field
  );

  const filteredStudents = translatedStudents.filter(student => {
    const matchesSearch = student.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         student.id.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesClass = selectedClass === 'all' || student.class === selectedClass;
    return matchesSearch && matchesClass;
  });

  const deleteStudent = (studentId) => {
    if (window.confirm('Are you sure you want to delete this student?')) {
      setStudents(students.filter(student => student.id !== studentId));
    }
  };

  const getAttendanceColor = (rate) => {
    if (rate >= 95) return 'text-green-600 bg-green-100';
    if (rate >= 85) return 'text-yellow-600 bg-yellow-100';
    return 'text-red-600 bg-red-100';
  };

  const classes = ['all', '5A', '5B', '6A', '6B', '7A', '7B'];

  const AddStudentModal = () => (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white rounded-2xl p-6 w-full max-w-md mx-4">
        <h3 className="text-xl font-bold text-neutral-dark mb-4">{t('addNewStudent')}</h3>
        <form className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">{t('studentId')}</label>
            <input
              type="text"
              className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder={t('enterStudentId')}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">{t('fullName')}</label>
            <input
              type="text"
              className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder={t('enterFullName')}
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">{t('class')}</label>
            <select className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent">
              {classes.filter(cls => cls !== 'all').map(cls => (
                <option key={cls} value={cls}>{t('class')} {cls}</option>
              ))}
            </select>
          </div>
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">{t('parentContact')}</label>
            <input
              type="tel"
              className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent"
              placeholder={t('enterParentContact')}
            />
          </div>
          <div className="flex gap-3 pt-4">
            <button
              type="button"
              onClick={() => setShowAddModal(false)}
              className="flex-1 px-4 py-2 border border-gray-300 text-gray-700 rounded-2xl hover:bg-gray-50 transition-colors"
            >
              {t('cancel')}
            </button>
            <button
              type="submit"
              className="flex-1 px-4 py-2 bg-primary text-white rounded-2xl hover:bg-green-700 transition-colors"
            >
              {t('addStudent')}
            </button>
          </div>
        </form>
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-neutral-dark mb-2">{t('students')}</h1>
            <p className="text-gray-600">{t('manageStudentInfo')}</p>
          </div>
          <button
            onClick={() => setShowAddModal(true)}
            className="mt-4 lg:mt-0 px-6 py-2 bg-primary text-white rounded-2xl hover:bg-green-700 transition-colors flex items-center gap-2"
          >
            <Plus className="h-4 w-4" />
            {t('addStudent')}
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Search */}
          <div>
            <label className="block text-sm font-medium text-neutral-dark mb-2">
              <Search className="inline h-4 w-4 mr-1" />
              {t('searchStudent')}
            </label>
            <input
              type="text"
              placeholder={t('searchStudents')}
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

      {/* Students Grid */}
      {studentsLoading ? (
        <div className="bg-white rounded-2xl p-12 shadow-lg">
          <LoadingSpinner size="large" />
          <p className="text-center text-gray-600 mt-4">
            {t('loadingTranslations')}...
          </p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredStudents.map((student) => (
          <div key={student.id} className="bg-white rounded-2xl p-6 shadow-lg hover:shadow-xl transition-shadow">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center">
                <div className="w-12 h-12 bg-primary-light rounded-full flex items-center justify-center mr-3">
                  <User className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-neutral-dark">{student.name}</h3>
                  <p className="text-sm text-gray-600">{student.id}</p>
                </div>
              </div>
              <div className="flex gap-1">
                <button className="p-2 text-gray-400 hover:text-primary transition-colors">
                  <Edit className="h-4 w-4" />
                </button>
                <button 
                  onClick={() => deleteStudent(student.id)}
                  className="p-2 text-gray-400 hover:text-red-500 transition-colors"
                >
                  <Trash2 className="h-4 w-4" />
                </button>
              </div>
            </div>

            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{t('class')}:</span>
                <span className="font-medium text-neutral-dark">{student.class}</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{t('attendance')}:</span>
                <span className={`px-2 py-1 rounded-full text-xs font-medium ${getAttendanceColor(student.attendanceRate)}`}>
                  {student.attendanceRate}%
                </span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{t('lastAttended')}:</span>
                <span className="text-sm text-neutral-dark">{student.lastAttendance}</span>
              </div>
              
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">{t('parentContact')}:</span>
                <span className="text-sm text-neutral-dark">{student.parentContact}</span>
              </div>
            </div>

            <div className="mt-4 pt-4 border-t border-gray-200">
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div 
                  className="bg-primary h-2 rounded-full transition-all"
                  style={{ width: `${student.attendanceRate}%` }}
                ></div>
              </div>
              <p className="text-xs text-gray-500 mt-1 text-center">
                {t('attendanceProgress')}
              </p>
            </div>
          </div>
          ))}
        </div>
      )}

      {/* Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="bg-white rounded-2xl p-4 shadow-lg text-center">
          <p className="text-2xl font-bold text-primary">{students.length}</p>
          <p className="text-sm text-gray-600">{t('totalStudents')}</p>
        </div>
        <div className="bg-white rounded-2xl p-4 shadow-lg text-center">
          <p className="text-2xl font-bold text-green-600">
            {students.filter(s => s.attendanceRate >= 95).length}
          </p>
          <p className="text-sm text-gray-600">{t('excellent')} (95%+)</p>
        </div>
        <div className="bg-white rounded-2xl p-4 shadow-lg text-center">
          <p className="text-2xl font-bold text-yellow-600">
            {students.filter(s => s.attendanceRate >= 85 && s.attendanceRate < 95).length}
          </p>
          <p className="text-sm text-gray-600">{t('good')} (85-94%)</p>
        </div>
        <div className="bg-white rounded-2xl p-4 shadow-lg text-center">
          <p className="text-2xl font-bold text-red-600">
            {students.filter(s => s.attendanceRate < 85).length}
          </p>
          <p className="text-sm text-gray-600">{t('needsAttention')} (&lt;85%)</p>
        </div>
      </div>

      {/* Add Student Modal */}
      {showAddModal && <AddStudentModal />}
    </div>
  );
};

export default Students;
