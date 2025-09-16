import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

def generate_forecast(filename):
    """
    Args:
        data_file_path (str): The path to the CSV file containing the data.
    """
    try:
        # --- Step 1: Data Loading and Inspection ---
        print("--- Step 1: Loading and Inspecting Data ---\n")
        df = pd.read_csv('filename', sep=',')
        print(f"Data loaded successfully. Columns detected: {df.columns.tolist()}")
        print("Here's a preview of the raw data:")
        print(df.head())
        print("\n" + "-"*40 + "\n")

        # --- Step 2: Preprocessing Data ---
        print("--- Step 2: Preprocessing Data ---\n")
        df['ds'] = pd.to_datetime(df['ds'])
        print("'ds' column converted to datetime format.")
        print(df.info())
        print("\n" + "-"*40 + "\n")

        # --- Step 3: Initializing and Training the Prophet Model ---
        print("--- Step 3: Initializing and Training the Prophet Model ---\n")
        model = Prophet(
            daily_seasonality=False,
            weekly_seasonality=False
        )
        print("Fitting the model to your data...")
        model.fit(df)
        print("Model training complete.")
        print("\n" + "-"*40 + "\n")

        # --- Step 4: Generating Forecast ---
        print("--- Step 4: Generating Forecast ---\n")
        future = model.make_future_dataframe(periods=30)
        forecast = model.predict(future)
        print("30-day forecast generated successfully.")

        # Save the forecast results to a CSV file for internal use
        forecast_df = forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]
        forecast_df.to_csv('attendance_forecast.csv', index=False)
        print("Forecast results saved to 'attendance_forecast.csv'")
        print("Here are the last 5 entries of the forecast:")
        print(forecast_df.tail())
        print("\n" + "-"*40 + "\n")

        # --- Step 5: Generating Visualizations ---
        print("--- Step 5: Generating Visualizations ---\n")
        fig1 = model.plot(forecast, figsize=(10, 6))
        plt.title("30-Day Attendance Forecast", fontsize=18, fontweight='bold')
        plt.xlabel("Date", fontsize=14)
        plt.ylabel("Attendance Count", fontsize=14)
        plt.legend(['Actual Attendance', 'Predicted Forecast', 'Uncertainty Interval'])
        plt.grid(True)
        plt.tight_layout()

        print("\n--- All tasks completed. You can now use the returned data and plots. ---")

        return forecast_df, fig1, fig2

    except Exception as e:
        print(f"An error occurred in the forecasting process: {e}")
        return None, None, None

if __name__ == '__main__':
    # This block allows you to run the function directly for testing
    # and will save the plots to files.
    forecast_df, fig1, fig2 = generate_forecast('atdata.csv')
    if fig1 and fig2:
        fig1.savefig('forecast_plot.png')
        fig2.savefig('forecast_components.png')
        print("Plots saved to 'forecast_plot.png' and 'forecast_components.png'.")