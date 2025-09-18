import React from 'react';

function Insights({ statistics }) {
  return (
    <div>
      <h3>Attendance Insights</h3>
      <ul>
        <li>Total Students: {statistics.total_students}</li>
        <li>Present Today: {statistics.present_today}</li>
        <li>Attendance Rate: {statistics.attendance_rate}%</li>
      </ul>
    </div>
  );
}

export default Insights;
