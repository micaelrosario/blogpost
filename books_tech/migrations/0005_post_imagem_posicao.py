from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books_tech', '0004_usuario'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='imagem_posicao',
            field=models.CharField(
                choices=[
                    ('center', 'Centro'),
                    ('top', 'Topo'),
                    ('bottom', 'Base'),
                    ('left', 'Esquerda'),
                    ('right', 'Direita'),
                ],
                default='center',
                max_length=20,
            ),
        ),
    ]
