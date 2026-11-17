# Snake AI — 貪食蛇 3310 自動化

用 Python 鍵盤自動化玩 Nokia 3310 風格貪食蛇（HTML5 網頁版），外加一個可直接玩的網頁遊戲。

## 檔案說明

| 檔案 | 說明 |
|---|---|
| `snake_ai.html` | 可直接玩的貪食蛇網頁版（瀏覽器打開即玩） |
| `snake_ai.py` | **純鍵盤操控**自動化 — 透過 Windows API 送方向鍵，不碰滑鼠 |
| `snake_continue.py` | 進階版：螢幕截圖辨識 + 螺旋導航避牆策略 |
| `tools/check_state.py` / `check_game.py` / `check_game_over.py` | 遊戲狀態檢查/除錯小工具 |

## 使用方式

```bash
# 1. 瀏覽器開啟 snake_ai.html，把遊戲視窗切到前景
# 2. 執行自動化（需要 pyautogui + Pillow）
pip install pyautogui pillow numpy
python snake_ai.py        # 純鍵盤模式
python snake_continue.py  # 截圖辨識 + 螺旋導航模式
```

> 自動化透過 `ctypes` 對遊戲視窗送虛擬按鍵（`GAME_ID` 對應視窗標題），遊戲視窗需在前景。

## 除錯工具

`tools/` 底下的 `check_*.py` 用來讀取目前遊戲狀態（蛇的位置、遊戲是否結束），
寫新策略時先用它們確認畫面判讀是否正確。
