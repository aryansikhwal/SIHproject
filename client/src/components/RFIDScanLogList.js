import React, { useEffect, useState } from 'react';
import { rfidScanAPI } from '../services/api';

const RFIDScanLogList = () => {
  const [scans, setScans] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    rfidScanAPI.getRecentScans(10)
      .then(res => {
        setScans(res.data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
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
            <th className="py-2 px-4">Tag</th>
            <th className="py-2 px-4">Student Name</th>
          </tr>
        </thead>
        <tbody>
          {scans.map(scan => (
            <tr key={scan.id}>
              <td className="py-2 px-4">{scan.timestamp}</td>
              <td className="py-2 px-4">{scan.tag}</td>
              <td className="py-2 px-4">{scan.student_name}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default RFIDScanLogList;