# GitHub Stats

This is a Python script to retrieve GitHub stats for one or more users and display them in different ways.

## Requirements

```sh
pip install requests matplotlib pandas
```

## Usage

To use this script, you need to generate a [GitHub API token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with at least the repo and user scope

`python ghstats.py [-h] [--from_date FROM_DATE] [--to_date TO_DATE] [--plot {contributions,comparison}] username [username ...]`

example
```sh
GITHUB_API_TOKEN=<your_token_here> python ghstats.py user1 user2 user3 --from_date 2023-01-01 --to_date 2023-04-22
```

**Positional arguments**
- `username`: One or more GitHub usernames separated by spaces.

**Optional arguments**
- `-h`, `--help`: Show the help message and exit.
- `--from_date FROM_DATE`: The start date for the activity data in the format `YYYY-MM-DD`. Defaults to the first day of the current year.
- `--to_date TO_DATE`: The end date for the activity data in the format `YYYY-MM-DD`. Defaults to the current date.
- `--plot {contributions,comparison}`: Choose the plotting method. Available options are contributions and comparison. If this option is not provided, the script will display detailed user activity information in the console output.

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


