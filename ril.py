import json
import urllib
import urllib2

class ReadItLater:
    """
    @todo: add status checks
    """
    def __init__(self, **kwargs):
        self.STATUS_SUCCESS     = 200
        self.STATUS_INVALID     = 400
        self.STATUS_DENIED      = 401
        self.STATUS_EXCEEDED    = 403
        self.STATUS_MAINTENANCE = 503

        URL_BASE = 'https://readitlaterlist.com/v2'
        
        self.URLS = { 'add': "%s/add" % (URL_BASE), 
            'send': "%s/send" % (URL_BASE),
            'stats': "%s/stats" % (URL_BASE),
            'get': "%s/get" % (URL_BASE),
            'auth': "%s/auth" % (URL_BASE),
            'signup': "%s/signup" % (URL_BASE),
            'api': "%s/api" % (URL_BASE)
        }

        self.api_key = kwargs['api_key'] or None
        self.user = kwargs['user'] or None
        self.password = kwargs['password'] or None
        self.last_response = None

    def add(self, url, title):
        return self.query('add', url=url, title=title)

    """
    url https://readitlaterlist.com/v2/auth?username=name&password=123&apikey=yourapikey
    returns response code
    """
    def auth(self):
        return self.query('auth')


    """
    Allows you to send bulk request for changes. 
    actions: new, read, update_title, update_tags
    urls=[{'url': 'http://google.com', 'title': 'Google'}, {'url':'http://news.ycombinator.com', 'title': 'HN'}])

    url example: https://readitlaterlist.com/v2/send?username=name&password=123&apikey=yourapikey&new=%7B%220%22%3A%20%7B%22url%22%3A%20%22http%3A//google.com%22%2C%20%22title%22%3A%20%22Google%22%7D%2C%20%221%22%3A%20%7B%22url%22%3A%20%22http%3A//news.ycombinator.com%22%2C%20%22title%22%3A%20%22HN%22%7D%7D
    data: json example {'0':{'url':'http://docs.python.org/library/json.html','title':'Python Json'},'1':{'url':'http://www.reddit.com/help/gold','title':'Reddit Help Gold'}}))

    returns response code
    """
    def send(self, **kwargs):
        counter = 0

        action  = kwargs['action'] or None
        urls    = kwargs['urls']   or None
        ret     = False

        if action and urls:
            data = {}
            for i in urls:
                url = i['url']
                title = i['title']
                data[counter] = { "url": url,
                        "title": title
                }
                counter += 1
            ret = self.query('send', action=action, data=data)
        return ret

    """
    url https://readitlaterlist.com/v2/get?username=name&password=123&apikey=yourapikey&since=1245638446
    returns {"status":1,"list":{"54239972":{"item_id":"54239972","title":"Best Practices of Combining Typefaces - Smashing Magazine","url":"http:\/\/www.smashingmagazine.com\/2010\/11\/04\/best-practices-of-combining-typefaces\/","time_updated":"1288912743","time_added":"1288912743","state":"0"}},"since":1289060343,"complete":1}
    """
    def get(self):
        return self.query('get')
    
    """
    url example https://readitlaterlist.com/v2/stats?username=user&password=pass&apikey=api_key
    returns {"user_since":1288795930,"count_list":"1","count_read":"0","count_unread":"1"}
    """
    def stats(self):
        return self.query('stats')
    
    def api(self):
        return self.query('api')
    
    def query(self, method, **kwargs):
        user = self.user
        password = self.password
        api_key = self.api_key
        base_url = self.URLS[method]
        url = "%(base_url)s?username=%(user)s&password=%(password)s&apikey=%(api_key)s" % locals()

        if kwargs and kwargs['data'] and kwargs['action']:
            action = kwargs['action']
            data = urllib.quote(json.dumps(kwargs['data']))
            url = "%s&%s=%s" % (url, action, data)
        
        res = False
        res = urllib2.urlopen(url)
        self.last_response = res

        # debug statements
        #print res.read()
        #print res.geturl()
        #print res.info()
