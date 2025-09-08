from flask import current_app
import re

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def clean_text(text):
    """Clean and normalize text for better analysis"""
   
    text = re.sub(r'\s+', ' ', text)
    return text.strip()