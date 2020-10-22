from datetime import datetime


def suggested_time(list_1, list_2, start_time, end_time, duration):
    # combine the 2 list of slots into one and then sort by time
    meeting_slots = list_1 + list_2
    meeting_slots.sort(key=lambda date: datetime.strptime(date.split('-')[0], '%H:%M'))

    if not meeting_slots:
        return [f"{start_time}-{end_time}"]

    # merge the overlapping meeting times to generate a list of combined unique meeting times
    total_meetings = len(meeting_slots)
    prev_start_time = get_start_time(meeting_slots[0])
    prev_end_time = get_end_time(meeting_slots[0])
    merged_slots = [[prev_start_time, prev_end_time]]

    for i in range(1, total_meetings):
        curr_slot = meeting_slots[i]
        curr_start_time = get_start_time(curr_slot)
        curr_end_time = get_end_time(curr_slot)

        if prev_end_time >= curr_start_time:
            if curr_end_time > prev_end_time:
                new_time = [merged_slots[-1][0], curr_end_time]
                merged_slots[-1] = new_time
        else:
            merged_slots.append([curr_start_time, curr_end_time])

        prev_end_time = curr_end_time

    # from the list of merged meeting slots (merged_slots), generate the available slot for the new meeting
    curr_time = time_to_int(start_time)
    end_time = time_to_int(end_time)
    available_slots = []
    index = 0
    while curr_time < end_time and index < len(merged_slots):
        curr_start_time = merged_slots[index][0]
        curr_end_time = merged_slots[index][1]
        if curr_time < curr_start_time:
            time_available = merged_slots[index][0] - curr_time
            if number_to_minutes(time_available) >= duration:
                slot = f"{format_number_to_hour_min(curr_time)}-{format_number_to_hour_min(curr_start_time)}"
                available_slots.append(slot)
        index += 1
        curr_time = curr_end_time

    if curr_time < end_time and number_to_minutes(end_time-curr_time) >= duration:
        available_slots.append(f"{format_number_to_hour_min(curr_time)}-{format_number_to_hour_min(end_time)}")
    return available_slots


def time_to_int(time):
    return int(time.replace(':', ''))

def get_start_time(meeting_schedule):
    start_time = meeting_schedule.split("-")[0]
    return time_to_int(start_time)

def get_end_time(meeting_schedule):
    end_time = meeting_schedule.split("-")[1]
    return time_to_int(end_time)

def number_to_minutes(number):
    return number*60/100

def format_number_to_hour_min(number):
    number = str(number)
    if len(number) == 4:
        return f"{number[0:2]}:{number[-2:]}"
    return f"0{number[0]}:{number[-2:]}"
