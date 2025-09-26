import React, { useEffect, useState } from 'react';
import { rfidScanAPI } from '../services/api';

const RFIDScanLogList = () => {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    console.log('RFIDScanLogList: Starting to fetch RFID scans...');
    
    // Direct fetch test to bypass axios
    const testUrl = 'http://localhost:5000/api/rfid/scans?limit=5';
    console.log('Testing direct fetch to:', testUrl);
    
    fetch(testUrl)
      .then(response => {
        console.log('Direct fetch response status:', response.status);
        console.log('Direct fetch response headers:', response.headers);
        return response.json();
      })
      .then(data => {
        console.log('Direct fetch data:', data);
        if (data && data.scans) {
          setScans(data.scans);
        }
        setLoading(false);
      })
      .catch(error => {
        console.error('Direct fetch error:', error);
        // Fallback to axios
        rfidScanAPI.getRecentScans(10)
          .then(res => {
            console.log('RFIDScanLogList: API Response:', res.data);
            setScans(res.data.scans || []);
            setLoading(false);
          })
          .catch(error => {
            console.error('RFIDScanLogList: Error fetching scans:', error);
            setLoading(false);
          });
      });
  }, []);

  if (loading) return <div>Loading recent RFID scans...</div>;
  if (!scans.length) return <div>No recent RFID scans found.</div>;

  return (
    <div className="bg-white rounded-2xl p-6 shadow-lg mt-6">
      <h2 className="text-xl font-semibold mb-4">Recent RFID Scans</h2>
      <table className="min-w-full text-left">
        <thead>
          <tr>
            <th className="py-2 px-4">Time</th>
            <th className="py-2 px-4">RFID Tag</th>
            <th className="py-2 px-4">Student Name</th>
            <th className="py-2 px-4">Status</th>
          </tr>
        </thead>
        <tbody>
          {scans.map(scan => (
            <tr key={scan.id}>
              <td className="py-2 px-4">{new Date(scan.scan_time).toLocaleString()}</td>
              <td className="py-2 px-4">{scan.rfid_tag}</td>
              <td className="py-2 px-4">{scan.student_name || 'Unknown'}</td>
              <td className="py-2 px-4">
                <span className={`px-2 py-1 rounded-full text-xs ${
                  scan.status === 'success' ? 'bg-green-100 text-green-800' :
                  scan.status === 'invalid_tag' ? 'bg-red-100 text-red-800' :
                  scan.status === 'already_marked' ? 'bg-yellow-100 text-yellow-800' :
                  'bg-gray-100 text-gray-800'
                }`}>
                  {scan.status}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RFIDScanLogList;