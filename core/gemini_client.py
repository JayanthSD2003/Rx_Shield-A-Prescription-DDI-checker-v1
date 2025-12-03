import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if API_KEY:
    genai.configure(api_key=API_KEY)

def perform_ocr(image_path):
    """
    Sends an image to Gemini to extract text (medication names and dosages).
    """
    if not API_KEY:
        return "Error: Gemini API Key not found."

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Load the image
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        prompt = """
        Analyze this handwritten prescription. 
        Extract the medication names and their dosages.
        Return the result as a simple list.
        If you cannot read it, say "Could not read prescription".
        """
        
        response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': image_data}])
        return response.text
    except Exception as e:
        return f"Error during OCR: {str(e)}"

def check_ddi(medication_text):
    """
    Sends the extracted medication text to Gemini to check for Drug-Drug Interactions.
    """
    if not API_KEY:
        return "Error: Gemini API Key not found."

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = f"""
        Analyze the following medication list for potential Drug-Drug Interactions (DDI):
        {medication_text}
        
        Identify any serious interactions.
        Provide a brief summary of warnings.
        If no interactions are found, say "No significant interactions found."
        """
        
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error during DDI check: {str(e)}"

def analyze_prescription(image_path):
    """
    Sends an image to Gemini to extract text AND check for DDI in a single call.
    """
    if not API_KEY:
        return "Error: Gemini API Key not found."

    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        # Load the image
        with open(image_path, "rb") as f:
            image_data = f.read()
            
        prompt = """
        Analyze this handwritten prescription image.
        
        Task 1: Extract the medication names and their dosages accurately.
        Task 2: Check for any potential Drug-Drug Interactions (DDI) or safety warnings among these medications.
        
        Format your response exactly as follows:
        
        --- Prescribed Medications ---
        [List of medications and dosages here]
        
        --- Safety Analysis ---
        [DDI warnings and safety summary here. If none, say "No significant interactions found."]
        """
        
        response = model.generate_content([prompt, {'mime_type': 'image/jpeg', 'data': image_data}])
        return response.text
    except Exception as e:
        return f"Error during analysis: {str(e)}"
