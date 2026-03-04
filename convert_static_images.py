import os
from PIL import Image

def convert_to_webp(directory):
    for filename in os.listdir(directory):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            file_path = os.path.join(directory, filename)
            name, ext = os.path.splitext(filename)
            webp_path = os.path.join(directory, name + '.webp')
            
            if not os.path.exists(webp_path):
                try:
                    with Image.open(file_path) as img:
                        print(f"Converting {filename} to WebP...")
                        img.save(webp_path, 'WEBP', quality=80)
                        print(f"Success: {name}.webp")
                except Exception as e:
                    print(f"Error converting {filename}: {e}")
            else:
                print(f"Skipping {filename} (WebP already exists)")

if __name__ == "__main__":
    static_img_dir = r"c:\Users\LENOVO\Desktop\suarez_cauca\suarez\static\img"
    convert_to_webp(static_img_dir)
