from django.test import TestCase
import datetime as dt
from .models import Hood, Profile, Business

# Create your tests here.
class HoodTestClass(TestCase):
    """
    class that tests the characteristics of the Hood model
    """
    def setUp(self):
        """
        method that runs at the begginning of each test
        """
        self.hood = Hood(hoodName='Jamhuri')

    def test_hood_instance(self):
        """
        method that tests the instance of hood
        """
        self.assertTrue(isinstance(self.hood, Hood))

    def test_save_hood_method(self):
        """
        method that tests save method of the hood model
        """
        self.hood.save_hood()
        hood_object = Hood.objects.all()
        self.assertTrue(len(hood_object) > 0)

    def test_delete_hood_method(self):
        """
        method that tests the delete_profile method
        """
        self.hood.save_hood()
        hood_object = Hood.objects.all()
        self.hood.delete_hood()
        hood_object = Hood.objects.all()
        self.assertTrue(len(hood_object) == 0)


class BusinessTestClass(TestCase):
    """
    class that tests the characteristics of the Business model
    """
    def setUp(self):
        """
        method that runs at the begginning of each test
        """
        self.business = Business(business_name='Meat Point')

    def test_business_instance(self):
        """
        method that tests the instance of business
        """
        self.assertTrue(isinstance(self.business, Business))

    def test_save_business_method(self):
        """
        method that tests save method of the business model
        """
        self.business.save_business()
        business_object = Business.objects.all()
        self.assertTrue(len(business_object) > 0)

    def test_delete_business_method(self):
        """
        method that tests the delete method
        """
        self.business.save_business()
        business_object = Business.objects.all()
        self.business.delete_business()
        business_object = Business.objects.all()
        self.assertTrue(len(business_object) == 0)
