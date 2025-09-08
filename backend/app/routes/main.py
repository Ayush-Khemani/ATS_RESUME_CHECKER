from flask import Blueprint, request, jsonify, current_app
import os

# Import our services and utilities
from app.utils.file_utils import allowed_file, clean_text
from app.services.pdf_service import PDFService
from app.services.ai_service import AIService

main_bp = Blueprint('main', __name__)

@main_bp.route('/', methods=['GET'])
def home():
    return jsonify({"message": "ResumeMatch AI Backend is running!"})

@main_bp.route('/analyze', methods=['POST'])
def analyze_resume():
    """Main analyze endpoint - EXACT SAME LOGIC as your original"""
    try:
        # Check if request has file
        if 'resume' not in request.files:
            return jsonify({"error": "No resume file provided"}), 400
            
        file = request.files['resume']
        job_description = request.form.get('job_description', '')
        
        if file.filename == '':
            return jsonify({"error": "No file selected"}), 400
            
        if not job_description:
            return jsonify({"error": "Job description is required"}), 400
            
        if file and allowed_file(file.filename):
            # Process the file
            if file.filename.endswith('.pdf'):
                resume_text = PDFService.extract_text_from_pdf(file)
            else:
                resume_text = file.read().decode('utf-8')
            
            # Clean the text
            resume_text = clean_text(resume_text)
            job_description = clean_text(job_description)
            
            # Analyze with AI
            ai_service = AIService()
            analysis_result = ai_service.analyze_resume_job_match(resume_text, job_description)
            
            return jsonify({
                "success": True,
                "analysis": analysis_result,
                "resume_length": len(resume_text.split()),
                "job_description_length": len(job_description.split())
            })
            
        else:
            return jsonify({"error": "Invalid file type. Please upload PDF or TXT files only"}), 400
            
    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

@main_bp.route('/debug', methods=['GET'])
def debug_env():
    """Debug endpoint"""
    api_key = current_app.config.get('OPENAI_API_KEY')
    return jsonify({
        "env_loaded": api_key is not None,
        "key_starts_with_sk": api_key.startswith('sk-') if api_key else False,
        "key_length": len(api_key) if api_key else 0
    })

@main_bp.route('/test', methods=['GET'])
def test_api():
    """Test endpoint to verify API is working"""
    return jsonify({
        "status": "API is working",
        "openai_configured": True if current_app.config.get('OPENAI_API_KEY') else False,
        "allowed_extensions": list(current_app.config['ALLOWED_EXTENSIONS'])
    })