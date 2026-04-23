from PIL import Image
import os

png_path = r'C:\Users\user\.gemini\antigravity\brain\a4f74058-682b-4271-8220-1504896942a7\ox_icon_design_1775137311492.png'
ico_path = 'ox.ico'

if os.path.exists(png_path):
    img = Image.open(png_path)
    # Resize to standard icon size if necessary, or just save as ico
    icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]
    img.save(ico_path, sizes=icon_sizes)
    print(f"Icon saved to {ico_path}")
else:
    print(f"Error: PNG not found at {png_path}")
