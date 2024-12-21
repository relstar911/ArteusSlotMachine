from PIL import Image
import os

# Create icons directory if it doesn't exist
if not os.path.exists('assets/icons'):
    os.makedirs('assets/icons')

# Open the PNG image
img = Image.open('assets/sprites/pokeballs/master.png')

# Convert and save as ICO
img.save('assets/icons/pokeball.ico', format='ICO')
