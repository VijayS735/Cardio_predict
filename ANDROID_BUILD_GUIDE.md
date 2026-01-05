# Building Android App with Kivy

## Quick Start (Recommended)

### Option A: Use Your Web App on Mobile (Easiest - 5 minutes)
1. Open on your phone: https://cardiopredict-l4dazveqpfd43k4s8eruk4.streamlit.app/
2. Add to home screen (creates app icon)
3. Done! Works like a native app

---

## Option B: Build Native Android App with Kivy (Intermediate - 1-2 hours)

### Prerequisites:
- Windows/Mac/Linux
- Python 3.9+
- Java Development Kit (JDK)
- Android SDK

### Step 1: Install Buildozer

```bash
pip install buildozer cython
```

### Step 2: Reduce TensorFlow Size (Optional but Recommended)

TensorFlow is large. For production, convert to TFLite:

```python
# In your project directory
import tensorflow as tf

# Load original model
model = tf.keras.models.load_model('stroke_prediction_model.h5')

# Convert to TFLite
converter = tf.lite.TFLiteConverter.from_keras_model(model)
tflite_model = converter.convert()

# Save
with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

### Step 3: Configure Buildozer

Edit `buildozer.spec`:
```
[app]
title = Stroke Risk Predictor
package.name = strokepredictor
package.domain = org.cardio

requirements = python3,kivy,tensorflow,numpy,h5py,requests
```

### Step 4: Build APK

```bash
# For development/testing
buildozer android debug

# For release (requires keystore)
buildozer android release
```

### Step 5: Install on Device

```bash
# Connect Android phone via USB and enable Developer Mode
buildozer android debug install run
```

The APK file will be in `bin/` folder.

---

## Option C: Use Streamlit Sharing (Alternative)

Already done! Your app is at:
https://cardiopredict-l4dazveqpfd43k4s8eruk4.streamlit.app/

Works perfectly on mobile browsers.

---

## Option D: React Native (Production Grade - 2-4 weeks)

For a professional app with native feel:

```bash
npx create-expo-app StrokePrediction
cd StrokePrediction
npm install axios tensorflow.js
```

---

## File Structure

```
cardio_stroke_dnn_project-main/
├── app.py                          # Streamlit web app
├── main_kivy.py                    # Kivy mobile app
├── buildozer.spec                  # Build configuration
├── stroke_prediction_model.h5      # Model file
├── requirements.txt                # Python dependencies
├── MOBILE_APP_GUIDE.md            # This file
└── README.md
```

---

## Comparison Table

| Approach | Setup Time | Learning Curve | Distribution | Updates | Monetization |
|----------|-----------|----------------|--------------|---------|--------------|
| Web (Current) | Done | Easy | Via URL | Automatic | Ads/Freemium |
| Kivy Native | 2-4 hours | Medium | Google Play | Manual APK | Paid/Ads |
| React Native | 1-2 weeks | Hard | App Store | OTA Updates | Paid/Ads |
| Flutter | 1-2 weeks | Hard | App Store | OTA Updates | Paid/Ads |

---

## Troubleshooting

### TensorFlow Size Issue:
- Use TFLite (smaller)
- Or download model at runtime

### Build Fails:
- Update Java: `java -version`
- Update Android SDK
- Check Python 3.9+ installed

### App Crashes on Phone:
- Check logcat: `adb logcat`
- Test locally first: `python main_kivy.py`

---

## Recommended Path

1. **Right Now**: Use web app on mobile (100% working)
2. **This Week**: Build Kivy app for distribution
3. **Next Month**: Upload to Google Play Store

Your current setup is already serving mobile users! 🎉

---

## Commands Cheat Sheet

```bash
# Test locally
python main_kivy.py

# Build Android app
buildozer android debug

# Install on phone
buildozer android debug install run

# View phone logs
adb logcat | grep python

# Clean build files
buildozer android clean
```

---

## Support

For issues:
- Kivy: https://kivy.org/doc/stable/
- Buildozer: https://buildozer.readthedocs.io/
- TensorFlow Lite: https://www.tensorflow.org/lite

Happy coding! 🚀
