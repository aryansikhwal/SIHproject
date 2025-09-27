import React, { useState } from 'react';
import { School, User, Wifi, Bell, Lock, LogOut, Save, Edit } from 'lucide-react';

const Settings = () => {
  const [schoolInfo, setSchoolInfo] = useState({
    name: 'Government Primary School Rajasthan',
    code: 'GPS001',
    address: 'Village Khairpur, District Alwar, Rajasthan',
    contact: '+91 9876543210',
    email: 'gps.khairpur@education.gov.in',
    principal: 'Mrs. Sunita Sharma'
  });

  const [notifications, setNotifications] = useState({
    dailyReports: true,
    lowAttendance: true,
    weeklyDigest: false,
    systemUpdates: true
  });

  const [syncSettings, setSyncSettings] = useState({
    autoSync: true,
    syncInterval: '15',
    lastSync: '2025-09-16 10:30 AM',
    serverStatus: 'connected'
  });

  const [isEditing, setIsEditing] = useState(false);

  const handleSchoolInfoChange = (field, value) => {
    setSchoolInfo(prev => ({ ...prev, [field]: value }));
  };

  const handleNotificationChange = (field) => {
    setNotifications(prev => ({ ...prev, [field]: !prev[field] }));
  };

  const handleSyncSettingChange = (field, value) => {
    setSyncSettings(prev => ({ ...prev, [field]: value }));
  };

  const saveSettings = () => {
    // Mock save functionality
    alert('Settings saved successfully!');
    setIsEditing(false);
  };

  const handleLogout = () => {
    if (window.confirm('Are you sure you want to logout?')) {
      alert('Logging out...');
    }
  };

  const ToggleSwitch = ({ enabled, onChange, label, description }) => (
    <div className="flex items-center justify-between p-4 bg-gray-50 rounded-xl">
      <div>
        <h4 className="font-medium text-neutral-dark">{label}</h4>
        {description && <p className="text-sm text-gray-600">{description}</p>}
      </div>
      <button
        onClick={onChange}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
          enabled ? 'bg-primary' : 'bg-gray-300'
        }`}
      >
        <span
          className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
            enabled ? 'translate-x-6' : 'translate-x-1'
          }`}
        />
      </button>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold text-neutral-dark mb-2">Settings</h1>
            <p className="text-gray-600">Configure system preferences and school information</p>
          </div>
          <div className="mt-4 lg:mt-0 flex gap-3">
            <button
              onClick={() => setIsEditing(!isEditing)}
              className="px-6 py-2 bg-blue-500 text-white rounded-2xl hover:bg-blue-600 transition-colors flex items-center gap-2"
            >
              <Edit className="h-4 w-4" />
              {isEditing ? 'Cancel' : 'Edit'}
            </button>
            {isEditing && (
              <button
                onClick={saveSettings}
                className="px-6 py-2 bg-blue-600 text-white rounded-2xl hover:bg-blue-700 transition-colors flex items-center gap-2"
              >
                <Save className="h-4 w-4" />
                Save Changes
              </button>
            )}
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* School Information */}
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center mb-6">
            <School className="h-6 w-6 text-primary mr-3" />
            <h2 className="text-xl font-semibold text-neutral-dark">School Information</h2>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-neutral-dark mb-2">School Name</label>
              <input
                type="text"
                value={schoolInfo.name}
                onChange={(e) => handleSchoolInfoChange('name', e.target.value)}
                disabled={!isEditing}
                className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-neutral-dark mb-2">School Code</label>
              <input
                type="text"
                value={schoolInfo.code}
                onChange={(e) => handleSchoolInfoChange('code', e.target.value)}
                disabled={!isEditing}
                className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-neutral-dark mb-2">Address</label>
              <textarea
                value={schoolInfo.address}
                onChange={(e) => handleSchoolInfoChange('address', e.target.value)}
                disabled={!isEditing}
                rows="3"
                className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-neutral-dark mb-2">Contact Number</label>
              <input
                type="tel"
                value={schoolInfo.contact}
                onChange={(e) => handleSchoolInfoChange('contact', e.target.value)}
                disabled={!isEditing}
                className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-neutral-dark mb-2">Email</label>
              <input
                type="email"
                value={schoolInfo.email}
                onChange={(e) => handleSchoolInfoChange('email', e.target.value)}
                disabled={!isEditing}
                className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50"
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-neutral-dark mb-2">Principal Name</label>
              <input
                type="text"
                value={schoolInfo.principal}
                onChange={(e) => handleSchoolInfoChange('principal', e.target.value)}
                disabled={!isEditing}
                className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent disabled:bg-gray-50"
              />
            </div>
          </div>
        </div>

        {/* Teacher & Security Settings */}
        <div className="space-y-6">
          {/* Teacher Profile */}
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <div className="flex items-center mb-6">
              <User className="h-6 w-6 text-primary mr-3" />
              <h2 className="text-xl font-semibold text-neutral-dark">Teacher Profile</h2>
            </div>
            
            <div className="flex items-center space-x-4 mb-4">
              <div className="w-16 h-16 bg-primary rounded-full flex items-center justify-center">
                <User className="h-8 w-8 text-white" />
              </div>
              <div>
                <h3 className="font-semibold text-neutral-dark">Mr. Rajesh Kumar</h3>
                <p className="text-gray-600">Primary Teacher</p>
                <p className="text-sm text-gray-500">ID: TCH001</p>
              </div>
            </div>
            
            <div className="space-y-3">
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-xl">
                <span className="text-neutral-dark">Change Password</span>
                <button className="px-4 py-2 bg-blue-600 text-white rounded-2xl hover:bg-blue-700 transition-colors text-sm">
                  Update
                </button>
              </div>
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-xl">
                <span className="text-neutral-dark">Two-Factor Authentication</span>
                <span className="px-3 py-1 bg-green-100 text-green-700 text-sm rounded-full">
                  Enabled
                </span>
              </div>
            </div>
          </div>

          {/* Security Settings */}
          <div className="bg-white rounded-2xl p-6 shadow-lg">
            <div className="flex items-center mb-6">
              <Lock className="h-6 w-6 text-primary mr-3" />
              <h2 className="text-xl font-semibold text-neutral-dark">Security</h2>
            </div>
            
            <div className="space-y-3">
              <div className="p-4 bg-green-50 rounded-xl border-l-4 border-green-400">
                <div className="flex items-center justify-between mb-2">
                  <h4 className="font-medium text-green-800">System Security</h4>
                  <span className="text-xs text-green-600 bg-green-100 px-2 py-1 rounded-full">
                    Secure
                  </span>
                </div>
                <p className="text-sm text-green-700">
                  All connections encrypted. Last security check: Today
                </p>
              </div>
              
              <div className="flex justify-between items-center p-3 bg-gray-50 rounded-xl">
                <span className="text-neutral-dark">Session Timeout</span>
                <select className="px-3 py-1 border border-gray-300 rounded-lg text-sm">
                  <option value="30">30 minutes</option>
                  <option value="60">1 hour</option>
                  <option value="120">2 hours</option>
                </select>
              </div>
              
              <button
                onClick={handleLogout}
                className="w-full flex items-center justify-center p-3 bg-red-50 text-red-600 rounded-xl hover:bg-red-500 hover:text-white transition-colors"
              >
                <LogOut className="h-4 w-4 mr-2" />
                Logout from all devices
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Notification Settings */}
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center mb-6">
            <Bell className="h-6 w-6 text-primary mr-3" />
            <h2 className="text-xl font-semibold text-neutral-dark">Notifications</h2>
          </div>
          
          <div className="space-y-4">
            <ToggleSwitch
              enabled={notifications.dailyReports}
              onChange={() => handleNotificationChange('dailyReports')}
              label="Daily Attendance Reports"
              description="Receive daily attendance summaries"
            />
            
            <ToggleSwitch
              enabled={notifications.lowAttendance}
              onChange={() => handleNotificationChange('lowAttendance')}
              label="Low Attendance Alerts"
              description="Alert when attendance drops below threshold"
            />
            
            <ToggleSwitch
              enabled={notifications.weeklyDigest}
              onChange={() => handleNotificationChange('weeklyDigest')}
              label="Weekly Digest"
              description="Weekly performance and trend summaries"
            />
            
            <ToggleSwitch
              enabled={notifications.systemUpdates}
              onChange={() => handleNotificationChange('systemUpdates')}
              label="System Updates"
              description="Notifications about system maintenance and updates"
            />
          </div>
        </div>

        {/* Sync Settings */}
        <div className="bg-white rounded-2xl p-6 shadow-lg">
          <div className="flex items-center mb-6">
            <Wifi className="h-6 w-6 text-primary mr-3" />
            <h2 className="text-xl font-semibold text-neutral-dark">Data Sync</h2>
          </div>
          
          <div className="space-y-4">
            <div className="flex items-center justify-between p-4 bg-green-50 rounded-xl">
              <div>
                <h4 className="font-medium text-green-800">Server Status</h4>
                <p className="text-sm text-green-700">Connected and synchronized</p>
              </div>
              <div className="w-3 h-3 bg-green-500 rounded-full animate-pulse"></div>
            </div>
            
            <ToggleSwitch
              enabled={syncSettings.autoSync}
              onChange={() => handleSyncSettingChange('autoSync', !syncSettings.autoSync)}
              label="Auto Sync"
              description="Automatically sync data with central server"
            />
            
            <div>
              <label className="block text-sm font-medium text-neutral-dark mb-2">Sync Interval</label>
              <select
                value={syncSettings.syncInterval}
                onChange={(e) => handleSyncSettingChange('syncInterval', e.target.value)}
                className="w-full p-3 border border-gray-300 rounded-2xl focus:ring-2 focus:ring-primary focus:border-transparent"
              >
                <option value="5">Every 5 minutes</option>
                <option value="15">Every 15 minutes</option>
                <option value="30">Every 30 minutes</option>
                <option value="60">Every hour</option>
              </select>
            </div>
            
            <div className="p-3 bg-gray-50 rounded-xl">
              <div className="flex justify-between items-center mb-2">
                <span className="text-sm text-gray-600">Last Sync:</span>
                <span className="text-sm font-medium text-neutral-dark">{syncSettings.lastSync}</span>
              </div>
              <button className="w-full px-4 py-2 bg-blue-600 text-white rounded-2xl hover:bg-blue-700 transition-colors text-sm">
                Sync Now
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* System Information */}
      <div className="bg-white rounded-2xl p-6 shadow-lg">
        <h2 className="text-xl font-semibold text-neutral-dark mb-4">System Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
          <div className="p-4 bg-gray-50 rounded-xl text-center">
            <p className="text-sm text-gray-600">Version</p>
            <p className="font-semibold text-neutral-dark">v2.1.0</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-xl text-center">
            <p className="text-sm text-gray-600">Last Update</p>
            <p className="font-semibold text-neutral-dark">Sept 15, 2025</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-xl text-center">
            <p className="text-sm text-gray-600">Database Size</p>
            <p className="font-semibold text-neutral-dark">12.3 MB</p>
          </div>
          <div className="p-4 bg-gray-50 rounded-xl text-center">
            <p className="text-sm text-gray-600">Uptime</p>
            <p className="font-semibold text-neutral-dark">23 days</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Settings;
