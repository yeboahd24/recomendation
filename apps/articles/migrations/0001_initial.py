from django.db import migrations
from django.db import models


class Migration(migrations.Migration):
    initial = True
    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(db_index=True, max_length=255)),
                ('abstract', models.TextField()),
                ('body', models.TextField()),
                ('affiliations', models.TextField()),
                ('journal', models.TextField()),
                ('authors', models.CharField(max_length=255)),
                ('keywords', models.CharField(db_index=True, max_length=255)),
                ('url', models.CharField(max_length=255))
            ]
        ),
    ]
