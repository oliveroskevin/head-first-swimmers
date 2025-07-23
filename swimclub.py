import statistics
import hfpy_utils
import json

FOLDER = 'swimdata/'
CHARTS = 'charts/'
JSONDATA = 'records.json'

def read_swim_data(filename): 
    swimmer, age, distance, stroke = filename.removesuffix('.txt').split('-')

    with open(FOLDER + filename) as file:
        lines = file.readlines()

    swimmer_times = lines[0].strip().split(',')

    converts = []
    for swimmer_time in swimmer_times:
        if ':' in swimmer_time:
            minutes, rest = swimmer_time.split(':')
            seconds, hundredths = rest.split('.')
        else:
            minutes = 0
            seconds, hundredths = swimmer_time.split('.')
        converts.append((int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths))
    
    average = statistics.mean(converts)
    minute_seconds, hundredths = f"{average/100:.2f}".split(".")
    minute_seconds = int(minute_seconds)
    minute = (int(minute_seconds) // 60)
    seconds = int(minute_seconds) - (minute * 60)

    average_time = f"{minutes}:{seconds:0>2}.{hundredths}"



    return swimmer, age, distance, stroke, swimmer_times, average_time, converts

def produce_bar_chart(fn, location=CHARTS):
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(fn)
    from_max = max(converts)
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    header = f"""<!DOCTYPE html>
                <html>
                    <head>
                        <title>{title}</title>
                        <link rel="stylesheet" href="/static/webapp.css"/>
                    </head>
                    <body>
                        <h3>{title}</h3>
                    """
    body = ""

    for n, t in enumerate(times):
        bar_width = hfpy_utils.convert2range(converts[n], 0, from_max, 0, 350)
        body = body + f"""
                        <svg height="30" width="400">
                            <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);"/>
                        </svg>{t}<br/>
                        """
    
    with open(JSONDATA) as jf:
        records = json.load(jf)
    COURSES =  ("LC MEN", "LC WOMEN", "SC MEN", "SC WOMEN")
    time = []
    for course in COURSES:
        time.append(records[course][event_lookup(fn)])

    footer = f"""
            <p>Average time: {average}</p>
            <p>M: {time[0]} ({time[2]})<br />W: {time[1]} ({time[3]})</p>
        </body>
    </html>
    """

    page = header + body + footer
    save_to = f"{location}/{fn.removesuffix('.txt')}.html"
    with open(save_to, 'w') as sf:
        print(page, file=sf)

    return save_to

def event_lookup(filename: str):
    *_, distance, stroke = filename.removesuffix('.txt').split('-')
    conversions = {
        "Free": "freestyle",
        "Back": "backstroke",
        "Breast": "breaststroke",
        "Fly": "butterfly",
        "IM": "individual medley"
    }
    
    return f'{distance} {conversions[stroke]}'