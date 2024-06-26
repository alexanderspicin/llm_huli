# Generated by Django 4.2.13 on 2024-06-26 14:54

from django.db import migrations
import pgvector.django.vector


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_vectors',
            field=pgvector.django.vector.VectorField(blank=True, dimensions=10000, null=True),
        ),
    ]
