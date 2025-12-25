import pandas as pd
import pickle
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from scipy.sparse import hstack

print("🚀 HIGH ACCURACY RESUME CLASSIFIER")
print("=" * 50)

def clean_text(text):
    """Enhanced text cleaning for better accuracy"""
    if pd.isna(text):
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

# Load dataset
print("📊 Loading dataset...")
df = pd.read_csv("resume.csv")
print(f"Dataset shape: {df.shape}")

# Clean text
print("🧹 Cleaning text...")
df['clean_text'] = df['Resume_str'].apply(clean_text)

# Filter short resumes
df = df[df['clean_text'].str.len() > 150]
print(f"After filtering: {df.shape}")

# Check class distribution
class_counts = df['Category'].value_counts()
print(f"Categories: {len(class_counts)}")

# Keep classes with at least 20 samples
min_samples = 20
valid_classes = class_counts[class_counts >= min_samples].index
df = df[df['Category'].isin(valid_classes)]
print(f"Final shape: {df.shape}")
print(f"Final categories: {len(valid_classes)}")

# Prepare data
X = df['clean_text']
y = df['Category']

# Create multiple vectorizers for better features
print("🔧 Creating features...")

# Word-level TF-IDF
word_vectorizer = TfidfVectorizer(
    analyzer='word',
    ngram_range=(1, 3),
    max_features=8000,
    min_df=2,
    max_df=0.95,
    stop_words='english'
)

# Character-level TF-IDF
char_vectorizer = TfidfVectorizer(
    analyzer='char',
    ngram_range=(3, 6),
    max_features=4000,
    min_df=2,
    max_df=0.95
)

# Transform text
word_features = word_vectorizer.fit_transform(X)
char_features = char_vectorizer.fit_transform(X)

# Combine features
X_combined = hstack([word_features, char_features])
print(f"Combined features shape: {X_combined.shape}")

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X_combined, y, test_size=0.2, random_state=42, stratify=y
)

print(f"Training: {X_train.shape}")
print(f"Testing: {X_test.shape}")

# Train Random Forest with optimized parameters
print("🤖 Training Random Forest...")
model = RandomForestClassifier(
    n_estimators=500,
    max_depth=None,
    min_samples_split=2,
    min_samples_leaf=1,
    class_weight='balanced',
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# Evaluate
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print(f"\n🎯 ACCURACY: {accuracy:.4f} ({accuracy*100:.2f}%)")

# Detailed report
print("\n📋 Classification Report:")
report = classification_report(y_test, y_pred, output_dict=True)
for category, metrics in report.items():
    if category not in ['accuracy', 'macro avg', 'weighted avg']:
        f1 = metrics.get('f1-score', 0)
        if f1 > 0.8:
            print(f"✅ {category}: {f1:.3f}")
        elif f1 > 0.6:
            print(f"🟡 {category}: {f1:.3f}")
        else:
            print(f"❌ {category}: {f1:.3f}")

# Save model
print("\n💾 Saving model...")
model_data = {
    'model': model,
    'word_vectorizer': word_vectorizer,
    'char_vectorizer': char_vectorizer,
    'classes': model.classes_,
    'accuracy': accuracy
}

with open('high_accuracy_model.pkl', 'wb') as f:
    pickle.dump(model_data, f)

print("✅ Model saved as 'high_accuracy_model.pkl'")

# Test with samples
print("\n🧪 Testing samples...")

test_samples = {
    "CHEF": "Executive chef culinary arts cooking kitchen management food preparation restaurant",
    "INFORMATION-TECHNOLOGY": "software engineer programming python javascript web development coding",
    "HEALTHCARE": "registered nurse medical patient care hospital healthcare nursing",
    "FINANCE": "financial analyst banking investment portfolio management accounting",
    "ENGINEERING": "mechanical engineer design manufacturing CAD technical drawing"
}

for category, sample in test_samples.items():
    clean_sample = clean_text(sample)
    word_vec = word_vectorizer.transform([clean_sample])
    char_vec = char_vectorizer.transform([clean_sample])
    sample_features = hstack([word_vec, char_vec])
    
    prediction = model.predict(sample_features)[0]
    probabilities = model.predict_proba(sample_features)[0]
    max_prob = max(probabilities)
    
    status = "✅" if prediction == category else "❌"
    print(f"{status} {category}: Predicted {prediction} ({max_prob:.3f})")

print(f"\n🏆 TRAINING COMPLETED!")
print(f"📈 Final Accuracy: {accuracy*100:.2f}%")