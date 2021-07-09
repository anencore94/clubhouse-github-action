# -*- coding: utf-8 -*-
import json
import os
import re

import requests


def get_desired_workflow_state_id(state):
    open_workflow_state = os.environ["INPUT_PR_OPENED"]
    closed_id = os.environ["INPUT_PR_CLOSED"]

    print(f"current pr status is {state}")
    if state == "open":
        return open_workflow_state

    return closed_id


def parse_from_pr_body(body):
    regexp = re.compile(r'Fixes \[ch-\d+\]')
    if regexp.search(body):
        print('matched')
        candidates = re.findall(regexp, body)
        print(candidates)

    return candidates


if __name__ == "__main__":
    print("hello")
    gh_token = os.environ["INPUT_GITHUB_TOKEN"]
    pr_num = os.environ["INPUT_PR_NUMBER"]  # 1
    repo_name = os.environ["GITHUB_REPOSITORY"]  # anencore94/clubhouse-github-action
    clubhouse_api_token = os.environ["INPUT_CLUBHOUSE_API_TOKEN"]
    open_id = os.environ["INPUT_PR_OPENED"]
    closed_id = os.environ["INPUT_PR_CLOSED"]

    # TODO detailed validation check
    if not (gh_token and pr_num and repo_name and clubhouse_api_token and open_id and closed_id):
        print("some of your inputs are invalid")
        exit(1)

    # Fetch current pull request body
    headers = {"Accept": "application/vnd.github.v3+json", "Authorization": f"token {gh_token}"}
    URL = f"https://api.github.com/repos/{repo_name}/pulls/{pr_num}"

    print("sending github api")
    res = requests.get(url=URL, headers=headers)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # if not 200
        print(res.status_code)
        print(res.json())
        print("github token or github relevant inputs are invalid")
        exit(1)

    pr_body = res.json()["body"]
    print(f"pr_body is {pr_body}")

    # parse story id from pr_body
    stories = set()
    for candidate in parse_from_pr_body(body=pr_body):
        stories.add(candidate[10:-1])  # if candidate : Fixes [ch-xxxx], story : xxxx
    
    # pass, if no story id found
    if len(stories) == 0:
        print("no story found in PR body")
        exit(0)

    print(stories)

    # check current pr's state and find desired_workflow_state_id
    desired_workflow_state_id = get_desired_workflow_state_id(state=res.json()["state"])

    # send request to move storys' workflow state
    headers = {"Content-Type": "application/json", "Clubhouse-Token": clubhouse_api_token}
    BASE_URL = "https://api.clubhouse.io/api/v3/stories/"

    request_body = {
        "workflow_state_id": str(desired_workflow_state_id)
    }

    print("sending clubhouse api")
    for story in stories:
        if story == "0":
            continue
        res = requests.put(url=BASE_URL + story, data=json.dumps(request_body), headers=headers)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            # if not 200
            # TODO error msg 가 not found 이면 pass
            print(res.status_code)
            print(res.text)
            exit(1)

    print("clubhouse story workflow updated successfully!")
