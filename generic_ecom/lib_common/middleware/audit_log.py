from django.db.models import signals
from django.utils import timezone
from django.utils.functional import curry


class AuditLogMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        if not request.method in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
            if hasattr(request, 'user') and request.user.is_authenticated():
                user = request.user
            else:
                user = None

            mark_actor = curry(self.mark_actor, user)
            signals.pre_save.connect(mark_actor, dispatch_uid=(
                self.__class__, request,), weak=False)

        response = self.get_response(request)

        return response

    def process_response(self, request, response):
        signals.pre_save.disconnect(dispatch_uid=(self.__class__, request,))
        return response

    def mark_actor(self, user, sender, instance, **kwargs):
        if user is not None:
            if not getattr(instance, 'created_by_id', None):
                instance.created_by_id = user.id
            if not getattr(instance, 'created', None):
                instance.created = timezone.now()

            instance.modified_by_id = user.id
            instance.modified = timezone.now()
