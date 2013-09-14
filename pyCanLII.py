import urllib, urllib2, json

class CanLIIException(Exception):
    def __str__(self):
        return repr(self.args)

class CanLII(object):

    def __init__(self, api_key, language = 'en'):
        self.address = "http://api.canlii.org/v1/"
        self.language = language
        self.api_key = api_key

    def call(self, action, database = None, case = None, limit = 100, offset = 0,
            trailing_action=None):
        d = {'resultCount': limit, 'offset': offset, 'api_key': self.api_key}
        params = urllib.urlencode(dict((k,v) for k, v in d.iteritems() if v is not None))

        if database is None:
            path = "%s/%s" % (action, self.language)
        elif case is None:
            path = "%s/%s/%s" % (action, self.language, database)
        else:
            path = "%s/%s/%s/%s" % (action, self.language, database, case)

        if trailing_action:
            path = path + "/" + trailing_action

        url = urllib.basejoin(self.address, path) 

        r = urllib2.urlopen(url, params)
        response = json.loads(r.read())

        #canlii api returns code 200 OK even if there were errors.
        if type(response) is list and'error' in response[0].keys():
            raise CanLIIException(response[0]['message'])

        return response

    def caseBrowse(self, *args, **kwargs):
        return self.call('caseBrowse', *args, **kwargs)

    def legislationBrowse(self, *args, **kwargs):
        return self.call('legislationBrowse', *args, **kwargs)

    def citedCases(self, *args, **kwargs):
        return self.call('caseCitator', *args, trailing_action='citedCases',
            **kwargs)

    def citingCases(self, *args, **kwargs):
        return self.call('caseCitator', *args, trailing_action='citingCases',
            **kwargs)
