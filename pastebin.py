import urllib.parse
import urllib.request
from auth import PASTE_KEY

def paste(title, content):

    url = "https://pastebin.com/api/api_post.php"

    values = {'api_option' : 'paste',
            'api_dev_key' : PASTE_KEY,
            'api_paste_code' : content,
            'api_paste_private' : '0',
            'api_paste_name' : '{}.md'.format(title),
            'api_paste_expire_date' : 'N',
            'api_paste_format' : 'text'}
    data = urllib.parse.urlencode(values)
    data = data.encode('utf-8') # data should be bytes
    req = urllib.request.Request(url, data)
    with urllib.request.urlopen(req) as response:
        the_page = response.read()
    return the_page

