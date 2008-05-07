from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.has_perm('clients.is_client'))
