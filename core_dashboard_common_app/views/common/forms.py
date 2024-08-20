"""
Common Forms
"""

from django import forms

from core_main_app.components.user import api as user_api


class ActionForm(forms.Form):
    """
    Form to select the action in the user dashboard.
    """

    actions = forms.ChoiceField(label="", required=True, choices=[])

    def __init__(self, list_actions):
        super().__init__()
        self.fields["actions"].choices = list_actions


class UserForm(forms.Form):
    """
    Form to select a user.
    """

    users = forms.ChoiceField(label="", required=True)
    user_options = []

    def __init__(self, current_user):
        self.user_options = []
        self.user_options.append(("", "-----------"))

        # We retrieve all users
        sort_users = user_api.get_active_users()
        # We sort by username, case insensitive
        sort_users = sorted(sort_users, key=lambda s: s.username.lower())

        # We add them
        for user in sort_users:
            if user.id != current_user.id or current_user.is_superuser:
                self.user_options.append((user.id, user.username))

        super().__init__()
        self.fields["users"].choices = []
        self.fields["users"].choices = self.user_options
