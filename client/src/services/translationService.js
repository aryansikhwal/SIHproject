// Simple browser-based translation service
// Note: For production, integrate with Google Translate API or similar service

// Cache for translated text to avoid repeated API calls
const translationCache = new Map();

// Static UI translations (fast, no API calls needed)
export const staticTranslations = {
  en: {
    // Navigation
    dashboard: "Dashboard",
    attendance: "Attendance", 
    students: "Students",
    reports: "Reports",
    trends: "Trends",
    settings: "Settings",
    
    // Dashboard
    totalStudents: "Total Students",
    presentToday: "Present Today",
    absentToday: "Absent Today", 
    attendanceRate: "Attendance Rate",
    weeklyAverage: "Weekly Average",
    fromLastWeek: "from last week",
    absentees: "absentees",
    welcomeMessage: "Welcome back! Here's your attendance overview for today.",
    recentActivity: "Recent Activity",
    attendanceOverview: "Attendance Overview",
    monthlyTrends: "Monthly Trends",
    classAttendanceMarked: "Class 5A attendance marked",
    weeklyReportGenerated: "Weekly report generated",
    newStudentsAdded: "3 new students added",
    minutesAgo: "2 minutes ago",
    hourAgo: "1 hour ago",
    yesterday: "Yesterday",
    complete: "Complete",
    new: "New",
    processed: "Processed",
    
    // Students
    addStudent: "Add Student",
    addNewStudent: "Add New Student",
    searchStudents: "Search students...",
    searchStudent: "Search Student",
    allStudents: "All Students",
    allClasses: "All Classes",
    class: "Class",
    filterByClass: "Filter by Class",
    manageStudentInfo: "Manage student information and records",
    studentId: "Student ID",
    fullName: "Full Name",
    enterStudentId: "Enter student ID",
    enterFullName: "Enter full name",
    enterParentContact: "Enter parent contact number",
    parentContact: "Parent Contact",
    lastAttended: "Last Attended",
    attendanceProgress: "Attendance Progress",
    needsAttention: "Needs Attention",
    loadingTranslations: "Loading translations",
    excellent: "Excellent",
    good: "Good", 
    needsImprovement: "Needs Improvement",
    editStudent: "Edit Student",
    deleteStudent: "Delete Student",
    
    // Attendance
    markAttendance: "Mark Attendance",
    markManageAttendance: "Mark and manage student attendance",
    selectDate: "Select Date",
    exportCsv: "Export CSV",
    markAllPresent: "Mark All Present",
    markAllAbsent: "Mark All Absent",
    searchByNameOrId: "Search by name or ID...",
    name: "Name",
    status: "Status",
    action: "Action",
    mark: "Mark",
    present: "Present",
    absent: "Absent",
    
    // Reports
    generateReport: "Generate Report",
    exportReport: "Export Report",
    keyInsights: "Key Insights",
    
    // Trends
    aiPredictions: "AI Predictions",
    seasonalAnalysis: "Seasonal Analysis",
    overallTrend: "Overall Trend",
    weeklyTrend: "Weekly Trend", 
    monthlyTrend: "Monthly Trend",
    
    // Settings
    schoolInformation: "School Information",
    notifications: "Notifications", 
    security: "Security",
    dataSync: "Data Sync",
    schoolName: "School Name",
    address: "Address",
    contactNumber: "Contact Number",
    principalName: "Principal Name",
    emailNotifications: "Email Notifications",
    smsNotifications: "SMS Notifications",
    pushNotifications: "Push Notifications",
    changePassword: "Change Password",
    enableTwoFactor: "Enable Two-Factor Authentication",
    autoSync: "Auto Sync",
    backupData: "Backup Data",
    
    // Common
    save: "Save",
    cancel: "Cancel",
    edit: "Edit",
    delete: "Delete",
    view: "View",
    search: "Search",
    filter: "Filter",
    language: "Language",
    loading: "Loading...",
    
    // Profile
    profile: "Profile",
    logout: "Logout",
    teacher: "Teacher"
  },
  
  hi: {
    // Navigation
    dashboard: "डैशबोर्ड",
    attendance: "उपस्थिति",
    students: "छात्र",
    reports: "रिपोर्ट",
    trends: "रुझान",
    settings: "सेटिंग्स",
    
    // Dashboard
    totalStudents: "कुल छात्र",
    presentToday: "आज उपस्थित",
    absentToday: "आज अनुपस्थित",
    attendanceRate: "उपस्थिति दर",
    weeklyAverage: "साप्ताहिक औसत",
    fromLastWeek: "पिछले सप्ताह से",
    absentees: "अनुपस्थित",
    welcomeMessage: "वापसी पर स्वागत! यहाँ आज की आपकी उपस्थिति का अवलोकन है।",
    recentActivity: "हाल की गतिविधि",
    attendanceOverview: "उपस्थिति अवलोकन",
    monthlyTrends: "मासिक रुझान",
    classAttendanceMarked: "कक्षा 5A उपस्थिति चिह्नित",
    weeklyReportGenerated: "साप्ताहिक रिपोर्ट तैयार",
    newStudentsAdded: "3 नए छात्र जोड़े गए",
    minutesAgo: "2 मिनट पहले",
    hourAgo: "1 घंटा पहले",
    yesterday: "कल",
    complete: "पूर्ण",
    new: "नया",
    processed: "प्रक्रिया पूर्ण",
    
    // Students
    addStudent: "छात्र जोड़ें",
    addNewStudent: "नया छात्र जोड़ें",
    searchStudents: "छात्रों को खोजें...",
    searchStudent: "छात्र खोजें",
    allStudents: "सभी छात्र",
    allClasses: "सभी कक्षाएं",
    class: "कक्षा",
    filterByClass: "कक्षा के अनुसार फिल्टर करें",
    manageStudentInfo: "छात्र की जानकारी और रिकॉर्ड प्रबंधित करें",
    studentId: "छात्र आईडी",
    fullName: "पूरा नाम",
    enterStudentId: "छात्र आईडी दर्ज करें",
    enterFullName: "पूरा नाम दर्ज करें",
    enterParentContact: "माता-पिता का संपर्क नंबर दर्ज करें",
    parentContact: "माता-पिता का संपर्क",
    lastAttended: "अंतिम उपस्थिति",
    attendanceProgress: "उपस्थिति प्रगति",
    needsAttention: "ध्यान की आवश्यकता",
    loadingTranslations: "अनुवाद लोड हो रहे हैं",
    excellent: "उत्कृष्ट",
    good: "अच्छा",
    needsImprovement: "सुधार की आवश्यकता",
    editStudent: "छात्र संपादित करें",
    deleteStudent: "छात्र हटाएं",
    
    // Attendance
    markAttendance: "उपस्थिति चिह्नित करें",
    markManageAttendance: "छात्र उपस्थिति चिह्नित और प्रबंधित करें",
    selectDate: "दिनांक चुनें",
    exportCsv: "CSV निर्यात करें",
    markAllPresent: "सभी को उपस्थित चिह्नित करें",
    markAllAbsent: "सभी को अनुपस्थित चिह्नित करें",
    searchByNameOrId: "नाम या आईडी से खोजें...",
    name: "नाम",
    status: "स्थिति",
    action: "कार्य",
    mark: "चिह्नित करें",
    present: "उपस्थित",
    absent: "अनुपस्थित",
    
    // Reports
    generateReport: "रिपोर्ट तैयार करें",
    exportReport: "रिपोर्ट निर्यात करें",
    keyInsights: "मुख्य अंतर्दृष्टि",
    
    // Trends
    aiPredictions: "AI भविष्यवाणियां",
    seasonalAnalysis: "मौसमी विश्लेषण",
    overallTrend: "समग्र रुझान",
    weeklyTrend: "साप्ताहिक रुझान",
    monthlyTrend: "मासिक रुझान",
    
    // Settings
    schoolInformation: "स्कूल की जानकारी",
    notifications: "सूचनाएं",
    security: "सुरक्षा",
    dataSync: "डेटा सिंक",
    schoolName: "स्कूल का नाम",
    address: "पता",
    contactNumber: "संपर्क नंबर",
    principalName: "प्रधानाचार्य का नाम",
    emailNotifications: "ईमेल सूचनाएं",
    smsNotifications: "SMS सूचनाएं",
    pushNotifications: "पुश सूचनाएं",
    changePassword: "पासवर्ड बदलें",
    enableTwoFactor: "द्विकारक प्रमाणीकरण सक्षम करें",
    autoSync: "स्वचालित सिंक",
    backupData: "डेटा बैकअप",
    
    // Common
    save: "सेव करें",
    cancel: "रद्द करें",
    edit: "संपादित करें",
    delete: "हटाएं",
    view: "देखें",
    search: "खोजें",
    filter: "फिल्टर",
    language: "भाषा",
    loading: "लोड हो रहा है...",
    
    // Profile
    profile: "प्रोफाइल",
    logout: "लॉगआउट",
    teacher: "शिक्षक"
  },
  
  pa: {
    // Navigation  
    dashboard: "ਡੈਸ਼ਬੋਰਡ",
    attendance: "ਹਾਜ਼ਰੀ",
    students: "ਵਿਦਿਆਰਥੀ",
    reports: "ਰਿਪੋਰਟਾਂ",
    trends: "ਰੁਝਾਨ",
    settings: "ਸੈਟਿੰਗਾਂ",
    
    // Dashboard
    totalStudents: "ਕੁੱਲ ਵਿਦਿਆਰਥੀ",
    presentToday: "ਅੱਜ ਹਾਜ਼ਰ",
    absentToday: "ਅੱਜ ਗੈਰ-ਹਾਜ਼ਰ",
    attendanceRate: "ਹਾਜ਼ਰੀ ਦਰ",
    weeklyAverage: "ਹਫ਼ਤਾਵਾਰੀ ਔਸਤ",
    fromLastWeek: "ਪਿਛਲੇ ਹਫ਼ਤੇ ਤੋਂ",
    absentees: "ਗੈਰ-ਹਾਜ਼ਰ",
    welcomeMessage: "ਵਾਪਸੀ ਤੇ ਸੁਆਗਤ! ਇੱਥੇ ਅੱਜ ਦੀ ਤੁਹਾਡੀ ਹਾਜ਼ਰੀ ਦਾ ਸਮੀਖਿਆ ਹੈ।",
    recentActivity: "ਹਾਲੀਆ ਗਤੀਵਿਧੀ",
    attendanceOverview: "ਹਾਜ਼ਰੀ ਸਮੀਖਿਆ",
    monthlyTrends: "ਮਾਸਿਕ ਰੁਝਾਨ",
    classAttendanceMarked: "ਕਲਾਸ 5A ਹਾਜ਼ਰੀ ਲਗਾਈ ਗਈ",
    weeklyReportGenerated: "ਹਫ਼ਤਾਵਾਰੀ ਰਿਪੋਰਟ ਤਿਆਰ",
    newStudentsAdded: "3 ਨਵੇਂ ਵਿਦਿਆਰਥੀ ਜੋੜੇ ਗਏ",
    minutesAgo: "2 ਮਿੰਟ ਪਹਿਲਾਂ",
    hourAgo: "1 ਘੰਟਾ ਪਹਿਲਾਂ",
    yesterday: "ਕੱਲ੍ਹ",
    complete: "ਪੂਰਾ",
    new: "ਨਵਾਂ",
    processed: "ਪ੍ਰਕਿਰਿਆ ਪੂਰੀ",
    
    // Students
    addStudent: "ਵਿਦਿਆਰਥੀ ਜੋੜੋ",
    addNewStudent: "ਨਵਾਂ ਵਿਦਿਆਰਥੀ ਜੋੜੋ",
    searchStudents: "ਵਿਦਿਆਰਥੀਆਂ ਨੂੰ ਖੋਜੋ...",
    searchStudent: "ਵਿਦਿਆਰਥੀ ਖੋਜੋ",
    allStudents: "ਸਾਰੇ ਵਿਦਿਆਰਥੀ",
    allClasses: "ਸਾਰੀਆਂ ਕਲਾਸਾਂ",
    class: "ਕਲਾਸ",
    filterByClass: "ਕਲਾਸ ਦੇ ਅਨੁਸਾਰ ਫਿਲਟਰ ਕਰੋ",
    manageStudentInfo: "ਵਿਦਿਆਰਥੀ ਦੀ ਜਾਣਕਾਰੀ ਅਤੇ ਰਿਕਾਰਡ ਪ੍ਰਬੰਧਿਤ ਕਰੋ",
    studentId: "ਵਿਦਿਆਰਥੀ ਆਈਡੀ",
    fullName: "ਪੂਰਾ ਨਾਮ",
    enterStudentId: "ਵਿਦਿਆਰਥੀ ਆਈਡੀ ਦਰਜ ਕਰੋ",
    enterFullName: "ਪੂਰਾ ਨਾਮ ਦਰਜ ਕਰੋ",
    enterParentContact: "ਮਾਤਾ-ਪਿਤਾ ਦਾ ਸੰਪਰਕ ਨੰਬਰ ਦਰਜ ਕਰੋ",
    parentContact: "ਮਾਤਾ-ਪਿਤਾ ਦਾ ਸੰਪਰਕ",
    lastAttended: "ਆਖਰੀ ਹਾਜ਼ਰੀ",
    attendanceProgress: "ਹਾਜ਼ਰੀ ਪ੍ਰਗਤੀ",
    needsAttention: "ਧਿਆਨ ਦੀ ਲੋੜ",
    loadingTranslations: "ਅਨੁਵਾਦ ਲੋਡ ਹੋ ਰਹੇ ਹਨ",
    excellent: "ਸ਼ਾਨਦਾਰ",
    good: "ਚੰਗਾ",
    needsImprovement: "ਸੁਧਾਰ ਦੀ ਲੋੜ",
    editStudent: "ਵਿਦਿਆਰਥੀ ਸੰਪਾਦਿਤ ਕਰੋ",
    deleteStudent: "ਵਿਦਿਆਰਥੀ ਮਿਟਾਓ",
    
    // Attendance
    markAttendance: "ਹਾਜ਼ਰੀ ਲਗਾਓ",
    markManageAttendance: "ਵਿਦਿਆਰਥੀ ਹਾਜ਼ਰੀ ਲਗਾਓ ਅਤੇ ਪ੍ਰਬੰਧਿਤ ਕਰੋ",
    selectDate: "ਤਾਰੀਖ ਚੁਣੋ",
    exportCsv: "CSV ਨਿਰਯਾਤ ਕਰੋ",
    markAllPresent: "ਸਾਰਿਆਂ ਨੂੰ ਹਾਜ਼ਰ ਲਗਾਓ",
    markAllAbsent: "ਸਾਰਿਆਂ ਨੂੰ ਗੈਰ-ਹਾਜ਼ਰ ਲਗਾਓ",
    searchByNameOrId: "ਨਾਮ ਜਾਂ ਆਈਡੀ ਰਾਹੀਂ ਖੋਜੋ...",
    name: "ਨਾਮ",
    status: "ਸਥਿਤੀ",
    action: "ਕਾਰਵਾਈ",
    mark: "ਲਗਾਓ",
    present: "ਹਾਜ਼ਰ",
    absent: "ਗੈਰ-ਹਾਜ਼ਰ",
    
    // Reports
    generateReport: "ਰਿਪੋਰਟ ਤਿਆਰ ਕਰੋ",
    exportReport: "ਰਿਪੋਰਟ ਨਿਰਯਾਤ ਕਰੋ",
    keyInsights: "ਮੁੱਖ ਸਮਝ",
    
    // Trends
    aiPredictions: "AI ਭਵਿੱਖਬਾਣੀਆਂ",
    seasonalAnalysis: "ਮੌਸਮੀ ਵਿਸ਼ਲੇਸ਼ਣ",
    overallTrend: "ਸਮੁੱਚਾ ਰੁਝਾਨ",
    weeklyTrend: "ਹਫ਼ਤਾਵਾਰੀ ਰੁਝਾਨ",
    monthlyTrend: "ਮਾਸਿਕ ਰੁਝਾਨ",
    
    // Settings
    schoolInformation: "ਸਕੂਲ ਦੀ ਜਾਣਕਾਰੀ",
    notifications: "ਸੂਚਨਾਵਾਂ",
    security: "ਸੁਰੱਖਿਆ",
    dataSync: "ਡਾਟਾ ਸਿੰਕ",
    schoolName: "ਸਕੂਲ ਦਾ ਨਾਮ",
    address: "ਪਤਾ",
    contactNumber: "ਸੰਪਰਕ ਨੰਬਰ",
    principalName: "ਪ੍ਰਿੰਸਿਪਲ ਦਾ ਨਾਮ",
    emailNotifications: "ਈਮੇਲ ਸੂਚਨਾਵਾਂ",
    smsNotifications: "SMS ਸੂਚਨਾਵਾਂ",
    pushNotifications: "ਪੁਸ਼ ਸੂਚਨਾਵਾਂ",
    changePassword: "ਪਾਸਵਰਡ ਬਦਲੋ",
    enableTwoFactor: "ਦੋ-ਕਾਰਕ ਪ੍ਰਮਾਣੀਕਰਣ ਸਮਰੱਥ ਕਰੋ",
    autoSync: "ਸਵੈਚਲਿਤ ਸਿੰਕ",
    backupData: "ਡਾਟਾ ਬੈਕਅੱਪ",
    
    // Common
    save: "ਸੇਵ ਕਰੋ",
    cancel: "ਰੱਦ ਕਰੋ",
    edit: "ਸੰਪਾਦਿਤ ਕਰੋ",
    delete: "ਮਿਟਾਓ",
    view: "ਦੇਖੋ",
    search: "ਖੋਜੋ",
    filter: "ਫਿਲਟਰ",
    language: "ਭਾਸ਼ਾ",
    loading: "ਲੋਡ ਹੋ ਰਿਹਾ ਹੈ...",
    
    // Profile
    profile: "ਪ੍ਰੋਫਾਇਲ",
    logout: "ਲਾਗਆਉਟ",
    teacher: "ਅਧਿਆਪਕ"
  }
};

// Language code mapping for Google Translate API
const languageMap = {
  en: 'en',
  hi: 'hi',
  pa: 'pa'
};

/**
 * Auto-translate dynamic content using Google Translate API
 * @param {string} text - Text to translate
 * @param {string} targetLang - Target language code (hi, pa, en)
 * @returns {Promise<string>} - Translated text
 */
export const autoTranslate = async (text, targetLang = 'en') => {
  // If target language is English, return original text
  if (targetLang === 'en' || !text || text.trim() === '') {
    return text;
  }

  // Check cache first
  const cacheKey = `${text}_${targetLang}`;
  if (translationCache.has(cacheKey)) {
    return translationCache.get(cacheKey);
  }

  try {
    // Simulate translation delay for demo purposes
    await new Promise(resolve => setTimeout(resolve, 500));
    
    // Simple demonstration translation (in production, use actual translation API)
    let translatedText = text;
    
    // Basic word replacements for demonstration
    if (targetLang === 'hi') {
      const hindiReplacements = {
        'Welcome': 'स्वागत',
        'Hello': 'नमस्ते',
        'Good morning': 'शुभ प्रभात',
        'Assignment': 'असाइनमेंट',
        'Students': 'छात्र',
        'Teacher': 'शिक्षक',
        'Class': 'कक्षा',
        'School': 'स्कूल',
        'Attendance': 'उपस्थिति'
      };
      
      Object.entries(hindiReplacements).forEach(([english, hindi]) => {
        translatedText = translatedText.replace(new RegExp(english, 'gi'), hindi);
      });
    } else if (targetLang === 'pa') {
      const punjabiReplacements = {
        'Welcome': 'ਜੀ ਆਇਆਂ ਨੂੰ',
        'Hello': 'ਸਤ ਸ੍ਰੀ ਅਕਾਲ',
        'Good morning': 'ਸੁਪਰਭਾਤ',
        'Assignment': 'ਅਸਾਈਨਮੈਂਟ',
        'Students': 'ਵਿਦਿਆਰਥੀ',
        'Teacher': 'ਅਧਿਆਪਕ',
        'Class': 'ਕਲਾਸ',
        'School': 'ਸਕੂਲ',
        'Attendance': 'ਹਾਜ਼ਰੀ'
      };
      
      Object.entries(punjabiReplacements).forEach(([english, punjabi]) => {
        translatedText = translatedText.replace(new RegExp(english, 'gi'), punjabi);
      });
    }
    
    // Cache the result
    translationCache.set(cacheKey, translatedText);
    
    return translatedText;
  } catch (error) {
    console.warn(`Translation failed for "${text}" to ${targetLang}:`, error);
    return text;
  }
};

/**
 * Translate an array of strings
 * @param {Array<string>} texts - Array of texts to translate
 * @param {string} targetLang - Target language code
 * @returns {Promise<Array<string>>} - Array of translated texts
 */
export const autoTranslateMultiple = async (texts, targetLang = 'en') => {
  if (targetLang === 'en') {
    return texts;
  }

  try {
    const translations = await Promise.all(
      texts.map(text => autoTranslate(text, targetLang))
    );
    return translations;
  } catch (error) {
    console.warn('Batch translation failed:', error);
    return texts; // Return original texts if translation fails
  }
};

/**
 * Translate object properties recursively
 * @param {Object} obj - Object with text properties to translate
 * @param {Array<string>} fieldsToTranslate - Array of field names to translate
 * @param {string} targetLang - Target language code
 * @returns {Promise<Object>} - Object with translated fields
 */
export const autoTranslateObject = async (obj, fieldsToTranslate, targetLang = 'en') => {
  if (targetLang === 'en' || !obj) {
    return obj;
  }

  try {
    const translatedObj = { ...obj };
    
    for (const field of fieldsToTranslate) {
      if (obj[field] && typeof obj[field] === 'string') {
        translatedObj[field] = await autoTranslate(obj[field], targetLang);
      }
    }
    
    return translatedObj;
  } catch (error) {
    console.warn('Object translation failed:', error);
    return obj;
  }
};

/**
 * Clear translation cache (useful for memory management)
 */
export const clearTranslationCache = () => {
  translationCache.clear();
};

/**
 * Get cache size for debugging
 */
export const getTranslationCacheSize = () => {
  return translationCache.size;
};
