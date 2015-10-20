"""
This file contains a small subset of the tests we will run on your backend submission
"""

import unittest
import os
import testLib
import random
from time import time

class TestSmiles(testLib.RestTestCase):

    ### THESE TESTS ARE NOT FINALIZED. FEEL FREE TO MODIFY
    def testSanityReg(self):
        self.makeRequest('/users', 'POST', {
            "username": "testuser",
            "password": "password",
            "nickname": "nick"
        });
    def testSanityLogin(self):
        self.makeRequest('/users/login', 'PUT', {
            "username": "testuser",
            "password": "password"
        });
        
    def testSanityLogout(self):
        self.makeRequest('/users/login', 'DELETE');
