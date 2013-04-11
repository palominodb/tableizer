class SinceStringMiddleware(object):
    def process_request(self, request):
        if request.REQUEST.get('since') is not None:
            request.session['since_string'] = request.REQUEST.get('since')
        elif not request.session.get('since_string'):
            request.session['since_string'] = '72h'
