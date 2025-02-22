# Generated by Django 5.1.2 on 2024-10-15 07:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('propertyapp', '0002_rename_document_tenant_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgentFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('feedback', models.TextField()),
                ('reply', models.CharField(blank=True, max_length=300, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='propertyapp.agent')),
            ],
        ),
        migrations.CreateModel(
            name='BuyNow',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('totalprice', models.IntegerField()),
                ('buynow_status', models.BooleanField(default=0)),
                ('address', models.TextField()),
                ('phone', models.CharField(max_length=10)),
                ('post', models.CharField(max_length=6)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userid', to='propertyapp.tenant')),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cardnumber', models.CharField(max_length=19)),
                ('cvv', models.CharField(max_length=3)),
                ('expiry_date', models.CharField(max_length=7)),
                ('buynowProduct', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='buynow', to='propertyapp.buynow')),
            ],
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(upload_to='media/')),
                ('name', models.CharField(max_length=100)),
                ('details', models.TextField()),
                ('price', models.CharField(max_length=100)),
                ('status', models.BooleanField(default=0)),
                ('agent', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property', to='propertyapp.agent')),
            ],
        ),
        migrations.AddField(
            model_name='buynow',
            name='property',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='property_id', to='propertyapp.property'),
        ),
        migrations.CreateModel(
            name='AddToCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cart_status', models.BooleanField(default=0)),
                ('tenant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenantid', to='propertyapp.tenant')),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='propertyid', to='propertyapp.property')),
            ],
        ),
        migrations.CreateModel(
            name='TenantFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(auto_now=True)),
                ('feedback', models.TextField()),
                ('reply', models.CharField(blank=True, max_length=300, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tenant', to='propertyapp.tenant')),
            ],
        ),
    ]
