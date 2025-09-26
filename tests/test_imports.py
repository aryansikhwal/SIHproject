try:
    print("Attempting to import all required packages...")
    from flask import Flask
    from flask_sqlalchemy import SQLAlchemy
    from flask_login import LoginManager
    from flask_cors import CORS
    import pandas as pd
    import sqlite3
    from werkzeug.security import generate_password_hash
    from datetime import datetime, date
    print("All imports successful!")
except ImportError as e:
    print(f"Import error: {e}")
