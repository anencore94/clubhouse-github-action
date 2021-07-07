# -*- coding: utf-8 -*-
import json
import os
import requests

def parse_from_pr_body():

    return str(6027)
    pass

if __name__ == "__main__":
    print(os.environ)
    with open('/github/workflow/event.json') as f:
        a = json.load(f)
        print(a)

    exit(1)
    clubhouse_api_token = os.environ["INPUT_CLUBHOUSE_API_TOKEN"]
    open_id = os.environ["INPUT_PR_OPENED"]
    merged_id = os.environ["INPUT_PR_MERGED"]
    closed_id = os.environ["INPUT_PR_CLOSED"]

    # TODO detailed validation check
    if not (clubhouse_api_token and open_id and merged_id and closed_id):
        print("some of your inputs are invalid")
        exit(1)

    # when pr opened with "Fixed [ch-xxxx]" in pr body
    # send request to move ch story
    headers = {"Content-Type": "application/json", "Clubhouse-Token": clubhouse_api_token}
    BASE_URL = "https://api.clubhouse.io/api/v3/stories/"

    parsed_story_id = parse_from_pr_body()
    request_body = {
        "workflow_state_id": str(open_id)
    }

    print("sending clubhouse api")
    res = requests.put(url=BASE_URL + parsed_story_id, data=json.dumps(request_body), headers=headers)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # if not 200
        print(res.status_code)
        print(res.text)
        exit(1)

    print("clubhouse story workflow updated successfully!")
