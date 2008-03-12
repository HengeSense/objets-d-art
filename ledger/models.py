from django.db import models

#####
# Transaction
#
# This model describes each sort of transaction that can occur within the business.
#
class Transaction(models.Model):
    TYPE_CHOICES = (
	('S', 'Sale'),     # Positive
	('P', 'Payment'),  # Negative
	('C', 'Credit'),   # Negative
	('E', 'Expense'),  # Negative
	('A', 'Purchase'), # Negative
    )
    amount = models.FloatType(max_digits = 6, decimal_places = 2)
    type = models.CharField(maxlength = 1, choices = TYPE_CHOICES)
    date_time = models.DateTimeFiled()
    second_party = models.TextField()
    explanation = models.TextField()

    class Admin:
	pass
