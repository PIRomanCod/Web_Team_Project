from django.views import View
from django.shortcuts import render
class BaseView(View):
    '''Decorator for all storageapp views to catch exceptions'''

    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            return render(request, 'storageapp/error.html', context={'error_message': f'Something goes wrong: {e}'})
        return response