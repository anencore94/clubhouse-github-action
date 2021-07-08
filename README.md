# clubhouse-github-action
github action to integrate clubhouse.io story


## Action Setup

- This is an example of using this github action
```yaml
name: Test

on:
  pull_request:
    types: [opened, synchronize, edited, reopened, closed]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - name: 'CH-GH-TEST'
      uses: anencore94/clubhouse-github-action@v1.0.0
      with:
        github_token: ${{ secrets.GITHUB_TOKEN }}
        pr_number: ${{ github.event.number }}
        clubhouse_api_token: ${{ secrets.CLUBHOUSE_API_TOKEN }} # you need to setup this
        pr_opened: 500001413 # you need to setup this
        pr_closed: 500001409 # you need to setup this
```

### Input parameters
- github_token
  - need to request github apis
    - recommend to use github workflows's temporary token (:`${{ secrets.GITHUB_TOKEN }}`)
- pr_number
  - need to fetch current pr's information
    - recommend to use github workflow's internal variable (:`${{ github.event.number }}`)
- **clubhouse_api_token**
  - need to request clubhouse apis
    - you could generate token by following [official docs](https://help.clubhouse.io/hc/en-us/articles/205701199-Clubhouse-API-Tokens)
    - and you need to store it in your repository secret by following [official docs](https://docs.github.com/en/actions/reference/encrypted-secrets)
- **pr_opened**
  - your desired clubhouse workflow state id when pr opened
- **pr_closed**
  - your desired clubhouse workflow state id when pr closed (or merged)