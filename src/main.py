import os
import requests

if __name__ == "__main__":
    print("hello world")
    clubhouse_api_token = os.environ["INPUT_CLUBHOUSE_API_TOKEN"]
    config_path = os.environ["INPUT_CONFIG_PATH"]
    my_output = f"Hello {clubhouse_api_token}"

    print(my_output)
    print(config_path)
