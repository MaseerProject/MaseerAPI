# Import necessary modules and functions
from fastapi import APIRouter, File, UploadFile
from analysing.dataExtract import process_video
from analysing.violationDetect import detect_vaiolation, track_vehicles
import cv2
from tempfile import NamedTemporaryFile
from database import report_violation
import os
from datetime import datetime


# Create an instance of APIRouter
router = APIRouter()



# Define a POST route for uploading videos and detecting violations
@router.post("/uploadVideo/{user_id}")
async def uploadVideo(user_id:int,  user_video: UploadFile = File(...)):
    # Save the uploaded video to a temporary file
    with NamedTemporaryFile(delete=False) as tmp:
        tmp.write(await user_video.read())
        tmp_path = tmp.name

    # Open the temporary video file using cv2.VideoCapture
    cap = cv2.VideoCapture(tmp_path)

    if not cap.isOpened():
        # Handle the error if the video file can't be opened
        return {"error": "Unable to open video file"}

    # Get video properties
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # Track vehicles in the video
    tracked_vehicles = track_vehicles(cap)

    # Detect violations and get violation frames
    violations, violationFrame = detect_vaiolation(tracked_vehicles, frame_height, frame_width)
    
    # Print information about detected violations
    print ("========================= Tracking Vehicles & Detecting Violations ==========================")
    print ("Number of detected violation: ",len(violations))
    print ("")

    # Loop through detected violations
    for car_id, frames in violations.items():
        start_frame, violation_frame , end_frame= frames
        
        # Process the video to extract plate numbers and timestamps
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        Plate_Eng_No, Plate_Arb_No, best_value_date, best_value_time = process_video(cap, start_frame, end_frame) 

        # Crop the video to extract the violation clip
        #video_bytes = crop_video(cap, frame_width, frame_height, start_frame, violation_frame, end_frame, violationFrame, car_id)    
        
        video_bytes = None
        max_video_size = 16 * 1024 * 1024
        frames_number = 30
        while True:
            cropped_video_filename = crop_video(cap, frame_width, frame_height, start_frame, violation_frame, end_frame, violationFrame, car_id, frames_number)

            # Read the cropped video file to bytes
            with open(cropped_video_filename, "rb") as f:
                video_bytes = f.read()

            # Get the size of video_bytes in bytes
            video_size = len(video_bytes)
            print(video_size)

            # Remove the temporary output file
            os.remove(cropped_video_filename)

            if video_size <= max_video_size:
                break
        
            # Reduce the end_crop_frame and start_f variables
            end_frame -= 5
            start_frame += 5






        # Report the violation to the database
        try:
            report_violation(user_id, best_value_date, best_value_time, Plate_Eng_No, Plate_Arb_No, video_bytes)
        except:
            report_violation(user_id, best_value_date, best_value_time, Plate_Eng_No, Plate_Arb_No, None)

    # Release VideoCapture object
    cap.release()
    
    # Return the number of violations detected    
    return {"violations": len(violations)}



# Define a function to crop a video clip based on specified frames and draw lane lines and bounding boxes
def crop_video(cap, frame_width, frame_height, start_frame, violation_frame, end_frame, violationFrame, car_id, frames_number):

    # Get frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Set the start and end frames for cropping with an additional buffer
    start_f = max(0, start_frame - frames_number)
    end_crop_frame = min(violation_frame + frames_number, end_frame)

    # Seek to start_frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_f)

    # Create a VideoWriter object to write frames to memory
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Generate a unique filename based on current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"temp_output_{timestamp}.mp4"


    out = cv2.VideoWriter(file_name, fourcc, fps, (frame_width, frame_height))

    # Define lane points for drawing
    lane_point_A = (int(frame_width*0.50), int(frame_height*0.76))
    lane_point_B = (int(frame_width*0.46), int(frame_height*0.55))
    lane_point_C = (int(frame_width*0.37), int(frame_height*0.76))
    lane_point_D = (int(frame_width*0.42), int(frame_height*0.55))


    
    # Loop through frames and write only the required frames
    current_frame = start_f
    x1, y1, x2, y2 = 0,0,0,0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if no frame is read

        # Draw lines on the frame
        #cv2.line(frame, lane_point_A, lane_point_B, (255, 0, 0), 7)
        #cv2.line(frame, lane_point_C, lane_point_D, (255, 0, 0), 7)
        
        # Draw border box around car if available in violationFrame
        key = "{:03d}{}".format(car_id, current_frame)
        if key in violationFrame:
            x1, y1, x2, y2 = violationFrame[key]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Draw different colored lines based on frame range
        if current_frame < start_frame:
            color = (0, 255, 0)  # Green color for frames before violation
        elif current_frame < violation_frame:
            color = (0, 255, 255)  # Yellow color for frames during violation
        else:
            color = (0, 0, 255)  # Red color for frames after violation

        # Draw four lines around the detected object
        cv2.line(frame, (x1, y1), (x2, y1), color, 7)  # Top line
        cv2.line(frame, (x2, y1), (x2, y2), color, 7)  # Right line
        cv2.line(frame, (x2, y2), (x1, y2), color, 7)  # Bottom line
        cv2.line(frame, (x1, y2), (x1, y1), color, 7)  # Left line


        # Write the frame if it's within the specified range
        if current_frame <= end_crop_frame:
            out.write(frame)
        else:
            break  # Break the loop if we've passed the end_frame

        current_frame += 1

    # Release VideoWriter object
    out.release()

    # Read the written video file to bytes
    with open(file_name, "rb") as f:
        video_bytes = f.read()

    # Get the size of video_bytes in bytes
    #video_size = len(video_bytes)
    #print(video_size)



    return (file_name)


'''
        while True:
            cropped_video_filename = crop_video(cap, frame_width, frame_height, start_frame, violation_frame, end_frame, violationFrame, car_id, frames_number)

            # Read the cropped video file to bytes
            with open(cropped_video_filename, "rb") as f:
                video_bytes = f.read()

            # Get the size of video_bytes in bytes
            video_size = len(video_bytes)
            print(video_size)

            if video_size <= max_video_size:
                break
        
        if start_frame >= violation_frame and frames_number < 5:
            break
        
        # Reduce the frames_number
        if frames_number > 5:
            frames_number -=5

        else:
            # Reduce the end_crop_frame and start_f variables
            if start_frame+5 >= violation_frame:
                start_frame = violation_frame
            else:
                start_frame += 5




        # Report the violation to the database
        report_violation(user_id, best_value_date, best_value_time, Plate_Eng_No, Plate_Arb_No, video_bytes)

    # Release VideoCapture object
    cap.release()
    
    # Return the number of violations detected    
    return {"violations": len(violations)}



# Define a function to crop a video clip based on specified frames and draw lane lines and bounding boxes
def crop_video(cap, frame_width, frame_height, start_frame, violation_frame, end_frame, violationFrame, car_id, frames_number):

    # Get frames per second (fps) of the video
    fps = cap.get(cv2.CAP_PROP_FPS)

    # Set the start and end frames for cropping with an additional buffer
    start_f = max(0, start_frame - frames_number)
    end_crop_frame = min(violation_frame + frames_number, end_frame)

    # Seek to start_frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_f)

    # Create a VideoWriter object to write frames to memory
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    # Generate a unique filename based on current timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"temp_output_{timestamp}.mp4"


    out = cv2.VideoWriter(file_name, fourcc, fps, (frame_width, frame_height))

    # Define lane points for drawing
    lane_point_A = (int(frame_width*0.50), int(frame_height*0.76))
    lane_point_B = (int(frame_width*0.46), int(frame_height*0.55))
    lane_point_C = (int(frame_width*0.37), int(frame_height*0.76))
    lane_point_D = (int(frame_width*0.42), int(frame_height*0.55))


    
    # Loop through frames and write only the required frames
    current_frame = start_f
    x1, y1, x2, y2 = 0,0,0,0
    while True:
        ret, frame = cap.read()
        if not ret:
            break  # Break the loop if no frame is read

        # Draw lines on the frame
        #cv2.line(frame, lane_point_A, lane_point_B, (255, 0, 0), 7)
        #cv2.line(frame, lane_point_C, lane_point_D, (255, 0, 0), 7)
        
        # Draw border box around car if available in violationFrame
        key = "{:03d}{}".format(car_id, current_frame)
        if key in violationFrame:
            x1, y1, x2, y2 = violationFrame[key]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        # Draw different colored lines based on frame range
        if current_frame < start_frame:
            color = (0, 255, 0)  # Green color for frames before violation
        elif current_frame < violation_frame:
            color = (0, 255, 255)  # Yellow color for frames during violation
        else:
            color = (0, 0, 255)  # Red color for frames after violation

        # Draw four lines around the detected object
        cv2.line(frame, (x1, y1), (x2, y1), color, 7)  # Top line
        cv2.line(frame, (x2, y1), (x2, y2), color, 7)  # Right line
        cv2.line(frame, (x2, y2), (x1, y2), color, 7)  # Bottom line
        cv2.line(frame, (x1, y2), (x1, y1), color, 7)  # Left line


        # Write the frame if it's within the specified range
        if current_frame <= end_crop_frame:
            out.write(frame)
        else:
            break  # Break the loop if we've passed the end_frame

        current_frame += 1

    # Release VideoWriter object
    out.release()

    # Read the written video file to bytes
    with open(file_name, "rb") as f:
        video_bytes = f.read()

    # Get the size of video_bytes in bytes
    video_size = len(video_bytes)
    #print(video_size)

    # Remove the temporary output file
    #os.remove(file_name)


    return (file_name)

'''