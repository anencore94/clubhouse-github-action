# -*- coding: utf-8 -*-
"""
clubhouse github action
"""
import json
import os
import re
import sys
from typing import Set

import requests


def get_desired_workflow_state_id(state: str) -> str:
    """
    get desired workflow_state_id by current pr's status

    :param state: current pr's state
    :return: workflow_state_id
    """
    open_workflow_state_id = os.environ["INPUT_PR_OPENED"]
    closed_workflow_state_id = os.environ["INPUT_PR_CLOSED"]

    print(f"current pr status is {state}")
    if state == "open":
        return open_workflow_state_id

    return closed_workflow_state_id


def parse_story_from_pr_body(body: str) -> Set[str]:
    """
    parse keyword (Fixes [ch-xxx]) from pr_body

    :param body: the body of pull request
    :return: stories set
    """
    candidates = []
    stories: Set[str] = set()
    regexp = re.compile(r"Fixes \[ch-\d+\]")

    if regexp.search(body):
        print("matched")
        candidates = re.findall(regexp, body)
        print(candidates)

    if not candidates:
        print("no matching stories")
        return stories

    for candidate in candidates:
        stories.add(candidate[10:-1])

    return stories


if __name__ == "__main__":
    gh_token = os.environ["INPUT_GITHUB_TOKEN"]
    pr_num = os.environ["INPUT_PR_NUMBER"]
    repo_name = os.environ["GITHUB_REPOSITORY"]
    clubhouse_api_token = os.environ["INPUT_CLUBHOUSE_API_TOKEN"]
    open_id = os.environ["INPUT_PR_OPENED"]
    closed_id = os.environ["INPUT_PR_CLOSED"]

    if not pr_num:
        print("This is not triggered by pr," " so skip this github action workflow")
        sys.exit(0)

    # TODO detailed validation check
    if not (gh_token and repo_name and clubhouse_api_token and open_id and closed_id):
        print("some of your inputs are invalid")
        sys.exit(1)

    # Fetch current pull request body
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {gh_token}",
    }
    URL = f"https://api.github.com/repos/{repo_name}/pulls/{pr_num}"

    print("----------Sending github api----------")
    res = requests.get(url=URL, headers=headers)
    try:
        res.raise_for_status()
    except requests.exceptions.HTTPError as ex:
        print(ex)
        # if not 200
        print(res.status_code)
        print(res.json())
        print("github token or github relevant inputs are invalid")
        sys.exit(1)

    pr_body = res.json()["body"]
    print(f"pr_body is {pr_body}")

    # pass, if body is empty
    if not pr_body:
        sys.exit(0)

    # parse story id from pr_body
    story_ids = parse_story_from_pr_body(body=pr_body)

    # pass, if no story id found in PR body
    if len(story_ids) == 0:
        print("no story found in PR body")
        sys.exit(0)

    # check current pr's state and find desired_workflow_state_id
    desired_workflow_state_id = get_desired_workflow_state_id(state=res.json()["state"])

    print(
        f"----------Following stories: {story_ids} "
        f"will be moved to {desired_workflow_state_id}----------"
    )

    # send request to move stories' workflow state
    headers = {
        "Content-Type": "application/json",
        "Clubhouse-Token": clubhouse_api_token,
    }
    BASE_URL = "https://api.clubhouse.io/api/v3/stories/"
    request_body = {"workflow_state_id": str(desired_workflow_state_id)}

    print("----------Sending clubhouse api----------")
    for story_id in story_ids:
        if story_id == "0":
            continue
        res = requests.put(
            url=BASE_URL + story_id, data=json.dumps(request_body), headers=headers
        )
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as ex:
            print(ex)
            # if not 200
            # TODO error msg 가 not found 이면 pass
            print(res.status_code)
            print(res.text)
            sys.exit(1)

    print("----------Clubhouse story workflow updated successfully!----------")
