"""
貪食蛇3310 - 智能避牆自動化 (螺旋導航)
策略: 左→下→右→上 螺旋遍歷，避免撞牆
"""
import ctypes, time, numpy as np, pyautogui, subprocess
from PIL import Image

user32 = ctypes.windll.user32
VK_LEFT, VK_DOWN, VK_RIGHT, VK_UP = 0x25, 0x28, 0x27, 0x26
GAME_ID = "57365.3310_0bde4r8renxae"

def find_game():
    return user32.FindWindowW(None, '貪食蛇3310')

def set_foreground(hwnd):
    """Bring window to foreground and keep it visible."""
    if not hwnd: return False
    thread_id = user32.GetWindowThreadProcessId(hwnd, None)
    fg_id = user32.GetWindowThreadProcessId(user32.GetForegroundWindow(), None)
    try: user32.AttachThreadInput(thread_id, fg_id, True)
    except: pass
    user32.SetForegroundWindow(hwnd)
    user32.BringWindowToTop(hwnd)
    time.sleep(0.2)
    try: user32.AttachThreadInput(thread_id, fg_id, False)
    except: pass
    return True

def resize_window(hwnd, width=500, height=880):
    """Resize and center the game window on screen."""
    screen_w = user32.GetSystemMetrics(0)
    screen_h = user32.GetSystemMetrics(1)
    x = (screen_w - width) // 2
    y = (screen_h - height) // 2
    user32.SetWindowPos(hwnd, None, x, y, width, height, 0x0040 | 0x0002)
    time.sleep(0.2)
    return True

def send_key(vk):
    """Send key via keybd_event (global input) for UWP compatibility."""
    # Click game area to ensure focus
    pyautogui.click(300, 300)
    time.sleep(0.05)
    user32.keybd_event(vk, 0, 0, 0)
    time.sleep(0.03)
    user32.keybd_event(vk, 0, 2, 0)
    time.sleep(0.05)
    # Click D-pad area to trigger input
    pyautogui.click(210, 275)
    time.sleep(0.05)

def click_dpad(direction='left'):
    if direction == 'left':   pyautogui.click(160, 275)
    elif direction == 'down': pyautogui.click(210, 320)
    elif direction == 'right':pyautogui.click(260, 275)
    elif direction == 'up':   pyautogui.click(210, 230)
    time.sleep(0.2)

def take_screenshot(path):
    img = np.array(pyautogui.screenshot())[30:360, 0:520]
    Image.fromarray(img).save(path)

def get_snake_state():
    venv_python = r'C:\Users\STKRPNFAD-NCHQW\AppData\Local\hermes\installs\4ae13c26679c192f\environments\acf03d9a2a2c4d018f733a48e918c365\venv\Scripts\python'
    try:
        r = subprocess.run(
            [venv_python, 'check_state.py'],
            capture_output=True, text=True, timeout=10,
            cwd=r'C:\Users\STKRPNFAD-NCHQW\Desktop'
        )
        return r.stdout.strip()
    except Exception as e:
        return f"Error: {e}"

def restart_game():
    """Restart the game via shell:AppsFolder."""
    global GAME_ID
    try:
        subprocess.run(
            ['powershell', '-Command',
             f'Stop-Process -Name "貪食蛇3310" -Force; '
             f'Start-Process shell:AppsFolder\\{GAME_ID}'],
            capture_output=True, timeout=10
        )
        time.sleep(3)
        hwnd = find_game()
        if hwnd:
            set_foreground(hwnd)
            resize_window(hwnd, 500, 880)
            print(f"遊戲重啟成功: {hwnd}")
            return hwnd
    except Exception as e:
        print(f"重啟失敗: {e}")
    return None

def main():
    hwnd = find_game()
    if not hwnd:
        print("ERROR: Game not found!")
        return
    print(f"Game found: {hwnd}")
    set_foreground(hwnd)
    resize_window(hwnd, 500, 880)
    time.sleep(0.3)
    
    # Save initial screenshot for check_state.py
    take_screenshot(r'C:\Users\STKRPNFAD-NCHQW\Desktop\game_fresh3.png')
    time.sleep(0.5)
    click_dpad('left')
    time.sleep(0.5)
    
    print("蛇3310 螺旋導航啟動")
    print("策略: 左->下->右->上 避牆")
    print("Ctrl+C to stop")
    
    # Expanding spiral
    n = 8
    seq = [(VK_LEFT, n), (VK_DOWN, n), (VK_RIGHT, n+1), (VK_UP, n+1)]
    seq_idx = 0
    
    try:
        while True:
            vk, steps = seq[seq_idx % 4]
            dir_name = {VK_LEFT:'左', VK_DOWN:'下', VK_RIGHT:'右', VK_UP:'上'}[vk]
            
            for _ in range(steps):
                send_key(vk)
                click_dpad({VK_LEFT:'left', VK_DOWN:'down', VK_RIGHT:'right', VK_UP:'up'}[vk])
                time.sleep(0.08)
            
            state = get_snake_state()
            print(f"{dir_name} {steps}步 | {state}")
            
            if 'Snake: 0 pixels' in state or 'Error' in state:
                print("蛇撞牆或偵測錯誤！重新啟動遊戲...")
                restart_game()
                continue
            
            seq_idx += 1
            if seq_idx % 4 == 0:
                n += 1
                
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == '__main__':
    main()
