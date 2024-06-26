# Generated by Django 4.1.7 on 2024-04-25 00:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_curriculum_user_remove_subjectlesson_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='lessonobject',
            old_name='subject',
            new_name='course',
        ),
        migrations.AddField(
            model_name='lessonobject',
            name='parent_subject_lesson',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parent_subject_lesson', to='api.subjectlesson'),
        ),
        migrations.AlterField(
            model_name='subjectlesson',
            name='learning_type',
            field=models.CharField(blank=True, choices=[('text', 'text'), ('auditory', 'auditory'), ('interactive', 'interactive')], default='interactive', max_length=500, null=True),
        ),
    ]
