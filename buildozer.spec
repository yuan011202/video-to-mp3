[app]
title = 视频转MP3
package.name = videotomp3
package.domain = com.videotomp3

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,mp3,mp4
source.include_patterns = ffmpeg

version = 1.0

requirements = python3,kivy==2.1.0,pyjnius==1.6.1,android

orientation = portrait
fullscreen = 0

android.permissions = READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,READ_MEDIA_VIDEO,READ_MEDIA_AUDIO

android.api = 31
android.minapi = 21
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.allow_backup = True

[buildozer]
log_level = 2
warn_on_root = 1
android.accept_sdk_license = True