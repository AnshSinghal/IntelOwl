import logging
import os
from pathlib import Path
from typing import List
from urllib.parse import urlparse

from bbot.scanner import Preset, Scanner
from django.conf import settings

from api_app.analyzers_manager.classes import ObservableAnalyzer
from api_app.analyzers_manager.exceptions import AnalyzerRunException
from api_app.choices import Classification
from intel_owl.settings._util import set_permissions
from tests.mock_utils import MockUpResponse, if_mock_connections, patch

logger = logging.getLogger(__name__)


class BBOT(ObservableAnalyzer):
    """
    BBOT analyzer
    """

    modules: List[str] = ["httpx"]
    presets: List[str] = ["web-basic"]  # Default preset

    def update(self):
        pass

    def run(self):

        observable = self.observable_name
        files_dir = settings.BBOT_FILES_PATH / f"bbot_analysis_{observable}"
        os.makedirs(files_dir, exist_ok=True)
        set_permissions(files_dir)

        if self.observable_classification == Classification.URL:
            logger.debug(f"BBOT analyzer extracting hostname from URL: {observable}")
            hostname = urlparse(observable).hostname
            observable = hostname

        logger.debug(f"BBOT analyzer running on observable: {observable}")
        preset_config = {"home": files_dir}

        preset = Preset(
            observable,
            modules=self.modules,
            presets=self.presets,
            output_modules=["json"],
            config=preset_config,
        )

        scan = Scanner(preset=preset)
        scan.home = Path(files_dir)

        try:
            for event in scan.start():
                logger.debug(f"BBOT analyzer event: {event}")
                print(f"Event: {event}\n")
                print(f"Type of Event: {type(event)}\n")

        except Exception as e:
            raise AnalyzerRunException(f"BBOT analyzer failed: {e}")

    @classmethod
    def _monkeypatch(cls):
        patches = [
            if_mock_connections(
                patch(
                    "bbot.scanner.Scanner.start",
                    return_value=MockUpResponse(
                        json=lambda: {
                            "module": "module",
                            "category": "category",
                            "name": "name",
                            "description": "description",
                            "severity": "severity",
                            "confidence": "confidence",
                            "tags": ["tag1", "tag2"],
                            "details": {"key1": "value1", "key2": "value2"},
                        }
                    ),
                )
            )
        ]
        return super()._monkeypatch(patches=patches)
