[app]
title = PS5 Payload Manager
package.name = ps5payload
package.domain = com.mohammad.ps5payload

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,json

version = 1.0
requirements = python3,kivy,requests,urllib3

orientation = portrait
fullscreen = 0

# Android permissions required for downloading and sending payloads
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# Architecture for modern Android devices
android.archs = arm64-v8a, armeabi-v7a
android.api = 33
android.minapi = 21

# Fixes for headless GitHub Actions build (SDK license and modern branch)
android.accept_sdk_license = True
p4a.branch = master

[buildozer]
log_level = 2
warn_on_root = 1
