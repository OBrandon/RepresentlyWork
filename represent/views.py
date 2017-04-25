# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, Http404
from .forms import SubmitZipCode
import requests
import json

# Create your views here.
def congressmen(request):
	if request.method == "POST":
		form = SubmitZipCode(request.POST)
		if form.is_valid():
			zipcode = form.cleaned_data['zipcode']
			datazip = {'zip': zipcode}
			resp = requests.get('https://congress.api.sunlightfoundation.com/districts/locate', params=datazip)
			if resp.status_code != 200:
				raise Http404("District number could not be found StatusCode:".format(resp.status_code))
			js = resp.json()
			state_name = js['results'][0]['state'] 
			district_number = js['results'][0]['district']
			house = 'house'
			congress_data = {'house':'house',
			'state_name':state_name, 'district_number':district_number}
			response = requests.get('https://api.propublica.org/congress/v1/members/house/'+state_name+'/{}'.format(district_number)+
				'/current.json', headers={'X-API-Key': 'HeU67wOwjMas9zx1MWRRg4fB09F4YyJ87jgec6xv'})
			if response.status_code != 200:
				raise Http404("Congressperson could not be found StatusCode:".format(response.status_code))
			congress = response.json()
			member_id = congress['results'][0]['id'] 
			res = requests.get('https://api.propublica.org/congress/v1/members/'+member_id+'/votes.json', 
				headers={'X-API-Key': 'HeU67wOwjMas9zx1MWRRg4fB09F4YyJ87jgec6xv'})
			if res.status_code != 200:
				raise Http404("District number could not be found StatusCode:".format(res.status_code))
			politicianVotes = res.json()
			newDict = {}
			votes = politicianVotes['results'][0]['votes']
			for value in votes:
				emptyBill = value['bill']
				if emptyBill:
					billName = value['bill']['title']
					newDict[billName] = value['position']
		return render(request, 'submit.html', {'newDict': newDict,'congress': congress['results'][0]})
	else:
		form = SubmitZipCode()

	return render(request, 'index.html', {'form': form})
