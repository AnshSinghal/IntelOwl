# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.

import logging

from elasticsearch import Elasticsearch

from intel_owl import secrets

logger = logging.getLogger(__name__)

# business intelligence (bi)
ELASTICSEARCH_BI_ENABLED = (
    secrets.get_secret("ELASTICSEARCH_BI_ENABLED", False) == "True"
)
if ELASTICSEARCH_BI_ENABLED:
    ELASTICSEARCH_BI_HOST = secrets.get_secret("ELASTICSEARCH_BI_HOST").split(",")
    ELASTICSEARCH_BI_INDEX = secrets.get_secret("ELASTICSEARCH_BI_INDEX")
    if ELASTICSEARCH_BI_HOST and ELASTICSEARCH_BI_INDEX:
        elasticsearch_bi_conf = {
            "hosts": ELASTICSEARCH_BI_HOST,
            "maxsize": 20,
            "max_retries": 10,
            "retry_on_timeout": True,
            "timeout": 30,
        }
        if any("elasticsearch:9200" in host for host in ELASTICSEARCH_BI_HOST):
            elasticsearch_bi_conf["verify_certs"] = True
            elasticsearch_bi_conf["ca_certs"] = (
                "/opt/deploy/intel_owl/certs/elastic_ca/ca.crt"
            )
        ELASTICSEARCH_BI_CLIENT = Elasticsearch(**elasticsearch_bi_conf)
        try:
            if not ELASTICSEARCH_BI_CLIENT.ping():
                try:
                    info = ELASTICSEARCH_BI_CLIENT.info()
                except Exception as info_error:
                    info = f"info unavailable: {info_error}"
                logger.warning(
                    "ELASTICSEARCH BI client configuration did not connect correctly: %s",
                    info,
                )
        except Exception as e:
            logger.warning(
                "ELASTICSEARCH BI client configuration did not connect correctly: %s",
                e,
            )
    else:
        logger.warning("Elasticsearch BI not correctly configured")


# advanced search
ELASTICSEARCH_DSL_ENABLED = (
    secrets.get_secret("ELASTICSEARCH_DSL_ENABLED", False) == "True"
)
if ELASTICSEARCH_DSL_ENABLED:
    ELASTICSEARCH_DSL_HOST = secrets.get_secret("ELASTICSEARCH_DSL_HOST")
    if ELASTICSEARCH_DSL_HOST:
        elastic_search_conf = {"hosts": ELASTICSEARCH_DSL_HOST}

        ELASTICSEARCH_DSL_PASSWORD = secrets.get_secret("ELASTICSEARCH_DSL_PASSWORD")
        if ELASTICSEARCH_DSL_PASSWORD:
            elastic_search_conf["basic_auth"] = (
                "elastic",
                ELASTICSEARCH_DSL_PASSWORD,
            )
        if "elasticsearch:9200" in ELASTICSEARCH_DSL_HOST:
            # in case we use Elastic as container we need the generated
            # in case we use Elastic as external service it should have a valid cert
            elastic_search_conf["verify_certs"] = True
            elastic_search_conf["ca_certs"] = (
                "/opt/deploy/intel_owl/certs/elastic_ca/ca.crt"
            )
        ELASTICSEARCH_DSL_CLIENT = Elasticsearch(**elastic_search_conf)
        if not ELASTICSEARCH_DSL_CLIENT.ping():
            try:
                info = ELASTICSEARCH_DSL_CLIENT.info()
            except Exception as info_error:
                info = f"info unavailable: {info_error}"
            logger.warning(
                "ELASTICSEARCH DSL client configuration did not connect correctly: %s",
                info,
            )
    else:
        logger.warning(
            "you have to configure ELASTIC_HOST with the URL of your ElasticSearch instance"
        )
