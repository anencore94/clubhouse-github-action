# -*- coding: utf-8 -*-
"""
clubhouse github action
"""
import json
import re
import sys
from typing import Set

import requests
from pydantic import BaseSettings, Field


def parse_story_from_pr_body(body: str) -> Set[str]:
    """
    parse keyword (Fixes [ch-xxx]) from pr_body

    :param body: the body of pull request
    :return: stories set
    """
    candidates = []
    stories: Set[str] = set()

    regexp = re.compile(
        r"(fix|fixes|fixed|resolve|resolved|resolves|close|closed|closes)"
        r"\s+"
        r"(\[ch-\d+\]|\[sc-\d+\])",
        re.IGNORECASE,
    )

    for match in regexp.finditer(body):
        match_string = match.group()
        print("matched :", match_string)
        candidates.append(match_string)

    if not candidates:
        print("no matching stories")
        return stories

    for candidate in candidates:
        story = candidate.split()[-1][4:-1]
        print("story :", story)
        stories.add(story)

    return stories


# pylint: disable=too-few-public-methods
class Settings(BaseSettings):
    """
    Env variables
    """

    gh_token: str = Field(..., env="INPUT_GITHUB_TOKEN")
    pr_num: str = Field(..., env="INPUT_PR_NUMBER")
    repo_name: str = Field(..., env="GITHUB_REPOSITORY")
    shortcut_api_token: str = Field(..., env="INPUT_SHORTCUT_API_TOKEN")
    open_id: str = Field(..., env="INPUT_PR_OPENED")
    closed_id: str = Field(..., env="INPUT_PR_CLOSED")


if __name__ == "__main__":
    setting = Settings()

    # Fetch current pull request body
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {setting.gh_token}",
    }
    URL = f"https://api.github.com/repos/{setting.repo_name}/pulls/{setting.pr_num}"

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
    pr_state = res.json()["state"]
    desired_workflow_state_id = (
        setting.open_id if pr_state == "open" else setting.closed_id
    )

    print(
        f"----------Following stories: {story_ids} "
        f"will be moved to {desired_workflow_state_id}----------"
    )

    # send request to move stories' workflow state
    headers = {
        "Content-Type": "application/json",
        "Shortcut-Token": setting.shortcut_api_token,
    }

    BASE_URL = "https://api.app.shortcut.com/api/v3/stories/"
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
