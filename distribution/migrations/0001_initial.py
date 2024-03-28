# Generated by Django 4.2.11 on 2024-03-27 11:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255, verbose_name='имя')),
                ('last_name', models.CharField(max_length=255, verbose_name='фамилия')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='email')),
                ('comment', models.TextField(blank=True, null=True, verbose_name='комментарий')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
            ],
            options={
                'verbose_name': 'клиент',
                'verbose_name_plural': 'клиенты',
            },
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attempt_time', models.DateTimeField(auto_now_add=True, verbose_name='дата попытки')),
                ('status', models.CharField(choices=[('success', 'Success'), ('failed', 'Failed')], max_length=20, verbose_name='статус')),
                ('response', models.TextField(blank=True, null=True, verbose_name='ответ')),
            ],
            options={
                'verbose_name': 'лог',
                'verbose_name_plural': 'логи',
            },
        ),
        migrations.CreateModel(
            name='MailingEvent',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField(verbose_name='время начала рассылки')),
                ('end_time', models.DateTimeField(blank=True, null=True, verbose_name='время окончания рассылки')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='дата изменения')),
                ('frequency', models.CharField(choices=[('once', 'Однократно'), ('daily', 'Ежедневно'), ('weekly', 'Еженедельно'), ('monthly', 'Ежемесячно')], max_length=20, verbose_name='периодичность')),
                ('status', models.CharField(choices=[('created', 'Создано'), ('started', 'Начато'), ('completed', 'Завершено')], default='created', max_length=20, verbose_name='статус')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активация рассылки')),
                ('clients', models.ManyToManyField(related_name='mailing_events', to='distribution.client', verbose_name='клиенты')),
            ],
            options={
                'verbose_name': 'рассылка',
                'verbose_name_plural': 'рассылки',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255, verbose_name='тема письма')),
                ('body', models.TextField(verbose_name='тело письма')),
                ('mailing_event', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='distribution.mailingevent', verbose_name='рассылка')),
            ],
            options={
                'verbose_name': 'сообщение',
                'verbose_name_plural': 'сообщения',
            },
        ),
    ]
