import PyPDF2

class PDFService:
    @staticmethod
    def extract_text_from_pdf(file_stream):
        """Extract text from PDF file"""
        try:
            pdf_reader = PyPDF2.PdfReader(file_stream)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"