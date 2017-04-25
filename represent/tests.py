# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class ViewsTest(TestCase):
	def test_404_error(self):
		response = self.client.get('/')
		self.assertEqual(response.status_code, 404)

	def test_correct_Response(self):
		response = self.client.get(reverse('templates:index'))
		self.assertEqual(response.status_code, 200)