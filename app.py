from flask import Flask, render_template, request, send_file
import os
# Import the function from your model.py file
from model import generate_forecast

app = Flask(__name__)

# The main page where users can trigger the forecast
@app.route('/')
def home():
    return render_template('index.html')

# The endpoint that runs the model and returns the result
@app.route('/forecast', methods=['POST'])
def run_forecast():
    try:
        data_path = 'atdata.csv'

        # Call the function from your model.py
        forecast, fig1, fig2 = generate_forecast(data_path)

        if forecast is None:
            raise Exception("Model forecasting failed.")

        # Ensure the static directory exists
        if not os.path.exists('static'):
            os.makedirs('static')

        # Save the forecast plot
        fig1.savefig('static/forecast_plot.png')
        
        # Save the forecast CSV
        forecast_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast_df.to_csv('static/attendance_forecast.csv', index=False)
        
        # Render the result page with success message
        return render_template('result.html', status='success')
    
    except Exception as e:
        # Render the result page with an error message
        return render_template('result.html', status='error', message=str(e))

# An endpoint to allow users to download the forecast CSV
@app.route('/download')
def download_file():
    path = 'static/attendance_forecast.csv'
    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)