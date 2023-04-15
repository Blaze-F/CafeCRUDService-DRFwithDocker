# Generated by Django 4.2 on 2023-04-14 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("name", models.CharField(max_length=20)),
                ("price", models.IntegerField()),
                ("cost", models.IntegerField()),
                ("barcode", models.CharField(max_length=13)),
                ("expire_date", models.DateTimeField()),
                ("description", models.CharField(max_length=200)),
                ("size", models.CharField(default="S", max_length=1)),
            ],
            options={
                "abstract": False,
                "managed": False,
            },
        ),
    ]
