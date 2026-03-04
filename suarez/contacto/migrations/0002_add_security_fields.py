# Generated manually for contacto app

from django.db import migrations, models
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('contacto', '0001_initial'),  # Ajusta esto según tu última migración
    ]

    operations = [
        migrations.AddField(
            model_name='mensajecontacto',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='mensajecontacto',
            name='asunto',
            field=models.CharField(max_length=200, validators=[django.core.validators.MinLengthValidator(5, 'El asunto debe tener al menos 5 caracteres.')]),
        ),
        migrations.AlterField(
            model_name='mensajecontacto',
            name='email',
            field=models.EmailField(max_length=254, validators=[django.core.validators.EmailValidator('Ingresa un email válido.')]),
        ),
        migrations.AlterField(
            model_name='mensajecontacto',
            name='mensaje',
            field=models.TextField(validators=[django.core.validators.MinLengthValidator(10, 'El mensaje debe tener al menos 10 caracteres.')]),
        ),
        migrations.AlterField(
            model_name='mensajecontacto',
            name='nombre',
            field=models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(3, 'El nombre debe tener al menos 3 caracteres.')]),
        ),
        migrations.AlterModelOptions(
            name='mensajecontacto',
            options={'ordering': ['-fecha_envio'], 'verbose_name': 'Mensaje de Contacto', 'verbose_name_plural': 'Mensajes de Contacto'},
        ),
    ]
