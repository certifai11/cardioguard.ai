import random
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import gradio as gr

# Simulation parameters
SIM_DURATION_HOURS = 24
DATA_POINTS_PER_HOUR = 60
TOTAL_DATA_POINTS = SIM_DURATION_HOURS * DATA_POINTS_PER_HOUR

# Simulate wristband data with realistic adjustments
def simulate_wristband_data(age, weight, height, gender, smoking, family_history):
    user_profile = {
        "age": age,
        "weight": weight,
        "height": height,
        "gender": gender,
        "smoking": smoking,
        "family_history": family_history
    }
    
    data = {
        "time": [],
        "heart_rate": [],
        "hrv_sdnn": [],
        "spo2": [],
        "steps": [],
        "sleep": [],
        "activity": []
    }
    
    current_time = datetime.now()
    steps_total = 0
    max_hr = 220 - age  # Maximum heart rate based on age
    
    for i in range(TOTAL_DATA_POINTS):
        data["time"].append(current_time + timedelta(minutes=i))
        hour = (i // DATA_POINTS_PER_HOUR) % 24
        
        # Activity and sleep states
        if 0 <= hour < 6:  # Sleeping (midnight to 6 AM)
            activity = 0
            sleep_state = random.choice([1, 2, 3])  # Light, deep, REM
            steps = 0
        elif 18 <= hour < 21:  # Active period (6 PM to 9 PM)
            activity = random.choice([1, 2])  # Light or vigorous
            sleep_state = 0
            steps = random.randint(10, 30) if activity == 1 else random.randint(30, 60)
        else:  # Resting
            activity = 0
            sleep_state = 0
            steps = random.randint(0, 3)
        
        steps_total += steps
        
        # Heart rate based on activity and user profile
        if sleep_state > 0:  # Sleeping
            hr = random.randint(45, 65) + (5 if smoking else 0)  # Smokers have slightly higher HR
        elif activity == 0:  # Resting awake
            hr = random.randint(60, 80) + (5 if smoking else 0)
        elif activity == 1:  # Light activity
            hr = random.randint(80, int(max_hr * 0.7))
        else:  # Vigorous activity
            hr = random.randint(int(max_hr * 0.7), int(max_hr * 0.9))
        hr = max(40, min(max_hr, hr + random.randint(-3, 3)))  # Add noise, cap at max HR
        
        # HRV (SDNN): Lower with age, smoking, or activity
        base_hrv = 50 - (age // 5) - (10 if smoking else 0)  # Age and smoking reduce HRV
        hrv = random.randint(max(15, base_hrv - 20), base_hrv) if activity > 0 else random.randint(base_hrv, base_hrv + 30)
        
        # SpO2: Lower during sleep or for smokers
        spo2 = random.randint(95, 99) - (2 if smoking else 0) if sleep_state == 0 else random.randint(90, 97) - (2 if smoking else 0)
        spo2 = max(85, min(100, spo2))  # Cap SpO2
        
        data["heart_rate"].append(hr)
        data["hrv_sdnn"].append(hrv)
        data["spo2"].append(spo2)
        data["steps"].append(steps)
        data["sleep"].append(sleep_state)
        data["activity"].append(activity)
    
    return data, user_profile

# Analyze data
def analyze_data(data):
    resting_hr = [hr for hr, act, slp in zip(data["heart_rate"], data["activity"], data["sleep"]) if act == 0 and slp == 0]
    avg_rhr = sum(resting_hr) / max(1, len(resting_hr)) if resting_hr else 60
    avg_hrv = sum(data["hrv_sdnn"]) / TOTAL_DATA_POINTS
    avg_spo2 = sum(data["spo2"]) / TOTAL_DATA_POINTS
    total_steps = sum(data["steps"])
    sleep_hours = sum(1 for s in data["sleep"] if s > 0) / DATA_POINTS_PER_HOUR
    
    return {
        "avg_rhr": avg_rhr,
        "avg_hrv": avg_hrv,
        "avg_spo2": avg_spo2,
        "total_steps": total_steps,
        "sleep_hours": sleep_hours
    }

# Assess heart disease risk with BMI
def assess_risk(stats, user_profile):
    risk_score = 0
    risk_factors = []
    
    # Calculate BMI
    bmi = user_profile["weight"] / ((user_profile["height"] / 100) ** 2)
    
    if stats["avg_rhr"] > 80:
        risk_score += 20
        risk_factors.append("High resting HR (>80 bpm)")
    if stats["avg_hrv"] < 25:
        risk_score += 20
        risk_factors.append("Low HRV (<25 ms)")
    if stats["avg_spo2"] < 92:
        risk_score += 20
        risk_factors.append("Low SpO2 (<92%)")
    if stats["total_steps"] < 5000:
        risk_score += 15
        risk_factors.append("Low activity (<5000 steps)")
    if stats["sleep_hours"] < 6:
        risk_score += 10
        risk_factors.append("Poor sleep (<6 hours)")
    if user_profile["age"] > 50:
        risk_score += 10
        risk_factors.append("Age > 50")
    if user_profile["smoking"]:
        risk_score += 20
        risk_factors.append("Smoking")
    if user_profile["family_history"]:
        risk_score += 15
        risk_factors.append("Family history")
    if bmi > 30:
        risk_score += 15
        risk_factors.append("Obesity (BMI > 30)")
    
    risk_level = "High" if risk_score >= 60 else "Moderate" if risk_score >= 30 else "Low"
    return risk_level, risk_score, risk_factors, bmi

# Generate plot
def generate_plot(data):
    plt.figure(figsize=(10, 6))
    plt.subplot(3, 1, 1)
    plt.plot(data["time"], data["heart_rate"], label="Heart Rate (bpm)")
    plt.ylabel("Heart Rate")
    plt.legend()
    
    plt.subplot(3, 1, 2)
    plt.plot(data["time"], data["spo2"], label="SpO2 (%)", color="orange")
    plt.ylabel("SpO2")
    plt.legend()
    
    plt.subplot(3, 1, 3)
    plt.plot(data["time"], data["steps"], label="Steps", color="green")
    plt.ylabel("Steps")
    plt.xlabel("Time")
    plt.legend()
    
    plt.tight_layout()
    plot_path = "simulation_plot.png"
    plt.savefig(plot_path)
    plt.close()
    return plot_path

# Main function for Gradio
def run_simulation(age, weight, height, gender, smoking, family_history):
    data, user_profile = simulate_wristband_data(age, weight, height, gender, smoking, family_history)
    stats = analyze_data(data)
    risk_level, risk_score, risk_factors, bmi = assess_risk(stats, user_profile)
    plot_path = generate_plot(data)
    
    summary = (
        f"Average Resting HR: {stats['avg_rhr']:.1f} bpm\n"
        f"Average HRV (SDNN): {stats['avg_hrv']:.1f} ms\n"
        f"Average SpO2: {stats['avg_spo2']:.1f}%\n"
        f"Total Steps: {stats['total_steps']}\n"
        f"Sleep Duration: {stats['sleep_hours']:.1f} hours\n"
        f"BMI: {bmi:.1f}"
    )
    
    risk_output = (
        f"Risk Level: {risk_level}\n"
        f"Risk Score: {risk_score}\n"
        f"Contributing Factors: {', '.join(risk_factors) if risk_factors else 'None'}"
    )
    
    return summary, risk_output, plot_path

# Gradio interface
with gr.Blocks(title="Smart Wristband Heart Disease Risk Simulator") as demo:
    gr.Markdown("# Smart Wristband Heart Disease Risk Simulator")
    gr.Markdown("Enter your profile to simulate 24 hours of data and assess heart disease risk.")
    
    with gr.Row():
        with gr.Column():
            age = gr.Slider(18, 100, value=45, label="Age (years)")
            weight = gr.Slider(40, 150, value=85, label="Weight (kg)")
            height = gr.Slider(140, 200, value=175, label="Height (cm)")
            gender = gr.Dropdown(["Male", "Female", "Other"], value="Male", label="Gender")
            smoking = gr.Checkbox(label="Smoking", value=False)
            family_history = gr.Checkbox(label="Family History of Heart Disease", value=False)
            submit_btn = gr.Button("Run Simulation")
        
        with gr.Column():
            summary_output = gr.Textbox(label="Simulation Summary")
            risk_output = gr.Textbox(label="Heart Disease Risk Assessment")
            plot_output = gr.Image(label="Data Visualization")
    
    submit_btn.click(
        fn=run_simulation,
        inputs=[age, weight, height, gender, smoking, family_history],
        outputs=[summary_output, risk_output, plot_output]
    )

demo.launch()