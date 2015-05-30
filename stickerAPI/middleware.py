__author__ = 'Otacilio Lacerda'

import json


class FillRequestMiddleware:
    """
    Fill POST middleware gets the string from the request.body when it exists, convert to a dictionary and add it to
    the request.REQUEST.
    """

    #The constructor will run only once
    #def __init__(self):
        #Loads the configuration


    #It's called on each request, before Django decides which view to execute.
    def process_request(self, request):
        try:
            dict = json.loads(request.body)
            print 'DICT ', dict
            copy = request.POST.copy()
            copy.update(dict)
            request.POST = copy
        except:
            pass

    #Its called just before Django calls the view and after django decides the view.
    #def process_view(self, request, view_func, view_args, view_kwargs):
        # view_func is the view function (not a string)
        # view_args is a param list
        # view_kwargs is a dict use to pass params too

    #It's called if any exception is raised.
    # def process_exception(self, request, exception):
    #     pass

    #It's called just after the view has finished executing
    # def process_template_response(self, request, response):
    #     pass

    #It is called on all responses before they are returned to the browser. It is always executed.
    # def process_response(self, request, response):
    #     pass