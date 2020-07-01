from allauth.account.adapter import DefaultAccountAdapter
from django.http import HttpResponse
import json
class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.username = data['username']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)

    # def ajax_response(self, request, response, redirect_to=None, form=None, data=None):
    #     data = {}
    #     status = response.status_code
    #     if redirect_to:
    #         status = 200
    #         data['location'] = redirect_to
    #     if form:
    #         if form.is_valid():
    #             status = 200
    #         else:
    #             status = 200
    #             data['form_errors'] = form.errors
    #         if hasattr(response, 'render'):
    #             response.render()
    #         data = response.content
    #     return HttpResponse(json.dumps(data),
    #                         status=status,
    #                         content_type='application/json')
