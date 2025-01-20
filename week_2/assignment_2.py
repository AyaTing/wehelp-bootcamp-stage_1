# Task 1:
print("=== Task 1 ===")
def find_and_print(messages, current_station):
# your code here
    main_line = ["Songshan","Nanjing Sanmin","Taipei Arena","Nanjing Fuxing","Songjiang Nanjing","Zhongshan","Beimen","Ximen","Xiaonanmen","Chiang Kai-Shek Memorial Hall","Guting","Taipower Building","Gongguan","Wanlong","Jingmei","Dapinglin","Qizhang","Xindian City Hall","Xindian",]
    branch_line = ["Songshan","Nanjing Sanmin","Taipei Arena","Nanjing Fuxing","Songjiang Nanjing","Zhongshan","Beimen","Ximen","Xiaonanmen","Chiang Kai-Shek Memorial Hall","Guting","Taipower Building","Gongguan","Wanlong","Jingmei","Dapinglin","Qizhang","Xiaobitan"]
    # current_station = {line: 主線或支線, index: 位置}
    current_station_info = {"line": "branch line", "index": branch_line.index(current_station)} if current_station == "Xiaobitan" else {"line": "main line", "index": main_line.index(current_station)}
    positions = []
    for name, message in messages.items():
        for station in main_line + ["Xiaobitan"]:
            if station in message:
                if station == "Xiaobitan":
                    positions.append({"name": name, "line": "branch line", "index": branch_line.index("Xiaobitan")})
                else:
                    positions.append({"name": name, "line": "main line", "index": main_line.index(station)})

    for position in positions:
        if position["line"] == current_station_info["line"]:
            distance = abs(position["index"] - current_station_info["index"])
            position["distance"] = distance
        else:
            transfer_point = main_line.index("Qizhang")
            distance = abs(position["index"] - transfer_point) + abs(current_station_info["index"] - transfer_point)
            position["distance"] = distance

    closest_friend = min(positions, key=lambda x:x["distance"])
    print(closest_friend["name"])

messages={
"Leslie":"I'm at home near Xiaobitan station.",
"Bob":"I'm at Ximen MRT station.",
"Mary":"I have a drink near Jingmei MRT station.",
"Copper":"I just saw a concert at Taipei Arena.",
"Vivian":"I'm at Xindian station waiting for you."
}
find_and_print(messages, "Wanlong") # print Mary
find_and_print(messages, "Songshan") # print Copper
find_and_print(messages, "Qizhang") # print Leslie
find_and_print(messages, "Ximen") # print Bob
find_and_print(messages, "Xindian City Hall") # print Vivian

# Task 2:
print("=== Task 2 ===")
# your code here, maybe
schedule = []
def book(consultants, hour, duration, criteria):
# your code here
    start_time = hour
    end_time = hour + duration
    available_consultants = [
        consultant for consultant in consultants
        if all(
            not (start_time < appointment["unavailable"]["end_time"] and end_time > appointment["unavailable"]["start_time"])
            for appointment in schedule if appointment['name'] == consultant['name']
        )
    ] 

    if len(available_consultants) == 0:
        print("No Service")
        return
    
    if criteria == "price":
        best_consultant = sorted(available_consultants,key=lambda x:x["price"])[0]
    
    if criteria == "rate":
        best_consultant = sorted(available_consultants,key=lambda x:x["rate"],reverse=True)[0]

    print(best_consultant["name"])
    schedule.append({
        "name": best_consultant["name"],
        "unavailable": {"start_time": start_time, "end_time": end_time}
    })

consultants=[
{"name":"John", "rate":4.5, "price":1000},
{"name":"Bob", "rate":3, "price":1200},
{"name":"Jenny", "rate":3.8, "price":800}
]
book(consultants, 15, 1, "price") # Jenny
book(consultants, 11, 2, "price") # Jenny
book(consultants, 10, 2, "price") # John
book(consultants, 20, 2, "rate") # John
book(consultants, 11, 1, "rate") # Bob
book(consultants, 11, 2, "rate") # No Service
book(consultants, 14, 3, "price") # John

# Task 3:
print("=== Task 3 ===")
def func(*data):
# your code here
    mid_words = [name[len(name) // 2] for name in data]
    match_word = [w for w in mid_words if mid_words.count(w) == 1]
    matched_word = [data[mid_words.index(match_word[i])] for i in range(len(match_word))]
    if matched_word:
        print(",".join(matched_word))
    else:
        print("沒有")

func("彭大牆", "陳王明雅", "吳明") # print 彭大牆
func("郭靜雅", "王立強", "郭林靜宜", "郭立恆", "林花花") # print 林花花
func("郭宣雅", "林靜宜", "郭宣恆", "林靜花") # print 沒有
func("郭宣雅", "夏曼藍波安", "郭宣恆") # print 夏曼藍波安

# Task 4:
print("=== Task 4 ===")
def get_number(index):
# your code here
    num = [0]
    for i in range(1, index + 1):
        if i % 3 == 0:
            num.append(num[i - 1] - 1)
        else:
            num.append(num[i - 1] + 4)
    print(num[index])
get_number(1) # print 4
get_number(5) # print 15
get_number(10) # print 25
get_number(30) # print 70

# Task 5:
print("=== Task 5 ===")
def find(spaces, stat, n):
# your code here
    seats = zip(spaces, stat , range(len(spaces)))
    filtered_seats = [seat for seat in seats if seat[0]>= n and seat[1] != 0]
    if not filtered_seats:
        print(-1)
    else: 
        best_seat = sorted(filtered_seats, key=lambda x:x[0])[0][2]
        print(best_seat)

find([3, 1, 5, 4, 3, 2], [0, 1, 0, 1, 1, 1], 2) # print 5
find([1, 0, 5, 1, 3], [0, 1, 0, 1, 1], 4) # print -1
find([4, 6, 5, 8], [0, 1, 1, 1], 4) # print 2