##########################################################################
#####
##### googlecheckout.py - An implementation of the Google Checkout XML API
#####   by Matt Scott
#####
##### This software is released under the GNU General Public License v.3
##### Find out more here: < http://www.gnu.org/licenses/gpl.html >
#####
##########################################################################

from xml.dom.minidom import *

#####
# Exception classes
#
# These classes are provided as fairly empty classes to throw as exceptions.
#
class GCBaseException(Exception):
    pass

class MissingRequiredElement(GCBaseException):
    pass

class MissingRequiredAttribute(GCBaseException):
    pass

class XMLError(GCBaseException):
    pass

class ServerError(GCBaseException):
    pass

#####
# Item class
#
# This 'empty' class acts as a data structure to describe an item
#
class Item:
    def __init__(self, item_dict = None, item_node = None):
    if item_dict:
        self._parse_dict(item_dict)
    elif item_node:
        self.node = item_node
    def _parse_dict(self, item_dict):
    """_parse_dict builds a DOM object from a dict
        item_dict = {'name': '', 'description': '', 'unit price': '', 'quantity': '', 'sku': 'tax table': '', 'digital content': {'description': '', 'email delivery': '', 'key': '', 'url': '', 'display disposition': ''}, 'merchant-private-item-data': ''}
    """

    self.xml = Document()
    self.node = self._xmldoc.createElement("item")

    # These first four elements are required, so throw a fit if they're not around
    try:
        item_name = self.xml.createElement("item-name")
        item_name.appendChild(self.xml.createTextNode(item_dict['name']))
        self.node.appendChild(item_name)
    except KeyError:
        raise MissingRequiredElement("Element 'name' is required in the item dictionary")

    try:
        item_desc = self.xml.createNode("item-description")
        item_desc.appendChild(self.xml.createTextNode(item_dict['description']))
        self.node.appendChild(item_desc)
    except KeyError:
        raise MissingRequiredElement("Element 'description' is required in the item dictionary")

    try:
        unit_price = self.xml.createNode("unit-price")
        unit_price.appendChild(self.xml.createTextNode(item_dict['unit price']))
        self.node.appendChild(unit_price)
    except KeyError:
        raise MissingRequiredElement("Element 'unit price' is required in the item dictionary")

    try:
        quantity = self.xml.createNode("quantity")
        quantity.appendChild(self.xml.createTextNode(item_dict['quantity']))
        self.node.appendChild(unit_price)
    except KeyError:
        raise MissingRequiredElement("Element 'quantity' is required in the item dictionary")

    # These next elements are not required, so handle them gracefully
    try:
        sku = self.xml.createNode("merchant-item-id")
        sku.appendChild(self.xml.createTextNode(item_dict['sku']))
        self.node.appendChild(sku)
    except KeyError:
        pass

    try:
        tax_table = self.xml.createNode("tax-table-selector")
        tax_table.appendChild(self.xml.createTextNode(item_dict['tax_table']))
        self.node.appendChild(tax_table)
    except KeyError:
        pass

    try:
        dc = item_dict['digital content']
        digital_content = self.xml.createNode("digital-content")

        # Since this is a dictionary, try to fetch each key for the digital-content tag - since all are optional, don't throw any exceptions
        try:
            if dc['description']:
            dc_desc = self.xml.createNode("description")
            dc_desc.appendChild(selfxml.createTextNode(dc['description']))
            digital_content.appendChild(dc_desc)
        except KeyError:
            pass
        try:
        if dc['email delivery']:
            dc_email = self.xml.createNode("email-delivery")
            dc_email.appendChild(self.xml.createTextNode(dc['email delivery']))
            digital_content.appendChild(dc_email)
        except KeyError:
            pass
        try:
            if dc['key']:
            dc_key = self.xml.createNode("key")
            dc_key.appendChild(self.xml.createTextNode(dc['key']))
            digital_content.appendChild(dc_key)
        except KeyError:
            pass
        try:
            if dc['url']:
            dc_url = self.xml.createNode("url")
            dc_url.appendChild(self.xml.createTextNode(dc['url']))
            digital_content.appendChild(dc_url)
        except KeyError:
            pass
        try:
            if dc['display disposition']:
            dc_disp = self.xml.createNode("display-disposition")
            dc_disp.appendChild(self.xml.createTextNode(dc['display disposition']))
            digital_content.appendChild(dc_disp)
        except KeyError:
            pass
        self.node.appendChild(digital_content)
    except KeyError:
        pass

    try:
        private_data = xml.createNode("merchant-private-item-data")
        private_data.appendChild(self.xml.createTextNode(item_dict['private_data']))
        self.node.appendChild(private_data)
    except KeyError:
        pass

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

    #####
    # Shipping class
    #
    # Because this class is just a container for XML nodes that are handled internally, it can be empty
    #
    class _shipping:
        def __init__(self, node):
            if node:
                self.node = node
            else:
                raise MissingRequiredElement("An empty node was passed to shipping: logic error")

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
  <order-processing-support>
  </order-processing-support>
</checkout-shopping-cart>"""

    def __init__(self, to_parse = None):
    """initializes an instance of the Cart object
       to_parse is a STRING to be parsed by parseString"""
    self.index = 0
    self.item_list = ()
    self.shipping_list = ()

    # if we have data in the cart, take it apart and keep it in
    # easier-to-process lists
    if to_parse:
        self.xml_cart = xml.dom.minidom.parseString(to_parse)
        for item in self.xml_cart.getElementsByTagName("item"):
            self.item_list.append(Item(item_node = item))
        for shipping in self.xml_cart.getElementsbyTagName("shipping-methods")[0].childNodes:
            self.shipping_list.append(Cart._shipping(node = shipping))
    # Start with an empty cart that can be repopulated with lists.
    self.xml_cart = xml.dom.minidom.parseString(empty_cart)

    def __iter__(self):
        """ iterates through items in the cart
            since we have a next() function, we don't need to do much other than return this object"""
        return self

    def next(self):
        """"""
        if self.index >= len(self.item_list):
            raise StopIteration
        self.index = self.index + 1
        return self.item_list[self.index]
    
    #####
    # Local functions
    #
    # These functions only affect the local cart (i.e. nothing sent to google)
    #
    def add_item(self, item):
       """ adds an item to the cart
           item is an instance of the Item class"""
        self.item_list.append(item)

    def del_item(self, idx):
        """ deletes an item from the cart
            idx is the index of the item in item_list"""
        self.item_list[idx].node.unlink()
        del self.item_list[idx]

    def add_shipping_flat_rate(self, rate):
        """ adds a flat-rate shipping method
            shipping methods are built into a list and only added to the cart when serialize() is called"""
        self.xml_cart.createElement

    def set_shipping_merchant_calculated(self, rate): pass

    def set_shipping_carrier_calculated(self, carrier, default_cost): pass

    def set_shiping_pickup(self): pass

    def set_shipping_digital(self): pass
    
    def del_shipping(self, idx):
        """ deletes a shipping method from the list
           idx is the index of the item in shipping_list"""
        self.shipping_list[idx].node.unlink()
        del self.shipping_list[idx]

    def del_all_shipping(self):
        """ deletes all shipping methods from the list
            useful particularly for not having to search through DOM objects for a particular shipping method to delete"""
        i = 0
        for i in len(self.shipping_list) - 1:
            self.del_shipping(i)

    def set_request_auth_details(self, value = "False"):
        tag = self.xml_cart.createElement("request-initial-auth-details")
        tag.appendChild(self.xml_cart.createTextNode(value))
        self.xml_cart.getElementsByTagName("order-processing-support")[0].appendChild(tag)
    
    def serialize(self):
        """ serializes the XML data
            the DOM is first built, and then toxml() is called"""
        for item in self.item_list:
            self.xml_cart.getElementsByTagName("items")[0].appendChild(item.node)
        for shipping in self.shipping_list:
            self.xml_cart.getElementsbyTagName("shipping-methods")[0].appendChild(shipping.node)
        self.xml_cart.getElementsByTagName("shopping-cart")[0].appendChild(items)
        return self.xml_cart.toxml("utf-8")

    #####
    # Remote functions
    #
    # These are functions that actually send data to a remote server
    #
    def diagnose(self): pass
    def test(self): pass
    def commit(self): pass

class Interaction:
    def __init__(self, merchant_id, merchant_key, xml_data, testing = False):
        self.xml_data = xml_data
        self.testing = testing
        self.merchant_id = merchant_id
        self.merchant_key = merchant_key
        self.auth_data = b64encode(merchant_id + ':' + merchant_key)
        self._postinit()

    def _postinit(self): pass

    def _hello(self):
        xml_temp = xml.dom.minidom.parseString('<hello xmlns="http://checkout.google.com/schema/2" />')
        return self._write(xml_temp.toxml())
    def test_server(self):
        if ~the root node is bye~: #XXX
            return True
        else:
            return False

    def _diagnose(self):
        url_temp = self.url + '/diagnose'
        return self._write(self.xml_data, url = url_temp)
    def test_request(self):
        response = self._diagnose()
        if response.documentElement.tagname == "diagnosis":
            return (True, response)
        else:
            return (False, response)

    def _commit(self):
        return self._write(self.xml_data)
    def send_request(self): 
        import re
        response = self._commit()
        exec("self.%s(response)" % '_' + re.sub('-', '_', response.documentElement.tagname)) # SAX made simple

    def _write(self, xml, url = self.url):
        import urllib2, base64
        request = urllib2.Request(url, data = xml)
        request.add_header('Authorization', 'Basic ' + base64.b64encode(self.merchant_id + ':' + self.merchant_key))
        request.add_header('Content-type', 'application/xml;charset=UTF-8')
        request.add_header('Accept', 'application/xml;charset=UTF-8')
        try:
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            raise ServerError(str(e))
        return xml.dom.minidom.parseString(response.read())

class Checkout(Interaction):
    def _postinit(self):
        if self.testing is True:
            self.url = "https://sandbox.google.com/checkout/api/checkout/v2/merchantCheckout/Merchant/" + self.merchant_id
        else:
            self.url = "https://checkout.google.com/api/checkout/v2/merchantCheckout/Merchant/" + self.merchant_id

    def send_request(self):
        response = self._commit()

class Calculation:
    def _postinit(self):
        if self.testing is True:
            self.url = "" + self.merchant_id
        else:
            self.url = "" + self.merchant_id

    def send_request(self):
        x = self._commit()

class Notification: pass
    def _postinit(self):
        if self.testing is True:
            self.url = "" + self.merchant_id
        else:
            self.url = "" + self.merchant_id

    def send_request(self):
        x = self._commit()

class Processing: pass
    def _postinit(self):
        if self.testing is True:
            self.url = "https://sandbox.google.com/checkout/api/checkout/v2/request/Merchant/" + self.merchant_id
        else:
            self.url = "https://checkout.google.com/api/checkout/v2/request/Merchant/" + self.merchant_id

    def send_request(self):
        x = self._commit()
