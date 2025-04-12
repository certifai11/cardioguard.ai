document.addEventListener('DOMContentLoaded', function() {
    // Form elements
    const assessmentForm = document.getElementById('assessment-form');
    const clearFormBtn = document.getElementById('clear-form-btn');
    const resultContainer = document.getElementById('result-container');
    const resultTitle = document.getElementById('result-title');
    const resultDescription = document.getElementById('result-description');
    const riskLevel = document.getElementById('risk-level');
    const riskFactors = document.getElementById('risk-factors');
    
    // Dashboard metrics
    const assessmentsCountEl = document.getElementById('assessments-count');
    const highRiskCountEl = document.getElementById('high-risk-count');
    const moderateRiskCountEl = document.getElementById('moderate-risk-count');
    const lowRiskCountEl = document.getElementById('low-risk-count');
    
    // Audio elements
    const highRiskAudio = document.getElementById('high-risk-audio');
    const moderateRiskAudio = document.getElementById('moderate-risk-audio');
    
    // Threshold slider
    const thresholdSlider = document.getElementById('threshold-slider');
    const thresholdValue = document.getElementById('threshold-value');
    
    // About button
    const aboutBtn = document.getElementById('about-btn');
    
    // Initialize dashboard metrics
    let assessmentsCount = 0;
    let highRiskCount = 0;
    let moderateRiskCount = 0;
    let lowRiskCount = 0;
    
    // Default prediction threshold
    let predictionThreshold = 0.5;
    
    // Form submission handler
    assessmentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        submitAssessment();
    });
    
    // Clear form button handler
    clearFormBtn.addEventListener('click', function() {
        assessmentForm.reset();
        resultContainer.style.display = 'none';
    });
    
    // About button handler
    aboutBtn.addEventListener('click', function() {
        window.location.href = '/about';
    });
    
    // Threshold slider handler
    thresholdSlider.addEventListener('input', function() {
        predictionThreshold = parseFloat(this.value);
        thresholdValue.textContent = predictionThreshold.toFixed(2);
    });
    
    // Submit assessment data to API
    function submitAssessment() {
        // Get form data
        const formData = {
            age: document.getElementById('age').value,
            sex: document.querySelector('input[name="sex"]:checked').value,
            cp: document.getElementById('cp').value,
            trestbps: document.getElementById('trestbps').value,
            chol: document.getElementById('chol').value,
            fbs: document.getElementById('fbs').value,
            restecg: document.getElementById('restecg').value,
            thalach: document.getElementById('thalach').value,
            exang: document.getElementById('exang').value,
            oldpeak: document.getElementById('oldpeak').value,
            slope: document.getElementById('slope').value,
            ca: document.getElementById('ca').value,
            thal: document.getElementById('thal').value
        };
        
        // Send data to API
        fetch(`/api/predict?threshold=${predictionThreshold}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                displayResult(data);
                updateMetrics(data.risk_level);
            } else {
                alert('Error: ' + data.error);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while processing your request.');
        });
    }
    
    // Display assessment result
    function displayResult(data) {
        // Update result container
        resultContainer.style.display = 'block';
        resultTitle.textContent = data.message;
        
        // Set result description based on risk level
        if (data.risk_level === 'high') {
            resultDescription.innerHTML = `
                <p class="fw-bold">The assessment indicates a ${data.risk_percentage}% probability of heart disease.</p>
                <p>This high-risk result suggests immediate consultation with a healthcare provider. 
                This is not a diagnosis but indicates that several risk factors are present.</p>
            `;
            resultContainer.className = 'result-box result-high-risk';
            riskLevel.style.width = `${data.risk_percentage}%`;
            riskLevel.style.backgroundColor = '#dc3545';
            highRiskAudio.play();
        } else if (data.risk_level === 'moderate') {
            resultDescription.innerHTML = `
                <p class="fw-bold">The assessment indicates a ${data.risk_percentage}% probability of heart disease.</p>
                <p>This moderate-risk result suggests scheduling a consultation with a healthcare provider.
                Consider lifestyle modifications and follow-up evaluation.</p>
            `;
            resultContainer.className = 'result-box result-moderate-risk';
            riskLevel.style.width = `${data.risk_percentage}%`;
            riskLevel.style.backgroundColor = '#ffc107';
            moderateRiskAudio.play();
        } else {
            resultDescription.innerHTML = `
                <p class="fw-bold">The assessment indicates a ${data.risk_percentage}% probability of heart disease.</p>
                <p>This low-risk result suggests maintaining a heart-healthy lifestyle.
                Continue regular check-ups with your healthcare provider.</p>
            `;
            resultContainer.className = 'result-box result-low-risk';
            riskLevel.style.width = `${data.risk_percentage}%`;
            riskLevel.style.backgroundColor = '#28a745';
        }
        
        // Display risk factors
        riskFactors.innerHTML = '';
        data.risk_factors.forEach(factor => {
            const li = document.createElement('li');
            li.textContent = factor;
            riskFactors.appendChild(li);
        });
        
        // Scroll to result
        resultContainer.scrollIntoView({ behavior: 'smooth' });
    }
    
    // Update dashboard metrics
    function updateMetrics(riskLevel) {
        assessmentsCount++;
        
        if (riskLevel === 'high') {
            highRiskCount++;
        } else if (riskLevel === 'moderate') {
            moderateRiskCount++;
        } else {
            lowRiskCount++;
        }
        
        // Update UI
        assessmentsCountEl.textContent = assessmentsCount;
        highRiskCountEl.textContent = highRiskCount;
        moderateRiskCountEl.textContent = moderateRiskCount;
        lowRiskCountEl.textContent = lowRiskCount;
        
        // Send statistics update to server
        fetch('/api/stats', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                assessment_count: assessmentsCount,
                high_risk_count: highRiskCount,
                moderate_risk_count: moderateRiskCount,
                low_risk_count: lowRiskCount
            })
        })
        .catch(error => console.error('Error updating stats:', error));
    }
    
    // Initialize form validation
    function initFormValidation() {
        // Add custom validation styles
        assessmentForm.addEventListener('input', function(e) {
            const input = e.target;
            if (input.validity.valid) {
                input.classList.remove('is-invalid');
                input.classList.add('is-valid');
            } else {
                input.classList.remove('is-valid');
                input.classList.add('is-invalid');
            }
        });
    }
    
    // Initialize
    initFormValidation();
});