from django.views import View
from django.shortcuts import render
class BaseView(View):
    '''Decorator for all storageapp views to catch exceptions'''

    def dispatch(self, request, *args, **kwargs):
        """
        The dispatch function is the main entry point for class-based views.
        It calls the appropriate method, passing any arguments captured in the URL.
        The following methods are supported by default: get(), post(), put(), delete() and head().
        You can override this function to customize how your class-based view processes requests.

        :param self: Represent the instance of the object itself
        :param request: Get the request object
        :param args: Send a non-keyworded variable length argument list to the function
        :param kwargs: Pass keyworded, variable-length argument list to the function
        :return: A response object
        """
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return render(request, 'storageapp/error.html', context={'error_message': f'Something goes wrong: {e}',
                                                                    'title': 'Some error'})

        print(request)
        print(self.__class__.__name__)

        return response