# Product Image Downloader

This script downloads product images using the Go UPC API based on barcodes and product numbers from an Excel file.

## Setup

1. Install the required dependencies:

```bash
pip install -r requirements.txt
```

2. Create a `.env` file in the same directory and add your Go UPC API key:

```
GO_UPC_API_KEY=your_api_key_here
```

3. Create an Excel file named `product_data.xlsx` with two columns:
   - `barcode`: The product barcode/UPC
   - `product_number`: The unique product number to use as the image filename

## Usage

1. Make sure your Excel file (`product_data.xlsx`) is in the same directory as the script
2. Run the script:

```bash
python download_product_images.py
```

The script will:

- Create a `product_images` directory if it doesn't exist
- Download images for each product in the Excel file
- Save images with the product number as the filename (e.g., `12345.jpg`)
- Show progress and results in the console

## Notes

- The script includes a 1-second delay between requests to avoid hitting API rate limits
- Images are saved in JPG format
- If an image can't be downloaded, the script will continue with the next product
- A summary of successful downloads will be shown at the end
# PhotoBarcodeLookup
