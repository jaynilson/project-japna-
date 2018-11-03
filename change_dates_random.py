import random
from datetime import datetime, timedelta
from git import Repo

def random_date(start, end):
    return start + timedelta(
        seconds=random.randint(0, int((end - start).total_seconds())),
    )

def to_git_date(date):
    return date.strftime("%Y-%m-%dT%H:%M:%S")

start_date = datetime(2017, 2, 1)
end_date = datetime(2019, 12, 28)

repo = Repo('.')

for commit in repo.iter_commits():
    # Generate random dates
    new_author_date = random_date(start_date, end_date)
    new_committer_date = random_date(start_date, end_date)

    # Update commit information
    commit_author = commit.author
    commit_committer = commit.committer
    commit_author_date = new_author_date
    commit_committer_date = new_committer_date
    commit_message = commit.message

    # Create a new commit with the updated information
    repo.git.filter_branch(
        '--commit-filter',
        f'GIT_AUTHOR_NAME="{commit_author.name}" '
        f'GIT_AUTHOR_EMAIL="{commit_author.email}" '
        f'GIT_AUTHOR_DATE="{to_git_date(commit_author_date)}" '
        f'GIT_COMMITTER_NAME="{commit_committer.name}" '
        f'GIT_COMMITTER_EMAIL="{commit_committer.email}" '
        f'GIT_COMMITTER_DATE="{to_git_date(commit_committer_date)}" '
        f'git commit-tree "{commit.tree.hexsha}"'
    )
