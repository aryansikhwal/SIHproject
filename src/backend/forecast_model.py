"""
Fresh ML Forecasting Model for AttenSync
Clean implementation with proper database integration
"""
import pandas as pd
import numpy as np
from prophet import Prophet
import sqlite3
import os
from datetime import datetime, date, timedelta
import warnings
import logging

# Suppress Prophet warnings
warnings.filterwarnings('ignore')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AttendanceForecastModel:
    """
    ML model for forecasting attendance patterns using Prophet
    Integrates directly with AttenSync database
    """
    
    def __init__(self, db_path=None):
        """Initialize the forecasting model"""
        if db_path is None:
            # Use absolute path relative to this file
            project_root = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(project_root, 'instance', 'attensync.db')
        
        self.db_path = db_path
        self.model = None
        self.is_trained = False
        self.last_training_date = None
        self.forecast_cache = {}
        
        logger.info("🤖 Attendance Forecast Model initialized")
    
    def _get_db_connection(self):
        """Get database connection"""
        try:
            if not os.path.exists(self.db_path):
                raise FileNotFoundError(f"Database file not found: {self.db_path}")
            
            conn = sqlite3.connect(self.db_path)
            return conn
        except Exception as e:
            logger.error(f"❌ Database connection failed: {e}")
            raise
    
    def load_attendance_data(self, days_back=90, class_id=None):
        """
        Load attendance data from database for training
        
        Args:
            days_back (int): Number of days to look back
            class_id (int, optional): Filter by specific class
        
        Returns:
            pandas.DataFrame: Attendance data formatted for Prophet
        """
        try:
            conn = self._get_db_connection()
            
            # Calculate date range
            end_date = date.today()
            start_date = end_date - timedelta(days=days_back)
            
            # Build SQL query
            base_query = """
                SELECT 
                    a.attendance_date as date,
                    COUNT(CASE WHEN a.status = 'present' THEN 1 END) as present_count,
                    COUNT(a.id) as total_marked,
                    s.class_id,
                    c.name as class_name
                FROM attendance a
                JOIN students s ON a.student_id = s.id
                JOIN classes c ON s.class_id = c.id
                WHERE a.attendance_date >= ? AND a.attendance_date <= ?
            """
            
            params = [start_date.isoformat(), end_date.isoformat()]
            
            if class_id:
                base_query += " AND s.class_id = ?"
                params.append(class_id)
            
            base_query += " GROUP BY a.attendance_date, s.class_id ORDER BY a.attendance_date"
            
            df = pd.read_sql_query(base_query, conn, params=params)
            conn.close()
            
            if df.empty:
                logger.warning("⚠️ No attendance data found for the specified period")
                return pd.DataFrame()
            
            # Calculate attendance percentage
            df['attendance_rate'] = (df['present_count'] / df['total_marked'] * 100).fillna(0)
            
            # Aggregate by date if multiple classes
            if not class_id:
                df_agg = df.groupby('date').agg({
                    'present_count': 'sum',
                    'total_marked': 'sum'
                }).reset_index()
                df_agg['attendance_rate'] = (df_agg['present_count'] / df_agg['total_marked'] * 100).fillna(0)
                df = df_agg
            
            # Format for Prophet (requires 'ds' and 'y' columns)
            prophet_df = pd.DataFrame({
                'ds': pd.to_datetime(df['date']),
                'y': df['attendance_rate']
            })
            
            logger.info(f"✅ Loaded {len(prophet_df)} days of attendance data")
            logger.info(f"📊 Average attendance rate: {prophet_df['y'].mean():.1f}%")
            
            return prophet_df
            
        except Exception as e:
            logger.error(f"❌ Error loading attendance data: {e}")
            return pd.DataFrame()
    
    def train_model(self, class_id=None, days_back=90):
        """
        Train the Prophet model on attendance data
        
        Args:
            class_id (int, optional): Train for specific class
            days_back (int): Days of historical data to use
        
        Returns:
            bool: Success status
        """
        try:
            logger.info("🎯 Training attendance forecast model...")
            
            # Load training data
            training_data = self.load_attendance_data(days_back=days_back, class_id=class_id)
            
            if training_data.empty:
                logger.error("❌ No training data available")
                return False
            
            if len(training_data) < 14:  # Need at least 2 weeks of data
                logger.warning(f"⚠️ Limited training data ({len(training_data)} days). Need at least 14 days.")
                return False
            
            # Initialize and configure Prophet model
            self.model = Prophet(
                daily_seasonality=True,
                weekly_seasonality=True,
                yearly_seasonality=False,  # Not enough data for yearly patterns
                seasonality_mode='additive',
                interval_width=0.80,  # 80% confidence intervals
                changepoint_prior_scale=0.05  # Less aggressive changepoints
            )
            
            # Add custom seasonalities
            self.model.add_seasonality(
                name='school_term',
                period=180,  # Approximate school term length
                fourier_order=3
            )
            
            # Fit the model
            self.model.fit(training_data)
            
            self.is_trained = True
            self.last_training_date = datetime.now()
            
            logger.info("✅ Model training completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"❌ Model training failed: {e}")
            return False
    
    def generate_forecast(self, periods=30, class_id=None):
        """
        Generate attendance forecast
        
        Args:
            periods (int): Number of days to forecast
            class_id (int, optional): Class to forecast for
        
        Returns:
            dict: Forecast results with dates, values, and confidence intervals
        """
        try:
            if not self.is_trained:
                logger.info("🔄 Model not trained. Training now...")
                if not self.train_model(class_id=class_id):
                    raise Exception("Model training failed")
            
            logger.info(f"📈 Generating {periods}-day forecast...")
            
            # Create future dataframe
            future = self.model.make_future_dataframe(periods=periods)
            
            # Generate forecast
            forecast = self.model.predict(future)
            
            # Extract forecast data
            forecast_data = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail(periods)
            
            # Format results
            results = {
                'dates': forecast_data['ds'].dt.strftime('%Y-%m-%d').tolist(),
                'predicted_attendance': np.maximum(0, np.minimum(100, forecast_data['yhat'])).round(1).tolist(),
                'lower_bound': np.maximum(0, np.minimum(100, forecast_data['yhat_lower'])).round(1).tolist(),
                'upper_bound': np.maximum(0, np.minimum(100, forecast_data['yhat_upper'])).round(1).tolist(),
                'confidence_level': 80,
                'model_info': {
                    'training_date': self.last_training_date.isoformat() if self.last_training_date else None,
                    'periods_forecasted': periods,
                    'class_id': class_id
                }
            }
            
            # Calculate summary statistics
            avg_forecast = np.mean(results['predicted_attendance'])
            results['summary'] = {
                'average_predicted_attendance': round(avg_forecast, 1),
                'trend': 'increasing' if results['predicted_attendance'][-1] > results['predicted_attendance'][0] else 'decreasing',
                'volatility': round(np.std(results['predicted_attendance']), 1)
            }
            
            logger.info(f"✅ Forecast generated - Average: {avg_forecast:.1f}%")
            return results
            
        except Exception as e:
            logger.error(f"❌ Forecast generation failed: {e}")
            return None
    
    def get_attendance_insights(self, class_id=None):
        """
        Generate insights about attendance patterns
        
        Returns:
            dict: Attendance insights and recommendations
        """
        try:
            logger.info("🔍 Generating attendance insights...")
            
            # Load recent data for analysis
            recent_data = self.load_attendance_data(days_back=30, class_id=class_id)
            
            if recent_data.empty:
                return {'error': 'No data available for insights'}
            
            # Calculate statistics
            current_avg = recent_data['y'].mean()
            recent_trend = recent_data['y'].tail(7).mean() - recent_data['y'].head(7).mean()
            volatility = recent_data['y'].std()
            min_attendance = recent_data['y'].min()
            max_attendance = recent_data['y'].max()
            
            # Identify patterns
            insights = {
                'current_statistics': {
                    'average_attendance': round(current_avg, 1),
                    'trend_direction': 'improving' if recent_trend > 0 else 'declining' if recent_trend < 0 else 'stable',
                    'trend_magnitude': round(abs(recent_trend), 1),
                    'volatility': round(volatility, 1),
                    'range': {
                        'min': round(min_attendance, 1),
                        'max': round(max_attendance, 1)
                    }
                },
                'insights': [],
                'recommendations': []
            }
            
            # Generate insights based on patterns
            if current_avg >= 95:
                insights['insights'].append("Excellent attendance rate - among the top performers")
            elif current_avg >= 85:
                insights['insights'].append("Good attendance rate with room for improvement")
            elif current_avg >= 75:
                insights['insights'].append("Average attendance - requires attention")
            else:
                insights['insights'].append("Low attendance - immediate intervention needed")
            
            if recent_trend > 2:
                insights['insights'].append("Positive trend - attendance is improving")
            elif recent_trend < -2:
                insights['insights'].append("Concerning downward trend in attendance")
            
            if volatility > 10:
                insights['insights'].append("High attendance variability - inconsistent patterns")
            
            # Generate recommendations
            if current_avg < 85:
                insights['recommendations'].append("Consider implementing attendance incentives")
                insights['recommendations'].append("Review and address common absence reasons")
            
            if recent_trend < -1:
                insights['recommendations'].append("Investigate factors causing declining attendance")
                insights['recommendations'].append("Implement early intervention strategies")
            
            if volatility > 10:
                insights['recommendations'].append("Focus on creating consistent daily routines")
            
            logger.info("✅ Attendance insights generated")
            return insights
            
        except Exception as e:
            logger.error(f"❌ Insights generation failed: {e}")
            return {'error': str(e)}
    
    def get_student_count(self, class_id=None):
        """Get total number of active students for reference"""
        try:
            conn = self._get_db_connection()
            
            query = "SELECT COUNT(*) as count FROM students WHERE is_active = 1"
            params = []
            
            if class_id:
                query += " AND class_id = ?"
                params.append(class_id)
            
            result = pd.read_sql_query(query, conn, params=params)
            conn.close()
            
            return result['count'].iloc[0] if not result.empty else 0
            
        except Exception as e:
            logger.error(f"❌ Error getting student count: {e}")
            return 0


# ==================== UTILITY FUNCTIONS ====================

def generate_forecast_report(class_id=None, periods=30):
    """
    Generate a complete forecast report
    
    Args:
        class_id (int, optional): Class to forecast for
        periods (int): Days to forecast
    
    Returns:
        dict: Complete forecast report
    """
    try:
        model = AttendanceForecastModel()
        
        # Generate forecast
        forecast = model.generate_forecast(periods=periods, class_id=class_id)
        if not forecast:
            return {'error': 'Failed to generate forecast'}
        
        # Get insights
        insights = model.get_attendance_insights(class_id=class_id)
        
        # Get student count for context
        student_count = model.get_student_count(class_id=class_id)
        
        # Combine results
        report = {
            'forecast': forecast,
            'insights': insights,
            'context': {
                'student_count': student_count,
                'class_id': class_id,
                'generated_at': datetime.now().isoformat()
            }
        }
        
        return report
        
    except Exception as e:
        logger.error(f"❌ Report generation failed: {e}")
        return {'error': str(e)}


# ==================== MAIN EXECUTION ====================

if __name__ == '__main__':
    """Test the forecasting model"""
    print("🤖 Testing AttenSync Forecasting Model")
    print("=" * 50)
    
    try:
        # Initialize model
        model = AttendanceForecastModel()
        
        # Test database connection
        conn = model._get_db_connection()
        print("✅ Database connection successful")
        conn.close()
        
        # Load sample data
        data = model.load_attendance_data(days_back=30)
        print(f"✅ Loaded {len(data)} days of data")
        
        if len(data) >= 14:
            # Train model
            if model.train_model():
                print("✅ Model training successful")
                
                # Generate forecast
                forecast = model.generate_forecast(periods=7)
                if forecast:
                    print("✅ Forecast generation successful")
                    print(f"📊 Average predicted attendance: {forecast['summary']['average_predicted_attendance']}%")
                
                # Generate insights
                insights = model.get_attendance_insights()
                print("✅ Insights generation successful")
            else:
                print("❌ Model training failed")
        else:
            print("⚠️ Insufficient data for training (need at least 14 days)")
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
    
    print("=" * 50)
    print("🏁 Test completed")