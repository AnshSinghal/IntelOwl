# This file is a part of IntelOwl https://github.com/intelowlproject/IntelOwl
# See the file 'LICENSE' for copying permission.
"""
Test cases for big file upload functionality.
Issue #3156: 75MB files upload but "Scan page" hangs

This test validates that the Django settings for file upload limits
are properly configured to match nginx's client_max_body_size (100M).

The bug: Django's DATA_UPLOAD_MAX_MEMORY_SIZE and FILE_UPLOAD_MAX_MEMORY_SIZE
are set to 50MB while nginx allows 100MB. This causes files between 50-100MB
to fail silently at the Django level.
"""

from tests import CustomTestCase


class BigFileUploadSettingsTestCase(CustomTestCase):
    """
    Test that Django file upload settings are consistent with nginx configuration.

    nginx: client_max_body_size 100m (100MB)
    Django settings should allow at least 100MB to match nginx.
    """

    # 100MB in bytes - should match nginx client_max_body_size
    NGINX_MAX_BODY_SIZE = 100 * (10**6)  # 100MB

    # Common large file sizes that users might upload
    LARGE_FILE_SIZE_75MB = 75 * (10**6)  # 75MB - reported in issue #3156
    LARGE_FILE_SIZE_80MB = 80 * (10**6)  # 80MB
    LARGE_FILE_SIZE_90MB = 90 * (10**6)  # 90MB

    def test_data_upload_max_memory_size_allows_100mb(self):
        """
        Test that DATA_UPLOAD_MAX_MEMORY_SIZE allows files up to 100MB.

        This setting controls the maximum size of request data that Django
        will read into memory. It should be at least 100MB to match nginx.
        """
        from django.conf import settings

        self.assertGreaterEqual(
            settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
            self.NGINX_MAX_BODY_SIZE,
            f"DATA_UPLOAD_MAX_MEMORY_SIZE ({settings.DATA_UPLOAD_MAX_MEMORY_SIZE / (10**6):.0f}MB) "
            f"should be at least {self.NGINX_MAX_BODY_SIZE / (10**6):.0f}MB to match nginx config",
        )

    def test_file_upload_max_memory_size_allows_100mb(self):
        """
        Test that FILE_UPLOAD_MAX_MEMORY_SIZE allows files up to 100MB.

        This setting controls the maximum size of an uploaded file that will
        be held in memory. It should be at least 100MB to match nginx.
        """
        from django.conf import settings

        self.assertGreaterEqual(
            settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
            self.NGINX_MAX_BODY_SIZE,
            f"FILE_UPLOAD_MAX_MEMORY_SIZE ({settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (10**6):.0f}MB) "
            f"should be at least {self.NGINX_MAX_BODY_SIZE / (10**6):.0f}MB to match nginx config",
        )

    def test_data_upload_allows_75mb_file(self):
        """
        Test that DATA_UPLOAD_MAX_MEMORY_SIZE allows 75MB files.

        Issue #3156 specifically mentions 75MB files failing.
        """
        from django.conf import settings

        self.assertGreaterEqual(
            settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
            self.LARGE_FILE_SIZE_75MB,
            f"DATA_UPLOAD_MAX_MEMORY_SIZE ({settings.DATA_UPLOAD_MAX_MEMORY_SIZE / (10**6):.0f}MB) "
            f"should allow 75MB files as reported in issue #3156",
        )

    def test_file_upload_allows_75mb_file(self):
        """
        Test that FILE_UPLOAD_MAX_MEMORY_SIZE allows 75MB files.

        Issue #3156 specifically mentions 75MB files failing.
        """
        from django.conf import settings

        self.assertGreaterEqual(
            settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
            self.LARGE_FILE_SIZE_75MB,
            f"FILE_UPLOAD_MAX_MEMORY_SIZE ({settings.FILE_UPLOAD_MAX_MEMORY_SIZE / (10**6):.0f}MB) "
            f"should allow 75MB files as reported in issue #3156",
        )

    def test_upload_settings_are_consistent(self):
        """
        Test that DATA_UPLOAD and FILE_UPLOAD settings are consistent.

        Both settings should have the same value for predictable behavior.
        """
        from django.conf import settings

        self.assertEqual(
            settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
            settings.FILE_UPLOAD_MAX_MEMORY_SIZE,
            "DATA_UPLOAD_MAX_MEMORY_SIZE and FILE_UPLOAD_MAX_MEMORY_SIZE should match "
            "for consistent behavior",
        )

    def test_upload_limit_has_safety_margin(self):
        """
        Test that upload limit has some safety margin above nginx limit.

        Django's limit should be at least equal to nginx's limit,
        ideally with some margin for multipart overhead.
        """
        from django.conf import settings

        # Minimum acceptable: equal to nginx limit
        minimum_acceptable = self.NGINX_MAX_BODY_SIZE

        self.assertGreaterEqual(
            settings.DATA_UPLOAD_MAX_MEMORY_SIZE,
            minimum_acceptable,
            f"Django upload limit should be at least {minimum_acceptable / (10**6):.0f}MB "
            "to handle files up to nginx's client_max_body_size",
        )
