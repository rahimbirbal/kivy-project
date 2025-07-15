[app]
title = WarnaApp
package.name = warna_app
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3,kivy,opencv-python-headless,pandas,scikit-learn,joblib
orientation = portrait
osx.kivy_version = 2.2.1

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.permissions = CAMERA,INTERNET
android.minapi = 21
android.sdk = 24
android.ndk = 25b
android.ndk_path = 
android.sdk_path = 
