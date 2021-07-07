# -*- coding: utf-8 -*-

import os
import requests

if __name__ == "__main__":
    print("hello world")

    clubhouse_api_token = os.environ["INPUT_CLUBHOUSE_API_TOKEN"]
    print(clubhouse_api_token)

    open_id = os.environ["INPUT_PR_OPENED"]
    merged_id = os.environ["INPUT_PR_MERGED"]
    closed_id = os.environ["INPUT_PR_CLOSED"]

    print(open_id)
    print(merged_id)
    print(closed_id)