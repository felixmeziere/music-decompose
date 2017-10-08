from rest_framework.authentication import SessionAuthentication


class CsrfExemptSessionAuthentication(SessionAuthentication):
    """
    Removes the need for CSRF check in session authentication.

    This class is used to authenticate a request using django's sessions - this
    happens when you make the request as staff or superadmin.
    """

    def enforce_csrf(self, request):
        return None
