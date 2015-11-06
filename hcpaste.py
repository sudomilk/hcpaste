import argparse
import requests
import config
import string
import sys

#set up the vars from config
hc_api_url = os.environ['HCP_HC_API_URL']
hc_api_headers = os.environ['HCP_HC_API_HEADERS']


#parse the arguments
parser = argparse.ArgumentParser(
    description='pipe to this command; sends the piped stuff to a hipchat user',
    prog='hcpaste'
    )
parser.add_argument(
    'user',
    nargs=1,
    help='the user to send the message to'
    )
parser.add_argument(
    '--prefix', '-p',
    help='code or quote will prefix the message',
    choices=['code', 'quote']
    )
args = parser.parse_args() #args.prefix args.user
destination = args.user[0] #assign user arg
if destination == 'users': #do they need a list of the user mention names?
    r = requests.get(
        '{url}/user'.format(url=hc_api_url),
        params={'max-results': 1000},
        headers=hc_api_headers
        )
    users = r.json()['items']
    for user in users:
        try:
            print(user['name'] + '|@' + user['mention_name'])
        except UnicodeEncodeError:
            print(user['name'].encode('UTF-8') + '|@' + user['mention_name'].encode('UTF-8'))
    sys.exit()


#let's do it! everything is set
if args.prefix is not None:
    unfiltered_content = '/{prefix} {content}'.format(
        prefix=args.prefix,
        content=sys.stdin.read()
        )
else:
    unfiltered_content = unicode(sys.stdin.read())
#if content contains certain control sequences, it will break the hipchat convo
#let's kill the possibility of that happening (ie wp plugin status)
content = ''.join(s for s in unfiltered_content if s in string.printable)


hc_api_headers['Content-Type'] = 'text/plain'
r = requests.post(
    '{url}/user/{user}/message'.format(url=hc_api_url, user=destination),
    data=content,
    headers=hc_api_headers
    )
