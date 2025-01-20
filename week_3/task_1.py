import urllib.request as request
import json
import csv
import os
os.environ["no_proxy"] = "*"

src_url_1 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-1"
src_url_2 = "https://padax.github.io/taipei-day-trip-resources/taipei-attractions-assignment-2"  

with request.urlopen(src_url_1) as response:
    attraction_info = json.load(response)
with request.urlopen(src_url_2) as response:
    mrt_info = json.load(response)

spot_data = []
mrt_data = {}
           
for attraction in  attraction_info["data"]["results"]:
    spot_title = attraction["stitle"]
    longitude = attraction["longitude"]
    latitude = attraction["latitude"]
    attraction_lower = attraction["filelist"].lower()
    image_index = attraction_lower.find(".jpg")
    image_url = attraction["filelist"][:image_index + 4]
    serial_no = attraction["SERIAL_NO"]
    for mrt in mrt_info["data"]:
        if mrt["SERIAL_NO"] == serial_no:
            district_index = mrt["address"].find("區")
            district = mrt["address"][district_index - 2 :district_index + 1]
            station = mrt["MRT"]

    spot_data.append([spot_title,district,longitude,latitude,image_url])
    if station not in mrt_data:
        mrt_data[station] = []
    mrt_data[station].append(spot_title)

with open("spot.csv","w",encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(spot_data)

with open("mrt.csv","w",encoding="utf-8") as file:
    writer = csv.writer(file)
    rows = [[station] + attractions for station, attractions in mrt_data.items()]
    writer.writerows(rows)
