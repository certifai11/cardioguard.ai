document.addEventListener('DOMContentLoaded', function() {
    // Simulator elements
    const simulatorSelect = document.getElementById('simulator-select');
    const simulatorBtn = document.getElementById('simulator-btn');
    
    // Test cases for simulator
    const testCases = {
        'high-risk': {
            age: 65,
            sex: 1,
            cp: 0,
            trestbps: 170,
            chol: 280,
            fbs: 1,
            restecg: 2,
            thalach: 120,
            exang: 1,
            oldpeak: 4.2,
            slope: 2,
            ca: 3,
            thal: 2
        },
        'moderate-risk': {
            age: 52,
            sex: 1,
            cp: 1,
            trestbps: 140,
            chol: 230,
            fbs: 0,
            restecg: 1,
            thalach: 140,
            exang: 0,
            oldpeak: 1.5,
            slope: 1,
            ca: 1,
            thal: 2
        },
        'low-risk': {
            age: 38,
            sex: 0,
            cp: 3,
            trestbps: 110,
            chol: 190,
            fbs: 0,
            restecg: 0,
            thalach: 185,
            exang: 0,
            oldpeak: 0,
            slope: 0,
            ca: 0,
            thal: 0
        }
    };
    
    // Enable simulator button when a test case is selected
    simulatorSelect.addEventListener('change', function() {
        simulatorBtn.disabled = !this.value;
    });
    
    // Run simulation when button is clicked
    simulatorBtn.addEventListener('click', function() {
        const selectedCase = simulatorSelect.value;
        
        // Generate random data if 'random' is selected
        if (selectedCase === 'random') {
            fillFormWithRandomData();
        } else {
            // Fill form with selected test case data
            fillFormWithTestCase(selectedCase);
        }
        
        // Submit the form
        document.getElementById('assessment-form').dispatchEvent(new Event('submit'));
    });
    
    // Fill form with test case data
    function fillFormWithTestCase(caseKey) {
        const data = testCases[caseKey];
        
        // Set form values
        document.getElementById('age').value = data.age;
        
        // Set sex radio button
        if (data.sex === 1) {
            document.getElementById('sex-male').checked = true;
        } else {
            document.getElementById('sex-female').checked = true;
        }
        
        document.getElementById('cp').value = data.cp;
        document.getElementById('trestbps').value = data.trestbps;
        document.getElementById('chol').value = data.chol;
        document.getElementById('fbs').value = data.fbs;
        document.getElementById('restecg').value = data.restecg;
        document.getElementById('thalach').value = data.thalach;
        document.getElementById('exang').value = data.exang;
        document.getElementById('oldpeak').value = data.oldpeak;
        document.getElementById('slope').value = data.slope;
        document.getElementById('ca').value = data.ca;
        document.getElementById('thal').value = data.thal;
    }
    
    // Fill form with random patient data
    function fillFormWithRandomData() {
        // Generate random data
        const randomData = {
            age: Math.floor(Math.random() * (80 - 25) + 25),
            sex: Math.random() > 0.5 ? 1 : 0,
            cp: Math.floor(Math.random() * 4),
            trestbps: Math.floor(Math.random() * (180 - 100) + 100),
            chol: Math.floor(Math.random() * (350 - 150) + 150),
            fbs: Math.random() > 0.7 ? 1 : 0,
            restecg: Math.floor(Math.random() * 3),
            thalach: Math.floor(Math.random() * (220 - 120) + 120),
            exang: Math.random() > 0.7 ? 1 : 0,
            oldpeak: Math.random() * 4,
            slope: Math.floor(Math.random() * 3),
            ca: Math.floor(Math.random() * 4),
            thal: Math.floor(Math.random() * 4)
        };
        
        // Round oldpeak to 1 decimal place
        randomData.oldpeak = Math.round(randomData.oldpeak * 10) / 10;
        
        // Fill form with random data
        fillFormWithTestCase(randomData);
    }
});