# Generated migration for adding is_superadmin field

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_superadmin',
            field=models.BooleanField(default=False, help_text='Designates that this user has all permissions including user management.'),
        ),
    ]
