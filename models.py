from django.db import models
from django.contrib.auth.models import User

###########################
##### Backend functionality
###########################

#####
# Tag
# 
# This model describes boolean tags and flags used on all of the other models, offering such information as ensemble, or state.
#
class Tag(models.Model):
    tag = models.CharField(maxlength = 100, primary_key = true)
    internal = models.BooleanField(default = True)
    description = models.TextField(blank = True)
    
    class Admin:
    	pass

    def __str__(self):
	    return self.description

#####
# NewsItem
#
# This model simply describes a news item
#
class NewsItem(models.Model):
    timestamp = models.DateTimeField(auto_now = True)
    title = models.CharField(maxlength = 512)
    body = models.TextField()

    class Admin:
        pass

    def __str__(self):
        return self.title

#####
# Score
# 
# This model describes a single score, along with ways to access it from both Client and Customer side.
#
class Score(models.Model):
    slug = models.SlugField(primary_key = True)
    title = models.CharField(maxlength = 250)
    description = models.TextField()
    duration = models.FloatField(max_digits = 5, decimal_places = 2)
    created = models.DateField()
    price = models.FloatField(max_digits = 5, decimal_places = 2)
    length = models.FloatField(max_digits = 3, decimal_places = 1) # In inches
    width = models.FloatField(max_digits = 3, decimal_places = 1) # In inches
    height = models.FloatField(max_digits = 3, decimal_places = 1) # In inches
    weight = models.FloatField(max_digits = 2, decimal_places = 1) # In ounces
    thumbnail_file = models.FileField(upload_to = "ThumbData/%Y/%m") # PNG
    editable_file = models.FileField(upload_to = "ScoreFiles/%Y/%m") # SIB
    viewable_file = models.FileField(upload_to = "ScorchData/%Y/%m") # SIB/Scorch
    printable_file = models.FileField(upload_to = "PrintData/%Y/%m") # PDF
    recording_file = models.FileField(upload_to = "AudioData/%Y/%m", blank = True) # MP3
    recording_credit = models.CharField(maxlength = 500)
    contract = models.ForeignKey('Contract')
    tags = models.ManyToManyField('Tag')

    class Admin:
	    pass

    def __str__(self):
	    return self.title

#####
# Contract
#
# This model represents a contract tied to an individual or a score, keeping all the information in the database for different output formats
#
class Contract(models.Model):
    # Contract basics
    title = models.CharField(maxlength = 500)
    date_created = models.DateField(auto_now_add = True)
    date_annulled = models.DateField(null = True)
    a = models.ForeignKey(User)
    b = models.ForeignKey(User) #Publishing company or commissioner
    inherits = models.ManyToManyField('self') 
    # Contract body
    duration = models.TextField(blank = True)
    termination = models.TextField(blank = True)
    breach = models.TextField(blank = True)
    pricing = models.TextField(blank = True)
    coupon_status = models.ManyToManyField('Tag')
    coupons = models.ManyToManyField('Coupon')
    bulk_discount = models.IntegerField(default = 0)
    bulk_discount_threshold = models.IntegerField(default = 0) # 0 means no bulk discount
    printing = models.TextField(blank = True)
    payment = models.ForeignKey('Tag') # tag refers to a module with a standard-named function that will notify the business to pay client
    rights = models.TextField(blank = True)
    # Business details
    copies_sold = models.IntegerField(default = 0)
    sold_since_payment = models.IntegerField(default = 0)
    tags = models.ManyToManyField('Tag')

    class Admin:
	    pass

    def __str__(self): #XXX: rewrite for Tag model
	    if (self.is_active):
	        active = 'Active'
	    else:
	        if (self.is_annulled):
	        	active = 'Annulled'
	        else:
		        active = 'Inactive'
	    if (self.is_addendum):
	        addendum = '(addendum)'
	    else:
	        addendum = ''
    	return join(' ', (self.title, 'between', a, '&', b, '-', self.date_created, addendum, active))
												      
#####
# Application
#
# This model contains client applications
#
class Application(models.Model):
    user = models.ForeignKey(User)
    portfolio = models.CharField(maxlength = 200) # url or 'Emailed'
    bio = models.TextField()
    education = models.TextField()
    influences = models.TextField()
    primary_style = models.TextField()
    why_join = models.TextField()
    other_info = models.TextField() # Other publishign contracts, jobs, hobbies, quirks, etc.
    tags = models.ManyToManyField('Tag')

#####
# Client
#
# This model is tied to a user and represents a artist/client as a profile
#
class Client(models.Model):
    user = models.ForeignKey(User)
    full_name = models.CharField(maxlength = 200) #for ease of searching
    profile = models.TextField(blank = True)
    bio = models.TextField(blank = True)
    works = models.ManyToManyField('Score')
    commissions = models.ManyToManyField('Commission')
    coupons = models.ManyToManyField('Coupon')
    contracts = models.ManyToManyField('Contract')
    balance = models.FloatField(max_digits = 5, decimal_places = 2)
    yearly_earnings = models.FloatField(max_digits=8, decimal_places = 2)
    total_earnings = models.FloatField(max_digits = 8, decimal_places = 2)
    tags = models.ManyToManyField('Tag')

    class Admin:
	    pass

    class Meta:
        permissions = (
                ("is_client", "User is a client"),
        )

    def __str__(self):
	    return self.user.get_full_name()

#####
# Cart
#
# The cart object belongs to a user and contain as many 'item' objects as needed
#
class Cart(models.Model):
    owner = models.ForeignKey(User)
    title = models.CharField(maxlength = 50)
    items = models.XMLField(schema_path = "/path/to/cartschema.rnc") # xml.dom.minidom - use this even if phone/mail order
    total = models.FloatField(max_digits = 5, decimal_places = 2)
    expires = models.DateField() # test: if ((expires - datetime.date.today()).days <= 0): delete this
    tags = models.ManyToManyField('Tag')

    class Admin:
    	pass

#####
# Commission
#
# The commission object represents a commission tied to a score.
#
class Commission(models.Model):
    customer = models.ForeignKey(User)
    contract = models.ForeignKey('Contract')
    score = models.ForeignKey('Score')
    base = models.FloatField(max_digits = 6, decimal_places = 2)
    rate = models.FloatField(max_digits = 2, decimal_places = 1)
    tags = models.ManyToManyField('Tag')

    class Admin:
	    pass

#####
# Coupon
# 
# Coupons are percentage-based discounts applicable to certain scores
#
class Coupon(models.Model):
    coupon_code = models.CharField(maxlength = 30, primary_key = True)
    type =  models.ForeignKey('Tag')
    description = models.CharField(maxlength = 500)
    discount = models.IntegerField()
    begins = models.DateField()
    expires = models.DateField(blank = True) # test: if ((expires - datetime.date.today()).days <= 0): this.is_expired = True
    tags = models.ManyToManyField('Tag')

    class Admin: 
    	pass

    def __str__(self):
	    return self.discount + '% off!  ' + self.description

#####
# Credit
#
# A credit is a gift certificate, introductory offer,  refund, or client payment redeemable as money
#
class Credit(models.Model):
    type = models.ManyToManyField('Tag')
    passphrase = models.CharField(maxlenth = 30)
    user_restrict = models.ManyToManyField(User) #TODO: Make sure to create a null user
    amount = models.FloatField(max_digits = 6, decimal_places = 2)
    expires = models.DateField(blank = True) # To be set when activated (i.e.: G = +1 year, I = +30 days, R = +1 year, P = +5 years)
    tags = models.ManyToManyField('Tag')

    class Admin:
    	pass

    def __str__(self):
	    if (self.user_restrict):
	        u = join(' ', "for", self.user_restrict.first_name, self.user_restrict.last_name)
    	else:
	        u = ''
    	return join(' ', self.type, u, str(self.id) + ':', '$' + self.amount)

#####
# Notifications
#
# Notifications act as tasks for the business to deal with, such as items to ship or submissions to review.
class Notification(models.Model):
    tags = models.ManyToManyField('Tag')
    data = models.XMLField('/path/to/notifications.rnc')

    class Admin:
        pass

##########################
##### Ledger functionality
##########################

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

############################
##### Callback functionality
############################

#####
# CheckoutBackup
#
# Stores backups of transactions with Google Checkout
#
class CheckoutBackup(models.Model):
    serial_number = models.CharField(maxlength = 120, primary_key = true)
    request = models.TextField()
    response = models.TextField()

    class Admin:
        pass

#
