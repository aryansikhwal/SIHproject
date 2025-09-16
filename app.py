from flask import Flask, render_template, request, send_file, jsonify, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
import pandas as pd
from datetime import datetime
from model import generate_forecast

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'csv'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create required directories
for directory in ['uploads', 'static']:
    if not os.path.exists(directory):
        os.makedirs(directory)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def validate_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        required_columns = ['ds', 'y']
        
        # Check if required columns exist
        if not all(col in df.columns for col in required_columns):
            return False, "CSV must contain 'ds' and 'y' columns"
        
        # Validate date format
        try:
            pd.to_datetime(df['ds'])
        except:
            return False, "Date column 'ds' must be in YYYY-MM-DD format"
        
        # Validate attendance numbers
        if not pd.to_numeric(df['y'], errors='coerce').notnull().all():
            return False, "Attendance column 'y' must contain valid numbers"
            
        return True, "Valid CSV file"
    except Exception as e:
        return False, f"Error validating CSV: {str(e)}"

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('home'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('home'))
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Validate the uploaded CSV
        is_valid, message = validate_csv(filepath)
        if not is_valid:
            os.remove(filepath)  # Remove invalid file
            flash(message, 'error')
            return redirect(url_for('home'))
            
        return redirect(url_for('forecast', filename=filename))
    else:
        flash('Invalid file type. Please upload a CSV file.', 'error')
        return redirect(url_for('home'))

@app.route('/forecast/<filename>')
def forecast(filename):
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        if not os.path.exists(filepath):
            flash('File not found', 'error')
            return redirect(url_for('home'))

        # Generate forecast
        forecast, fig1, fig2 = generate_forecast(filepath)
        
        if forecast is None:
            raise Exception("Model forecasting failed.")

        # Save visualizations
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        plot_path = f'static/forecast_plot_{timestamp}.png'
        trends_path = f'static/trends_plot_{timestamp}.png'
        csv_path = f'static/forecast_{timestamp}.csv'
        
        fig1.savefig(plot_path)
        if fig2:
            fig2.savefig(trends_path)
        
        # Save forecast data
        forecast_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast_df.to_csv(csv_path, index=False)
        
        # Calculate summary statistics
        avg_attendance = forecast_df['yhat'].mean()
        max_attendance = forecast_df['yhat'].max()
        min_attendance = forecast_df['yhat'].min()
        
        return render_template('result.html',
                             status='success',
                             plot_path=plot_path,
                             trends_path=trends_path if fig2 else None,
                             csv_path=csv_path,
                             stats={
                                 'average': f"{avg_attendance:.1f}",
                                 'maximum': f"{max_attendance:.1f}",
                                 'minimum': f"{min_attendance:.1f}"
                             })
    
    except Exception as e:
        flash(f"Error generating forecast: {str(e)}", 'error')
        return render_template('result.html', status='error', message=str(e))

@app.route('/download/<path:filename>')
def download_file(filename):
    try:
        return send_file(f'static/{filename}', as_attachment=True)
    except Exception as e:
        flash('Error downloading file', 'error')
        return redirect(url_for('home'))

# API Endpoints
@app.route('/api/forecast', methods=['POST'])
def api_forecast():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
            
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Validate CSV
            is_valid, message = validate_csv(filepath)
            if not is_valid:
                os.remove(filepath)
                return jsonify({'error': message}), 400
            
            # Generate forecast
            forecast, _, _ = generate_forecast(filepath)
            
            if forecast is None:
                return jsonify({'error': 'Forecast generation failed'}), 500
            
            # Prepare response
            forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_dict('records')
            
            return jsonify({
                'status': 'success',
                'forecast': forecast_data
            })
            
        return jsonify({'error': 'Invalid file type'}), 400
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)