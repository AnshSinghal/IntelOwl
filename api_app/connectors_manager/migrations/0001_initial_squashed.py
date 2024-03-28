# Generated by Django 4.2.8 on 2024-02-08 10:53

import django.contrib.postgres.fields
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True
    replaces = [
        # ("connectors_manager", "0001_initial"),
        # ("connectors_manager", "0002_connectorreport_parent_playbook"),
        # ("connectors_manager", "0003_connectorconfig"),
        # ("connectors_manager", "0004_datamigration"),
        # ("connectors_manager", "0005_auto_20230301_1415"),
        # ("connectors_manager", "0006_connectorconfig_disabled_in_org"),
        # ("connectors_manager", "0007_alter_connectorreport_job"),
        # ("connectors_manager", "0008_auto_20230308_1623"),
        # ("connectors_manager", "0009_parent_playbook_foreign_key"),
        # ("connectors_manager", "0010_remove_parent_playbook"),
        # ("connectors_manager", "00011_remove_runtime_configuration"),
        # ("connectors_manager", "0012_slack"),
        # ("connectors_manager", "0013_tlp_clear"),
        # (
        #     "connectors_manager",
        #     "0014_alter_connectorconfig_disabled_in_organizations_and_more",
        # ),
        # ("connectors_manager", "0015_params"),
        # ("connectors_manager", "0016_alter_connectorconfig_name"),
        # ("connectors_manager", "0017_alter_connectorconfig_options"),
        # ("connectors_manager", "0018_alter_connectorconfig_name"),
        # (
        #     "connectors_manager",
        #     "0019_rename_connectors__python__0fb146_idx_connectors__python__f23fd8_idx_and_more",
        # ),
        # ("connectors_manager", "0020_alter_python_module"),
        # ("connectors_manager", "0021_alter_connectorconfig_python_module"),
        # ("connectors_manager", "0022_alter_connectorconfig_python_module"),
        # ("connectors_manager", "0023_connectorconfig_routing_key_and_more"),
        # ("connectors_manager", "0024_connectorconfig_health_check_task"),
        # ("connectors_manager", "0025_connectorconfig_health_check_status"),
        # ("connectors_manager", "0026_connectorreport_parameters"),
        # ("connectors_manager", "0027_connectorreport_sent_to_bi"),
        # ("connectors_manager", "0028_connectorreport_connectorreportsbisearch"),
    ]

    dependencies = [("api_app", "0001_1_initial_squashed")]
    operations = [
        migrations.CreateModel(
            name="ConnectorConfig",
            fields=[
                (
                    "name",
                    models.CharField(
                        max_length=100,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                        validators=[
                            django.core.validators.RegexValidator(
                                "^\\w+$",
                                "Your name should match the [A-Za-z0-9_] characters",
                            )
                        ],
                    ),
                ),
                (
                    "python_module",
                    models.ForeignKey(
                        limit_choices_to={
                            "base_path": "api_app.connectors_manager.connectors"
                        },
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="%(class)ss",
                        to="api_app.pythonmodule",
                    ),
                ),
                ("description", models.TextField()),
                ("disabled", models.BooleanField(default=False)),
                (
                    "disabled_in_organizations",
                    models.ManyToManyField(
                        blank=True,
                        related_name="%(app_label)s_%(class)s_disabled",
                        to="certego_saas_organization.organization",
                    ),
                ),
                (
                    "health_check_status",
                    models.BooleanField(default=True, editable=False),
                ),
                (
                    "health_check_task",
                    models.OneToOneField(
                        blank=True,
                        editable=False,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="healthcheck_for_%(class)s",
                        to="django_celery_beat.periodictask",
                    ),
                ),
                (
                    "soft_time_limit",
                    models.IntegerField(
                        default=60,
                        validators=[django.core.validators.MinValueValidator(0)],
                    ),
                ),
                ("routing_key", models.CharField(default="default", max_length=50)),
                (
                    "maximum_tlp",
                    models.CharField(
                        choices=[
                            ("CLEAR", "Clear"),
                            ("GREEN", "Green"),
                            ("AMBER", "Amber"),
                            ("RED", "Red"),
                        ],
                        default="CLEAR",
                        max_length=50,
                    ),
                ),
                ("run_on_failure", models.BooleanField(default=True)),
            ],
            options={"abstract": False, "ordering": ["name", "disabled"]},
        ),
        migrations.AddIndex(
            model_name="connectorconfig",
            index=models.Index(
                fields=["python_module", "disabled"],
                name="connectors__python__0fb146_idx",
            ),
        ),
        migrations.RenameIndex(
            model_name="connectorconfig",
            new_name="connectors__python__f23fd8_idx",
            old_name="connectors__python__0fb146_idx",
        ),
        migrations.CreateModel(
            name="ConnectorReport",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("FAILED", "Failed"),
                            ("PENDING", "Pending"),
                            ("RUNNING", "Running"),
                            ("SUCCESS", "Success"),
                            ("KILLED", "Killed"),
                        ],
                        max_length=50,
                    ),
                ),
                ("report", models.JSONField(default=dict)),
                (
                    "errors",
                    django.contrib.postgres.fields.ArrayField(
                        base_field=models.CharField(max_length=512),
                        blank=True,
                        default=list,
                        size=None,
                    ),
                ),
                ("start_time", models.DateTimeField(default=django.utils.timezone.now)),
                ("end_time", models.DateTimeField(default=django.utils.timezone.now)),
                ("task_id", models.UUIDField()),
                (
                    "job",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="%(class)ss",
                        to="api_app.job",
                    ),
                ),
                ("sent_to_bi", models.BooleanField(default=False, editable=False)),
                ("parameters", models.JSONField(default={}, editable=False)),
                (
                    "config",
                    models.ForeignKey(
                        "ConnectorConfig",
                        related_name="reports",
                        on_delete=models.CASCADE,
                    ),
                ),
            ],
        ),
        migrations.AddIndex(
            model_name="connectorreport",
            index=models.Index(
                fields=["sent_to_bi", "-start_time"], name="connectorreportsBISearch"
            ),
        ),
        migrations.AlterUniqueTogether(
            name="connectorreport",
            unique_together={("config", "job")},
        ),
        migrations.AlterField(
            model_name="connectorreport",
            name="parameters",
            field=models.JSONField(editable=False),
        ),
    ]
