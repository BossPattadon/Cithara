import uuid
from django.db import migrations, models


def gen_tokens(apps, schema_editor):
    Song = apps.get_model('music', 'Song')
    for song in Song.objects.all():
        song.share_token = uuid.uuid4()
        song.save(update_fields=['share_token'])


class Migration(migrations.Migration):

    dependencies = [
        ('music', '0002_songgeneration_task_id_alter_songgeneration_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='share_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(gen_tokens, migrations.RunPython.noop),
        migrations.AlterField(
            model_name='song',
            name='share_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]
