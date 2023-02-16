# Generated by Django 4.1.1 on 2023-02-12 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("alert", "0003_movie_is_released"),
    ]

    operations = [
        migrations.AlterField(
            model_name="date",
            name="has_games",
            field=models.BooleanField(
                db_index=True, db_tablespace="date_indexes", default=False
            ),
        ),
        migrations.AlterField(
            model_name="date",
            name="has_movies",
            field=models.BooleanField(
                db_index=True, db_tablespace="date_indexes", default=False
            ),
        ),
        migrations.AlterField(
            model_name="games",
            name="date",
            field=models.ForeignKey(
                db_tablespace="game_indexes",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="games",
                to="alert.date",
            ),
        ),
        migrations.AlterField(
            model_name="games",
            name="genres",
            field=models.ManyToManyField(
                db_index=True,
                db_tablespace="game_indexes",
                related_name="games",
                to="alert.genre",
            ),
        ),
        migrations.AlterField(
            model_name="games",
            name="is_active",
            field=models.BooleanField(
                db_index=True, db_tablespace="game_indexes", default=True
            ),
        ),
        migrations.AlterField(
            model_name="games",
            name="is_released",
            field=models.BooleanField(
                db_index=True, db_tablespace="game_indexes", default=False
            ),
        ),
        migrations.AlterField(
            model_name="games",
            name="platforms",
            field=models.ManyToManyField(
                db_index=True,
                db_tablespace="game_indexes",
                related_name="games",
                to="alert.platform",
            ),
        ),
        migrations.AlterField(
            model_name="games",
            name="slug",
            field=models.SlugField(
                blank=True, db_tablespace="game_indexes", null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="genre",
            name="is_game",
            field=models.BooleanField(
                db_index=True, db_tablespace="genre_indexes", default=False
            ),
        ),
        migrations.AlterField(
            model_name="genre",
            name="is_movie",
            field=models.BooleanField(
                db_index=True, db_tablespace="genre_indexes", default=False
            ),
        ),
        migrations.AlterField(
            model_name="genre",
            name="name",
            field=models.CharField(
                db_index=True, db_tablespace="genre_indexes", max_length=50, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="genre",
            name="slug",
            field=models.SlugField(
                blank=True, db_tablespace="genre_indexes", null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="date",
            field=models.ForeignKey(
                db_tablespace="movie_indexes",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="movies",
                to="alert.date",
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="genres",
            field=models.ManyToManyField(
                db_index=True,
                db_tablespace="movie_indexes",
                related_name="movies",
                to="alert.genre",
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="is_active",
            field=models.BooleanField(
                db_index=True, db_tablespace="movie_indexes", default=True
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="is_released",
            field=models.BooleanField(
                db_index=True, db_tablespace="movie_indexes", default=False
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="region",
            field=models.ForeignKey(
                db_tablespace="movie_indexes",
                on_delete=django.db.models.deletion.PROTECT,
                related_name="movies",
                to="alert.region",
            ),
        ),
        migrations.AlterField(
            model_name="movie",
            name="slug",
            field=models.SlugField(
                blank=True, db_tablespace="movie_indexes", null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="platform",
            name="name",
            field=models.CharField(
                db_index=True,
                db_tablespace="platform_indexes",
                max_length=35,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="platform",
            name="slug",
            field=models.SlugField(
                blank=True, db_tablespace="platform_indexes", null=True, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="region",
            name="code",
            field=models.CharField(
                db_index=True, db_tablespace="region_indexes", max_length=2, unique=True
            ),
        ),
        migrations.AlterField(
            model_name="region",
            name="country",
            field=models.CharField(
                db_index=True,
                db_tablespace="region_indexes",
                max_length=50,
                unique=True,
            ),
        ),
        migrations.AlterField(
            model_name="region",
            name="slug",
            field=models.SlugField(
                blank=True, db_tablespace="region_indexes", null=True, unique=True
            ),
        ),
    ]
