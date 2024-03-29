import os
from PIL import Image
import math 
import PyPDF2

def calculate_booklet_page_order(total_pages):
    pages_per_sheet = 8  # 4 A6 pages per side on an A4 sheet
    N = math.ceil(total_pages / pages_per_sheet) # Amount of A4's needed 
    N_total = N*pages_per_sheet
    page_order = []

   
    for i in range(N):
    # Initialize the pages for the back and front
        back = [None] * (pages_per_sheet // 2)
        front = [None] * (pages_per_sheet // 2)

        a = 1
        b = a + N*2
        c =  (N_total-2)
        d = N_total -(N+1)*2

        f = N*2 
        g = 0
        h = d+1 
        j = N_total-1

        # Fill in the page numbers for the front side
        front[0] = a + (N-i-1)*2 if total_pages - (i * 4 + 3) > 0 else None # top left
        front[1] = b + (N-i-1)*2 if total_pages - (i * 4 + 4) > 0 else None # top right
        front[2] = c - (N-i-1)*2 if i * 4 + 3 <= total_pages else None # bottom left
        front[3] = d -(N-i-1)*2 if i * 4 + 4 <= total_pages else None # bottom right 

        # Fill in the page numbers for the back side
        back[2] = g + (N-i-1)*2 if i * 4 + 2 <= total_pages else None   # top left
        back[3] = f +  (N-i-1)*2 if i * 4 + 1 <= total_pages else None # top right
        back[0] = j-(N-i-1)*2 if total_pages - (i * 4 + 1) > 0 else None # bottom left
        back[1] = h - (N-i-1)*2  if total_pages - (i * 4 + 2) > 0 else None # bottom right

       
        page_order.append((front, back))
    return page_order


def mm_to_points(mm):
    return mm * 2.83465  # Convert mm to points

def mm_to_pixels(mm, dpi):
    # Convert mm to inches (1 inch = 25.4 mm)
    inches = mm / 25.4

    # Convert inches to pixels
    pixels = int(inches * dpi)

    return pixels

def filename_to_int_tuple(filename):
    """Converts a filename like '1_2.png' to an integer tuple (1, 2)."""
    name_part = os.path.splitext(filename)[0]  # Remove the extension
    return tuple(map(int, name_part.split('_')))  # Split at '_', convert to integers


def create_booklet(folder_path, output_path ):
    dpi = 300  # Standard print resolution
    a4_size_pixels = (mm_to_pixels(210, dpi), mm_to_pixels(297, dpi))  # A4 size in pixels



    a6_width_adjusted = (a4_size_pixels[0] / 2)
    a6_height_adjusted = (a4_size_pixels[1] / 2) 
    a6_size = (int(a6_width_adjusted*0.9), int(a6_height_adjusted*0.9))

    input_paths = {int(os.path.splitext(f)[0]): os.path.join(folder_path, f)
               for f in sorted(os.listdir(folder_path), key=lambda x: int(os.path.splitext(x)[0]))
               if f.lower().endswith('.png')}
    
    # Calculate the order of the pages in the booklet
    booklet_page_order =calculate_booklet_page_order(len(input_paths))

    pdf_files = []

    for sheet_num, (front_side, back_side) in enumerate(booklet_page_order):
        for side_num, side in enumerate([front_side, back_side]):
            a4_page = Image.new('RGBA', a4_size_pixels, (255, 255, 255, 0))

            for idx, page_num in enumerate(side):
                if page_num is None or page_num not in input_paths:
                    continue

                a6_image = Image.open(input_paths[page_num]).resize(a6_size, Image.ANTIALIAS)
            
                # Calculate the center of the quadrant
                quadrant_center_x = ((idx % 2) * a4_size_pixels[0] / 2) + (a4_size_pixels[0] / 4)
                quadrant_center_y = ((idx // 2) * a4_size_pixels[1] / 2) + (a4_size_pixels[1] / 4)

                # Adjust position to center the A6 image in the quadrant
                x = quadrant_center_x - (a6_image.width / 2)
                y = quadrant_center_y - (a6_image.height / 2)

                a4_page.paste(a6_image, (int(x), int(y)), a6_image)
            side_label = 'front' if side_num == 0 else 'back'
            output_file_name = os.path.join(output_path, f"{sheet_num+1}_{side_label}.pdf")
            a4_page.convert('RGB').save(output_file_name)
            pdf_files.append(output_file_name)

    merge_pdfs(pdf_files, os.path.join(output_path, 'booklet.pdf'))

def merge_pdfs(pdf_files, output_filename):
    pdf_merger = PyPDF2.PdfMerger()
    for pdf_file in pdf_files:
        pdf_merger.append(pdf_file)
    with open(output_filename, 'wb') as f:
        pdf_merger.write(f)
    pdf_merger.close()