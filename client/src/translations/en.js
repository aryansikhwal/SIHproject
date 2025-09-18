const translations = {
  // Common
  loading: 'Loading...',
  error: 'An error occurred',
  success: 'Success',
  save: 'Save',
  cancel: 'Cancel',
  delete: 'Delete',
  edit: 'Edit',
  add: 'Add',
  search: 'Search',
  filter: 'Filter',
  export: 'Export',
  teacher: 'Teacher',
  principal: 'Principal',
  
  // Login
  login: {
    title: 'Sign in to AttenSync',
    username: 'Username',
    password: 'Password',
    submit: 'Sign in',
    loading: 'Signing in...',
    error: 'Invalid username or password',
  },
  
  // Navigation
  nav: {
    dashboard: 'Dashboard',
    attendance: 'Attendance',
    students: 'Students',
    reports: 'Reports',
    trends: 'Trends',
    settings: 'Settings',
  },

  // Dashboard
  dashboard: {
    title: 'Dashboard',
    totalStudents: 'Total Students',
    presentToday: 'Present Today',
    attendanceRate: 'Attendance Rate',
    recentActivity: 'Recent Activity',
    weeklyTrends: 'Weekly Trends',
  },

  // Attendance
  attendance: {
    title: 'Attendance',
    markAttendance: 'Mark Attendance',
    bulkUpload: 'Bulk Upload',
    present: 'Present',
    absent: 'Absent',
    date: 'Date',
    class: 'Class',
    status: 'Status',
  },

  // Students
  students: {
    title: 'Students',
    addStudent: 'Add Student',
    editStudent: 'Edit Student',
    studentDetails: 'Student Details',
    rollNumber: 'Roll Number',
    name: 'Name',
    fatherName: "Father's Name",
    motherName: "Mother's Name",
    contactNumber: 'Contact Number',
    actions: 'Actions',
  },

  // Reports
  reports: {
    title: 'Reports',
    generateReport: 'Generate Report',
    classWise: 'Class-wise Report',
    monthlyReport: 'Monthly Report',
    customRange: 'Custom Range',
    startDate: 'Start Date',
    endDate: 'End Date',
  },

  // Trends
  trends: {
    title: 'Trends',
    forecast: 'Attendance Forecast',
    seasonalPatterns: 'Seasonal Patterns',
    weeklyPatterns: 'Weekly Patterns',
    yearlyComparison: 'Yearly Comparison',
  },

  // Settings
  settings: {
    title: 'Settings',
    generalSettings: 'General Settings',
    notifications: 'Notifications',
    dataSync: 'Data Synchronization',
    systemInfo: 'System Information',
  },

  // Errors
  errors: {
    networkError: 'Network error. Please check your connection.',
    serverError: 'Server error. Please try again later.',
    authError: 'Authentication required',
    accessDenied: 'Access denied',
    invalidRequest: 'Invalid request data',
  },
};

export default translations;