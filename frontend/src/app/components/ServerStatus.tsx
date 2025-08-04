'use client';

import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export default function ServerStatus() {
  const [isOnline, setIsOnline] = useState<boolean | null>(null);
  const [isChecking, setIsChecking] = useState(true);

  useEffect(() => {
    checkServerStatus();
    const interval = setInterval(checkServerStatus, 30000); // Check every 30 seconds
    
    return () => clearInterval(interval);
  }, []);

  const checkServerStatus = async () => {
    try {
      const status = await apiService.checkServerHealth();
      setIsOnline(status);
    } catch (error) {
      setIsOnline(false);
    } finally {
      setIsChecking(false);
    }
  };

  if (isChecking) {
    return (
      <div className="flex items-center space-x-2 text-sm text-gray-500">
        <div className="animate-spin rounded-full h-3 w-3 border-b-2 border-gray-500"></div>
        <span>Checking server status...</span>
      </div>
    );
  }

  return (
    <div className="flex items-center space-x-2">
      <div
        className={`w-2 h-2 rounded-full ${
          isOnline ? 'bg-green-500' : 'bg-red-500'
        }`}
      ></div>
      <span className="text-sm text-gray-600">
        Backend Server: {isOnline ? 'Online' : 'Offline'}
      </span>
      {!isOnline && (
        <button
          onClick={checkServerStatus}
          className="text-xs text-blue-600 hover:text-blue-800 underline"
        >
          Retry
        </button>
      )}
    </div>
  );
} 