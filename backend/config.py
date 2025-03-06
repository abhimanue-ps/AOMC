import os

class Config:
    # Core settings
    SECRET_KEY = os.getenv("SECRET_KEY", "aomc-secret-key")  # Change to a more secure one later
    DEBUG = True  # Set False when we are ready for final production

    # Future settings (examples, we will add more later)
    # DATABASE_URI = "sqlite:///aomc.db"
    # ALLOWED_EXTENSIONS = {"txt", "csv"}

# For now, we are only using 'Config', but if we want different setups (like Dev/Prod), we can do:
# class DevelopmentConfig(Config):
#     DEBUG = True
#
# class ProductionConfig(Config):
#     DEBUG = False

