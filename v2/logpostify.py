import re
from sys import argv
from os.path import join, dirname
from os import makedirs

logfile = argv[1]
log = open(logfile).read()
channel = logfile.split('/')[-1][:-3]
output_dir = join('issues', channel)
template = open('logs/post-issue-template.md').read()

splitter = '(\\*\\*Bill\\*\\*.*?\n\n)'

split_log = re.split(splitter, log)

rounds = []
rounddates = []
for line in split_log:
    if not line:
        continue
    if re.match(splitter, line):
        rounds.append([line])
        rounddates.append(re.search('[0-9]{4}-[0-9]{2}-[0-9]{2}', line).group())
    else:
        line = re.sub('-{3,}', '- - -', line)
        rounds[-1].append(line)

posts = []
for r in rounds:
    p = template.format(title='Round {}'.format(rounds.index(r)+1), table=channel, content=''.join(r))
    posts.append(p)

makedirs(output_dir, exist_ok=True)
for post, date in zip(posts, rounddates):
    fname = '{}-{}-Round-{}.md'.format(date, channel, posts.index(post)+1)
    open(join(output_dir, fname), 'w').write(post)
