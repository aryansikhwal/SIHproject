import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider } from './contexts/LanguageContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import Attendance from './pages/Attendance';
import Students from './pages/Students';
import Reports from './pages/Reports';
import Trends from './pages/Trends';
import Settings from './pages/Settings';
import indexedDBService from './services/indexedDB';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  // Initialize IndexedDB and fake data on app start
  useEffect(() => {
    const initializeApp = async () => {
      try {
        await indexedDBService.initializeDB();
        await indexedDBService.initializeFakeData();
        console.log('App initialized successfully');
      } catch (error) {
        console.error('Error initializing app:', error);
      }
    };
    
    initializeApp();
  }, []);

  return (
    <Router>
      <LanguageProvider>
        <div className="min-h-screen bg-neutral-light">
          <Navbar sidebarOpen={sidebarOpen} setSidebarOpen={setSidebarOpen} />
          <div className="flex">
            <Sidebar isOpen={sidebarOpen} />
            <main className={`flex-1 transition-all duration-300 ${sidebarOpen ? 'ml-64' : 'ml-16'} mt-16 p-6`}>
              <Routes>
                <Route path="/" element={<Navigate to="/dashboard" replace />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/attendance" element={<Attendance />} />
                <Route path="/students" element={<Students />} />
                <Route path="/reports" element={<Reports />} />
                <Route path="/trends" element={<Trends />} />
                <Route path="/settings" element={<Settings />} />
              </Routes>
            </main>
          </div>
        </div>
      </LanguageProvider>
    </Router>
  );
}

export default App;
