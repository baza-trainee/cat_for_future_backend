from sqladmin import ModelView

from src.documents.models import Document


class DocumentAdmin(ModelView, model=Document):
    column_list = [
        Document.name,
        Document.media_path,
    ]
    can_export = False
    can_create = False
    can_delete = False
