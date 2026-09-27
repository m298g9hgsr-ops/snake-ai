from PIL import Image
import numpy as np

img = Image.open(r'C:\Users\STKRPNFAD-NCHQW\Desktop\game_check2.png')
arr = np.array(img)

# Check if game is paused - look for '暫停' overlay
# Pause overlay is dark/gray
center = arr[400:700, 500:1000]
dark = np.sum((center[:,:,0] < 30) & (center[:,:,1] < 30) & (center[:,:,2] < 30))
print(f'Dark center pixels: {dark}')

# Check for game over text - dark text in middle of screen
game_over_region = arr[450:550, 700:1100]
game_over_dark = np.sum((game_over_region[:,:,0] < 50) & (game_over_region[:,:,1] < 50) & (game_over_region[:,:,2] < 50))
print(f'Game over text dark: {game_over_dark}')

# Check sidebar for score
sidebar = arr[150:350, 1400:1920]
# Look for bright pixels in sidebar
bright = np.sum((sidebar[:,:,0] > 200) & (sidebar[:,:,1] > 200) & (sidebar[:,:,2] > 200))
print(f'White sidebar pixels: {bright}')

# Check if snake is actually moving - look at edges
# Snake head might be at a different location now
# Find the non-background, non-dark areas in the game
# Look at top-left corner of game board
top_left = arr[40:120, 50:120]
tl_dark = np.sum((top_left[:,:,0] < 30) & (top_left[:,:,1] < 30) & (top_left[:,:,2] < 30))
print(f'Top-left dark: {tl_dark}')

# The snake might have died - check if there's a game over message
# Look at the full screenshot for any text-like patterns
# Find text by looking for rows with both dark and light pixels
text_rows = 0
for y in range(0, 1080, 10):
    row = arr[y]
    has_dark = np.any(row < 50)
    has_light = np.any(row > 200)
    if has_dark and has_light:
        text_rows += 1
print(f'Text rows found: {text_rows}')
