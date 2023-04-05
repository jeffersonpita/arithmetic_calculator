# -*- coding: utf-8 -*-
from django.db import models, migrations

def insert_operations(apps, schema_editor):
    Operation = apps.get_model("api", "Operation")
    for item in [(1,1), (2,1), (3,2), (4,2), (5,3), (6,10)]:
        op = Operation(type=item[0],cost=item[1])
        op.save()

class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_operations),
    ]