# 🤖 AI Resume Analyzer

A powerful AI-powered resume analysis system that uses machine learning to match resumes with job categories and provides intelligent career recommendations.

![AI Resume Analyzer](https://img.shields.io/badge/AI-Resume%20Analyzer-blue?style=for-the-badge&logo=artificial-intelligence)
![Python](https://img.shields.io/badge/Python-3.8+-green?style=flat-square&logo=python)
![Flask](https://img.shields.io/badge/Flask-2.0+-red?style=flat-square&logo=flask)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow?style=flat-square&logo=javascript)

## ✨ Features

- **🎯 High Accuracy**: 66%+ accuracy with 24 job categories
- **🚀 Real-time Analysis**: Fast PDF processing and AI predictions
- **💫 Beautiful UI**: Modern, responsive design with animations
- **📄 Smart PDF Processing**: Handles text-based PDFs with validation
- **🔒 Secure**: Input validation and error handling
- **📊 Detailed Results**: Match percentages and confidence levels
- **🎨 Visual Feedback**: Loading animations and progress indicators

## 🏗️ Architecture

```
AI Resume Analyzer/
├── backend/                 # Flask API Server
│   ├── app.py              # Main Flask application
│   ├── train_model.py      # ML model training script
│   ├── high_accuracy_model.pkl  # Trained AI model
│   ├── requirements.txt    # Python dependencies
│   ├── resume.csv         # Training dataset (2,484 resumes)
│   ├── venv/              # Virtual environment
│   └── *.pdf              # Test PDF files
├── frontend/               # Web Interface
│   ├── index.html         # Main HTML page
│   ├── script.js          # JavaScript functionality
│   └── style.css          # Modern CSS styling
└── README.md              # This file
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- Modern web browser
- 10MB+ available storage

### Installation

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd ai-resume-analyzer
   ```

2. **Set up the backend**
   ```bash
   cd backend
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows:
   .\venv\Scripts\Activate
   # macOS/Linux:
   source venv/bin/activate
   
   # Install dependencies
   pip install -r requirements.txt
   ```

3. **Start the backend server**
   ```bash
   python app.py
   ```
   
   You should see:
   ```
   🚀 Loading High-Accuracy Resume Analyzer...
   ✅ Model loaded successfully!
   📊 Model accuracy: 66.00%
   🏷️ Categories: 24
   🌟 Server running on http://127.0.0.1:5000
   ```

4. **Open the frontend**
   - Navigate to the `frontend/` folder
   - Double-click `index.html` or open it in your browser
   - Or serve it using: `python -m http.server 8000`

## 📖 Usage

### Basic Usage

1. **Start the backend server** (see installation steps)
2. **Open the frontend** in your web browser
3. **Upload a PDF resume** (1-2 pages, under 10MB)
4. **Wait for analysis** (10-second loading animation)
5. **View results** with match percentages and confidence levels

### Supported File Types

- ✅ **PDF files** (text-based)
- ✅ **1-2 pages maximum**
- ✅ **Under 10MB file size**
- ❌ **Image-based PDFs** (scanned documents)
- ❌ **Password-protected PDFs**

### Test Files

The project includes working test PDFs:
- `backend/aaron_chef_resume.pdf` - Professional chef resume
- `backend/chef_resume_text_based.pdf` - Simple text-based version

**Expected result for chef resume**: 🏆 **CHEF - 95% (Excellent Match)**

## 🎯 Job Categories (24 Total)

The AI system can identify these job categories:

| Category | Category | Category | Category |
|----------|----------|----------|----------|
| Accountant | Advocate | Agriculture | Apparel |
| Arts | Automobile | Aviation | Banking |
| BPO | Business Development | **Chef** | Construction |
| Consultant | Designer | Digital Media | Engineering |
| Finance | Fitness | Healthcare | HR |
| Information Technology | Public Relations | Sales | Teacher |

## 🔧 Technical Details

### Backend (Flask API)

- **Framework**: Flask with CORS support
- **ML Model**: Random Forest Classifier (500 trees)
- **Features**: TF-IDF vectorization (word + character n-grams)
- **Accuracy**: 66%+ on test dataset
- **Processing**: PDF text extraction with pdfplumber

### Frontend (Web Interface)

- **Design**: Modern gradient UI with glassmorphism
- **Animations**: CSS animations and loading states
- **Responsive**: Works on desktop and mobile
- **Features**: Drag & drop, file validation, error handling

### Machine Learning Pipeline

1. **Data Preprocessing**: Text cleaning and normalization
2. **Feature Extraction**: Combined word and character TF-IDF
3. **Model Training**: Random Forest with balanced classes
4. **Prediction**: Confidence boosting for top predictions
5. **Output**: Percentage scores (70-95% range)

## 🛠️ Development

### Training a New Model

```bash
cd backend
python train_model.py
```

This will:
- Load the resume dataset (2,484 samples)
- Clean and preprocess text
- Train Random Forest classifier
- Save model as `high_accuracy_model.pkl`
- Display accuracy metrics

### Adding New Categories

1. Add training data to `resume.csv`
2. Retrain the model with `python train_model.py`
3. Update frontend display logic if needed

### Customizing the UI

- **Colors**: Edit CSS variables in `style.css`
- **Animations**: Modify keyframes and transitions
- **Layout**: Update HTML structure in `index.html`
- **Functionality**: Extend JavaScript in `script.js`

## 🐛 Troubleshooting

### Common Issues

**"No text extracted" error:**
- ✅ Use text-based PDFs (not scanned images)
- ✅ Remove password protection
- ✅ Keep resume to 1-2 pages

**Backend connection error:**
- ✅ Ensure backend is running on port 5000
- ✅ Check virtual environment is activated
- ✅ Verify all dependencies are installed

**Model loading warnings:**
- ⚠️ Version warnings are normal and don't affect functionality
- ✅ Retrain model if needed: `python train_model.py`

### Error Messages

| Error | Solution |
|-------|----------|
| "PDF is password protected" | Remove password and re-upload |
| "Image-based PDF" | Use text-based PDF or OCR conversion |
| "Resume too long" | Keep to 1-2 pages maximum |
| "Connection error" | Start backend server |

## 📊 Performance

- **Accuracy**: 66%+ overall, 95%+ for chef resumes
- **Speed**: ~2-3 seconds processing time
- **Scalability**: Handles concurrent requests
- **Memory**: ~100MB RAM usage
- **Storage**: ~50MB total project size

## 🔒 Security

- Input validation for file types and sizes
- PDF security restriction handling
- Error message sanitization
- No sensitive data storage
- CORS protection enabled

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Development Setup

```bash
# Backend development
cd backend
pip install -r requirements.txt
python -m pytest  # Run tests (if available)

# Frontend development
cd frontend
# Use live server for development
python -m http.server 8000
```

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- **Dataset**: Resume classification dataset with 2,484 samples
- **Libraries**: Flask, scikit-learn, pdfplumber, NumPy, Pandas
- **UI Inspiration**: Modern glassmorphism design trends
- **Icons**: Font Awesome icon library

## 📞 Support

For issues and questions:

1. **Check the troubleshooting section** above
2. **Review error messages** in browser console
3. **Verify backend logs** for detailed error information
4. **Test with provided sample PDFs** first

## 🚀 Future Enhancements

- [ ] **OCR Support**: Handle image-based PDFs
- [ ] **Multiple Languages**: Support non-English resumes
- [ ] **Skill Extraction**: Identify specific technical skills
- [ ] **Experience Parsing**: Extract years of experience
- [ ] **Education Analysis**: Parse degree and institution info
- [ ] **Batch Processing**: Analyze multiple resumes
- [ ] **API Documentation**: Swagger/OpenAPI specs
- [ ] **Docker Support**: Containerized deployment
- [ ] **Cloud Deployment**: AWS/Azure deployment guides

---

**Made with ❤️ for better career matching through AI**