# Generated by Django 4.0 on 2022-01-10 07:53

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('Seller', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buyer',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('profile_pic', models.ImageField(null=True, upload_to='Buyer/Images')),
                ('gender', models.CharField(max_length=10)),
                ('dob', models.DateField(max_length=10, null=True)),
                ('phoneNumber', models.CharField(max_length=50, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='BuyerWishlist',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.product')),
            ],
        ),
        migrations.CreateModel(
            name='BuyerCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.product')),
            ],
        ),
        migrations.CreateModel(
            name='BuyerCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('card_number', models.IntegerField(max_length=100)),
                ('card_name', models.CharField(max_length=500)),
                ('expiry_date', models.DateField()),
                ('cvc_num', models.IntegerField(max_length=100)),
                ('token', models.CharField(max_length=500)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
            ],
        ),
        migrations.CreateModel(
            name='BuyerAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('full_name', models.CharField(max_length=500)),
                ('address', models.TextField(max_length=500)),
                ('county', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=100)),
                ('street_number', models.IntegerField(max_length=50)),
                ('home_number', models.IntegerField(max_length=50)),
                ('postal_code', models.IntegerField(max_length=50)),
                ('address_type', models.CharField(choices=[('HO', 'House'), ('OF', 'Office')], max_length=2)),
                ('buyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Buyer.buyer')),
            ],
        ),
    ]
