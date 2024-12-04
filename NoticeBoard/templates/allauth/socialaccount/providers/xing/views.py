from allauth.socialaccount.providers.oauth.client import OAuth
from allauth.socialaccount.providers.oauth.views import (
    OAuthAdapter,
    OAuthCallbackView,
    OAuthLoginView,
)


class XingAPI(OAuth):
    url = "https://api.xing.com/v1/users/me.json"

    def get_user_info(self):
        user = self.query(self.url).json()
        return user


class XingOAuthAdapter(OAuthAdapter):
    provider_id = "xing"
    request_token_url = "https://api.xing.com/v1/request_token"  # nosec
    access_token_url = "https://api.xing.com/v1/access_token"  # nosec
    authorize_url = "https://www.xing.com/v1/authorize"

    def complete_login(self, request, app, token, response):
        client = XingAPI(request, app.client_id, app.secret, self.request_token_url)
        extra_data = client.get_user_info()["users"][0]
        return self.get_provider().sociallogin_from_response(request, extra_data)


oauth_login = OAuthLoginView.adapter_view(XingOAuthAdapter)
oauth_callback = OAuthCallbackView.adapter_view(XingOAuthAdapter)