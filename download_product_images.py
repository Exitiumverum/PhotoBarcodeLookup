import os
import pandas as pd
import requests
from dotenv import load_dotenv
import time
from pathlib import Path
from datetime import datetime

# Load environment variables
load_dotenv()

# Get API key from environment variable
GO_UPC_API_KEY = os.getenv('GO_UPC_API_KEY')
if not GO_UPC_API_KEY:
    raise ValueError("Please set GO_UPC_API_KEY in your .env file")

def create_image_directory():
    """Create a directory to store the downloaded images if it doesn't exist."""
    image_dir = Path("product_images")
    image_dir.mkdir(exist_ok=True)
    return image_dir

def download_product_image(barcode, product_number, image_dir):
    """Download product image using Go UPC API and save it with the product number as filename."""
    url = f"https://go-upc.com/api/v1/code/{barcode}?key={GO_UPC_API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if 'product' in data and 'imageUrl' in data['product']:
            image_url = data['product']['imageUrl']
            if image_url:
                # Download the image
                image_response = requests.get(image_url)
                image_response.raise_for_status()
                
                # Save the image with product number as filename
                image_path = image_dir / f"{product_number}.jpg"
                with open(image_path, 'wb') as f:
                    f.write(image_response.content)
                print(f"Successfully downloaded image for product {product_number}")
                return True, None
            else:
                print(f"No image URL found for product {product_number}")
                return False, "No image URL found"
        else:
            print(f"No product data found for barcode {barcode}")
            return False, "No product data found"
            
    except requests.exceptions.RequestException as e:
        print(f"Error downloading image for product {product_number}: {str(e)}")
        return False, str(e)

def create_failed_products_report(failed_products, timestamp):
    """Create an Excel file with failed products."""
    if not failed_products:
        print("\nNo failed products to report!")
        return
    
    # Create a DataFrame for failed products
    df_failed = pd.DataFrame(failed_products, columns=['barcode', 'product_number', 'reason'])
    
    # Create filename with timestamp
    report_filename = f"failed_products_{timestamp}.xlsx"
    
    # Save to Excel
    df_failed.to_excel(report_filename, index=False)
    print(f"\nFailed products report saved as: {report_filename}")

def main():
    # Create directory for images
    image_dir = create_image_directory()
    
    # Get current timestamp for the report file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Read the Excel file
    try:
        # Read Excel file, using the first two columns (A and B)
        df = pd.read_excel('PhotosList.xlsx', usecols=[0, 1], names=['barcode', 'product_number'])
    except FileNotFoundError:
        print("Error: PhotosList.xlsx not found. Please make sure the file exists in the current directory.")
        return
    
    # Remove any rows where either barcode or product_number is empty
    df = df.dropna(subset=['barcode', 'product_number'])
    
    # Convert barcode and product_number to strings and strip whitespace
    def clean_barcode(val):
        try:
            # Remove .0 if present (from float conversion)
            return str(int(float(val))).strip()
        except Exception:
            return str(val).strip()

    df['barcode'] = df['barcode'].apply(clean_barcode)
    df['product_number'] = df['product_number'].astype(str).str.strip()
    
    # List to store failed products
    failed_products = []
    
    # Download images for each product
    success_count = 0
    total_products = len(df)
    
    print(f"\nStarting download of {total_products} product images...")
    
    for index, row in df.iterrows():
        barcode = row['barcode']
        product_number = row['product_number']
        
        print(f"\nProcessing product {index + 1}/{total_products}")
        print(f"Barcode: {barcode}, Product Number: {product_number}")
        
        success, error_reason = download_product_image(barcode, product_number, image_dir)
        if success:
            success_count += 1
        else:
            # Add to failed products list
            failed_products.append([barcode, product_number, error_reason])
        
        # Add a small delay to avoid hitting API rate limits
        time.sleep(1)
    
    # Create report for failed products
    create_failed_products_report(failed_products, timestamp)
    
    print(f"\nDownload complete!")
    print(f"Successfully downloaded {success_count} out of {total_products} images")
    print(f"Failed to download {len(failed_products)} images")
    print(f"Images have been saved in the 'product_images' directory")

if __name__ == "__main__":
    main() 