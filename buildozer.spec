[app]

# (str) Title of your application
title = Jippy Store

# (str) Package name
package.name = jippystore

# (str) Package domain (needed for android/ios packaging)
package.domain = com.jippystore.app

# (str) Source code where the main.py or app.py lives
source.dir = .

# (list) Source files to include (including kv files in templates)
source.include_exts = py,png,jpg,jpeg,kv,atlas

# (list) List of inclusions using pattern matching
source.include_patterns = templates/*.kv, assets/*

# (str) Application versioning
version = 0.1

# (list) Application requirements
# Note: Add all python modules used in app.py
requirements = python3,kivy,requests,pymongo,dnspython,urllib3,chardet,idna,certifi

# (str) Main entry point script
source.filename = app.py

# (list) Permissions
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# (str) Target Android API
android.api = 33
android.minapi = 21

# (str) Android NDK version
android.ndk = 25b

# (bool) Use --private data dir (True) or --dir public storage (False)
android.private_data = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (list) List of Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# (str) Build artifact format (.aab for Google Play Store)
android.release_artifact = aab

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (str) Path to build work dir
build_dir = ./.buildozer

# (str) Path to build output (where .aab file will be saved)
bin_dir = ./bin