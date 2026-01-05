import streamlit as st
import numpy as np
import h5py
from tensorflow import keras
import json
import warnings
warnings.filterwarnings('ignore')

# Load trained model with compatibility fix
def load_model_with_fix(model_path):
    """Load model and handle quantization_config compatibility issue"""
    try:
        return keras.models.load_model(model_path)
    except (TypeError, ValueError) as e:
        if "quantization_config" in str(e):
            # Remove quantization_config from the h5 file
            with h5py.File(model_path, 'r+') as f:
                if 'model_config' in f.attrs:
                    config_str = f.attrs['model_config']
                    if isinstance(config_str, bytes):
                        config_str = config_str.decode('utf-8')
                    config = json.loads(config_str)
                    
                    # Remove quantization_config from all layers
                    def remove_quantization(layer_config):
                        if isinstance(layer_config, dict):
                            if 'quantization_config' in layer_config:
                                del layer_config['quantization_config']
                            for key, value in layer_config.items():
                                if isinstance(value, (dict, list)):
                                    remove_quantization(value)
                        elif isinstance(layer_config, list):
                            for item in layer_config:
                                remove_quantization(item)
                    
                    remove_quantization(config)
                    f.attrs['model_config'] = json.dumps(config)
            
            return keras.models.load_model(model_path)
        else:
            raise

model = load_model_with_fix("stroke_prediction_model.h5")

st.title("💓 Cardiovascular Stroke Prediction")
st.write("Select patient details to assess stroke risk")

# ---------------- INPUTS (WORDS ONLY) ----------------
gender = st.selectbox("Gender", ["Female", "Male", "Other"])
gender_val = {"Female": 0, "Male": 1, "Other": 2}[gender]

age = st.number_input("Age", min_value=1, max_value=120, value=45)

hypertension = st.selectbox("Hypertension", ["No", "Yes"])
hypertension_val = {"No": 0, "Yes": 1}[hypertension]

heart_disease = st.selectbox("Heart Disease", ["No", "Yes"])
heart_disease_val = {"No": 0, "Yes": 1}[heart_disease]

avg_glucose_level = st.number_input(
    "Average Glucose Level (mg/dL)", min_value=50.0, max_value=300.0, value=95.0
)

bmi = st.number_input("BMI", min_value=10.0, max_value=60.0, value=24.0)

ever_married = st.selectbox("Ever Married", ["No", "Yes"])
ever_married_val = {"No": 0, "Yes": 1}[ever_married]

work_type = st.selectbox(
    "Work Type",
    ["Government Job", "Private Job", "Self-employed", "Children", "Never worked"]
)
work_type_val = {
    "Government Job": 0,
    "Private Job": 1,
    "Self-employed": 2,
    "Children": 3,
    "Never worked": 4
}[work_type]

residence = st.selectbox("Residence Type", ["Rural", "Urban"])
residence_val = {"Rural": 0, "Urban": 1}[residence]

smoking = st.selectbox(
    "Smoking Status",
    ["Never smoked", "Formerly smoked", "Smokes", "Unknown"]
)
smoking_val = {
    "Formerly smoked": 0,
    "Never smoked": 1,
    "Smokes": 2,
    "Unknown": 3
}[smoking]

# ---------------- PREDICTION ----------------
if st.button("Predict Stroke Risk"):

    # Normalize input data
    input_data = np.array([[ 
        gender_val / 2,
        age / 100,
        hypertension_val,
        heart_disease_val,
        avg_glucose_level / 300,
        bmi / 60,
        ever_married_val,
        work_type_val / 4,
        residence_val,
        smoking_val / 3
    ]])

    # Model prediction
    prediction = model.predict(input_data)
    prob_percent = prediction[0][0] * 100  # convert to percentage

    st.write(f"### Stroke Probability: **{prob_percent:.2f}%**")

    # -------- RULE-BASED OVERRIDE FOR CLEARLY HEALTHY CASES --------
    if (
        age < 50 and
        hypertension_val == 0 and
        heart_disease_val == 0 and
        avg_glucose_level < 110 and
        bmi < 25 and
        smoking == "Never smoked"
    ):
        st.success("🟢 Low Risk of Stroke (Normal)")
    else:
        # -------- SCIENTIFIC RISK BANDS --------
        if prob_percent < 30:
            st.success("🟢 Low Risk of Stroke (Normal)")
        elif prob_percent < 60:
            st.warning("🟡 Moderate Risk of Stroke (Borderline)")
        else:
            st.error("🔴 High Risk of Stroke")

# ---------------- FOOTER ----------------
st.markdown("---")
st.caption("⚠️ This prediction is for educational purposes only and not a medical diagnosis.")

