from flask import Flask, request, jsonify
import pdfplumber
import pickle
from flask_cors import CORS
import numpy as np
import re
from scipy.sparse import hstack

# ================================
# Create Flask App
# ================================
app = Flask(__name__)
CORS(app)

print("🚀 Loading High-Accuracy Resume Analyzer...")

# ================================
# Load High-Accuracy Model
# ================================
try:
    with open('high_accuracy_model.pkl', 'rb') as f:
        model_data = pickle.load(f)
    
    model = model_data['model']
    word_vectorizer = model_data['word_vectorizer']
    char_vectorizer = model_data['char_vectorizer']
    classes = model_data['classes']
    model_accuracy = model_data['accuracy']
    
    print(f"✅ Model loaded successfully!")
    print(f"📊 Model accuracy: {model_accuracy*100:.2f}%")
    print(f"🏷️  Categories: {len(classes)}")
    
except Exception as e:
    print(f"❌ Error loading model: {e}")
    exit(1)

# ================================
# Text Cleaning Function
# ================================
def clean_text(text):
    """Enhanced text cleaning for better accuracy"""
    if not text:
        return ""
    
    text = str(text).lower()
    
    # Normalize important terms
    text = re.sub(r'\b(years?|yrs?)\b', 'years', text)
    text = re.sub(r'\b(experience|exp)\b', 'experience', text)
    text = re.sub(r'\b(management|mgmt)\b', 'management', text)
    text = re.sub(r'\b(development|dev)\b', 'development', text)
    text = re.sub(r'\b(technology|tech)\b', 'technology', text)
    text = re.sub(r'\b(engineering|engineer)\b', 'engineering', text)
    text = re.sub(r'\b(software|programming)\b', 'software', text)
    text = re.sub(r'\b(design|designer)\b', 'design', text)
    text = re.sub(r'\b(culinary|cooking|chef|kitchen)\b', 'culinary', text)
    text = re.sub(r'\b(healthcare|medical|nurse)\b', 'healthcare', text)
    text = re.sub(r'\b(finance|financial|banking)\b', 'finance', text)
    text = re.sub(r'\b(aviation|aircraft|pilot)\b', 'aviation', text)
    
    # Remove special characters
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    
    return text.strip()

# ================================
# Helper Functions
# ================================
def get_match_level(probability):
    """Determine match level based on probability - More optimistic thresholds"""
    if probability >= 0.4:
        return "Excellent Match"
    elif probability >= 0.25:
        return "Very High Match"
    elif probability >= 0.15:
        return "High Match"
    elif probability >= 0.08:
        return "Good Match"
    else:
        return "Moderate Match"

def get_match_percentage(probability):
    """Convert probability to realistic percentage (70-95%) - Higher range"""
    # Scale probability to 70-95% range for better UX and confidence
    return round(70 + (probability * 25), 1)

# ================================
# Routes
# ================================
@app.route("/")
def home():
    return jsonify({
        "status": "AI Resume Analyzer is running",
        "model_accuracy": f"{model_accuracy*100:.2f}%",
        "categories": len(classes),
        "version": "2.0 - High Accuracy"
    })

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "model_loaded": True})

@app.route("/categories")
def get_categories():
    """Get all available job categories"""
    return jsonify({
        "categories": sorted(classes.tolist()),
        "total": len(classes)
    })

@app.route("/analyze", methods=["POST"])
def analyze_resume():
    """Analyze uploaded resume and return job matches"""
    
    # Validate request
    if "resume" not in request.files:
        return jsonify({"error": "No resume file uploaded"}), 400
    
    file = request.files["resume"]
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    if not file.filename.lower().endswith('.pdf'):
        return jsonify({"error": "Only PDF files are supported"}), 400
    
    try:
        # Extract text from PDF with enhanced error handling
        print(f"📄 Processing file: {file.filename}")
        print(f"📊 File size: {file.content_length if hasattr(file, 'content_length') else 'Unknown'} bytes")
        text = ""
        
        with pdfplumber.open(file) as pdf:
            # Check page count - limit to 1-2 pages for resumes
            total_pages = len(pdf.pages)
            print(f"📊 PDF has {total_pages} pages")
            
            if total_pages > 2:
                return jsonify({
                    "error": f"Resume should be 1-2 pages only. Your PDF has {total_pages} pages. Please upload a shorter resume."
                }), 400
            
            if total_pages == 0:
                return jsonify({"error": "PDF appears to be empty"}), 400
            
            # Extract text from each page (max 2 pages)
            for page_num, page in enumerate(pdf.pages[:2]):  # Limit to first 2 pages
                try:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + " "
                        print(f"📝 Page {page_num + 1}: {len(page_text)} characters extracted")
                        print(f"📝 Sample text: {page_text[:100]}...")
                    else:
                        print(f"⚠️  Page {page_num + 1}: No text extracted - might be image-based")
                except Exception as page_error:
                    print(f"⚠️  Error extracting from page {page_num + 1}: {page_error}")
                    continue
        
        print(f"📊 Total extracted text: {len(text)} characters")
        
        if not text.strip():
            return jsonify({
                "error": "Could not extract text from PDF. The file might be:\n• Image-based (scanned document)\n• Password protected\n• Corrupted\n• Have security restrictions\n\nPlease try:\n• Converting to text-based PDF\n• Removing password protection\n• Using a different PDF creator"
            }), 400
        
        print(f"✅ Successfully extracted {len(text)} characters from {total_pages} page(s)")
        
        # Clean text
        cleaned_text = clean_text(text)
        
        if len(cleaned_text) < 50:
            return jsonify({"error": "Resume text too short for analysis"}), 400
        
        print(f"🧹 Cleaned text: {len(cleaned_text)} characters")
        
        # Vectorize text using both vectorizers
        word_features = word_vectorizer.transform([cleaned_text])
        char_features = char_vectorizer.transform([cleaned_text])
        
        # Combine features
        combined_features = hstack([word_features, char_features])
        
        # Get predictions and probabilities
        probabilities = model.predict_proba(combined_features)[0]
        
        # Apply confidence boost to make results more encouraging
        # Boost the top predictions to show higher confidence
        sorted_indices = np.argsort(probabilities)[::-1]
        boosted_probabilities = probabilities.copy()
        
        # Apply progressive boost to top 5 predictions
        boost_factors = [1.8, 1.5, 1.3, 1.2, 1.1]  # Higher boost for top predictions
        for i, idx in enumerate(sorted_indices[:5]):
            if i < len(boost_factors):
                boosted_probabilities[idx] *= boost_factors[i]
        
        # Normalize to ensure probabilities don't exceed 1.0
        max_prob = np.max(boosted_probabilities)
        if max_prob > 1.0:
            boosted_probabilities = boosted_probabilities / max_prob
        
        # Create results with boosted probabilities
        results = []
        for i, category in enumerate(classes):
            prob = boosted_probabilities[i]
            results.append({
                'category': category,
                'probability': prob,
                'percentage': get_match_percentage(prob),
                'level': get_match_level(prob)
            })
        
        # Sort by probability (highest first)
        results.sort(key=lambda x: x['probability'], reverse=True)
        
        # Get top 5 matches
        top_matches = results[:5]
        
        # Format response
        response = []
        for match in top_matches:
            response.append({
                "job": match['category'].replace('-', ' ').title(),
                "percentage": match['percentage'],
                "level": match['level']
            })
        
        print(f"🎯 Top prediction: {response[0]['job']} ({response[0]['percentage']}%)")
        
        return jsonify(response)
        
    except Exception as e:
        error_msg = str(e).lower()
        
        # Handle common PDF errors
        if "password" in error_msg or "encrypted" in error_msg:
            return jsonify({
                "error": "PDF is password protected or encrypted. Please remove protection and try again."
            }), 400
        elif "permission" in error_msg or "unauthorized" in error_msg or "not allowed" in error_msg:
            return jsonify({
                "error": "PDF has security restrictions that prevent text extraction. Please use a different PDF or remove restrictions."
            }), 400
        elif "damaged" in error_msg or "corrupt" in error_msg or "invalid" in error_msg:
            return jsonify({
                "error": "PDF file appears to be damaged or corrupted. Please try a different file."
            }), 400
        elif "eof" in error_msg or "unexpected end" in error_msg:
            return jsonify({
                "error": "PDF file is incomplete or truncated. Please upload the complete file."
            }), 400
        elif "syntax" in error_msg or "parse" in error_msg:
            return jsonify({
                "error": "PDF file format is invalid or corrupted. Please try a different PDF file."
            }), 400
        elif "timeout" in error_msg:
            return jsonify({
                "error": "PDF processing timed out. File might be too complex or large."
            }), 400
        else:
            print(f"❌ Unexpected error analyzing resume: {str(e)}")
            return jsonify({
                "error": f"Error processing PDF: Please ensure your PDF is:\n• Not password protected\n• Text-based (not scanned image)\n• 1-2 pages maximum\n• Under 10MB in size"
            }), 500

@app.route("/test", methods=["POST"])
def test_with_text():
    """Test endpoint for direct text input (for debugging)"""
    data = request.get_json()
    
    if not data or 'text' not in data:
        return jsonify({"error": "No text provided"}), 400
    
    try:
        text = data['text']
        cleaned_text = clean_text(text)
        
        # Vectorize
        word_features = word_vectorizer.transform([cleaned_text])
        char_features = char_vectorizer.transform([cleaned_text])
        combined_features = hstack([word_features, char_features])
        
        # Predict
        probabilities = model.predict_proba(combined_features)[0]
        
        # Get top 5 results
        results = []
        for i, category in enumerate(classes):
            prob = probabilities[i]
            results.append({
                'category': category,
                'probability': prob,
                'percentage': get_match_percentage(prob)
            })
        
        results.sort(key=lambda x: x['probability'], reverse=True)
        
        response = []
        for match in results[:5]:
            response.append({
                "job": match['category'].replace('-', ' ').title(),
                "percentage": match['percentage'],
                "level": get_match_level(match['probability'])
            })
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================================
# Run Server
# ================================
if __name__ == "__main__":
    print("🌟 High-Accuracy Resume Analyzer Server Starting...")
    print("📡 Server will run on http://127.0.0.1:5000")
    print("🔗 Frontend should connect to this URL")
    print("=" * 50)
    
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=True
    )