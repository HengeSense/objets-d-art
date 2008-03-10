from django.db import models
from django.contrib.auth.models import User

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
# Objet
# 
# This model describes a single distributable object, along with ways to access it from both Client and Customer side.
#
class Objet(models.Model):
    title = models.CharField(maxlength = 250)
    duration = models.FloatField(max_digits = 5, decimal_places = 2)
    created = models.DateField()
    coupons = models.ManyToManyField('Coupon')
    bulk_discount_threshold = models.IntegerField(default = 0) # 0 means no bulk discount
    contract = models.ForeignKey('Contract') #TODO: Make sure to make a null contract
    price = models.FloatField(max_digits = 5, decimal_places = 2)
    length = models.FloatField(max_digits = 3, decimal_places = 1) # In inches
    width = models.FloatField(max_digits = 3, decimal_places = 1) # In inches
    tens_height = models.FloatField(max_digits = 3, decimal_places = 1) # The height of ten shippable objects in inches
    copies_sold = models.IntegerField()
    thumbnail_file = models.FileField(upload_to = "ThumbData/%Y/%m")
    editable_file = models.FileField(upload_to = "ScoreFiles/%Y/%m") # Protect with .htaccess
    viewable_file = models.FileField(upload_to = "ScorchData/%Y/%m")
    printable_file = models.FileField(upload_to = "PrintData/%Y/%m") # Protect with .htaccess
    tags = models.ManyToManyField('Tag')

    class Admin:
	pass

    def __str__(self):
	return self.title

#####
# Contract
#
# This model represents a contract tied to an individual or a object, keeping all the information in the database for different output formats
#
class Contract(models.Model):
    # Contract basics
    title = models.CharField(maxlength = 500)
    date_created = models.DateField(auto_now_add = True)
    date_annulled = models.DateField(null = True)
    a = models.ForeignKey(User)
    b = models.ForeignKey(User)
    signature_method = models.ManyToManyField('Tag')
    a_signature = models.TextField(blank = True) # Usually client
    b_signature = models.TextField(blank = True) # Usually MJS Publishing, may be customer
    parent_contract = models.ForeignKey('self') #TODO: Make sure to make a null contract
    # Contract body
    duration = models.TextField(blank = True)
    termination = models.TextField(blank = True)
    breach = models.TextField(blank = True)
    pricing = models.TextField(blank = True)
    coupons = models.ManyToManyField('Tag')
    bulk_discount = models.IntegerField(default = 0)
    printing = models.TextField(blank = True)
    payment = models.TextField(blank = True)
    rights = models.TextField(blank = True)
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
    # For populating the User model
    username = models.CharField(maxlength = 30, primary_key = True)
    first_name = models.CharField(maxlength = 30)
    last_name = models.CharField(maxlength = 30)
    email = models.EmailField()

    # Other information
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
    profile = models.TextField(blank = True)
    bio = models.TextField(blank = True)
    works = models.ManyToManyField('Objet')
    commissions = models.ManyToManyField('Commission')
    coupons = models.ManyToManyField('Coupon')
    contracts = models.ManyToManyField('Contract')
    balance = models.FloatField(max_digits = 8, decimal_places = 2)
    tags = models.ManyToManyField('Tag')

    class Admin:
	pass

    def __str__(self):
	return join(' ', self.user.first_name, self.user.last_name)

#####
# Customer
#
# This model is tied to a user and represents a store customer
#
class Customer(models.Model):
    user = models.ForeignKey(User)
    shipping_address1 = models.CharField(blank = True, maxlength = 250)
    shipping_address2 = models.CharField(blank = True, maxlength = 250)
    shipping_city = models.CharField(blank = True, maxlength = 120)
    shipping_state = models.USStateField(blank = True)
    cart = models.ManyToManyField('Cart')
    flags = models.ManyToManyField('Tag')

    class Admin:
	pass

    def __str__(self):
	return join(' ', self.user.first_name, self.user.last_name)

#####
# Cart
#
# The cart object belongs to a customer and contain as many 'item' objects as needed
#
class Cart(models.Model):
    title = models.CharField(maxlength = 50)
    items = models.XMLField(schema_path = "/path/to/cartschema.rnc") # xml.dom.minidom
    total = models.FloatField(max_digits = 5, decimal_places = 2)
    shipping = models.ForeignKey('Tag')
    payment = models.ManyToManyField('Tag')
    expires = models.DateField() # test: if ((expires - datetime.date.today()).days <= 0): delete this
    flags = models.ManyToManyField('Tag')

    class Admin:
	pass

#####
# Commission
#
# The commission object represents a commission tied to a score.
#
class Commission(models.Model):
    customer = models.ForeignKey('Customer')
    contract = models.ForeignKey('Contract')
    objet = models.ForeignKey('Objet')
    base = models.FloatField(max_digits = 6, decimal_places = 2)
    rate = models.FloatField(max_digits = 2, decimal_places = 1)
    flags = models.ManyToManyField('Tag')

    class Admin:
	pass

#####
# Correspondence
#
# This class represents a communcation between two or more people.
#
class Correspondence(model.Model)
    when = models.DateTimeField(auto_now_add = True)
    creator = models.ForeignKey(User)
    between = models.ManyToManyField(User)
    subject = models.CharField(maxlength = 500)
    message = models.TextField()
    flags = models.ManyToManyField('Tag')

#####
# Coupon
# 
# Coupons are percentage-based discounts applicable to certain objets
#
class Coupon(models.Model):
    coupon_code = models.CharField(maxlength = 30)
    type =  models.ManyToManyField('Tag')
    description = models.CharField(maxlength = 500)
    discount = models.IntegerField()
    begins = models.DateField()
    expires = models.DateField(blank = True) # test: if ((expires - datetime.date.today()).days <= 0): this.is_expired = True
    flags = models.ManyToManyField('Tag')

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
    flags = models.ManyToManyField('Tag')

    class Admin:
	pass

    class Meta:
	ordering = ['type', 'expires'

    def __str__(self):
	if (self.user_restrict):
	    u = join(' ', "for", self.user_restrict.first_name, self.user_restrict.last_name)
	else:
	    u = ''
	return join(' ', self.type, u, str(self.id) + ':', '$' + self.amount)
