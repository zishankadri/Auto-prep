from django.core.files.storage import default_storage
from django.conf import settings
from django.templatetags.static import static

import os
import shutil
import subprocess
import csv
import cv2
from pyzbar.pyzbar import decode


def get_id_from_image(img_path):
    init_image = cv2.imread(img_path)

    height, width = init_image.shape[:2]
    crop_height = int(0.5 * width)
    crop_width = int(0.5 * width)
    cropped_image = init_image[:crop_height, -crop_width:]

    # Convert the image to grayscale
    gray = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)

    # Decode QR codes
    qr_codes = decode(gray)

    # Iterate through detected QR codes
    for qr_code in qr_codes:
        # Extract QR code data
        data = qr_code.data.decode('utf-8')
        
        # Draw a rectangle around the QR code
        rect_points = qr_code.polygon
        if rect_points:
            rect_points = [tuple(point) for point in rect_points]
            for j in range(len(rect_points)):
                cv2.line(cropped_image, rect_points[j], rect_points[(j+1) % len(rect_points)], (0, 255, 0), 2)

                print(f"QR Code Data: {data}")
                return int(data)


# Reading the CSV file response.
def read_output(output_folder):
    response_file = os.listdir(os.path.join(output_folder, "Results"))[-1]
    response_file_path = os.path.join(output_folder, "Results", response_file)

    with open(response_file_path, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        response = {}
        for i, row in enumerate(csv_reader):
            if i < 1: continue  # Skip the labels row
            
            id = get_id_from_image(row[2])

            grades = []
            for j, col in enumerate(row):
                if j < 4: continue   # Skip to the grade columns.
                grades.append(col)
                
            response[id] = grades

        return response
    
def scan(test, input_folder, output_folder):
    try:
        # Add template file and marker image to the specific directory
        template_file = os.path.join(settings.MEDIA_ROOT, f"template-{test.no_of_questions}", "template.json")
        if settings.DEV_ENVIROMENT:
            marker_image = os.path.join(settings.BASE_DIR, "static", "images", "omr_marker.jpg")
        else:
            marker_image = os.path.join(settings.STATIC_ROOT, "images", "omr_marker.jpg")
        shutil.copy(template_file, input_folder)
        shutil.copy(marker_image, input_folder)

        command = f"python3 ./MCQs/OMRChecker/main.py -i '{input_folder}' -o '{output_folder}'"
        subprocess.run(command, shell=True)

        data = read_output(output_folder)

        # Remove the temporary folders
        shutil.rmtree(input_folder)
        shutil.rmtree(output_folder)

        return data
    except Exception as e:
        return None

















    # Add each uploaded image to the specific directory
    # for uploaded_image in images:
    #     file_path = os.path.join(this_input_folder, uploaded_image.name)
    #     default_storage.save(file_path, uploaded_image)
    #     print("✅ File saved at:", file_path)