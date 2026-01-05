"""
Kivy-based Mobile App for Stroke Risk Prediction
Build with: buildozer android debug
"""

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from kivy.uix.image import Image

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

from tensorflow import keras
import numpy as np
import requests
import threading

# Set window size for mobile
Window.size = (400, 800)

class StrokePredictorApp(App):
    def build(self):
        self.title = '💓 Stroke Risk Predictor'
        self.model = None
        self.model_loaded = False
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title_label = Label(
            text='💓 Cardiovascular Stroke Prediction',
            size_hint_y=0.08,
            bold=True,
            font_size='18sp'
        )
        main_layout.add_widget(title_label)
        
        # Scrollable content area
        scroll = ScrollView(size_hint=(1, 0.8))
        form_layout = GridLayout(cols=2, spacing=10, size_hint_y=None, padding=10)
        form_layout.bind(minimum_height=form_layout.setter('height'))
        
        # Gender
        form_layout.add_widget(Label(text='Gender:', size_hint_y=None, height=40))
        self.gender = Spinner(
            text='Female',
            values=('Female', 'Male', 'Other'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.gender)
        
        # Age
        form_layout.add_widget(Label(text='Age:', size_hint_y=None, height=40))
        self.age = TextInput(
            hint_text='18-100',
            input_filter='int',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.age)
        
        # Hypertension
        form_layout.add_widget(Label(text='Hypertension:', size_hint_y=None, height=40))
        self.hypertension = Spinner(
            text='No',
            values=('No', 'Yes'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.hypertension)
        
        # Heart Disease
        form_layout.add_widget(Label(text='Heart Disease:', size_hint_y=None, height=40))
        self.heart_disease = Spinner(
            text='No',
            values=('No', 'Yes'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.heart_disease)
        
        # Average Glucose Level
        form_layout.add_widget(Label(text='Glucose (mg/dL):', size_hint_y=None, height=40))
        self.glucose = TextInput(
            hint_text='50-300',
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.glucose)
        
        # BMI
        form_layout.add_widget(Label(text='BMI:', size_hint_y=None, height=40))
        self.bmi = TextInput(
            hint_text='10-60',
            input_filter='float',
            multiline=False,
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.bmi)
        
        # Ever Married
        form_layout.add_widget(Label(text='Ever Married:', size_hint_y=None, height=40))
        self.married = Spinner(
            text='No',
            values=('No', 'Yes'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.married)
        
        # Work Type
        form_layout.add_widget(Label(text='Work Type:', size_hint_y=None, height=40))
        self.work_type = Spinner(
            text='Private Job',
            values=('Government Job', 'Private Job', 'Self-employed', 'Children', 'Never worked'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.work_type)
        
        # Residence Type
        form_layout.add_widget(Label(text='Residence:', size_hint_y=None, height=40))
        self.residence = Spinner(
            text='Urban',
            values=('Rural', 'Urban'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.residence)
        
        # Smoking Status
        form_layout.add_widget(Label(text='Smoking:', size_hint_y=None, height=40))
        self.smoking = Spinner(
            text='Never smoked',
            values=('Never smoked', 'Formerly smoked', 'Smokes', 'Unknown'),
            size_hint_y=None,
            height=40
        )
        form_layout.add_widget(self.smoking)
        
        scroll.add_widget(form_layout)
        main_layout.add_widget(scroll)
        
        # Predict Button
        predict_btn = Button(
            text='🔮 Predict Stroke Risk',
            size_hint_y=0.12,
            background_color=(0.2, 0.6, 0.8, 1)
        )
        predict_btn.bind(on_press=self.predict_risk)
        main_layout.add_widget(predict_btn)
        
        # Result Label
        self.result_label = Label(
            text='Enter your details and tap Predict',
            size_hint_y=0.08,
            color=(0.2, 0.2, 0.2, 1)
        )
        main_layout.add_widget(self.result_label)
        
        # Load model on app start
        self.load_model_async()
        
        return main_layout
    
    def load_model_async(self):
        """Load model in background thread"""
        thread = threading.Thread(target=self._load_model)
        thread.daemon = True
        thread.start()
    
    def _load_model(self):
        """Load the trained model"""
        try:
            self.result_label.text = '⏳ Loading model...'
            
            model_path = 'stroke_prediction_model.h5'
            
            # Download if not present
            if not os.path.exists(model_path):
                self.result_label.text = '📥 Downloading model...'
                url = 'https://github.com/VijayS735/Cardio_predict/raw/main/cardio_stroke_dnn_project-main/stroke_prediction_model.h5'
                response = requests.get(url, timeout=60)
                with open(model_path, 'wb') as f:
                    f.write(response.content)
            
            # Load model
            self.model = keras.models.load_model(model_path)
            self.model_loaded = True
            self.result_label.text = '✅ Ready to predict!'
        except Exception as e:
            self.result_label.text = f'❌ Error: {str(e)}'
    
    def predict_risk(self, instance):
        """Make stroke risk prediction"""
        if not self.model_loaded:
            self.result_label.text = '⏳ Model still loading...'
            return
        
        try:
            # Validate and get inputs
            try:
                age = float(self.age.text) / 100
            except:
                self.result_label.text = '❌ Invalid age'
                return
            
            try:
                glucose = float(self.glucose.text) / 300
            except:
                self.result_label.text = '❌ Invalid glucose'
                return
            
            try:
                bmi = float(self.bmi.text) / 60
            except:
                self.result_label.text = '❌ Invalid BMI'
                return
            
            # Convert categorical values
            gender_map = {'Female': 0, 'Male': 1, 'Other': 2}
            gender_val = gender_map[self.gender.text] / 2
            
            hypertension_val = 1 if self.hypertension.text == 'Yes' else 0
            heart_disease_val = 1 if self.heart_disease.text == 'Yes' else 0
            married_val = 1 if self.married.text == 'Yes' else 0
            
            work_map = {
                'Government Job': 0,
                'Private Job': 1,
                'Self-employed': 2,
                'Children': 3,
                'Never worked': 4
            }
            work_val = work_map[self.work_type.text] / 4
            
            residence_val = 1 if self.residence.text == 'Urban' else 0
            
            smoking_map = {
                'Formerly smoked': 0,
                'Never smoked': 1,
                'Smokes': 2,
                'Unknown': 3
            }
            smoking_val = smoking_map[self.smoking.text] / 3
            
            # Prepare input
            input_data = np.array([[
                gender_val, age, hypertension_val, heart_disease_val,
                glucose, bmi, married_val, work_val, residence_val, smoking_val
            ]])
            
            # Make prediction
            prediction = self.model.predict(input_data, verbose=0)
            prob_percent = prediction[0][0] * 100
            
            # Display result
            if prob_percent < 30:
                risk_level = '🟢 LOW RISK'
                color = (0.2, 0.8, 0.2, 1)
            elif prob_percent < 60:
                risk_level = '🟡 MODERATE RISK'
                color = (0.8, 0.8, 0.2, 1)
            else:
                risk_level = '🔴 HIGH RISK'
                color = (0.8, 0.2, 0.2, 1)
            
            self.result_label.text = f'{risk_level}\nProbability: {prob_percent:.1f}%'
            self.result_label.color = color
            
        except Exception as e:
            self.result_label.text = f'❌ Error: {str(e)}'
            self.result_label.color = (0.8, 0.2, 0.2, 1)

if __name__ == '__main__':
    StrokePredictorApp().run()
