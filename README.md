# clubhouse-github-action
github action to integrate clubhouse.io story

### Now shortcut.io story

## About

- To automatically control shortcut(clubhouse) story with github PR
- Using this github action, you could get following benefits
  - If PR contains `Fixes [ch-xxxx]` or `Fixes [sc-xxxx]` on its body,
    - such clubhouse story will be moved automatically if such pr is opened or closed(merged)
    - all of github issue linking keywords are supported
      - close, closed, closes, fix, fixes, fixed, resolve, resolved, resolves

## Action Setup

- This is an example of using this github action
```yaml
name: Test

on:
  pull_request:  # you should use this github action with on:pull_request
    types: [opened, synchronize, edited, reopened, closed] # must contain opened and closed

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: 'Synchronize Github PR to Shortcut story'
      uses: anencore94/clubhouse-github-action@v2.1.0
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        pr_number: ${{ github.event.number }}
        shortcut_api_token: ${{ secrets.SHORTCUT_API_TOKEN }} # you need to setup this
        pr_opened: 500001413 # you need to setup this
        pr_closed: 500001409 # you need to setup this
        pr_wip: 500001411 # you need to setup this (Optional)
        wip_keyword: WIP # you need to setup this (Optional)
```

### Input parameters
- github_token
  - need to request github apis
    - recommend to use github workflows's temporary token (:`${{ secrets.GITHUB_TOKEN }}`)
- pr_number
  - need to fetch current pr's information
    - recommend to use github workflow's internal variable (:`${{ github.event.number }}`)
- **shortcut_api_token**
  - need to request shortcut apis 
    - you could generate token by following [official docs](https://help.shortcut.com/hc/en-us/articles/205701199-Shortcut-API-Tokens)
    - and you need to store it in your repository secret by following [official docs](https://docs.github.com/en/actions/reference/encrypted-secrets)
- **pr_opened**
  - your desired shortcut workflow state id when pr opened
- **pr_closed**
  - your desired shortcut workflow state id when pr closed (or merged)
- **pr_wip**
  - your desired shortcut workflow state id when pr is working in progress (Optional)
- **wip_keyword**
  - The keyword which indicates the pr is working in progress (Optional)
