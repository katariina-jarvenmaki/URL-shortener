# app/settings.py

import os

# Example configuration
database_url = os.getenv("DATABASE_URL", "sqlite:///default.db")
debug = os.getenv("DEBUG", "True") == "True"