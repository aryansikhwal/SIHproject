import React from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { 
  LayoutDashboard, 
  Users, 
  ClipboardList, 
  BarChart3, 
  TrendingUp, 
  Settings 
} from 'lucide-react';
import { useLanguage } from '../contexts/LanguageContext';

const Sidebar = ({ isOpen }) => {
  const { t } = useLanguage();
  const navigate = useNavigate();
  const location = useLocation();
  const currentPath = location.pathname.substring(1) || 'dashboard';
  
  const menuItems = [
    { id: 'dashboard', nameKey: 'dashboard', icon: LayoutDashboard },
    { id: 'attendance', nameKey: 'attendance', icon: ClipboardList },
    { id: 'students', nameKey: 'students', icon: Users },
    { id: 'reports', nameKey: 'reports', icon: BarChart3 },
    { id: 'trends', nameKey: 'trends', icon: TrendingUp },
    { id: 'settings', nameKey: 'settings', icon: Settings },
  ];

  return (
    <div className={`fixed left-0 top-16 h-full bg-white shadow-lg transition-all duration-300 z-40 ${
      isOpen ? 'w-64' : 'w-16'
    }`}>
      <div className="p-4">
        <nav className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                key={item.id}
                onClick={() => navigate(`/${item.id}`)}
                className={`w-full flex items-center px-3 py-3 rounded-2xl transition-all duration-200 ${
                  currentPath === item.id
                    ? 'bg-primary text-white shadow-lg'
                    : 'text-neutral-dark hover:bg-primary-light hover:text-white'
                }`}
              >
                <Icon className="h-5 w-5 flex-shrink-0" />
                {isOpen && (
                  <span className="ml-3 font-medium">{t(item.nameKey)}</span>
                )}
              </button>
            );
          })}
        </nav>
      </div>
    </div>
  );
};

export default Sidebar;
