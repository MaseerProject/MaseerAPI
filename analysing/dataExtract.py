# Import necessary modules
from ultralytics import YOLO
import cv2
import easyocr
import re

# Initialize the YOLO license plate detector model
license_model = YOLO('.\models\license_plate_detector.pt')

# Initialize the OCR reader for text recognition
reader = easyocr.Reader(['en'], gpu=True)



# --------------------------------------------------------------------------------------
# Define a function to convert English characters to Arabic symbols
# --------------------------------------------------------------------------------------
def convert_to_arabic(input_string):
    # Define mapping between English characters and Arabic symbols
    mapping = {
        'A': ' أ',
        'B': ' ب',    
        'J': ' ح',
        'D': ' د',
        'R': ' ر',
        'S': ' س',
        'X': ' ص',        
        'T': ' ط',
        'E': ' ع',
        'G': ' ق',        
        'K': ' ك',
        'L': ' ل',
        'Z': ' م',
        'N': ' ن',
        'H': ' ه',
        'U': ' و',
        'V': ' ى', 
        '0': '٠',
        '1': '١',
        '2': '٢',
        '3': '٣',
        '4': '٤',
        '5': '٥',
        '6': '٦',
        '7': '٧',
        '8': '٨',
        '9': '٩',
    }
    
    # Convert each character in the input string
    output_string = ''
    for char in input_string:
        # Use mapping.get() to handle characters not in the mapping
        arabic_char = mapping.get(char, char)
        output_string += arabic_char
    
    return output_string



# --------------------------------------------------------------------------------------
# Define a function to read date and time from an image region
# --------------------------------------------------------------------------------------
def read_date_time(x1, x2, y1, y2, img, allow_list):
    
    # Crop the image to the specified region
    imgCrop = img[y1:y2, x1:x2]
    
    # Convert the cropped image to grayscale
    gray = cv2.cvtColor(imgCrop , cv2.COLOR_RGB2GRAY)
    
    # Apply thresholding to the grayscale image
    _, img_thresh_low = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)

    # Perform OCR on the thresholded image to recognize text
    result = reader.readtext(img_thresh_low, allowlist=allow_list)
    
    try:
        # Attempt to perform OCR on the cropped region from the threshold image
        value_date = result[0][1]
        confidence_date = result[0][2]
    except:
        # Handle the case where no text is detected in the threshold image
        value_date = "No text detected"
        confidence_date = 0.0
       
 
    try:
        # Attempt to perform OCR on the cropped region from the threshold image
        value_time = result[1][1]
        confidence_time = result[1][2]
    except:
        # Handle the case where no text is detected in the threshold image
        value_time = "No text detected"
        confidence_time = 0.0
        
    return value_date, confidence_date, value_time, confidence_time



# --------------------------------------------------------------------------------------
# Define a function to read license plate from an image region
# --------------------------------------------------------------------------------------
def read_plate(x1, x2, y1, y2, img, allow_list):
    
    # Crop the image to the specified region
    imgCrop = img[y1:y2, x1:x2]
    
    # Convert the cropped image to grayscale
    gray = cv2.cvtColor(imgCrop , cv2.COLOR_RGB2GRAY)
    
    # Apply a low threshold to the grayscale image
    _, img_thresh_low = cv2.threshold(gray, 64, 255, cv2.THRESH_BINARY_INV)

    # Perform OCR on the low threshold image to recognize text
    result_low = reader.readtext(img_thresh_low, allowlist=allow_list)
    
    try:
        # Attempt to perform OCR on the cropped region from the low threshold image
        value_low = result_low[0][1]
        confidence_low = result_low[0][2]
    except:
        # Handle the case where no text is detected in the low threshold image
        value_low = "No text detected"
        confidence_low = 0.0
        
    # Check if confidence from the low threshold image is high enough
    if confidence_low > 0.8:
        return value_low, confidence_low
    

    # Apply a high threshold to the grayscale image
    _, img_thresh_high = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY_INV)
    try:
        # Attempt to perform OCR on the cropped region from the high threshold image
        result_high = reader.readtext(img_thresh_high, allowlist=allow_list)
        value_high = result_high[0][1]
        confidence_high = result_high[0][2]
    except:
        # Handle the case where no text is detected in the high threshold image
        value_high = "No text detected"
        confidence_high = 0.0

    # Compare confidence scores and return the value and confidence of the one with higher confidence
    if confidence_high > confidence_low:
        return value_high, confidence_high
    else:
        return value_low, confidence_low



# --------------------------------------------------------------------------------------
# Define a function to detect license plate from an image
# --------------------------------------------------------------------------------------
def detect_plate(img):
    # Detect license plates in the image using the YOLO license plate detector
    license_plates = license_model(img)[0]
    try:
        # Extract bounding box coordinates, score, and class ID of the detected license plate
        x1, y1, x2, y2, score, class_id = license_plates.boxes.data[0]

        # Define coordinates for digit and letter regions within the license plate
        x1_digit, y1_digit, x2_digit, y2_digit = int(x1), int((y1 + y2) /2), int((x1 + x2) / 2), int(y1 + (y2-y1)*0.9) 
        x1_letter, y1_letter, x2_letter, y2_letter = int((x1 + x2) / 2), int((y1 + y2) /2), int(x1 + (x2-x1)*0.8), int(y1 + (y2-y1)*0.9) 

        # Perform OCR on digit and letter regions to read the license plate
        value_digit, confidence_digit = read_plate(x1_digit, x2_digit, y1_digit, y2_digit, img, '0123456789')
        value_letter, confidence_letter = read_plate(x1_letter, x2_letter, y1_letter, y2_letter, img, 'ABDEGHJKLNRSTUVXZ')

    except:
        # Handle the case where no license plate is detected
        value_digit = "No text detected"
        confidence_digit = 0.0
        value_letter = "No text detected"
        confidence_letter = 0.0

    # Return the extracted values and confidences for digit and letter regions of the license plate
    return value_digit, confidence_digit, value_letter, confidence_letter



# --------------------------------------------------------------------------------------
# Define a function to process a video, extracting license plate data, date, and time
# --------------------------------------------------------------------------------------
def process_video(cap,start_frame, end_frame):

    # Initialize previous confidence levels
    prev_conf_digit, prev_conf_letter, prev_conf_date, prev_conf_time = 0.0, 0.0, 0.0, 0.0
    best_value_digit, best_value_letter, best_value_date, best_value_time = '', '', '', ''

    # Get the height and width of video frames
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # Define region coordinates for date extraction
    x1_date, x2_date, y1_date, y2_date = int (width*0.4), int (width*0.6), int (height*0.9), height

    current_frame = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_frame += 1
        if current_frame < start_frame:
            continue  # Skip frames until reaching the start_frame
        if current_frame > end_frame:
            break  # Break the loop after processing up to end_frame

        if (prev_conf_date < 0.8 or prev_conf_time < 0.8):

            # Perform date and time recognition if confidence levels are below 0.8
            value_date, confidence_date, value_time, confidence_time = read_date_time(x1_date, x2_date, y1_date, y2_date, frame, '0123456789:-')
            
            #print("value_date", value_date, "Confidence:", confidence_date)
            #print("value_time", value_time, "Confidence:", confidence_time)

            # Update values only if confidence is higher than previous and meets format requirements
            if confidence_date > prev_conf_date  and re.match(r'^\d{4}-\d{2}-\d{2}$', value_date):
                prev_conf_date = confidence_date
                best_value_date = value_date

            if confidence_time > prev_conf_time  and re.match(r'^\d{2}:\d{2}:\d{2}$', value_time):
                prev_conf_time = confidence_time
                best_value_time = value_time

        # Perform license plate detection and character recognition
        value_digit, confidence_digit, value_letter, confidence_letter = detect_plate(frame)
        
        #print("value_digit", value_digit, "Confidence:", confidence_digit)
        #print("value_letter", value_letter, "Confidence:", confidence_letter)
        
        # Update values only if confidence is higher than previous and meets length requirements
        if confidence_digit > 0.4 and confidence_digit > prev_conf_digit and len(value_digit) <= 4:
            prev_conf_digit = confidence_digit
            best_value_digit = value_digit

        if confidence_letter > 0.5 and confidence_letter > prev_conf_letter and len(value_letter) == 3:
            prev_conf_letter = confidence_letter
            best_value_letter = value_letter


    # Print the extracted data
    print("======================= Detect Plate & Extract Data ============================")

    print("plate_digit: ", best_value_digit, "Confidence:", prev_conf_digit)
    print("plate_letter: ", best_value_letter, "Confidence:", prev_conf_letter)
    print("date: ", best_value_date, "Confidence:", prev_conf_date)
    print("time: ", best_value_time, "Confidence:", prev_conf_time)


    # Combine digit and letter parts of the license plate to form the English and Arabic versions
    Plate_Eng_No = best_value_digit + " " + best_value_letter
    Plate_Arb_digit = convert_to_arabic(best_value_digit)
    Plate_Arb_letter = convert_to_arabic(best_value_letter)
    Plate_Arb_letter = Plate_Arb_letter[::-1]
    Plate_Arb_No = Plate_Arb_letter + Plate_Arb_digit


    return Plate_Eng_No, Plate_Arb_No, best_value_date, best_value_time

