# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-30 14:40


import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import django_grainy.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0008_alter_user_username_max_length"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="GroupPermission",
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
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grainy_permissions",
                        to="auth.Group",
                    ),
                ),
            ],
            options={
                "verbose_name": "Group Permission",
                "verbose_name_plural": "Group Permissions",
                "base_manager_name": "objects",
            },
        ),
        migrations.CreateModel(
            name="UserPermission",
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
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="grainy_permissions",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "User Permission",
                "verbose_name_plural": "User Permissions",
                "base_manager_name": "objects",
            },
        ),
    ]
