# Generated by Django 1.11.7 on 2020-04-10 09:59


import django.db.models.deletion
from django.db import migrations, models

import django_grainy.fields
import django_grainy.models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="APIKey",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("key", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="APIKeyPermission",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "namespace",
                    models.CharField(
                        help_text="Permission namespace (A '.' delimited list of keys",
                        max_length=255,
                    ),
                ),
                ("permission", django_grainy.fields.PermissionField(default=1)),
                (
                    "api_key",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grainy_permissions",
                        to="django_grainy_test.APIKey",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="ModelA",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
            ],
            options={
                "abstract": False,
            },
            bases=(django_grainy.handlers.GrainyMixin, models.Model),
        ),
        migrations.CreateModel(
            name="ModelB",
            fields=[
                (
                    "modela_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_grainy_test.ModelA",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("django_grainy_test.modela",),
        ),
        migrations.CreateModel(
            name="ModelC",
            fields=[
                (
                    "modela_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_grainy_test.ModelA",
                    ),
                ),
                (
                    "b",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="c",
                        to="django_grainy_test.ModelB",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("django_grainy_test.modela",),
        ),
        migrations.CreateModel(
            name="ModelD",
            fields=[
                (
                    "modela_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_grainy_test.ModelA",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("django_grainy_test.modela",),
        ),
        migrations.CreateModel(
            name="ModelX",
            fields=[
                (
                    "modela_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_grainy_test.ModelA",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("django_grainy_test.modela",),
        ),
        migrations.CreateModel(
            name="ModelY",
            fields=[
                (
                    "modela_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_grainy_test.ModelA",
                    ),
                ),
                (
                    "x",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="y",
                        to="django_grainy_test.ModelX",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("django_grainy_test.modela",),
        ),
        migrations.CreateModel(
            name="ModelZ",
            fields=[
                (
                    "modela_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="django_grainy_test.ModelA",
                    ),
                ),
                (
                    "y",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="z",
                        to="django_grainy_test.ModelY",
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
            bases=("django_grainy_test.modela",),
        ),
    ]
