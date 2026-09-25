[app]

# (str) Title of your application
title = Jippy Store

# (str) Package name
package.name = jippystore

# (str) Package domain (needed for android/ios packaging)
package.domain = com.jippystore.app

# (str) Source code where the main.py or app.py lives
source.dir = .

# (list) Source files to include (let buildozer handle extensions and our specific folders)
source.include_exts = py,png,jpg,jpeg,kv,atlas
source.include_patterns = assets/*,templates/*

# (str) Application versioning
version = 1.0

# (list) Application requirements
# Note: pymongo needs dnspython to parse mongodb+srv:// URLs
requirements = python3,kivy==2.3.0,requests,pymongo,dnspython

# (str) Supported orientations (landscape, sensor, portrait, etc.)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Main entry point script
source.filename = app.py

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (str) Target Android API (Play Store currently requires API 34)
android.api = 34

# (str) Minimum API your APK / AAB will support. API 24 is Android 7.0
android.minapi = 24

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data dir (True) or --dir public storage (False)
android.private_data = True

# (list) List of Android architectures to build for (Play store needs both 64 and 32 bit)
android.archs = arm64-v8a, armeabi-v7a

# (str) Build artifact format (.aab for Google Play Store, .apk for testing)
android.release_artifact = aab

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0
