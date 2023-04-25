# GitHub Stats

This is a Python script that retrieves and visualizes various GitHub user statistics. It uses the GitHub GraphQL API to gather data, including repository activity, contributions, issues, pull requests, and more.

```sh
usage: ghstats.py [-h] [--from_date FROM_DATE] [--to_date TO_DATE]
                  [--plot {contributions,comparison,activity}]
                  usernames [usernames ...]

positional arguments:
  usernames             GitHub usernames to analyze (comma-separated)

optional arguments:
  -h, --help            show this help message and exit
  --from_date FROM_DATE
                        Start date for the analysis (YYYY-MM-DD)
  --to_date TO_DATE     End date for the analysis (YYYY-MM-DD)
  --plot {contributions,comparison,activity}
                        Plotting option
```

## Requirements

```sh
pip install requests matplotlib pandas
```

## Usage

To use this script, you need to generate a [GitHub API token](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token) with at least the repo and user scope

`python ghstats.py [-h] [--from_date FROM_DATE] [--to_date TO_DATE] [--plot {contributions,comparison,activity}] username [username ...]`

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
- `--plot {contributions,comparison,activity}`: Choose the plotting method. Available options are contributions, comparison and activity. If this option is not provided, the script will display detailed user activity information in the console output.

OBS: activity only plots one user at a time.

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


## Develop

Clone

```sh
git clone https://github.com/yourusername/ghstats.git
cd ghstats
```

Install deps

```sh
pip install -r requirements.txt
```

Set the `GITHUB_API_TOKEN` environment variable

```sh
export GITHUB_API_TOKEN=<your_token_here>
```

Run

```sh
python ghstats.py user1 user2 user3 --from_date 2023-04-01 --to_date 2023-04-25
```

