# 📱 Build Native Mobile App - Step by Step

## Which Platform Do You Want?

### Android (Google Play Store)
Best if you want to reach most Android users worldwide.

### iOS (Apple App Store)
Best if you want iPhone/iPad users. More complex setup.

### Both (Cross-Platform)
Use Flutter or React Native.

---

# 🟢 OPTION A: Android Native App with Kivy (Recommended & Easiest)

## Overview
- **Language:** Python (same as your project!)
- **Time to build:** 2-4 hours
- **File size:** ~500MB (includes TensorFlow)
- **Distribution:** Google Play Store
- **Monetization:** Ads, in-app purchases, or paid app

---

## STEP 1: Install Prerequisites (30 minutes - One Time Only)

### 1.1 Install Java Development Kit (JDK)

**Windows:**
```powershell
# Option A: Using Chocolatey (if installed)
choco install openjdk

# Option B: Manual download
# Download from: https://www.oracle.com/java/technologies/downloads/
# Install and note the installation path
```

**Verify installation:**
```powershell
java -version
javac -version
```

Should show something like: `java version "21.0.1"`

### 1.2 Install Android SDK

**Windows:**
1. Download Android Studio: https://developer.android.com/studio
2. Install Android Studio
3. Open Android Studio → SDK Manager
4. Install:
   - Android API 31 (minimum)
   - Build Tools 34.0.0
   - Android SDK Platform

**Or use command line:**
```powershell
choco install android-sdk
```

### 1.3 Set Environment Variables

**Windows (Important!):**

1. Press `Win + X` → Settings
2. Search "Environment Variables"
3. Click "Edit the system environment variables"
4. Click "Environment Variables" button
5. Click "New" and add:

```
Variable Name:  JAVA_HOME
Variable Value: C:\Program Files\Java\jdk-21
```

```
Variable Name:  ANDROID_HOME
Variable Value: C:\Users\{YourUsername}\AppData\Local\Android\Sdk
```

6. Click OK, then restart PowerShell/Command Prompt

**Verify:**
```powershell
echo $env:JAVA_HOME
echo $env:ANDROID_HOME
```

### 1.4 Install Buildozer and Dependencies

```powershell
pip install buildozer cython numpy
```

---

## STEP 2: Prepare Your Project (5 minutes)

Navigate to your project:
```powershell
cd C:\Users\vijay\Downloads\cardio_stroke_dnn_project-main\cardio_stroke_dnn_project-main
```

Check that you have these files:
```
main_kivy.py                    ← Kivy app code
buildozer.spec                  ← Build configuration
stroke_prediction_model.h5      ← Your trained model
requirements.txt                ← Python dependencies
```

---

## STEP 3: Build the APK (30-45 minutes)

### First Time Build (Longer)

```powershell
cd C:\Users\vijay\Downloads\cardio_stroke_dnn_project-main\cardio_stroke_dnn_project-main

buildozer android debug
```

**What happens:**
1. Downloads Android SDK tools (~1-2 GB)
2. Compiles Python with Cython
3. Packages everything into APK
4. Creates `bin/` folder with APK file

**Result:** `bin/strokepredictor-1.0.0-debug.apk`

### Troubleshooting Build Errors

**Error: "Unable to find android.jar"**
```powershell
buildozer android clean
buildozer android debug
```

**Error: "Could not find Java"**
- Check JAVA_HOME is set correctly
- Restart terminal after setting environment variables

**Error: "TensorFlow wheel not found"**
- Buildozer will download automatically
- First build takes longer (~45 min)

---

## STEP 4: Install on Android Phone (10 minutes)

### Prerequisites
1. Android phone (Android 7.0 or higher)
2. USB cable
3. Developer Mode enabled

### Enable Developer Mode

On your Android phone:
1. Settings → About Phone
2. Tap "Build Number" 7 times
3. Settings → Developer Options → USB Debugging ON

### Install APK

```powershell
# Connect phone via USB

# Check if phone connected
buildozer android install

# Or manually install the APK
cd C:\Users\vijay\Downloads\cardio_stroke_dnn_project-main\cardio_stroke_dnn_project-main\bin
adb install strokepredictor-1.0.0-debug.apk
```

### Run App

```powershell
buildozer android debug install run
```

**Your app will launch automatically on the phone!**

---

## STEP 5: Test the App (5 minutes)

1. **Check it loaded:**
   - App icon "Stroke Risk Predictor" appears
   - Opens without errors

2. **Test predictions:**
   - Fill in sample patient data
   - Tap "Predict" button
   - See stroke risk result

3. **Common issues:**
   - Model downloading on first run (takes 1-2 minutes)
   - Check phone logs: `adb logcat | grep python`

---

## STEP 6: Optimize Before Releasing (Optional but Recommended)

### Reduce APK Size

Your current APK is ~500MB (mostly TensorFlow). Reduce it:

**Option A: Use TensorFlow Lite (Recommended)**

```python
# Run this ONCE to convert model
import tensorflow as tf

model = tf.keras.models.load_model('stroke_prediction_model.h5')
converter = tf.lite.TFLiteConverter.from_keras_model(model)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
tflite_model = converter.convert()

with open('model.tflite', 'wb') as f:
    f.write(tflite_model)
```

Benefits: 80% smaller, faster, same accuracy

**Option B: Download Model at Runtime**

Already implemented! Your app downloads from GitHub on first run.

---

## STEP 7: Create Release Version (For App Store)

### Generate Keystore (Sign APK)

```powershell
keytool -genkey -v -keystore my-release-key.jks `
  -keyalg RSA -keysize 2048 -validity 10000 `
  -alias alias_name
```

Answer the prompts:
```
Keystore password: (create one)
First/Last name: Your Name
Organization: Your Company
Country: US
```

### Build Release APK

```powershell
buildozer android release
```

### Sign Release APK

```powershell
jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 `
  -keystore my-release-key.jks `
  bin/strokepredictor-1.0.0-release-unsigned.apk `
  alias_name
```

Result: `bin/strokepredictor-1.0.0-release.apk`

This is ready for Google Play Store!

---

## STEP 8: Upload to Google Play Store (1-2 days review)

### Requirements
- Google Play Developer Account ($25 one-time)
- App signing certificate
- App screenshots & description

### Steps
1. Go to: https://play.google.com/console
2. Create new app
3. Fill in app details:
   - App name: "Stroke Risk Predictor"
   - Category: Medical/Health & Fitness
   - Content rating form
4. Upload APK (release version)
5. Add screenshots from your phone
6. Add description & pricing
7. Submit for review (takes 2-4 hours usually)

---

## 🟦 OPTION B: iOS App (Apple App Store)

More complex than Android.

### Requirements
- Mac computer (not Windows/Linux)
- iOS Developer Account ($99/year)
- Xcode installed

### Using BeeWare (Easier Alternative)

```powershell
pip install briefcase
briefcase new
```

### Or Use Flutter (Cross-Platform)

Covers both iOS and Android with one codebase.

```bash
flutter create stroke_prediction_app
# Add stroke prediction logic
# Deploy to iOS + Android simultaneously
```

**Time:** 2-4 weeks
**Best for:** Professional apps

---

## 🌈 OPTION C: Cross-Platform with Flutter (Best Long-Term)

Build once, run on iOS + Android + Web!

### Setup

```bash
# Install Flutter: https://flutter.dev/docs/get-started/install
flutter create stroke_prediction_app
cd stroke_prediction_app
```

### Structure

```
lib/
├── main.dart                    # App entry point
├── models/
│   └── prediction_model.dart   # TensorFlow Lite model
└── screens/
    └── prediction_screen.dart  # UI
```

### Basic Example

```dart
import 'package:flutter/material.dart';
import 'package:tflite_flutter/tflite_flutter.dart';

void main() => runApp(StrokeApp());

class StrokeApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      home: StrokePredictionScreen(),
    );
  }
}

class StrokePredictionScreen extends StatefulWidget {
  @override
  _StrokePredictionScreenState createState() => _StrokePredictionScreenState();
}

class _StrokePredictionScreenState extends State<StrokePredictionScreen> {
  late Interpreter interpreter;
  
  @override
  void initState() {
    super.initState();
    loadModel();
  }
  
  Future<void> loadModel() async {
    interpreter = await Interpreter.fromAsset('model.tflite');
  }
  
  void predictStroke() {
    // Call interpreter.run() with input
  }
  
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Stroke Risk Prediction')),
      body: Center(
        child: Column(
          children: [
            TextField(hint: 'Age'),
            TextField(hint: 'Glucose Level'),
            ElevatedButton(
              onPressed: predictStroke,
              child: Text('Predict'),
            ),
          ],
        ),
      ),
    );
  }
}
```

### Deploy

```bash
flutter build apk          # Android
flutter build ios          # iOS (requires Mac)
```

---

## 📊 COMPARISON TABLE

| Feature | Kivy | Flutter | React Native |
|---------|------|---------|--------------|
| **Language** | Python | Dart | JavaScript |
| **Setup Time** | 30 min | 1-2 hours | 1-2 hours |
| **Build Time** | 30-45 min | 15-20 min | 10-15 min |
| **iOS Support** | ❌ | ✅ | ✅ |
| **Android Support** | ✅ | ✅ | ✅ |
| **Learning Curve** | Easy | Medium | Medium |
| **Community** | Small | Large | Large |
| **Performance** | Good | Excellent | Very Good |
| **App Store Ready** | ✅ Yes | ✅ Yes | ✅ Yes |

---

## ⏱️ TIMELINE SUMMARY

### This Week
- ✅ Install Java + Android SDK (30 min)
- ✅ Build APK with Kivy (45 min)
- ✅ Test on Android phone (10 min)

### Next Week
- ✅ Optimize APK size (1-2 hours)
- ✅ Create release version (30 min)
- ✅ Test thoroughly

### This Month
- ✅ Create Google Play account ($25)
- ✅ Upload to Play Store (30 min)
- ✅ Wait for review (2-4 hours)
- ✅ App goes live! 🎉

---

## 🆘 TROUBLESHOOTING

### Q: App crashes on launch
**A:** Check logcat:
```powershell
adb logcat | grep python
```

### Q: Model takes too long to load
**A:** Convert to TFLite (80% smaller, faster)

### Q: APK too large
**A:** Use TFLite or split APK by architecture

### Q: Can't find Java/Android SDK
**A:** Verify environment variables are set:
```powershell
echo $env:JAVA_HOME
echo $env:ANDROID_HOME
```

### Q: Build fails on first attempt
**A:** Normal! First build downloads 1-2 GB. Try again:
```powershell
buildozer android clean
buildozer android debug
```

---

## 🎉 NEXT STEPS

1. **Install prerequisites** (30 minutes)
2. **Build APK** (45 minutes)
3. **Test on phone** (10 minutes)
4. **Celebrate!** 🎊

You now have a native mobile app!

---

## 📚 RESOURCES

- **Kivy Docs**: https://kivy.org/doc/stable/
- **Buildozer**: https://buildozer.readthedocs.io/
- **Flutter**: https://flutter.dev/
- **Android Studio**: https://developer.android.com/studio
- **Google Play Console**: https://play.google.com/console

---

**Your project is ready for native mobile deployment!** 🚀
