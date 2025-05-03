import win32gui
import win32con
import win32api
import time
import random
import threading

TARGET_WINDOW_TITLE = "卡拉彼丘"
stop_flag = False

key_map = {
    'W': 0x57,
    'A': 0x41,
    'S': 0x53,
    'D': 0x44,
    'SPACE': 0x20
}

def find_window(title):
    def callback(hwnd, extra):
        if win32gui.IsWindowVisible(hwnd):
            window_text = win32gui.GetWindowText(hwnd)
            if title.lower() in window_text.lower():
                extra.append(hwnd)
    hwnds = []
    win32gui.EnumWindows(callback, hwnds)
    return hwnds[0] if hwnds else None

def send_key(hwnd, key_code, hold_time=0.1):
    win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, key_code, 0)
    time.sleep(hold_time)
    win32api.PostMessage(hwnd, win32con.WM_KEYUP, key_code, 0)

def auto_play(hwnd):
    global stop_flag
    print("挂机脚本已启动，输入 stop 回车可中止。")
    while not stop_flag:
        # 1. 随机移动方向
        direction = random.choice(['W', 'A', 'S', 'D'])
        duration = random.uniform(0.2, 1.2)
        print(f"移动方向：{direction} 持续时间：{duration:.2f}s")
        send_key(hwnd, key_map[direction], hold_time=duration)

        # 2. 偶尔跳跃
        if random.random() < 0.2:
            print("跳跃")
            send_key(hwnd, key_map['SPACE'], hold_time=0.1)

        # 3. 偶尔愣住不动
        if random.random() < 0.1:
            pause = random.uniform(0.5, 2)
            print(f"停顿：{pause:.2f}s")
            time.sleep(pause)

        # 4. 每次循环后小等待，防止频率过高
        time.sleep(random.uniform(0.1, 0.4))

    print("脚本已停止。")

def input_listener():
    global stop_flag
    while True:
        cmd = input()
        if cmd.strip().lower() == 'stop':
            stop_flag = True
            break

if __name__ == "__main__":
    hwnd = find_window(TARGET_WINDOW_TITLE)
    if hwnd is None:
        print("未找到目标窗口")
    else:
        print(f"找到窗口句柄: {hwnd}")
        threading.Thread(target=input_listener, daemon=True).start()
        auto_play(hwnd)
