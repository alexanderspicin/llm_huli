# Generated by Django 4.2.13 on 2024-06-26 13:37

from django.db import migrations
from pgvector.django import VectorExtension


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        VectorExtension()
    ]
