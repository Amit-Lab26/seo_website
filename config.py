import os

class Config:
    """Application configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DATABASE_PATH = os.path.join(os.path.dirname(__file__), 'seoversion.db')
    
    # Email configuration (update with your SMTP settings)
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = 'contact@seoversion.com'
    
    # Admin email for notifications
    ADMIN_EMAIL = 'admin@seoversion.com'
    
    # Site configuration
    SITE_NAME = 'SEOversion'
    SITE_URL = 'https://seoversion.com'
    COMPANY_PHONE = '(555) 123-4567'
    COMPANY_EMAIL = 'contact@seoversion.com'
    COMPANY_ADDRESS = '123 Digital Avenue, Suite 500, San Francisco, CA 94102'
