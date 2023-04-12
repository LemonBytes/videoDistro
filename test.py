from math import floor


SEGEMENT = 55


def get_cutting_part(seconds, segment_time=SEGEMENT):
    if seconds % segment_time <= 1 and segment_time <= SEGEMENT:
        return segment_time
    elif segment_time <= 30:
        return segment_time
    return get_cutting_part(seconds=seconds, segment_time=segment_time - 1)


print(get_cutting_part(714))
