import os
import cv2
import numpy as np
import pandas as pd

# Configuration
IMAGE_DIR = 'ideathon\images'  # Directory containing blueprint images
CSV_FILE = 'wall_length_dataset.csv'  # Output CSV file path
SCALE_FACTOR = 0.05  # Example: 1 pixel = 0.05 meters

# Ensure the output directory and CSV file exist
os.makedirs(IMAGE_DIR, exist_ok=True)

def calculate_wall_length(image_path):
    """Calculate the total wall length from a blueprint image."""
    # Load the image and convert to grayscale
    image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Canny Edge Detection
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # Detect lines using Hough Line Transform
    lines = cv2.HoughLinesP(edges, rho=1, theta=np.pi / 180, threshold=100, 
                            minLineLength=50, maxLineGap=10)

    if lines is None:
        print(f"No lines detected in {image_path}.")
        return 0.0  # No walls detected, return 0 length

    # Calculate total length of detected lines (in pixels)
    total_length_pixels = sum([np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) 
                               for line in lines for x1, y1, x2, y2 in [line[0]]])

    # Convert pixels to meters using the scale factor
    total_length_meters = total_length_pixels * SCALE_FACTOR
    return round(total_length_meters, 2)  # Round to 2 decimal places





def calculate_materials(wall_length, wall_height=3.0):
    """Estimate bricks, cement, and sand needed based on wall length."""
    # Wall area in square meters (length * height)
    wall_area = wall_length * wall_height

    # Brick calculation (each brick is 0.19m x 0.09m)
    brick_area = 0.19 * 0.09  # Area of one brick in m^2
    bricks_required = wall_area / brick_area

    # Cement and sand calculation (1:4 ratio)
    cement_bags = wall_area * 0.2  # Example: 0.2 bags per m^2
    sand_volume = cement_bags * 4  # 4x the cement quantity (in volume)

    return round(bricks_required), round(cement_bags), round(sand_volume, 2)














# List to store image paths and corresponding wall lengths
data = []

# Process all images in the blueprints directory
for filename in os.listdir(IMAGE_DIR):
    if filename.lower().endswith(('.jpg', '.png')):  # Process only images
        image_path = os.path.join(IMAGE_DIR, filename)
        wall_length = calculate_wall_length(image_path)
        brick,cement,sand = calculate_materials(wall_length)
        print(f"Processed {filename}: Wall Length = {wall_length} meters")
        data.append([image_path, wall_length,brick,cement,sand])

# Save the results to a CSV file
df = pd.DataFrame(data, columns=['Image_Path', 'Wall_Length_Meters','Bricks','Cement','Sand'])
df.to_csv(CSV_FILE, index=False)

print(f"Dataset saved to {CSV_FILE}")