[app]
title = Stroke Risk Predictor
package.name = strokepredictor
package.domain = org.cardio

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,h5

version = 1.0.0

requirements = python3,kivy,tensorflow,numpy,h5py,requests

orientation = portrait
fullscreen = 0
android.permissions = INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
