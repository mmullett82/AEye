import cv2
import os
import time
import csv
import subprocess
from datetime import datetime
from skimage import color
from utils import config

# ---- Config ----
TARGET_SERIAL = "YLAF20221208V0"
BOX_SIZE = config.BOX_SIZE

# ---- Enhanced Camera Detection ----
def list_all_cameras():
    """List all available cameras with detailed info"""
    cameras = []
    print("Scanning for cameras...")
    
    # Check /dev/video* devices
    video_devices = []
    for i in range(20):  # Check more devices
        device_path = f"/dev/video{i}"
        if os.path.exists(device_path):
            video_devices.append(device_path)
            print(f"Found video device: {device_path}")
    
    # Test each device
    for device_path in video_devices:
        device_num = int(device_path.split('video')[1])
        try:
            cap = cv2.VideoCapture(device_num)
            if cap.isOpened():
                # Try to read a frame to verify it's working
                ret, frame = cap.read()
                if ret and frame is not None:
                    cameras.append({
                        'device': device_path,
                        'index': device_num,
                        'working': True,
                        'resolution': frame.shape[:2] if frame is not None else None
                    })
                    print(f"✓ Working camera found at {device_path}")
                else:
                    print(f"✗ Camera at {device_path} exists but can't capture frames")
            cap.release()
        except Exception as e:
            print(f"✗ Error testing {device_path}: {e}")
    
    return cameras

def get_camera_serial_v4l2(device_path):
    """Get camera serial using v4l2-ctl if available"""
    try:
        result = subprocess.run(['v4l2-ctl', '--device', device_path, '--info'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'Serial' in line or 'serial' in line:
                    return line.split(':')[-1].strip()
    except FileNotFoundError:
        print("v4l2-ctl not found - install v4l-utils for better camera info")
    except Exception as e:
        print(f"Error getting serial with v4l2-ctl: {e}")
    return None

def get_camera_serial_udev(device_path):
    """Get camera serial using udev if available"""
    try:
        result = subprocess.run(['udevadm', 'info', '--name', device_path], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if 'ID_SERIAL' in line:
                    return line.split('=')[-1].strip()
    except Exception as e:
        print(f"Error getting serial with udev: {e}")
    return None

def find_camera_by_serial(target_serial=None):
    """Enhanced camera finder with better detection"""
    cameras = list_all_cameras()
    
    if not cameras:
        print("No working cameras found!")
        return None
    
    print(f"\nFound {len(cameras)} working camera(s)")
    
    # If no target serial specified, return first working camera
    if not target_serial:
        print(f"No target serial specified, using first camera: {cameras[0]['device']}")
        return cameras[0]['device']
    
    # Try to find camera by serial
    for camera in cameras:
        device_path = camera['device']
        print(f"\nChecking {device_path} for serial {target_serial}...")
        
        # Try multiple methods to get serial
        serial = get_camera_serial_v4l2(device_path)
        if not serial:
            serial = get_camera_serial_udev(device_path)
        
        if serial:
            print(f"Found serial: {serial}")
            if target_serial in serial or serial in target_serial:
                print(f"✓ Serial match found! Using {device_path}")
                return device_path
        else:
            print("Could not determine serial number")
    
    # If no serial match found, ask user
    print(f"\nNo camera found with serial '{target_serial}'")
    print("Available cameras:")
    for i, camera in enumerate(cameras):
        print(f"{i}: {camera['device']} (resolution: {camera['resolution']})")
    
    try:
        choice = input(f"Enter camera number to use (0-{len(cameras)-1}) or 'q' to quit: ")
        if choice.lower() == 'q':
            return None
        choice = int(choice)
        if 0 <= choice < len(cameras):
            return cameras[choice]['device']
    except (ValueError, IndexError):
        pass
    
    print("Invalid choice, using first camera")
    return cameras[0]['device']

# ---- ROI Box Calculator ----
def get_roi_box(resolution, size):
    w, h = resolution
    margin_map = {
        "small": 0.375,   # 25% center box
        "medium": 0.25,   # 50% center box
        "large": 0.1      # 80% center box
    }
    margin = margin_map.get(size, 0.25)
    x1, x2 = int(w * margin), int(w * (1 - margin))
    y1, y2 = int(h * margin), int(h * (1 - margin))
    return x1, y1, x2, y2

# ---- Main Capture Function ----
def capture_and_log(sample_id, mode):
    print(f"Looking for camera with serial: {TARGET_SERIAL}")
    camera_path = find_camera_by_serial(TARGET_SERIAL)
    
    if not camera_path:
        print("No suitable camera found. Exiting.")
        return
    
    # Extract device number for OpenCV
    if '/dev/video' in camera_path:
        device_num = int(camera_path.split('video')[1])
    else:
        device_num = 0
    
    print(f"Using camera: {camera_path} (device {device_num})")
    
    cap = cv2.VideoCapture(device_num)
    if not cap.isOpened():
        raise RuntimeError(f"Could not open camera at {camera_path}")
    
    print(f"Capturing in '{BOX_SIZE}' mode... Press 'q' to capture.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame.")
            break
        
        x1, y1, x2, y2 = get_roi_box(frame.shape[:2], BOX_SIZE)
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.imshow("Live View (Press 'q' to capture)", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    cap.release()
    cv2.destroyAllWindows()
    
    # Crop to ROI & Convert to LAB
    roi = frame[y1:y2, x1:x2]
    lab_img = color.rgb2lab(roi)
    avg_lab = lab_img.reshape(-1, 3).mean(axis=0)
    L, A, B = [round(v, 2) for v in avg_lab]
    
    # Log Results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_file = f"data/logs/{mode}_log.csv"
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        if mode == "sample":
            writer.writerow([timestamp, sample_id, camera_path, L, A, B, "", "", ""])
        else:
            writer.writerow([timestamp, sample_id, camera_path, L, A, B])
    
    print(f"{mode.title()} logged: LAB = {{L}}, {{A}}, {{B}}")

# ---- Entry Point ----
if __name__ == "__main__":
    # First, list all cameras for debugging
    print("=== Camera Detection Debug ===")
    cameras = list_all_cameras()
    
    if not cameras:
        print("\n❌ No cameras detected!")
        print("Troubleshooting steps:")
        print("1. Check if camera is connected: lsusb")
        print("2. Check video devices: ls -la /dev/video*")
        print("3. Check Docker device mounting")
        exit(1)
    
    print(f"\n✅ Found {len(cameras)} working camera(s)")
    
    # Continue with normal operation
    mode = input("Enter mode ('master' or 'sample'): ").strip().lower()
    if mode not in ["master", "sample"]:
        print("Invalid mode.")
        exit()
    
    sample_id = input("Enter sample ID or color name: ").strip()
    capture_and_log(sample_id, mode)
