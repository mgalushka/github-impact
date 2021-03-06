import base64
import json
import sys
import time
import urllib2

from datetime import datetime, timedelta

ROOT = 'https://api.github.com'


def start_script(auth_string):
    for page in range(1, 10):
        print("Requesting page={0}".format(page))
        time.sleep(2)
        request = urllib2.Request((
            '{root}/search/repositories?database&q=stars:<50+language:cpp&sort=stars&'
            'order=desc&page={page}&per_page=100'
        ).format(
            root=ROOT,
            page=page,
        ))
        request.add_header("Authorization", "Basic {0}".format(auth_string))
        response = urllib2.urlopen(request)

        result = json.loads(response.read())
        for item in result['items']:
            name = item['full_name']
            # owner = item['owner']['login']

            created_at = item['created_at'][:10]
            updated_at = item['updated_at'][:10]
            pushed_at = item['pushed_at'][:10]

            # id = item['id']
            # time.sleep(6)
            request = urllib2.Request(
                '{root}/repos/{name}/contributors?per_page=100'.format(
                    root=ROOT,
                    name=name,
                ),
            )
            request.add_header("Authorization", "Basic {0}".format(auth_string))
            maintainers = urllib2.urlopen(request)

            m = json.loads(maintainers.read())
            contributors_count = len(m)
            open_issues = int(item['open_issues_count'])
            stars = int(item['stargazers_count'])
            forks = int(item['forks_count'])
            watchers = int(item['watchers'])

            if contributors_count < 5 or open_issues < 5:
                continue

            # time.sleep(6)
            request = urllib2.Request(
                '{root}/repos/{name}/commits?per_page=100'.format(
                    root=ROOT,
                    name=name,
                ))
            request.add_header("Authorization", "Basic {0}".format(auth_string))
            commits = urllib2.urlopen(request)

            # let's see how many commits happened to project recently
            # this is to evaluate how active this is
            project_commits = json.loads(commits.read())
            active_project = False
            last_commit = 'never'

            if len(project_commits) > 0:
                last_commit = \
                    project_commits[0]['commit']['committer']['date'][:10]
                count = 0
                date_now = datetime.now()
                LAST_30 = timedelta(days=-30)
                for commit in project_commits:
                    dt = commit['commit']['committer']['date'][:10]
                    if datetime.strptime(dt, '%Y-%m-%d') > date_now + LAST_30:
                        active_project = True
                    else:
                        active_project = False
                        break
                    count += 1
                    if count > 10:
                        break

            if active_project:
                print((
                    "Project: {0} - is_active={1}, contributors={2}, stars={3}, issues={4}, "
                    "forks={5}, watchers={6}, created={7}, updated={8}, pushed={9}, last commit={10}"
                ).format(
                    name, 'TRUE!' if active_project else 'false',
                    contributors_count, stars, open_issues, forks, watchers,
                    created_at,
                    updated_at, pushed_at, last_commit,
                ))


if __name__ == "__main__":
    auth = base64.encodestring(
        '{0}:{1}'.format(sys.argv[1], sys.argv[2]),
    ).strip()
    start_script(auth)
