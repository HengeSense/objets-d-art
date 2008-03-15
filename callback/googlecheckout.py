import xml.dom.minidom

#####
# Item class
#
# This 'empty' class acts as a data structure to describe an item
#
class Item:
    def __init__(self, item_dict):
	self.title = item_dict['name']
	self.description = item_dict['description']
	self.unit_price = item_dict['unit price']
	self.quantity = item_dict['quantity']
	self.sku = item_dict['sku']

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
    item_list = ()
    def __init__(self, to_parse):
	"""initializes an instance of the Cart object
	   to_parse is a STRING to be parsed by parseString"""
	self.xml_cart = xml.dom.minidom.parseString(to_parse)
	self.index = 0
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
	    item_list.append(Item({'name': name, 'description': description, 'unit price': unit_price, 'quantity': quantity, 'sku': sku}))


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
	   item_dict is an instance of the Item class"""
	item_list.append(item)
    
    def del_item(self, index):
	"""deletes an item from the cart
	   index is the index of the item in item_list"""
	try:
	    del item_list[index]
	except IndexError:
	    raise IndexError #XXX Will this be passed on?
    
    def serialize(self):
	"""serializes the XML data
	   this is a front-end to the minidom's 'toxml()' function"""
	return self.xml_cart.toxml("utf-8")

