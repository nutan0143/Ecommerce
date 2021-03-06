# Generated by Django 2.2 on 2020-10-31 12:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('email_address', models.EmailField(blank=True, max_length=50, null=True, unique=True, verbose_name='Email Address')),
                ('name', models.CharField(blank=True, max_length=100, null=True, verbose_name='First Name')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False)),
                ('is_superuser', models.BooleanField(default=False, verbose_name='Super User')),
                ('is_staff', models.BooleanField(default=False, verbose_name='Staff')),
                ('is_active', models.BooleanField(default=True, verbose_name='Status')),
                ('is_online', models.BooleanField(default=False, verbose_name='User is online')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product_name', models.CharField(max_length=100, verbose_name='Product Name')),
                ('image', models.TextField(verbose_name='Image')),
                ('type_of_product', models.CharField(max_length=100, verbose_name='Type of product')),
                ('decription', models.TextField(verbose_name='Description')),
                ('price', models.IntegerField(verbose_name='Product price')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BrowserCart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('added', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('browser_finger', models.CharField(max_length=225, verbose_name='Browser finger print')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.Product')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
