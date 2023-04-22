# GitHub Stats

This is a Python script to retrieve GitHub stats for one or more users and display them in different ways.

## Requirements

- Python 3.x
- matplotlib
- pandas
- requests

## Usage

To use this script, you need to generate a [GitHub API token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with at least the repo and user scope

```sh
GITHUB_API_TOKEN=<your_token_here> python ghstats.py <username1,username2> <from_date> <to_date>
```

- `<username1,username2>` is a comma-separated list of usernames to retrieve stats for
- `<from_date>` is the starting date for the stats, in the format YYYY-MM-DD
- `<to_date>` is the ending date for the stats, in the format YYYY-MM-DD

## Infos available

The script retrieves the following information for each user:

- Name
- Username
- Bio
- Location
- Email
- Starred Repositories count
- Total Commits count
- Total Pull Request count
- Total Pull Request Review count
- Issues (last 5)
- Pull Requests (last 5)
- Repositories (last 5 of the total count)
- Contributions (last 5)

It then displays the retrieved information in the console



