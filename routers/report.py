from fastapi import APIRouter, Response, HTTPException
from database import get_report_video, get_report, mark_report_as_visited
from datetime import datetime

router = APIRouter()

@router.get("/reportvideo/{report_id}")
async def get_video(report_id: int):
    video_data = get_report_video(report_id)
    if video_data:
        # Convert bytearray to bytes
        video_data = bytes(video_data)
        return Response(content=video_data, media_type="video/mp4")
    else:
        return Response(status_code=404)
    


@router.get("/report/{report_id}")
async def getReport(report_id: int):
    report_data = get_report(report_id)
    if report_data:
        mark_report_as_visited(report_id)

        # Extract the date, day, and time from the datetime object
        date = report_data[2].strftime("%Y-%m-%d")
        day = report_data[2].strftime("%A")  # %A gives the full name of the day
        time = report_data[2].strftime("%I:%M:%S %p")

        return {
            "report_id": report_data[0],
            "user_id": report_data[1],
            "generation_date": date,
            "generation_day": day,
            "generation_time": time,
            "name": report_data[3],
            "phone_number": report_data[4],
            "violation_type_id": report_data[5],
            "violation_type_a_des": report_data[6],
            "violation_type_e_des": report_data[7],
            "violation_date": report_data[8],
            "violation_time": report_data[9],
            "plate_eng_no": report_data[10],
            "plate_arb_no": report_data[11]
        }
    else:
        raise HTTPException(status_code=404, detail="Report_Not_Found")
    

