from datetime import datetime, timedelta
import json
import time
import urllib2

ROOT = 'https://api.github.com'

for page in range(1, 10):
    print("Requesting page={0}".format(page))
    time.sleep(6)
    response = urllib2.urlopen((
        '{root}/search/repositories?q=stars:<300+language:cpp&sort=stars&'
        'order=desc&page={page}&per_page=100').format(
            root=ROOT,
            page=page,
        ),
    )
    result = json.loads(response.read())
    for item in result['items']:
        name = item['full_name']
        owner = item['owner']['login']
        id = item['id']
        time.sleep(6)
        maintainers = urllib2.urlopen(
            '{root}/repos/{name}/contributors?per_page=100'.format(
                root=ROOT,
                name=name,
            ),
        )
        m = json.loads(maintainers.read())
        contributors_count = len(m)
        open_issues = item['open_issues_count']
        stars = item['stargazers_count']
        forks = item['forks_count']
        watchers = item['watchers']
        time.sleep(6)
        commits = urllib2.urlopen('{root}/repos/{name}/commits?per_page=100'.format(
            root=ROOT,
            name=name,
        ))
        c = json.loads(commits.read())
        active_project = False
        last_commit = 'never'

        if len(c) > 0:
            last_commit = c[0]['commit']['committer']['date'][:10]
            count = 0
            date_now = datetime.now()
            for commit in c:
                dt = commit['commit']['committer']['date'][:10]
                if datetime.strptime(dt, '%Y-%m-%d') > date_now + timedelta(days=-30):
                    active_project = True
                else:
                    active_project = False
                    break
                count = count + 1
                if count > 10:
                    break

        print((
            "Project: {0} - is_active={1}, contributors={2}, stars={3}, issues={4}, "
            "forks={5}, watchers={6}, last commit={7}").format(
            name, 'TRUE!' if active_project else 'false',
            contributors_count, stars, open_issues, forks, watchers, last_commit,
        ))
