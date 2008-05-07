from django.contrib.auth.decorators import user_passes_test
from project.models import *

@user_passes_test(lambda u: u.is_staff)
def index(request):
