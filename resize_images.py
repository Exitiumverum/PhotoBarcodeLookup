from PIL import Image
import os

def resize_image(image_path, max_width=512, max_height=300):
    """
    Resize an image if it exceeds the maximum dimensions while maintaining aspect ratio.
    Converts all images to JPEG, filling transparency with white if needed.
    
    Args:
        image_path (str): Path to the image file
        max_width (int): Maximum allowed width
        max_height (int): Maximum allowed height
    
    Returns:
        bool: True if image was resized, False if no resize was needed
    """
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Get original dimensions
            width, height = img.size
            
            # Check if resize is needed
            if width <= max_width and height <= max_height:
                print(f"Image {image_path} is already within size limits ({width}x{height})")
                return False
            
            # Calculate new dimensions maintaining aspect ratio
            ratio = min(max_width/width, max_height/height)
            new_width = int(width * ratio)
            new_height = int(height * ratio)
            
            # Resize the image
            resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Convert to RGB if needed (fill transparency with white)
            if resized_img.mode in ("RGBA", "P"):
                background = Image.new("RGB", resized_img.size, (255, 255, 255))
                if resized_img.mode == "P":
                    resized_img = resized_img.convert("RGBA")
                background.paste(resized_img, mask=resized_img.split()[-1] if resized_img.mode == "RGBA" else None)
                resized_img = background
            else:
                resized_img = resized_img.convert("RGB")
            
            # Save as JPEG (overwrite original, change extension if needed)
            jpeg_path = os.path.splitext(image_path)[0] + ".jpg"
            resized_img.save(jpeg_path, format="JPEG", quality=95, optimize=True)
            if jpeg_path != image_path and os.path.exists(image_path):
                os.remove(image_path)
            print(f"Resized and converted {image_path} to {jpeg_path} from {width}x{height} to {new_width}x{new_height}")
            return True
            
    except Exception as e:
        print(f"Error processing {image_path}: {str(e)}")
        return False

def process_directory(directory_path):
    """
    Process all images in a directory.
    
    Args:
        directory_path (str): Path to the directory containing images
    """
    # Supported image formats
    image_extensions = ('.jpg', '.jpeg', '.png', '.webp')
    
    # Counter for processed images
    total_images = 0
    resized_images = 0
    
    # Process each file in the directory
    for filename in os.listdir(directory_path):
        if filename.lower().endswith(image_extensions):
            file_path = os.path.join(directory_path, filename)
            total_images += 1
            if resize_image(file_path):
                resized_images += 1
    
    print(f"\nProcessing complete!")
    print(f"Total images processed: {total_images}")
    print(f"Images resized/converted: {resized_images}")

if __name__ == "__main__":
    # Directory containing the images
    image_dir = "product_images"
    
    # Check if directory exists
    if not os.path.exists(image_dir):
        print(f"Error: Directory '{image_dir}' does not exist!")
    else:
        process_directory(image_dir) 