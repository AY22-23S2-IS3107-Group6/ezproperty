import requests


def chunks(l, n):
    newn = int(1.0 * len(l) / n + 0.5)
    for i in range(0, n - 1):
        yield l[i * newn:i * newn + newn]
    yield l[n * newn - newn:]


def getUraApiHeaders():
    URA_API_ACCESSKEY = '84d7c27b-8dc6-4a34-9ea3-7769c174007c'

    # Fetches daily token which is needed along with access key for API calls
    header = {
        'Content-Type': 'application/json',
        'AccessKey': URA_API_ACCESSKEY,
        'Accept': 'application/json',
        'User-Agent': 'PostmanRuntime/7.28.4'  # Prevent return html
    }
    URA_API_TOKEN = requests.get(
        'https://www.ura.gov.sg/uraDataService/insertNewToken.action',
        headers=header).json()['Result']

    return {
        'Content-Type': 'application/json',
        'AccessKey': URA_API_ACCESSKEY,
        'Token': URA_API_TOKEN,
        'User-Agent': 'PostmanRuntime/7.30.1'
    }

# prepare floor_start_range & floor_end_range
def get_floor_range(floor):
    floor_start_range = generate_incrementing_floor_numbers(1, 100, 5)
    floor_end_range = generate_incrementing_floor_numbers(5, 100, 5)

    if (floor == 0):
        floor_start = 0
        floor_end = 0
    else:
        floor_start = find_closest_floor_number(floor, floor_start_range)
        floor_end = find_closest_floor_number(floor, floor_end_range)

    return {
        "floor_start": floor_start,
        "floor_end": floor_end,
    }

def generate_incrementing_floor_numbers(start, end, increment):
    floor_numbers_list = []
    current_num = start

    while current_num <= end:
        floor_numbers_list.append(current_num)
        current_num += increment

    return floor_numbers_list

def find_closest_floor_number(number, list_of_floor_numbers):
    closest_floor_number = None
    min_difference = float("inf")

    for num in list_of_floor_numbers:
        difference = abs(number - num)

        if difference < min_difference:
            closest_floor_number = num
            min_difference = difference

    return closest_floor_number
