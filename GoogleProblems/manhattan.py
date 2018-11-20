import statistics

def find_meeting_point(ray):
    """
    Find the best meeting point for an array of given locations of people (in x,y coords)
    Returns (x,y) of the meeting point
    """
    # according to google, the answer is the median, so here it is
    return (round(statistics.median([x[0] for x in ray])), round(statistics.median([y[1] for y in ray])))

print(find_meeting_point([(2,3), (4,5), (4,6)]))