from project.objetsdart.backend.models import Transaction
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render_to_response

@user_passes_test(lambda u: u.tags)
def index(request):
    """ index function
        This function displays the front-page (index) for ledger functionality"""

@user_passes_test(lambda u: u.has_perm('transactions.can_access')) #XXX
def display_ledger(request, summary = False, year = None, quarter = None, week = None, month = None, day = None, full = False):
    """ display_ledger function
        This function displays transactions for a given time period provided by the url.
        Query string options:
            output_format: 'HTML' (default), 'XML', 'LaTeX', 'PDF', or 'CSV'
            display_negatives: 'parentheses' (default), '-', 'red', or 'none'
            type: 'all' (default), 'sale', 'payment', 'credit', 'expense', 'purchase'"""

def _generate_summary(begin, end):
