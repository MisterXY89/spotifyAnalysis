
import json
import hashlib
import billboard
import pendulum

BILLBOARD_LIST_NAME: str = "hot-100"
JSON_FILE: str = "../../files/billbord_data_weekly_"

def getWeeks():
    endDate = pendulum.datetime(2019, 12, 31)
    date = pendulum.datetime(1969, 1, 1)
    weekDates = []
    while endDate.next(pendulum.FRIDAY).strftime('%Y-%m-%d') != date.next(pendulum.FRIDAY).strftime('%Y-%m-%d'):
        appendDate = date.format("YYYY-MM-DD")
        # appendDate = f"{date.year}-{date.month}-{date.day}"
        weekDates.append(appendDate)
        date = date.add(weeks=1)

    return weekDates


def singleWeekData(week):
    chart = billboard.ChartData(BILLBOARD_LIST_NAME, date=week, fetch=True, timeout=120, max_retries=20)
    md5 = hashlib.md5()
    weekData = []
    for entry in chart.entries:
        md5.update((week + str(entry.rank)).encode())
        weekData.append({
            "id" : str(int(md5.hexdigest(), 16))[0:12],
            "title" : entry.title,
            "artist" : entry.artist,
            "image" : entry.image,
            "peakPos" : entry.peakPos,
            "lastPos" : entry.lastPos,
            "weeks" : entry.weeks,
            "rank" : entry.rank,
            "isNew" : entry.isNew
        })
    return weekData


def billboardData(weeks, data):
    data = data
    for week in weeks:
        year = week.split("-")[0]
        if year in data and week in data[year] and len(data[year][week]) == 100:
            print("%s is already stored"%week)
            continue
        weekData = singleWeekData(week)
        if not year in data:
            data[year] = {}
        data[year][week] = weekData
        print("%s just added!"%week)
    return data


def loadData(file, year):
    try:
        with open(file + str(year) + ".json", "r") as readFile:
            jsonData = json.load(readFile)
    except FileNotFoundError as e:
        jsonData = {}
    return jsonData


def storeData(data, file, year):
    with open(file + str(year) + ".json", "w") as writeFile:
        json.dump(data, writeFile)


weeks = getWeeks()
years = {}
for week in weeks:
    y = week.split("-")[0]
    if not y in years:
        years[y] = []
    years[y].append(week)


for year in years.keys():
    data = loadData(JSON_FILE, year)
    bdata = billboardData(years[year], data)
    print("stored %s entrys" % len(years[year]))
    storeData(bdata, JSON_FILE, year)


# years = [weeks[x:x+10] for x in range(0, len(weeks), 52)]
# for weekChunk in chunks:
#     data = loadData(JSON_FILE)
#     bdata = billboardData(weekChunk, data)
#     print("stored %s entrys" % len(weekChunk))
#     storeData(data, JSON_FILE)
