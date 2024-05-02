# Import necessary modules and functions
from ultralytics import YOLO
from analysing.sort.sort import *


# Initialize the SORT tracker
mot_tracker = Sort()

# Load the YOLOv8n model
coco_model = YOLO('./models/yolov8n.pt')



# --------------------------------------------------------------------------------------
# Define a function to track vehicles
# --------------------------------------------------------------------------------------
def track_vehicles(cap):

    # Define a list of vehicle classes
    vehicles = [2, 3, 5, 7]
    # Initialize a dictionary to store tracked vehicles
    tracked_vehicles = {}
    # Initialize the frame number
    frame_nmr = -1
    # Iterate over frames until no more frames are available
    ret = True
    while ret:
        # Increment the frame number
        frame_nmr += 1
        # Read the next frame
        ret, frame = cap.read()
        if ret:
            # Detect vehicles in the frame using the YOLO model
            detections = coco_model(frame)[0]
            detections_ = []
            for detection in detections.boxes.data.tolist():
                x1, y1, x2, y2, score, class_id = detection
                # Check if the detected object belongs to a vehicle class
                if int(class_id) in vehicles:
                    detections_.append([x1, y1, x2, y2, score])
            
            try:
                # Update the tracking for the detected vehicles
                track_ids = mot_tracker.update(np.asarray(detections_))

            except:
                continue

            # Iterate over the tracked vehicles
            for j in range(len(track_ids)):
                xcar1, ycar1, xcar2, ycar2, car_id = track_ids[j]
                
                # Update the tracked vehicles dictionary
                if int(car_id) not in tracked_vehicles:
                    tracked_vehicles[int(car_id)] = [(frame_nmr, xcar1, ycar1, xcar2, ycar2)]
                else:
                    tracked_vehicles[int(car_id)].append((frame_nmr, xcar1, ycar1, xcar2, ycar2))

    return tracked_vehicles




# --------------------------------------------------------------------------------------
# Define intersect and ccw functions to check if two line segments intersect
# --------------------------------------------------------------------------------------
def intersect(A,B,C,D):
    return ccw(A,C,D) != ccw(B,C,D) and ccw(A,B,C) != ccw(A,B,D)

def ccw(A,B,C):
    return (C[1]-A[1]) * (B[0]-A[0]) > (B[1]-A[1]) * (C[0]-A[0])
# --------------------------------------------------------------------------------------



# --------------------------------------------------------------------------------------
# Define a function to detect violations based on vehicle tracking and lane intersection
# --------------------------------------------------------------------------------------
def detect_vaiolation(tracked_vehicles, height, width):

    # Initialize dictionaries to store violation frames and violations
    violationFrame = {}
    violations = {}

    # Define lane points for intersection detection
    lane_point_a = (int(width*0.5), int(height*0.76))
    lane_point_b = (int(width*0.46), int(height*0.55))
    lane_point_c = (int(width*0.5), int(height*0.76))
    lane_point_d = (int(width*0.46), int(height*0.55))

    # Iterate over tracked vehicles
    for car_id, frames in tracked_vehicles.items():
        frame_A, frame_B, frame_last = None, None, None
        flag_a = False
        flag_b = False

        prev_center_point, prev_left_point, prev_right_point = None, None, None

        # Iterate over frames of each vehicle
        for frame_nmr, x1, y1, x2, y2 in frames:
            frame_last = frame_nmr
            key = "{:03d}{}".format(car_id, frame_nmr)
            violationFrame[key] = (x1, y1, x2, y2)
            if not flag_a:
                center_point = (int((x2+x1)/ 2), (y2))
                left_point = (x1,y2)
                right_point = (x2,y2)

                if prev_left_point is not None:
                    if not flag_b:

                        # Check if the object is near the corner
                        if intersect(left_point, prev_left_point, lane_point_a, lane_point_b) or intersect(right_point, prev_right_point, lane_point_c, lane_point_d) or intersect(left_point, prev_left_point, lane_point_c, lane_point_d) or intersect(right_point, prev_right_point, lane_point_a, lane_point_b):
                            frame_A = frame_nmr
                            flag_b = True
                            violationFrame[key] = (x1, y1, x2, y2)
                    else:
                        violationFrame[key] = (x1, y1, x2, y2)
                        # Check if the object is near the center
                        if intersect(center_point, prev_center_point, lane_point_c, lane_point_d) or intersect(center_point, center_point, lane_point_a, lane_point_b):
                            frame_B = frame_nmr                        
                            flag_a = True                        

                prev_center_point, prev_left_point, prev_right_point = center_point, left_point, right_point # Update previous frame coordinates
            
            if flag_a:
                violationFrame[key] = (x1, y1, x2, y2)
        # If a violation is detected, record the violation frames and violations
        if flag_a:
            violations[car_id] = (frame_A, frame_B, frame_last)

    # Print detected violations
    print("========================  detected Violations  =========================")   
    for car_id, frames in violations.items():
        frame_A, frame_B, frame_last = frames
        print(f"Car ID: {car_id}, First Frame: {frame_A}, Violation Frame: {frame_B}, Last Frame: {frame_last}")

    return violations, violationFrame

