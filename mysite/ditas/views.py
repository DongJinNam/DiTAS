from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

def index(request):
	return HttpResponse("Hello, world. Welcome to DiTAS WebSite")

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
	user_name = return_json_str['user_key']

	return JsonResponse({
		'message': {
			'text' : user_name + "이 입력한 " + return_str
		},
		'keyboard': {
			'type' : 'text'
		}
	})

@csrf_exempt
def friend_add(request):
	json_str = (request.body).decode('utf-8')
	received_json_data = json.loads(json_str)
	print('친구 등록 하였습니다' + received_json_data)

@csrf_exempt
def friend_remove(request):
	json_str = (request.body).decode('utf-8')
	received_json_data = json.loads(json_str)
	print('친구 삭제 하였습니다' + received_json_data)
