import sys
import json
import urllib3
from splunk import get_results
from utils import send_email


def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    email = sys.argv[2]
    query = sys.argv[1]
    base_url = "https://ec2-3-86-128-32.compute-1.amazonaws.com:8089"

    results = get_results(query, base_url)
    with open("results.json", "w") as f:
        json.dump(results, f)

    # send_email(email, attachment)


main()
