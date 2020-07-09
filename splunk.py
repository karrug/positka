import time
import json
import requests


def get_session(base_url):
    auth_url = "%s/services/auth/login" % (base_url)
    d = {"username": "admin", "password": "password", "output_mode": "json"}
    h = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
    }
    r = requests.post(auth_url, headers=h, data=d, verify=False)
    r = r.json()
    return r["sessionKey"]


def create_search_job(auth_header, base_url, query):
    url = "%s/services/search/jobs" % base_url
    d = {"search": "search %s" % query, "output_mode": "json"}
    r = requests.post(url, headers=auth_header, data=d, verify=False)
    r = r.json()
    return r["sid"]


def get_job_status(auth_header, base_url, job_id):
    url = "%s/services/search/jobs/%s" % (base_url, job_id)
    d = {"output_mode": "json"}
    r = requests.get(url, headers=auth_header, data=d, verify=False)
    r = r.json()
    return r["entry"][0]["content"]["dispatchState"]


def wait_for_job_completion(auth_header, base_url, job_id):
    while True:
        s = get_job_status(auth_header, base_url, job_id)
        print(">>> job status:", s)
        if s == "DONE":
            return
        time.sleep(2)


def get_chunked_job_results(auth_header, base_url, job_id, offset, count):
    url = "%s/services/search/jobs/%s/results" % (base_url, job_id)
    d = {"output_mode": "json"}
    p = {"offset": offset, "count": count}
    r = requests.get(url, headers=auth_header, data=d, params=p, verify=False)
    return r.json()["results"]


def get_job_results(auth_header, base_url, job_id):
    """
    max count is 50000
    max total results is 500000
    """
    offset = 0
    count = 50000
    print(">>> count:", count)
    all_results = []
    while True:
        print(">>> offset:", offset)
        r = get_chunked_job_results(auth_header, base_url, job_id, offset, count)
        all_results += r
        if len(r) < count:
            return all_results
        offset += count
        time.sleep(1)


def get_results(query, base_url):
    print(">>> search query:", query)

    s = get_session(base_url)
    auth_header = {"Authorization": "Splunk %s" % s}

    job_id = create_search_job(auth_header, base_url, query)
    print(">>> job_id: ", job_id)
    wait_for_job_completion(auth_header, base_url, job_id)

    results = get_job_results(auth_header, base_url, job_id)
    print(">>> retrieved results:", len(results))

    return results
