from PIL import Image
import numpy as np

import pyautogui as _pg
img = _pg.screenshot()
img.save(r'C:\Users\STKRPNFAD-NCHQW\Desktop\game_current.png')
arr = np.array(img)

# Game area: small window at (50, 40) to (506, 172)
# But the actual game board might be smaller within this
# Use the whole game area
game_area = np.zeros_like(arr[:,:,0])
game_area[30:360, 0:520] = 1  # Game board in upper portion

# Food: red pixels (r > 150, g < 100, b < 100)
red_mask = (arr[:,:,0] > 150) & (arr[:,:,1] < 100) & (arr[:,:,2] < 100)
r_rows, r_cols = np.where(red_mask)
if len(r_rows) > 0:
    # Filter to game area only
    game_red_rows = r_rows[(r_rows >= 30) & (r_rows < 360)]
    game_red_cols = r_cols[(r_cols >= 0) & (r_cols < 520)]
    if len(game_red_rows) > 0:
        print(f'Food: ({game_red_cols.mean():.0f}, {game_red_rows.mean():.0f}), count: {len(game_red_rows)}')
    else:
        print('Food (in game area): not found')
else:
    print('No food found!')

# Snake - non-background green
bg_mask = (np.abs(arr[:,:,0].astype(int) - 196) < 25) & \
          (np.abs(arr[:,:,1].astype(int) - 204) < 25) & \
          (np.abs(arr[:,:,2].astype(int) - 34) < 25)
snake_mask = ((arr[:,:,1] > 80) & (arr[:,:,1] < 200) & \
              (arr[:,:,0] < 180) & (arr[:,:,2] < 180) & \
              ~bg_mask).astype(int) * game_area
snake_count = np.sum(snake_mask)
rows, cols = np.where(snake_mask)
print(f'Snake: {snake_count} pixels')
if len(rows) > 0:
    print(f'Snake center: ({cols.mean():.0f}, {rows.mean():.0f})')
    print(f'Snake bbox: x={cols.min()}-{cols.max()}, y={rows.min()}-{rows.max()}')
