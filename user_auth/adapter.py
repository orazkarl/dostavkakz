from allauth.account.adapter import DefaultAccountAdapter

class AccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        data = form.cleaned_data
        user.username = data['username']
        user.email = data['email']
        if 'first_name' in data.keys():
            user.first_name = data['first_name']
        if 'last_name' in data.keys():
            user.last_name = data['last_name']
        if 'phone' in data.keys():
            user.phone = data['phone']
        if 'password1' in data:
            user.set_password(data['password1'])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)

        if commit:
            user.save()
        return user
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
