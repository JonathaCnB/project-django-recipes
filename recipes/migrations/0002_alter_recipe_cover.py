# Generated by Django 4.0.5 on 2022-06-19 17:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipe',
            name='cover',
            field=models.ImageField(blank=True, default='place_holder.png', upload_to='recipes/covers/', verbose_name='Imagem'),
        ),
    ]
