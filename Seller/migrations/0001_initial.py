# Generated by Django 4.0 on 2022-01-12 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Brand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('brandName', models.CharField(max_length=50, unique=True)),
                ('brandImage', models.ImageField(upload_to='Brand/images')),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('category_id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category_name', models.CharField(max_length=500, unique=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Seller.category')),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('product_id', models.AutoField(primary_key=True, serialize=False)),
                ('gender', models.CharField(choices=[('ME', 'Men'), ('WO', 'Women'), ('KI', 'Kid')], default='ME', max_length=2)),
                ('product_title', models.CharField(max_length=50)),
                ('product_description', models.CharField(max_length=350, null=True)),
                ('product_price', models.IntegerField(max_length=100)),
                ('product_discount', models.IntegerField(max_length=100)),
                ('product_size', models.JSONField(null=True)),
                ('product_color', models.CharField(max_length=50)),
                ('product_image1', models.ImageField(null=True, upload_to='Product/images')),
                ('product_image2', models.ImageField(null=True, upload_to='Product/images')),
                ('product_image3', models.ImageField(null=True, upload_to='Product/images')),
                ('product_image4', models.ImageField(null=True, upload_to='Product/images')),
                ('product_image5', models.ImageField(null=True, upload_to='Product/images')),
                ('product_imageList', models.JSONField(null=True)),
                ('brandName', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.brand')),
                ('product_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.category')),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('sizeID', models.AutoField(primary_key=True, serialize=False)),
                ('size', models.CharField(max_length=50, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('sub_category', models.CharField(max_length=50)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.category')),
            ],
        ),
        migrations.CreateModel(
            name='ProductQuantity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(max_length=500)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.product')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.size')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='product_subcategory',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.subcategory'),
        ),
        migrations.CreateModel(
            name='CategorySizes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.category')),
                ('size', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Seller.size')),
            ],
        ),
    ]
