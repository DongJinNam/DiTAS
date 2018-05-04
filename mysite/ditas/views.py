from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def keyboard(request):
	return JsonResponse({
		'type' : 'buttons',
		'buttons' : ['정보 입력','건강 관리','건강정보 제공','Q&A']
	})

@csrf_exempt
def message(request):
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']

	return JsonResponse({
		'message': {
			'text' : "button test : " + return_str
		},
		'keyboard': {
			'type' : 'text'
		}
	})
