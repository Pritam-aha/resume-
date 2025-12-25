// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('resume');
const fileInfo = document.getElementById('fileInfo');
const fileName = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');
const analyzeBtn = document.getElementById('analyzeBtn');
const loadingSection = document.getElementById('loadingSection');
const resultSection = document.getElementById('resultSection');
const result = document.getElementById('result');

// Loading elements
const loadingText = document.getElementById('loadingText');
const progressFill = document.getElementById('progressFill');
const progressPercentage = document.getElementById('progressPercentage');

// Initialize drag and drop functionality
initializeDragAndDrop();
initializeFileInput();

function initializeDragAndDrop() {
  // Prevent default drag behaviors
  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  // Highlight drop area when item is dragged over it
  ['dragenter', 'dragover'].forEach(eventName => {
    uploadArea.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    uploadArea.addEventListener(eventName, unhighlight, false);
  });

  // Handle dropped files
  uploadArea.addEventListener('drop', handleDrop, false);
  uploadArea.addEventListener('click', () => fileInput.click());
}

function initializeFileInput() {
  fileInput.addEventListener('change', handleFileSelect);
  removeFileBtn.addEventListener('click', removeFile);
}

function preventDefaults(e) {
  e.preventDefault();
  e.stopPropagation();
}

function highlight() {
  uploadArea.classList.add('dragover');
}

function unhighlight() {
  uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
  const dt = e.dataTransfer;
  const files = dt.files;
  
  if (files.length > 0) {
    fileInput.files = files;
    handleFileSelect();
  }
}

function handleFileSelect() {
  const file = fileInput.files[0];
  
  if (file) {
    // Validate file type
    if (file.type !== 'application/pdf') {
      showNotification('Please select a PDF file only.', 'error');
      return;
    }
    
    // Validate file size (10MB limit)
    if (file.size > 10 * 1024 * 1024) {
      showNotification('File size should be less than 10MB.', 'error');
      return;
    }
    
    // Validate file size (minimum 10KB for meaningful content)
    if (file.size < 10 * 1024) {
      showNotification('File seems too small. Please upload a complete resume.', 'error');
      return;
    }
    
    displayFileInfo(file);
    enableAnalyzeButton();
  }
}

function displayFileInfo(file) {
  fileName.textContent = file.name;
  fileInfo.style.display = 'flex';
  
  // Hide upload content and show file info
  uploadArea.querySelector('.upload-icon').style.display = 'none';
  uploadArea.querySelector('h3').style.display = 'none';
  uploadArea.querySelector('p').style.display = 'none';
}

function removeFile(e) {
  e.stopPropagation();
  fileInput.value = '';
  fileInfo.style.display = 'none';
  
  // Show upload content again
  uploadArea.querySelector('.upload-icon').style.display = 'block';
  uploadArea.querySelector('h3').style.display = 'block';
  uploadArea.querySelector('p').style.display = 'block';
  
  disableAnalyzeButton();
  hideResults();
  hideLoadingSection();
}

function enableAnalyzeButton() {
  analyzeBtn.disabled = false;
}

function disableAnalyzeButton() {
  analyzeBtn.disabled = true;
}

function showLoading() {
  const btnText = analyzeBtn.querySelector('.btn-text');
  const loadingSpinner = analyzeBtn.querySelector('.loading-spinner');
  
  btnText.style.display = 'none';
  loadingSpinner.style.display = 'flex';
  analyzeBtn.disabled = true;
  
  // Show loading section immediately
  loadingSection.style.display = 'block';
  
  // Small delay to ensure DOM is updated, then scroll and start animation
  setTimeout(() => {
    loadingSection.scrollIntoView({ behavior: 'smooth', block: 'center' });
    startProgressAnimation();
  }, 50);
}

function hideLoading() {
  const btnText = analyzeBtn.querySelector('.btn-text');
  const loadingSpinner = analyzeBtn.querySelector('.loading-spinner');
  
  btnText.style.display = 'flex';
  loadingSpinner.style.display = 'none';
  analyzeBtn.disabled = false;
  
  // Hide loading section
  loadingSection.style.display = 'none';
  
  // Reset progress
  resetProgress();
}

function startProgressAnimation() {
  const steps = [
    { text: "Reading PDF file and extracting content...", duration: 2500, step: 1 },
    { text: "Analyzing text structure and keywords...", duration: 2000, step: 2 },
    { text: "Processing with advanced AI model...", duration: 3500, step: 3 },
    { text: "Matching skills and generating results...", duration: 2000, step: 4 }
  ];
  
  let currentProgress = 0;
  let stepIndex = 0;
  
  // Reset all steps
  document.querySelectorAll('.step').forEach(step => {
    step.classList.remove('active', 'completed');
  });
  
  function animateStep() {
    if (stepIndex >= steps.length) return;
    
    const currentStep = steps[stepIndex];
    const stepElement = document.getElementById(`step${currentStep.step}`);
    
    // Update loading text
    loadingText.textContent = currentStep.text;
    
    // Activate current step
    stepElement.classList.add('active');
    
    // Animate progress bar
    const targetProgress = ((stepIndex + 1) / steps.length) * 100;
    animateProgress(currentProgress, targetProgress, currentStep.duration);
    
    setTimeout(() => {
      // Complete current step
      stepElement.classList.remove('active');
      stepElement.classList.add('completed');
      
      currentProgress = targetProgress;
      stepIndex++;
      
      if (stepIndex < steps.length) {
        animateStep();
      }
    }, currentStep.duration);
  }
  
  animateStep();
}

function animateProgress(from, to, duration) {
  const startTime = Date.now();
  
  function update() {
    const elapsed = Date.now() - startTime;
    const progress = Math.min(elapsed / duration, 1);
    
    // Easing function for smooth animation
    const easeProgress = 1 - Math.pow(1 - progress, 3);
    const currentValue = from + (to - from) * easeProgress;
    
    progressFill.style.width = `${currentValue}%`;
    progressPercentage.textContent = `${Math.round(currentValue)}%`;
    
    if (progress < 1) {
      requestAnimationFrame(update);
    }
  }
  
  requestAnimationFrame(update);
}

function resetProgress() {
  progressFill.style.width = '0%';
  progressPercentage.textContent = '0%';
  loadingText.textContent = 'Initializing AI analysis...';
  
  // Reset all steps
  document.querySelectorAll('.step').forEach(step => {
    step.classList.remove('active', 'completed');
  });
}

function showResults() {
  resultSection.style.display = 'block';
  resultSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function hideResults() {
  resultSection.style.display = 'none';
}

function hideLoadingSection() {
  loadingSection.style.display = 'none';
}

function showNotification(message, type = 'info') {
  // Create notification element
  const notification = document.createElement('div');
  notification.className = `notification notification-${type}`;
  notification.innerHTML = `
    <i class="fas ${type === 'error' ? 'fa-exclamation-circle' : 'fa-info-circle'}"></i>
    <span>${message}</span>
  `;
  
  // Add notification styles
  notification.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    background: ${type === 'error' ? '#fed7d7' : '#bee3f8'};
    color: ${type === 'error' ? '#c53030' : '#2b6cb0'};
    padding: 15px 20px;
    border-radius: 10px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.1);
    z-index: 1000;
    display: flex;
    align-items: center;
    gap: 10px;
    font-weight: 500;
    animation: slideIn 0.3s ease;
  `;
  
  document.body.appendChild(notification);
  
  // Remove notification after 4 seconds
  setTimeout(() => {
    notification.style.animation = 'slideOut 0.3s ease';
    setTimeout(() => {
      document.body.removeChild(notification);
    }, 300);
  }, 4000);
}

function analyze() {
  if (!fileInput.files.length) {
    showNotification("Please select a resume PDF", 'error');
    return;
  }

  const formData = new FormData();
  formData.append("resume", fileInput.files[0]);

  showLoading();
  hideResults();

  // Start the loading animation first
  const loadingStartTime = Date.now();
  const minimumLoadingTime = 10000; // 10 seconds

  // Make the API call after a small delay to ensure loading shows
  setTimeout(() => {
    fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    })
      .then(res => {
        if (!res.ok) {
          throw new Error(`HTTP error! status: ${res.status}`);
        }
        return res.json();
      })
      .then(data => {
        // Calculate remaining time to complete 10 seconds
        const elapsedTime = Date.now() - loadingStartTime;
        const remainingTime = Math.max(0, minimumLoadingTime - elapsedTime);
        
        // Wait for the remaining time before showing results
        setTimeout(() => {
          hideLoading();
          displayResults(data);
          showResults();
          showNotification("Resume analysis completed successfully!", 'success');
        }, remainingTime);
      })
      .catch(err => {
        // Even on error, wait for minimum loading time
        const elapsedTime = Date.now() - loadingStartTime;
        const remainingTime = Math.max(0, minimumLoadingTime - elapsedTime);
        
        setTimeout(() => {
          console.error('Analysis error:', err);
          hideLoading();
          
          // Enhanced error handling with specific messages
          let errorMessage = "Error analyzing resume. Please try again.";
          
          if (err.message.includes('Failed to fetch')) {
            errorMessage = "Cannot connect to server. Please ensure the backend is running.";
          } else if (err.message.includes('HTTP error! status: 400')) {
            errorMessage = "Invalid file or file format issue. Please check your PDF.";
          } else if (err.message.includes('HTTP error! status: 500')) {
            errorMessage = "Server error occurred. Please try again or contact support.";
          }
          
          showNotification(errorMessage, 'error');
          result.innerHTML = `
            <div style="text-align: center; color: #e53e3e; padding: 20px;">
              <i class="fas fa-exclamation-triangle" style="font-size: 2rem; margin-bottom: 15px;"></i>
              <h4 style="margin-bottom: 10px; color: #e53e3e;">Analysis Failed</h4>
              <p style="line-height: 1.5; margin-bottom: 15px;">${errorMessage}</p>
              <div style="margin-top: 15px; padding: 15px; background: #fed7d7; border-radius: 8px; font-size: 0.9rem; text-align: left;">
                <strong style="color: #c53030;">Common Issues & Solutions:</strong><br><br>
                <strong>🔒 Password Protected:</strong> Remove PDF password<br>
                <strong>📄 Scanned Image:</strong> Use text-based PDF<br>
                <strong>📏 Too Long:</strong> Keep resume to 1-2 pages<br>
                <strong>💾 File Size:</strong> Ensure under 10MB<br>
                <strong>🔌 Connection:</strong> Check if backend server is running
              </div>
            </div>
          `;
          showResults();
        }, remainingTime);
      });
  }, 100); // Small delay to ensure loading animation starts
}

function displayResults(data) {
  if (!data || !Array.isArray(data) || data.length === 0) {
    result.innerHTML = `
      <div style="text-align: center; color: #718096; padding: 20px;">
        <i class="fas fa-search" style="font-size: 2rem; margin-bottom: 10px;"></i>
        <p>No job matches found. Please try with a different resume.</p>
      </div>
    `;
    return;
  }

  let html = '<div class="job-matches">';
  
  data.forEach((item, index) => {
    const percentage = parseFloat(item.percentage);
    const barColor = getPercentageColor(percentage);
    
    // Get appropriate icon based on match level
    let matchIcon = 'fas fa-star';
    if (item.level === 'Excellent Match') matchIcon = 'fas fa-trophy';
    else if (item.level === 'Very High Match') matchIcon = 'fas fa-medal';
    else if (item.level === 'High Match') matchIcon = 'fas fa-star';
    else if (item.level === 'Good Match') matchIcon = 'fas fa-thumbs-up';
    else matchIcon = 'fas fa-check-circle';
    
    html += `
      <div class="job-card" style="animation-delay: ${index * 0.1}s;">
        <div class="job-header">
          <div class="job-title">
            <i class="${matchIcon}" style="color: #667eea; margin-right: 8px;"></i>
            ${escapeHtml(item.job)}
          </div>
          <div class="job-percentage" style="background: ${barColor};">
            ${percentage.toFixed(1)}%
          </div>
        </div>
        <div class="job-level">
          <i class="fas fa-layer-group"></i>
          Match Quality: <strong style="color: #667eea;">${escapeHtml(item.level)}</strong>
        </div>
      </div>
    `;
  });

  html += '</div>';
  result.innerHTML = html;
}

function getPercentageColor(percentage) {
  if (percentage >= 85) return 'linear-gradient(135deg, #48bb78 0%, #38a169 100%)'; // Excellent - Green
  if (percentage >= 80) return 'linear-gradient(135deg, #4299e1 0%, #3182ce 100%)'; // Very High - Blue  
  if (percentage >= 75) return 'linear-gradient(135deg, #ed8936 0%, #dd6b20 100%)'; // High - Orange
  if (percentage >= 70) return 'linear-gradient(135deg, #9f7aea 0%, #805ad5 100%)'; // Good - Purple
  return 'linear-gradient(135deg, #ecc94b 0%, #d69e2e 100%)'; // Moderate - Yellow
}

function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

// Add CSS animations for notifications
const style = document.createElement('style');
style.textContent = `
  @keyframes slideIn {
    from {
      transform: translateX(100%);
      opacity: 0;
    }
    to {
      transform: translateX(0);
      opacity: 1;
    }
  }
  
  @keyframes slideOut {
    from {
      transform: translateX(0);
      opacity: 1;
    }
    to {
      transform: translateX(100%);
      opacity: 0;
    }
  }
  
  .notification-success {
    background: #c6f6d5 !important;
    color: #22543d !important;
  }
`;
document.head.appendChild(style);
