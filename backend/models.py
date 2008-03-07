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
    scorch_file = models.FilePathField(path = "/path/to/ScorchData", match = "*.sib")
    printable_file = models.FilePathField(path = "/path/to/PrintData", match = "*.pdf") # for internal use only
    tags = models.ManyToManyField('Tag')
    flags = models.ManyToManyField('Tag')

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
    flags = models.ManyToManyField('Tag')

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

    class Admin:
	pass

    def __str__(self):
	return join(' ', self.user.first_name, self.user.last_name)

#####
class Customer(models.Model):
    user = models.ForeignKey(User)
    shipping_address1 = models.CharField(blank = True, maxlength = 250)
    shipping_address2 = models.CharField(blank = True, maxlength = 250)
    shipping_city = models.CharField(blank = True, maxlength = 120)
    shipping_state = models.USStateField(blank = True)
    cart = models.ForeignKey('Cart')
    flags = models.ManyToManyField('Tag')

    class Admin:
	pass

    def __str__(self):
	return join(' ', self.user.first_name, self.user.last_name)

#####
class Cart(models.Model):
    items = models.ManyToManyField('Item')
    shipping = models.ManyToManyField('Tag')
    payment = models.ManyToManyField('Tag')
    expires = models.DateField() # test: if ((expires - datetime.date.today()).days <= 0): delete this
    flags = models.ManyToManyField('Tag')

    class Admin:
	pass

#####
class Item(models.Model):
    type = models.ManyToManyField('Tag')
    objet = models.ManyToManyField('Objet')
    commission = models.ManyToManyField('Commission')
    coupon = models.ManyToManyField('Coupon')
    credit = model.ManyToManyField('Credit')
    amount = models.IntegerField(null = True)

    def item(self): #XXX: Rewrite for tags
	if (self.type == 'P'):
	    return self.Objet
	else:
	    return self.Commission

#####
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
class Coorespondence(model.Model)
    when = models.DateTimeField(auto_now_add = True)
    creator = models.ForeignKey(User)
    between = models.ManyToManyField(User)
    subject = models.CharField(maxlength = 500)
    message = models.TextField()
    flags = models.ManyToManyField('Tag')

#####
class Coupon(models.Model):
    coupon_id = models.CharField(maxlength = 30, primary_key = True)
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
