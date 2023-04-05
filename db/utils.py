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
