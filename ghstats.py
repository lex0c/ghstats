import os
import json
import requests
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import argparse


GITHUB_API_TOKEN = os.environ["GITHUB_API_TOKEN"]
GITHUB_API_URL = "https://api.github.com/graphql"


def get_github_users_info(usernames, from_date, to_date):
    from_date_obj = from_date.strftime("%Y-%m-%dT00:00:00Z")
    to_date_obj = to_date.strftime("%Y-%m-%dT23:59:59Z")

    users_info = []

    for username in usernames:
        query = f"""
            query {{
                user(login: "{username}") {{
                    name
                    login
                    bio
                    location
                    email
                    repositories(last: 5) {{
                        totalCount
                        nodes {{
                            name
                            createdAt
                            owner {{
                                login
                            }}
                            primaryLanguage {{
                                name
                            }}
                        }}
                    }}
                    starredRepositories {{
                        totalCount
                    }}
                    organizations {{
                        totalCount
                    }}
                    contributionsCollection(from: "{from_date_obj}", to: "{to_date_obj}") {{
                        totalCommitContributions
                        totalIssueContributions
                        totalPullRequestContributions
                        totalPullRequestReviewContributions
                        totalRepositoriesWithContributedCommits
                        totalRepositoriesWithContributedIssues
                        totalRepositoriesWithContributedPullRequestReviews
                        totalRepositoriesWithContributedPullRequests
                    }}
                    repositoriesContributedTo(last: 5, includeUserRepositories: true) {{
                        totalCount
                        nodes {{
                            name
                            isPrivate
                            createdAt
                            updatedAt
                            pushedAt
                            object(expression: "main") {{
                                ... on Commit {{
                                    additions
                                    deletions
                                    history(first: 5) {{
                                        totalCount
                                        edges {{
                                            node {{
                                                message
                                                author {{
                                                    name
                                                    date
                                                }}
                                            }}
                                        }}
                                    }}
                                }}
                            }}
                            owner {{
                                login
                            }}
                            primaryLanguage {{
                                name
                            }}
                        }}
                    }}
                    issues(last: 5) {{
                        totalCount
                        nodes {{
                            title
                            url
                            createdAt
                        }}
                    }}
                    pullRequests(last: 5) {{
                        totalCount
                        nodes {{
                            title
                            url
                            createdAt
                        }}
                    }}
                }}
            }}
        """

        headers = {"Authorization": f"Bearer {GITHUB_API_TOKEN}"}
        response = requests.post(GITHUB_API_URL, json={"query": query}, headers=headers)

        if not "data" in response.json():
            print(response.json())
            sys.exit(1)

        user_info = response.json()["data"]["user"]
        users_info.append(user_info)

    return users_info


def plot_contributions_by_type(users_info):
    labels = []
    commit_contributions = []
    issue_contributions = []
    pr_contributions = []
    review_contributions = []

    for user_info in users_info:
        username = user_info["login"]
        total_commit_contributions = user_info["contributionsCollection"]["totalCommitContributions"]
        total_issue_contributions = user_info["contributionsCollection"]["totalIssueContributions"]
        total_pr_contributions = user_info["contributionsCollection"]["totalPullRequestContributions"]
        total_review_contributions = user_info["contributionsCollection"]["totalPullRequestReviewContributions"]
        labels.append(username)
        commit_contributions.append(total_commit_contributions)
        issue_contributions.append(total_issue_contributions)
        pr_contributions.append(total_pr_contributions)
        review_contributions.append(total_review_contributions)

    x = range(len(labels))
    width = 0.2

    fig, ax = plt.subplots()
    ax.bar(x, commit_contributions, width, label="Commits")
    ax.bar([i + width for i in x], issue_contributions, width, label="Issues")
    ax.bar([i + width * 2 for i in x], pr_contributions, width, label="Pull Requests")
    ax.bar([i + width * 3 for i in x], review_contributions, width, label="Pull Request Reviews")

    ax.set_xticks([i + 1.5 * width for i in x])
    ax.set_xticklabels(labels)
    ax.set(title='Contributions by Type')
    ax.legend()

    plt.show()


def plot_users_comparison(users_info):
    users = [user_info["name"] or user_info["login"] for user_info in users_info]

    df = pd.DataFrame(columns=["User", "Additions", "Deletions"])

    for user_info in users_info:
        additions = 0
        deletions = 0

        for repo in user_info["repositoriesContributedTo"]["nodes"]:
            additions += repo["object"]["additions"]
            deletions += repo["object"]["deletions"]

        df = pd.concat([df, pd.DataFrame({"User": user_info["name"] or user_info["login"], "Additions": additions, "Deletions": deletions}, index=[0])], ignore_index=True)

    ax = df.plot.bar(x="User", y=["Additions", "Deletions"], rot=0)
    ax.set_title("Code additions and deletions by user")
    ax.set_xlabel("User")
    ax.set_ylabel("Lines of code")
    plt.show()


def show_infos(users_info):
    print(users_info)

    for user_info in users_info:
        print("==========================================================================================================\n")
        print(f"Name: {user_info['name']}")
        print(f"Username: {user_info['login']}")
        print(f"Bio: {user_info['bio']}")
        print(f"Location: {user_info['location']}")
        print(f"Email: {user_info['email']}")
        print(f"Starred Repositories: {user_info['starredRepositories']['totalCount']}")
        print(f"Total Commits: {user_info['contributionsCollection']['totalCommitContributions']}")
        print(f"Total Pull Request: {user_info['contributionsCollection']['totalPullRequestContributions']}")
        print(f"Total PR Reviews: {user_info['contributionsCollection']['totalPullRequestReviewContributions']}")

        print("\nIssues (last 5):")
        for issue in user_info["issues"]["nodes"]:
            print(f"- Title: {issue['title']}, URL: {issue['url']}, Created at: {issue['createdAt']}")

        print("\nPull Requests (last 5):")
        for pr in user_info["pullRequests"]["nodes"]:
            print(f"- Title: {pr['title']}, URL: {pr['url']}, Created at: {pr['createdAt']}")

        print(f"\nRepositories (last 5 of {user_info['repositories']['totalCount']}):")
        for repo in user_info["repositories"]["nodes"]:
            repo['primaryLanguage'] = repo['primaryLanguage'] or {"name":"null"}
            print(f"- Name: {repo['name']}, Primary lang: {repo['primaryLanguage']['name']}, Created at: {repo['createdAt']}")

        print(f"\nContributions (last 5 of {user_info['repositoriesContributedTo']['totalCount']}):")
        for rc in user_info["repositoriesContributedTo"]["nodes"]:
            rc['primaryLanguage'] = rc['primaryLanguage'] or {"name":"null"}
            print(f"- Name: {rc['name']}, Private: {rc['isPrivate']}, Primary lang: {rc['primaryLanguage']['name']}, Created at: {rc['createdAt']}, Last push: {rc['pushedAt']}, Owner: {rc['owner']['login']}")
            print(f"    - Lines: +{rc['object']['additions']} -{rc['object']['deletions']}")
            print(f"    - Commits (last 5):")
            for commit in rc['object']['history']['edges']:
                print(f"        - {commit['node']['message']} (author: {commit['node']['author']['name']}, {commit['node']['author']['date']})")


        print("\n==========================================================================================================")


def validate_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        raise argparse.ArgumentTypeError("Invalid date format. Dates should be in format: YYYY-MM-DD")


def start(args):
    try:
        users_info = get_github_users_info(args.usernames, args.from_date, args.to_date)
    except requests.exceptions.RequestException as e:
        print(f"Error while connecting to the GitHub API: {e}")
        sys.exit(1)
    except KeyError as e:
        print(f"Error while processing data: {e}")
        sys.exit(1)

    if args.plot == "contributions":
        plot_contributions_by_type(users_info)
    elif args.plot == "comparison":
        plot_users_comparison(users_info)
    else:
        show_infos(users_info)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="GitHub user statistics.")
    parser.add_argument("usernames", type=str, nargs="+", help="List of GitHub usernames (separated by spaces)")
    parser.add_argument("--from_date", type=validate_date, required=True, help="Start date for the statistics (format: YYYY-MM-DD)")
    parser.add_argument("--to_date", type=validate_date, required=True, help="End date for the statistics (format: YYYY-MM-DD)")
    parser.add_argument("--plot", type=str, choices=["contributions", "comparison"], help="Choose the plotting method: 'contributions' or 'comparison'")

    args = parser.parse_args()

    start(args)
