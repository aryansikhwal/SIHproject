import React from 'react';

function ForecastButton({ onClick, loading }) {
  return (
    <button onClick={onClick} disabled={loading}>
      Predict Forecast
    </button>
  );
}

export default ForecastButton;
