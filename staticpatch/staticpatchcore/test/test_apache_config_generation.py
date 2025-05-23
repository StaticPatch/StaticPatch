import datetime
import unittest.mock

from django.test import TestCase
from django.utils import timezone

import staticpatchcore.apache_config
import staticpatchcore.models
from staticpatchcore.test.utils import ApacheConfigWithNoBoilerplate, MockCertbot


class TestApacheConfigCase(TestCase):

    def test_no_ssl(self):

        with unittest.mock.patch.object(timezone, "now", return_value=datetime.datetime(2020, 1, 1, 10, 0, 0)):
            site = staticpatchcore.models.SiteModel()
            site.slug = "test1"
            site.main_domain = "test.com"
            site.main_domain_ssl = False
            site.save()

            build = staticpatchcore.models.BuildModel()
            build.site = site
            build.finished_at = datetime.datetime(2020, 1, 1, 10, 0, 0)
            build.save()

        certbot = MockCertbot()
        apache_config = ApacheConfigWithNoBoilerplate(certbot=certbot)
        apache_config.generate()

        expected = """
            <VirtualHost *:80>
                ServerName test.com
                DocumentRoot {filestorage}/site/{siteid}/build/2020-01-01-10-00-00-{buildid}/out
                <Directory "{filestorage}/site/{siteid}/build/2020-01-01-10-00-00-{buildid}/out">
                    AllowOverride None
                    Require all granted
                </Directory>
                BOILERPLATE
            </VirtualHost>
            """.format(
            siteid=site.id, buildid=build.id, filestorage="file_storage"
        )

        self.assertEqual(
            [i.strip() for i in expected.split("\n") if i.strip()],
            [i.strip() for i in apache_config.get().split("\n") if i.strip() and not i.strip().startswith("#")],
        )

        self.assertEqual(apache_config.get_domains_missing_ssl(), [])

    def test_ssl_but_no_cert(self):

        with unittest.mock.patch.object(timezone, "now", return_value=datetime.datetime(2020, 1, 1, 10, 0, 0)):
            site = staticpatchcore.models.SiteModel()
            site.slug = "test1"
            site.main_domain = "test.com"
            site.main_domain_ssl = True
            site.save()

            build = staticpatchcore.models.BuildModel()
            build.site = site
            build.finished_at = datetime.datetime(2020, 1, 1, 10, 0, 0)
            build.save()

        certbot = MockCertbot()
        apache_config = ApacheConfigWithNoBoilerplate(certbot=certbot)
        apache_config.generate()

        expected = """
            <VirtualHost *:80>
                ServerName test.com
                DocumentRoot {filestorage}/site/{siteid}/build/2020-01-01-10-00-00-{buildid}/out
                <Directory "{filestorage}/site/{siteid}/build/2020-01-01-10-00-00-{buildid}/out">
                    AllowOverride None
                    Require all granted
                </Directory>
                BOILERPLATE
            </VirtualHost>
            """.format(
            siteid=site.id,
            buildid=build.id,
            filestorage="file_storage",
        )

        self.assertEqual(
            [i.strip() for i in expected.split("\n") if i.strip()],
            [i.strip() for i in apache_config.get().split("\n") if i.strip() and not i.strip().startswith("#")],
        )

        self.assertEqual(apache_config.get_domains_missing_ssl(), ["test.com"])

    def test_no_build(self):

        with unittest.mock.patch.object(timezone, "now", return_value=datetime.datetime(2020, 1, 1, 10, 0, 0)):
            site = staticpatchcore.models.SiteModel()
            site.slug = "test1"
            site.main_domain = "test.com"
            site.main_domain_ssl = False
            site.save()

        certbot = MockCertbot()
        apache_config = ApacheConfigWithNoBoilerplate(certbot=certbot)
        apache_config.generate()

        expected = """
            <VirtualHost *:80>
                ServerName test.com
                DocumentRoot {filestorage}/webroot
                <Directory "{filestorage}/webroot">
                    AllowOverride None
                    Require all granted
                </Directory>
                BOILERPLATE
            </VirtualHost>
            """.format(
            filestorage="file_storage"
        )

        self.assertEqual(
            [i.strip() for i in expected.split("\n") if i.strip()],
            [i.strip() for i in apache_config.get().split("\n") if i.strip() and not i.strip().startswith("#")],
        )

        self.assertEqual(apache_config.get_domains_missing_ssl(), [])
