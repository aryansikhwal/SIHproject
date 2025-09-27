import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Menu, Settings } from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';
import LanguageSwitcher from './LanguageSwitcher';
import OfflineStatusIndicator from './OfflineStatusIndicator';

const Navbar = ({ sidebarOpen, setSidebarOpen }) => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  
  return (
    <nav className="fixed top-0 left-0 right-0 bg-white shadow-lg z-50 h-16">
      <div className="flex items-center justify-between h-full px-6">
        <div className="flex items-center">
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 rounded-lg hover:bg-blue-500 hover:text-white transition-colors"
          >
            <Menu className="h-6 w-6 text-neutral-dark" />
          </button>
          <h1 className="ml-4 text-2xl font-bold text-primary">AttenSync</h1>
        </div>
        
        <div className="flex items-center space-x-4">
          <OfflineStatusIndicator />
          <LanguageSwitcher />
          <button 
            onClick={() => navigate('/settings')}
            className="p-2 rounded-lg hover:bg-blue-500 hover:text-white transition-colors"
          >
            <Settings className="h-5 w-5 text-neutral-dark" />
          </button>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
