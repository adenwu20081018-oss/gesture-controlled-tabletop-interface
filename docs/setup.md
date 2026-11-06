# Gesture-Controlled Tabletop Interface — Windows setup

### 1. Prerequisites

- **JDK 17**, with `java` and `javac` available in PowerShell.
- **64-bit Python 3.12**, accessible through `py -3.12`.
- A built-in webcam for gesture practice; an Arduino is optional for running the game.

Download/extract or clone this repository, then open PowerShell **inside the repository root**. Keep that working directory when running Java: the original game loads PNG/WAV files from the assets/ folder relative to the root.

```powershell
java -version
javac -version
py -3.12 --version
```

### 2. Set up vision

```powershell
py -3.12 -m venv computer-vision\.venv
.\computer-vision\.venv\Scripts\python.exe -m pip install -r computer-vision\requirements.txt
.\computer-vision\.venv\Scripts\python.exe -m pip check
.\computer-vision\.venv\Scripts\python.exe .\computer-vision\main.py --download-model
```

The model download is an explicit setup step; subsequent tracking uses the local model. The environment, model and camera-specific calibration files are excluded from Git. Use the pinned OpenCV-contrib distribution rather than installing a second package that also provides `cv2`.

### 3. Build and launch the game

```powershell
.\build-phase7a.ps1
java -cp 'build-phase5b2;arduino\java\lib\jSerialComm-2.11.4.jar' groupDGuessWho.Main --presentation --window-width 1000 --window-height 625 --viewport-fit stretch
```

The build uses `javac`, not Maven or Gradle. It downloads and verifies the pinned jSerialComm JAR when needed. The existing output directory is named `build-phase5b2`; the Phase 7A launcher intentionally reuses it. If Windows blocks the local build script, use `powershell -NoProfile -ExecutionPolicy Bypass -File .\build-phase7a.ps1` for that invocation only.

### 4. Connect gestures

Leave Java running. In a second PowerShell terminal at the same repository root:

```powershell
.\computer-vision\.venv\Scripts\python.exe .\computer-vision\main.py --camera 0 --width 640 --height 480 --connect-java --calibrate --calibration-file .\computer-vision\calibration-laptop-practice.json --viewport-width 1280 --viewport-height 720 --java-fit stretch
```

In the camera preview, click four corners in **top-left → top-right → bottom-right → bottom-left** order. For a laptop-facing webcam, choose a reachable rectangle in the image as a virtual input surface; the camera does not need to see the laptop screen. Open your fingers to arm detection, position the fingertip, then pinch and release. Press **S** to save calibration or **C** to recalibrate; **Q** exits the tracker.

Follow the [projector-ready setup guide](projector-setup.md) for camera selection, alignment checks, Windows Extend mode and recalibration after physically moving a projected image.

## Optional LED feedback

Upload the [Mega sketch](arduino-setup.md), close Arduino IDE Serial Monitor and append `--arduino-port COM5` to the Java command above. Replace COM5 with your board's port. Leave this option off for software-only use.

Use the mouse to advance through the introduction. Then move your fingertip in the calibrated area, pinch and release to select. Recheck alignment after changing the setup. The buzzer and projector are not required.
