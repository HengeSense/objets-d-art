from xml.dom.minidom import *

class BaseException:
    def __init__(self, error):
	self.error = error

    def __str__(self):
	return self.error

class MissingRequiredElement(BaseException):
    pass

class MissingRequiredAttribute(BaseException):
    pass

#####
# Item class
#
# This 'empty' class acts as a data structure to describe an item
# item_dict = {'name': '', 'description': '', 'unit price': '', 'quantity': '', 'sku': 'tax table': '', 'digital content': {'description': '', 'email delivery': '', 'key': '', 'url': '', 'display disposition': ''}, 'merchant-private-item-data': ''}
#
class Item:
    def __init__(self, item_dict):
	try:
	    self.title = item_dict['name']
	except:
	    raise MissingRequiredElement("Element 'name' is required in the item dictionary")

	try:
	    self.description = item_dict['description']
	except:
	    raise MissingRequiredElement("Element 'description' is required in the item dictionary")

	try:
	   self.unit_price = item_dict['unit price']
	except:
	    raise MissingRequiredElement("Element 'unit price' is required in the item dictionary")

	try:
	    self.quantity = item_dict['quantity']
	except:
	    raise MissingRequiredElement("Element 'quantity' is required in the item dictionary")

	try:
	    self.sku = item_dict['sku']
	except:
	    self.sku = None

	try:
	    self.tax_table = item_dict['tax table']
	except:
	    self.tax_table = None

	try:
	    self.digital_content = item_dict['digital content']
	except:
	    self.digital_content = None
	   
	try:
	    self.private_data = item_dict['private data']
	except:
	    self.private_data = None

#####
# Cart class
#
# This class represents a cart that can contain Items
#
class Cart:

    #####
    # Internal (mostly) functions
    #
    # These functions are pretty much only used internally, or at least transparently
    #
    empty_cart = """<?xml version="1.0" encoding="UTF-8"?>

<checkout-shopping-cart xmlns="http://checkout.google.com/schema/2">
  <shopping-cart>
    <items>
    </items>
  </shopping-cart>
  <checkout-flow-support>
    <merchant-checkout-flow-support>
      <shipping-methods>
      </shipping-methods>
    </merchant-checkout-flow-support>
  </checkout-flow-support>
</checkout-shopping-cart>"""

    def __init__(self, to_parse = empty_cart):
	"""initializes an instance of the Cart object
	   to_parse is a STRING to be parsed by parseString"""
	self.xml_cart = xml.dom.minidom.parseString(to_parse)
	self.index = 0
	self.item_list = ()
	for item in self.xml_cart.getElementsByTagName("item"):
	    for node in item.getElementsByTagName("item-name")[0]:
		if node.nodeType == node.TEXT_NODE:
		    name = node.data
	    for node in item.getElementsByTagName("item-description")[0]:
		if node.nodeType == node.TEXT_NODE:
		    description = node.data
	    for node in item.getElementsByTagName("unit-price")[0]:
		if node.nodeType == node.TEXT_NODE:
		    unit_price = node.data
	    for node in item.getElementsByTagName("quantity")[0]:
		if node.nodeType == node.TEXT_NODE:
		    quantity = node.data
	    for node in item.getElementsByTagName("merchant-item-id")[0]:
		if node.nodeType == node.TEXT_NODE:
		    sku = node.data
	    self.item_list.append(Item({'name': name, 'description': description, 'unit price': unit_price, 'quantity': quantity, 'sku': sku}))


    def __iter__(self):
	"""iterates through items in the cart
	   since we have a next() function, we don't need to do much other than return this object"""
	return self

    def next(self):
	""""""
    
    #####
    # Local functions
    #
    # These functions only affect the local cart (i.e. nothing sent to google)
    #
    def add_item(self, item):
	"""adds an item to the cart
	   item is an instance of the Item class"""
	self.item_list.append(item)
    
    def del_item(self, index):
	"""deletes an item from the cart
	   index is the index of the item in item_list"""
	try:
	    del self.item_list[index]
	except IndexError:
	    raise IndexError #XXX Will this be passed on?

    def set_shipping_flat_rate(self, rate):
    def set_shipping_merchant_calculated(self, rate):
    def set_shipping_carrier_calculated(self, carrier, default_cost):
    def set_shiping_pickup(self):
    def set_shipping_digital(self):

    
    def serialize(self):
	"""serializes the XML data
	   the DOM is first built, and then toxml() is called"""
	xml = parseString(self.empty_cart)
	items = xml.getElementsByTagName("items")[0]

	# Loop through all the items in the list and build a new container element to contain all the required and optional parts
	for item in item_list:
	    new_item = xml.createNode("item")

	    item_name = xml.createElement("item-name")
	    item_name.appendChild(xml.createTextNode(item.name))
	    new_item.appendChild(item_name)

	    item_desc = xml.createNode("item-description")
	    item_desc.appendChild(xml.createTextNode(item.description))
	    new_item.appendChild(item_desc)

	    unit_price = xml.createNode("unit-price")
	    unit_price.appendChild(xml.createTextNode(item.unit_price))
	    new_item.appendChild(unit_price)

	    quantity = xml.createNode("quantity")
	    quantity.appendChild(xml.createTextNode(item.quantity))
	    new_item.appendChild(unit_price)

	    if item.sku:
		sku = xml.createNode("merchant-item-id")
		sku.appendChild(xml.createTextNode(item.sku))
		new_item.appendChild(sku)

	    if item.tax_table:
		tax_table = xml.createNode("tax-table-selector")
		tax_table.appendChild(xml.createTextNode(item.tax_table))
		new_item.appendChild(tax_table)

	    if item.digital_content:
		digital_content = xml.createNode("digital_content")
		# Since this is a dictionary, try to fetch each key for the digital-content tag - since all are optional, don't throw any exceptions
		try:
		    if item.digital_content['description']:
			dc_desc = xml.createNode("description")
			dc_desc.appendChild(xml.createTextNode(item.digital_content['description']))
			digital_content.appendChild(dc_desc)
		except:
		    pass
		try:
		    if item.digital_content['email delivery']:
			dc_email = xml.createNode("email-delivery")
			dc_email.appendChild(xml.createTextNode(item.digital_content['email delivery']))
			digital_content.appendChild(dc_email)
		except:
		    pass
		try:
		    if item.digital_content['key']:
			dc_key = xml.createNode("key")
			dc_key.appendChild(xml.createTextNode(item.digital_content['key']))
			digital_content.appendChild(dc_key)
		except:
		    pass
		try:
		    if item.digital_content['url']:
			dc_url = xml.createNode("url")
			dc_url.appendChild(xml.createTextNode(item.digital_content['url']))
			digital_content.appendChild(dc_url)
		except:
		    pass
		try:
		    if item.digital_content['display disposition']:
			dc_disp = xml.createNode("display-disposition")
			dc_disp.appendChild(xml.createTextNode(item.digital_content['display disposition']))
			digital_content.appendChild(dc_disp)
		except:
		    pass
		new_item.appendChild(digital_content)

	    if item.private_data:
		private_data = xml.createNode("merchant-private-item-data")
		private_data.appendChild(xml.createTextNode(item.private_data))
		new_item.appendChild(private_data)

	    items.appendChild(new_item)

	return self.xml_cart.toxml("utf-8")


class Checkout:

class Calculation:

class Notification:

class Processing:
