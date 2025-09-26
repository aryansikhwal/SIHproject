import React, { useState, useEffect } from 'react';
import { Wifi, WifiOff, RefreshCcw, AlertCircle } from 'lucide-react';
import offlineAPI from '../services/offlineAPI';

const OfflineStatusIndicator = () => {
  const [isOnline, setIsOnline] = useState(navigator.onLine);
  const [syncStatus, setSyncStatus] = useState({ pendingSync: 0, lastSync: 'Never' });
  const [issyncing, setIssyncing] = useState(false);

  useEffect(() => {
    const handleOnline = () => setIsOnline(true);
    const handleOffline = () => setIsOnline(false);

    window.addEventListener('online', handleOnline);
    window.addEventListener('offline', handleOffline);

    // Update sync status periodically
    const updateSyncStatus = async () => {
      try {
        const status = await offlineAPI.getSyncStatus();
        setSyncStatus(status);
      } catch (error) {
        console.error('Error getting sync status:', error);
      }
    };

    updateSyncStatus();
    const interval = setInterval(updateSyncStatus, 30000); // Update every 30 seconds

    return () => {
      window.removeEventListener('online', handleOnline);
      window.removeEventListener('offline', handleOffline);
      clearInterval(interval);
    };
  }, []);

  const handleForceSync = async () => {
    if (!isOnline) return;
    
    setIssyncing(true);
    try {
      await offlineAPI.forceSync();
      const status = await offlineAPI.getSyncStatus();
      setSyncStatus(status);
    } catch (error) {
      console.error('Error syncing:', error);
    } finally {
      setIssyncing(false);
    }
  };

  if (isOnline && syncStatus.pendingSync === 0) {
    return (
      <div className="flex items-center space-x-2 px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm">
        <Wifi className="w-4 h-4" />
        <span>Online</span>
      </div>
    );
  }

  if (!isOnline) {
    return (
      <div className="flex items-center space-x-2 px-3 py-1 bg-yellow-100 text-yellow-800 rounded-full text-sm">
        <WifiOff className="w-4 h-4" />
        <span>Offline Mode</span>
      </div>
    );
  }

  if (syncStatus.pendingSync > 0) {
    return (
      <div className="flex items-center space-x-2">
        <div className="flex items-center space-x-2 px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm">
          <AlertCircle className="w-4 h-4" />
          <span>{syncStatus.pendingSync} pending</span>
        </div>
        <button
          onClick={handleForceSync}
          disabled={issyncing}
          className="flex items-center space-x-1 px-2 py-1 bg-blue-100 text-blue-800 rounded-full text-sm hover:bg-blue-200 transition-colors disabled:opacity-50"
        >
          <RefreshCcw className={`w-4 h-4 ${issyncing ? 'animate-spin' : ''}`} />
          <span>{issyncing ? 'Syncing...' : 'Sync'}</span>
        </button>
      </div>
    );
  }

  return null;
};

export default OfflineStatusIndicator;
