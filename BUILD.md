# Building FindMyStray APK for Android

This guide explains how to build an APK package for the FindMyStray application to install on Android devices.

## Prerequisites

### For Linux (Recommended)

1. **Install Buildozer dependencies**:
```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev
```

2. **Install Cython and Buildozer**:
```bash
pip3 install --upgrade cython buildozer
```

### For macOS

1. **Install Homebrew** (if not installed):
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

2. **Install dependencies**:
```bash
brew install python@3.9 autoconf automake libtool pkg-config
brew install --cask android-sdk android-ndk
pip3 install --upgrade cython buildozer
```

### For Windows

Building Android APKs on Windows is challenging. We recommend:
1. Use **WSL2 (Windows Subsystem for Linux)** and follow Linux instructions
2. Use a cloud build service
3. Use a Linux virtual machine

## Build Process

### 1. Navigate to Project Directory

```bash
cd /path/to/FindMyStray
```

### 2. First-Time Setup

On the first build, Buildozer will download:
- Android SDK
- Android NDK
- Required Python packages
- App dependencies

This process can take 30-60 minutes depending on your internet connection.

### 3. Build Debug APK

For testing purposes, build a debug APK:

```bash
buildozer android debug
```

The APK will be generated in: `bin/findmystray-1.0.0-arm64-v8a-debug.apk`

### 4. Build Release APK (Optional)

For production/distribution:

```bash
buildozer android release
```

**Note**: Release APKs need to be signed. See "Signing Release APK" section below.

## Installing APK on Android Device

### Method 1: USB Connection (ADB)

1. **Enable Developer Options** on your Android device:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
   - Go back to Settings > Developer Options
   - Enable "USB Debugging"

2. **Connect device via USB** and run:
```bash
buildozer android deploy run
```

This will build, install, and run the app on your device.

### Method 2: Transfer APK File

1. **Locate the APK**:
```bash
ls bin/*.apk
```

2. **Transfer to phone**:
   - Email the APK to yourself
   - Use cloud storage (Google Drive, Dropbox)
   - Transfer via USB cable to phone storage

3. **Install on phone**:
   - Open the APK file on your phone
   - Allow installation from unknown sources if prompted
   - Follow installation prompts

## Signing Release APK

To sign a release APK for distribution:

### 1. Generate Keystore

```bash
keytool -genkey -v -keystore findmystray-release.keystore -alias findmystray -keyalg RSA -keysize 2048 -validity 10000
```

### 2. Add to buildozer.spec

Add these lines under the `[app]` section:

```ini
# (str) Path to the keystore for signing
android.release_artifact = apk
android.keystore = /path/to/findmystray-release.keystore
android.keystore_alias = findmystray
android.keystore_password = your_password
android.key_password = your_key_password
```

### 3. Build signed APK

```bash
buildozer android release
```

## Troubleshooting

### Build Fails

1. **Clean build directory**:
```bash
buildozer android clean
```

2. **Update buildozer**:
```bash
pip3 install --upgrade buildozer
```

3. **Check logs**:
Look for errors in `.buildozer/android/platform/build/dists/findmystray/build.log`

### App Crashes on Startup

1. Check Android logcat:
```bash
adb logcat | grep python
```

2. Verify all permissions are granted in Android settings

### GPS Not Working

- Ensure location permissions are granted
- Test on a real device (GPS doesn't work in emulators without configuration)

### Firebase Connection Issues

- Check internet connectivity
- Verify Firebase URL in main.py is correct
- Ensure Firebase Realtime Database rules allow read/write access

## Build Configuration

The `buildozer.spec` file contains all build settings:

- **Package name**: `org.findmystray.findmystray`
- **Version**: `1.0.0`
- **Minimum Android API**: 21 (Android 5.0)
- **Target Android API**: 33 (Android 13)
- **Architectures**: arm64-v8a, armeabi-v7a

### Required Permissions

The app requests:
- `INTERNET` - Firebase communication
- `ACCESS_FINE_LOCATION` - GPS location
- `ACCESS_COARSE_LOCATION` - Network location
- `CAMERA` - Photo capture
- `READ_EXTERNAL_STORAGE` - Access photos
- `WRITE_EXTERNAL_STORAGE` - Save photos

## Testing

### Debug vs Release Builds

- **Debug APK**: Unsigned, for testing only, larger file size
- **Release APK**: Signed, optimized, for distribution

### Test Checklist

- [ ] App launches successfully
- [ ] Language toggle works (English/Greek)
- [ ] Can submit a pet report
- [ ] Map loads and displays markers
- [ ] GPS location works
- [ ] Photo capture/upload works
- [ ] Firebase sync works
- [ ] All buttons and navigation work

## APK Size Optimization

To reduce APK size:

1. Remove unused architectures in buildozer.spec:
```ini
android.archs = arm64-v8a
```

2. Enable ProGuard (add to buildozer.spec):
```ini
android.add_aars =
android.gradle_dependencies =
p4a.branch = master
android.enable_androidx = True
```

## Automated Builds

For CI/CD pipelines:

```bash
# Install dependencies
pip install buildozer cython

# Accept Android SDK licenses automatically
export ANDROID_SDK_ROOT="$HOME/.buildozer/android/platform/android-sdk"
yes | buildozer android debug

# APK will be in bin/ directory
```

## Additional Resources

- [Buildozer Documentation](https://buildozer.readthedocs.io/)
- [Kivy Android Documentation](https://kivy.org/doc/stable/guide/packaging-android.html)
- [Python for Android](https://python-for-android.readthedocs.io/)

## Support

For build issues:
1. Check buildozer logs in `.buildozer/` directory
2. Review [Buildozer GitHub Issues](https://github.com/kivy/buildozer/issues)
3. Visit [Kivy Discord Community](https://chat.kivy.org/)

## Quick Build Command Reference

```bash
# Debug build
buildozer android debug

# Deploy to connected device
buildozer android debug deploy run

# Clean build
buildozer android clean

# Release build
buildozer android release

# View logs
adb logcat | grep python

# List connected devices
adb devices
```
