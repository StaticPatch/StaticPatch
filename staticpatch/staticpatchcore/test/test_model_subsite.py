from django.test import TestCase

from staticpatchcore.models import SubSiteModel


class TestModelSubSite(TestCase):

    def test_url_ok(self):
        sub_site = SubSiteModel(url="/test")
        sub_site._pre_save()
        assert sub_site.url == "/test"

    def test_url_with_trailing_slash(self):
        sub_site = SubSiteModel(url="/test/")
        sub_site._pre_save()
        assert sub_site.url == "/test"

    def test_url_without_leading_slash(self):
        sub_site = SubSiteModel(url="test")
        sub_site._pre_save()
        assert sub_site.url == "/test"
