import pygetwindow as gw

windows = gw.getAllTitles()
for title in windows:
    if title.strip():  # 过滤空标题
        print(f"窗口标题: {title}")
