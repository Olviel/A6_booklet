# A6_booklet

A6 Booklet Creator
Overview
This Python script generates a booklet from a set of A6-sized images. The script arranges the images on A4-sized pages, suitable for printing and folding into a booklet format. The booklet pages are then saved as individual PDF files and optionally merged into a single PDF file. 

Production steps 
1. Print the booklet.pdf doublesided, along the short edge. 
2. Cut the document in half along the long side.
3. Stack the right half in the left half.
4. Optional: staple.
5. Fold.

Requirements
Python 3
Pillow (PIL Fork)
PyPDF2
Installation
Ensure you have Python installed on your system. You can download it from python.org.

Install the required Python packages using pip:

bash
Copy code
pip install pillow
pip install PyPDF2
Usage

To use the script, place your A6 images in a specified input folder and define an output folder for the generated PDF files. The image files should be named in the format 1.png, 1.png, 2.png, 2.png, ..., xx.png.

Clone the repository or download the functions.py script.
Prepare your images and place them in the input folder.
Set the folder_path to your input folder path.
Set the output_path to your desired output folder path.
Run the script:
python
Copy code
from functions import *

# Define the paths
folder_path = 'path/to/your/input/folder'  # Update with the correct folder path
output_path = 'path/to/your/output/folder'  # Output file path

# Create the booklet
create_booklet(folder_path, output_path)
The script will process the images and create individual PDF files for each page of the booklet, which are then merged into a single PDF named booklet.pdf in the output folder.

Function Descriptions
calculate_booklet_page_order(total_pages): Calculates the order of pages in the booklet.
mm_to_points(mm): Converts millimeters to points.
filename_to_int_tuple(filename): Converts a filename to an integer tuple based on the naming convention.
merge_pdfs(pdf_files, output_filename): Merges individual PDF files into a single PDF.
create_booklet(folder_path, output_path): Main function to create the booklet from images.