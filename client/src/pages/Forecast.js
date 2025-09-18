import React, { useState } from 'react';

function Forecast() {
  const [forecast, setForecast] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  const fetchForecast = async () => {
    setLoading(true);
    setMessage('');
    try {
      const res = await fetch('/api/forecast');
      const data = await res.json();
      setForecast(data);
    } catch (err) {
      setMessage('Error fetching forecast');
    }
    setLoading(false);
  };

  const triggerForecast = async () => {
    setLoading(true);
    setMessage('');
    try {
      await fetch('/api/trigger_forecast', { method: 'POST' });
      setMessage('Forecast updated!');
      fetchForecast();
    } catch (err) {
      setMessage('Error updating forecast');
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Attendance Forecast & Mid Day Meal Ration</h2>
      <button onClick={triggerForecast} disabled={loading}>
        Predict Forecast
      </button>
      {message && <p>{message}</p>}
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Predicted Present</th>
            <th>Recommended Ration</th>
          </tr>
        </thead>
        <tbody>
          {forecast.map(f => (
            <tr key={f.date}>
              <td>{f.date}</td>
              <td>{f.predicted_present}</td>
              <td>{Math.ceil(f.predicted_present * 0.95)} meals</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Forecast;
