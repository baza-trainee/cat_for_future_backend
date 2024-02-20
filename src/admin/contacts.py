from sqladmin import ModelView

from src.contacts.models import Contacts


class ContactsAdmin(ModelView, model=Contacts):
    column_list = [
        Contacts.phone_first,
        Contacts.phone_second,
        Contacts.email,
        Contacts.post_address,
        Contacts.facebook,
        Contacts.instagram,
    ]
    can_export = False
    can_delete = False
    can_create = False
