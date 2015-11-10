import json
import time
import urllib2

for page in range(1, 10):
    print("Requesting page={0}".format(page))
    response = urllib2.urlopen(
        'https://api.github.com/search/repositories?q=stars:<300+language:cpp&sort=stars&order=desc&page={0}&per_page=100'.format(page))
    result = json.loads(response.read())
    for item in result['items']:
        name = item['full_name']
        #print(name)
        owner = item['owner']['login']
        id = item['id']
        maintainers = urllib2.urlopen('https://api.github.com/repos/{name}/contributors?per_page=100'.format(name=name))
        m = json.loads(maintainers.read())
        # https://api.github.com/repos/nwjs/nw.js/contributors
        contributors_count = len(m)
        open_issues = item['open_issues_count']
        stars = item['stargazers_count']
        forks = item['forks_count']
        watchers = item['watchers']
        print("Contributors of {0} is: {1}, stars={2}, issues={3}, forks={4}, watchers={5}".format(
            name, contributors_count, stars, open_issues, forks, watchers))
        time.sleep(7)