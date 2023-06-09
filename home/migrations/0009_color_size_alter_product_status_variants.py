# Generated by Django 4.0.2 on 2022-04-09 12:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0008_product_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name='product',
            name='status',
            field=models.CharField(blank=True, choices=[('None', 'none'), ('Size', 'size'), ('Color', 'color')], default='None', max_length=200, null=True),
        ),
        migrations.CreateModel(
            name='Variants',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('amount', models.PositiveIntegerField(blank=True, null=True)),
                ('unit_price', models.PositiveIntegerField(blank=True, null=True)),
                ('discount', models.PositiveIntegerField(blank=True, null=True)),
                ('color_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.color')),
                ('product_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.product')),
                ('size_variant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='home.size')),
            ],
        ),
    ]
