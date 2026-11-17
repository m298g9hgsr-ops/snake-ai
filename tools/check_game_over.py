from PIL import Image
import numpy as np

img = Image.open(r'C:\Users\STKRPNFAD-NCHQW\Desktop\game_after_key.png')
arr = np.array(img)

# Check edges of game board
# Top edge (y=40)
top = arr[40:41, 50:1270]  # 3D array: (1, 1220, 3)
top_non_bg = np.sum((np.abs(top[:,:,0].astype(int) - 196) >= 25) | 
                     (np.abs(top[:,:,1].astype(int) - 204) >= 25) | 
                     (np.abs(top[:,:,2].astype(int) - 34) >= 25))
# Bottom edge
bottom = arr[980:981, 50:1270]
bot_non_bg = np.sum((np.abs(bottom[:,:,0].astype(int) - 196) >= 25) | 
                     (np.abs(bottom[:,:,1].astype(int) - 204) >= 25) | 
                     (np.abs(bottom[:,:,2].astype(int) - 34) >= 25))
# Left edge
left = arr[40:981, 50:51]
left_non_bg = np.sum((np.abs(left[:,:,0].astype(int) - 196) >= 25) | 
                      (np.abs(left[:,:,1].astype(int) - 204) >= 25) | 
                      (np.abs(left[:,:,2].astype(int) - 34) >= 25))
# Right edge
right = arr[40:981, 1266:1267]
right_non_bg = np.sum((np.abs(right[:,:,0].astype(int) - 196) >= 25) | 
                       (np.abs(right[:,:,1].astype(int) - 204) >= 25) | 
                       (np.abs(right[:,:,2].astype(int) - 34) >= 25))

print(f'Top edge non-bg: {top_non_bg}')
print(f'Bottom edge non-bg: {bot_non_bg}')
print(f'Left edge non-bg: {left_non_bg}')
print(f'Right edge non-bg: {right_non_bg}')

# Check bottom area for restart/game over buttons
for y in [950, 960, 970]:
    for x in [300, 600, 900, 1100]:
        pixel = arr[y, x]
        print(f'({x},{y}): RGB=({pixel[0]:3d},{pixel[1]:3d},{pixel[2]:3d})')

# Check if there's a game over text anywhere in the screen
# Look for dark text on lighter background
# Scan for any "GAME OVER" text
dark_count = 0
for y in range(300, 700, 10):
    for x in range(600, 1200, 10):
        if arr[y, x].all() < 50:
            dark_count += 1
print(f'\nDark pixels in center area: {dark_count}')

# The snake is dead - check if there's a restart button
# Look at the bottom-left corner
for y in [950, 960, 970]:
    for x in [100, 200, 300, 400, 500]:
        pixel = arr[y, x]
        print(f'({x},{y}): RGB=({pixel[0]:3d},{pixel[1]:3d},{pixel[2]:3d})')
