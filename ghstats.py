import os
import json
import requests
import sys
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd


GITHUB_API_TOKEN = os.environ["GITHUB_API_TOKEN"]
GITHUB_API_URL = "https://api.github.com/graphql"


def get_github_users_info(usernames, from_date, to_date):
    from_date_obj = datetime.strptime(from_date, "%Y-%m-%d").strftime("%Y-%m-%dT00:00:00Z")
    to_date_obj = datetime.strptime(to_date, "%Y-%m-%d").strftime("%Y-%m-%dT23:59:59Z")

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
                    repositoriesContributedTo(last: 5, includeUserRepositories: false) {{
                        totalCount
                        nodes {{
                            name
                            isPrivate
                            createdAt
                            updatedAt
                            pushedAt
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

        if "errors" in response.json():
            print(response.json())
            sys.exit(1)

        user_info = response.json()["data"]["user"]
        users_info.append(user_info)

    return users_info


def plot_users_contributions_pie(users_info):
    labels = []
    sizes = []

    for user_info in users_info:
        username = user_info["name"]
        total_contributions = user_info["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        labels.append(username)
        sizes.append(total_contributions)

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    ax.set(title='Contributions comparison')
    handles, _ = ax.get_legend_handles_labels()
    ax.legend(handles, labels, loc="best")
    plt.show()


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


def show_infos(users_info):
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

        print("\nContributions (last 5):")
        for rc in user_info["repositoriesContributedTo"]["nodes"]:
            rc['primaryLanguage'] = rc['primaryLanguage'] or {"name":"null"}
            print(f"- Name: {rc['name']}, Private: {rc['isPrivate']}, Primary lang: {rc['primaryLanguage']['name']}, Created at: {rc['createdAt']}, Last push: {rc['pushedAt']}, Owner: {rc['owner']['login']}")


        print("\n==========================================================================================================")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python ghstats.py <username> <from_date> <to_date>")
        print("Dates should be in format: YYYY-MM-DD")
        sys.exit(1)

    usernames = sys.argv[1].split(",")
    from_date = sys.argv[2]
    to_date = sys.argv[3]

    users_info = get_github_users_info(usernames, from_date, to_date)
    #plot_contributions_by_type(users_info)
    show_infos(users_info)

