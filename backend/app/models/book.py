from tortoise import fields
from tortoise.models import Model


class Book(Model):
    id = fields.IntField(primary_key=True)
    title = fields.CharField(max_length=200)
    author = fields.CharField(max_length=100)
    isbn = fields.CharField(max_length=20, null=True)
    publisher = fields.CharField(max_length=120, null=True)
    published_year = fields.IntField(null=True)
    description = fields.TextField(null=True)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "books"

