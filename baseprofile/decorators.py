from functools import wraps
from django.core.exceptions import PermissionDenied
from django.utils.decorators import available_attrs

def user_passes_test_or_forbidden(test_func):
    """
    Decorator for views that checks that the user passes the given test,
    returing 403 if not. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if test_func(request.user):
                return view_func(request, *args, **kwargs)

            raise PermissionDenied
        return _wrapped_view
    return decorator

def member_required(function=None):
    def test(user):
        if user.is_anonymous():
            return False

        try:
            p = user.get_profile()
        except:
            return False

        return p.accepted()

    actual_decorator = user_passes_test_or_forbidden(test)
    if function:
        return actual_decorator(function)

    return actual_decorator
