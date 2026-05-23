[app]

# (str) Title of your application
title = Floppy Bird

# (str) Package name
package.name = floppybird

# (str) Package domain (needed for android/ios packaging)
package.domain = org.taguinesdev

# (source.dir) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,ogg

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = .git,.github,.venv,__pycache__,bin,.buildozer

# (list) List of exclusions using pattern matching
#source.exclude_patterns = license,images/*/*.kv

# (str) Application versioning (method 1)
# version = 0.1

# (str) Application versioning (method 2)
version.regex = __version__ = ['"](.*)['"]
version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy

# (str) Supported orientation (landscape, sensorLandscape, portrait or sensorPortrait)
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_SERVICE [,NAME2:ENTRYPOINT_TO_SERVICE2] ...

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 1

# (string) Presentation mode to use on android
# android.window = picture-in-picture

# (bool) Indicate if the application should be portrait
# android.portrait = True

# (bool) Indicate if the application should be landscape
# android.landscape = False

# (list) Permissions
# android.permissions =

# (int) Target Android API, should be as high as possible.
android.api = 31

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android SDK version to use
# android.sdk is deprecated in current Buildozer and ignored.
# android.sdk = 31

# (str) Android NDK version to use
android.ndk = 25b

# (bool) Use --private data storage (True) or --dir public storage (False)
#android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
# android.theme = "@android:style/Theme.NoTitleBar"

# (bool) Copy library instead of making a libpymodules.so
#android.copy_libs = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.archs = arm64-v8a,armeabi-v7a

# (int) overrides automatic versionCode generation in buildozer.spec
# android.version_code = 1

# (list) Pattern to whitelist for the whole project
#android.whitelist = lib-dynload/termios.so

# (bool) enables Android auto backup & restore. Disable with android.allow_backup = False
android.allow_backup = True

# (str) XML file for custom backup scheme. See the documentation for details.
# android.backup_schemes = @xml/backup_scheme

# (str) If you need to insert Java code into the android.app.Activity class, set this value to the name of the Java class.
# android.add_src =

# (list) Pattern to match allowed java classes in the generated java code.
# this is only used in API 19+, let empty to prevent all adds, string * is not supported
#android.allowed_classes = android/webkit/WebView

# (bool) Add java code to generate Play Store api key "android.app.key_alias" from "android.keystore_alias"
#android.meta_data_base64 = False

# (str) Should be a reference to original file followed by a colon and the string to search (java key in .props, ie Value::Object)
#android.gradle_dependencies =

# (list) add java classes from any .jar file in libs folder
#android.add_jar = 

# (str) Filename of OUYA Console icon. It must be a 732x412 png image.
#android.ouya_icon_filename = %(source.dir)s/data/ouya_icon.png

# (str) XML file for custom backup scheme. See the documentation for details.
# android.backup_schemes = @xml/backup_scheme

# (bool) Enable AndroidX support. Enable with android.enable_androidx = True
android.enable_androidx = True

# (bool) Enable AndroidX support in Gradle dependencies.
# Note: this require to use at least buildozer > 1.30.0
android.gradle_dependencies = androidx.appcompat:appcompat:1.3.1

# (bool) Add support for Android Auto
# android.add_android_auto = False

#
# Python for android (p4a) specific
#

# (str) python for android URL, defaults to the value you see here
# Leave empty to disable it
#p4a.url = https://github.com/kivy/python-for-android/releases/download/develop/

# (str) python for android branch to use, defaults to the toolchain default.
# Using the default is generally more stable than pinning this project to a
# moving development branch.
# p4a.branch =

# (str) python for android directory (if empty, it will be automatically cloned from p4a.url)
#p4a.dir = %(cache_dir)s/python-for-android

# (list) python for android whitelist to use
#p4a.whitelist = lib-dynload/ossaudiodev.so

# (bool) python for android should logcat output be printed to console
#p4a.logcat_level = 2

# (int) port number to specify an explicit --port= p4a argument (eg for bootstrap flask)
#p4a.port = 5037

#
# iOS specific
#

# (bool) should we create a certificate for codesigning?
# Keychain certificates are safer than a self signed cert.
# Leave blank in git and configure signing on the macOS builder or in Xcode.
ios.codesign_certificate =

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning upon request for android permission (debatable, google is waiting)
# Can be 0 or 1 (0 = silent, 1 = verbose)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning upon request for android permission
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
# bin_dir = ./bin
