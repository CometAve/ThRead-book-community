# Generated by Django 4.2.13 on 2025-04-11 10:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(choices=[('소설/시/희곡', '소설/시/희곡'), ('경제/경영', '경제/경영'), ('자기계발', '자기계발'), ('인문/교양', '인문/교양'), ('과학', '과학'), ('취미/실용', '취미/실용'), ('어린이/청소년', '어린이/청소년')], max_length=100, unique=True),
        ),
    ]
