# Generated by Django 4.2 on 2025-05-28 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_rename_created_date_user_created_at_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='created_at',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='profile',
            old_name='updated_at',
            new_name='updated_date',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='created_date',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='updated_at',
            new_name='updated_date',
        ),
    ]
