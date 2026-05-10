from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Events", "0002_event_search_vector_and_more"),
    ]

    operations = [
        TrigramExtension(),
    ]
