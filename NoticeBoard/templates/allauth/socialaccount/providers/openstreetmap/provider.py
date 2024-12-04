from allauth.socialaccount.providers.base import ProviderAccount
from allauth.socialaccount.providers.oauth.provider import OAuthProvider
from allauth.socialaccount.providers.openstreetmap.views import (
    OpenStreetMapOAuthAdapter,
)


class OpenStreetMapAccount(ProviderAccount):
    def get_profile_url(self):
        return (
            "https://www.openstreetmap.org/user/"
            + self.account.extra_data["display_name"]
        )

    def get_avatar_url(self):
        ret = None
        if img := self.account.extra_data.get("img"):
            ret = img.get("href")
        if not ret:
            # Backwards compatible (OSM provider data originating from XML)
            ret = self.account.extra_data.get("avatar")
        return ret

    def get_username(self):
        return self.account.extra_data["display_name"]


class OpenStreetMapProvider(OAuthProvider):
    id = "openstreetmap"
    name = "OpenStreetMap"
    account_class = OpenStreetMapAccount
    oauth_adapter_class = OpenStreetMapOAuthAdapter

    def extract_uid(self, data):
        return str(data["id"])

    def extract_common_fields(self, data):
        return dict(username=data["display_name"])


provider_classes = [OpenStreetMapProvider]