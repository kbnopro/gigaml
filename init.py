import glob
from typing import List

from PIL.Image import Image
from ai_sdk import (
    extract_table_from_image,
    extract_data_from_header,
    extract_text_from_image,
)
from pdf2image import convert_from_path
import base64
from io import BytesIO, TextIOWrapper
import os


def img_to_base64(image):
    """Convert a PIL Image to a base64 encoded string"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode("utf-8")
    return img_str


def handle_first_page(file: str, image: Image, f: TextIOWrapper):
    """Handle the first page of the PDF, extracting header and body text"""
    header = image.crop((0, 170, image.width, 530))
    f.write(extract_data_from_header([img_to_base64(header)])[0].text)

    f.write("\n\n\n")

    body = image.crop((0, 530, image.width, image.height - 150))

    f.write(extract_text_from_image([img_to_base64(body)])[0].text)
    f.write("\n\n\n")
    f.write(extract_table_from_image([img_to_base64(body)])[0].text)
    f.write("\n\n\n")


def handle_other_pages(file: str, images: List[Image], f: TextIOWrapper):
    """Extract tables from the remaining pages of the PDF"""
    for image in images:
        f.write(
            extract_table_from_image(
                [img_to_base64(image)],
                "If there is a table without proper next to a graph, the heading of the table is the heading of the graph",
            )[0].text,
        )
        f.write("\n")


def handle_pdf(file: str):
    """Extract data from a PDF file and save it to a text file"""
    images = convert_from_path(file)

    if not os.path.exists("./processed_data/"):
        os.makedirs("./processed_data/")
    output_file = f"./processed_data/{file.split('/')[-1].split('.')[0]}.txt"

    # Check if output file already exists and not empty
    if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
        print(f"Skipping {file} as it has already been processed.")
        return

    with open(f"./processed_data/{file.split('/')[-1].split('.')[0]}.txt", "w+") as f:
        handle_first_page(file, images[0], f)
        handle_other_pages(file, images[1:], f)


for file_name in glob.glob("./data/*.pdf"):
    print(f"Processing file: {file_name}")
    handle_pdf(file_name)
