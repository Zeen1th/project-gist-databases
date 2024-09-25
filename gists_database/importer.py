import requests
from datetime import datetime

def import_gists_to_database(db, username, commit=True):
    url = f"https://api.github.com/users/{username}/gists"
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f"Failed to retrieve gists for user {username}. Status code: {response.status_code}")

    gists_data = response.json()
    
    for gist_data in gists_data:
        db.execute("""
            INSERT INTO gists (github_id, html_url, git_pull_url, git_push_url, commits_url, forks_url, public, created_at, updated_at, comments, comments_url)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            gist_data['id'],
            gist_data['html_url'],
            gist_data['git_pull_url'],
            gist_data['git_push_url'],
            gist_data['commits_url'],
            gist_data['forks_url'],
            gist_data['public'],
            datetime.strptime(gist_data['created_at'], '%Y-%m-%dT%H:%M:%SZ'),
            datetime.strptime(gist_data['updated_at'], '%Y-%m-%dT%H:%M:%SZ'),
            gist_data['comments'],
            gist_data['comments_url']
        ))

    if commit:
        db.commit()
