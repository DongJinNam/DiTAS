from sre_constants import _NamedIntConstant

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from ditas.models import User
from django.db import connection
from django.db.utils import OperationalError
from django.conf import settings
import json, datetime, os
import MySQLdb
# Create your views here.


def index(request):
	return HttpResponse("Hello, world. Welcome to DiTAS WebSite")

def keyboard(request):
	return JsonResponse({
		'type' : 'buttons',
		'buttons' : ['정보 입력','건강 관리','건강정보 제공','개발자에게 하고 싶은 이야기']
	})

def get_json(return_str, bPrint):

	if bPrint == True:
		return JsonResponse({
			'message': {
				'text': return_str
			},
			'keyboard': {
				'type': 'text'
			},
		})

	if return_str == '정보 입력':
		return JsonResponse({
			'message': {
				'text': "고객의 이름, 생년월일(ex.1993-10-04), 성(남,여), 키 입력해주세요. (ex. 입력/당순이/2018-05-21/남/180.0) "
			},
			'keyboard': {
				'type': 'text'
			},
		})

	elif return_str == '건강 관리':
		return JsonResponse({
			'message': {
				'text': "몸무게 입력 혹은 식단 입력 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': ['건강 관리-몸무게 입력', '건강 관리-식단 입력', '메인으로 복귀']
			}
		})

	elif return_str == '건강정보 제공':
		return JsonResponse({
			'message': {
				'text': "건강정보 제공 준비중입니다. 잠시 기다려주세요. "
			},
			'keyboard': {
				'type': 'text'
			},
		})

	elif return_str == '메인으로 복귀':
		return JsonResponse({
			'message': {
				'text': "다음 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': ['정보 입력', '건강 관리', '건강정보 제공', '개발자에게 하고 싶은 이야기']
			}
		})

	elif return_str == '문제 발생':
		return JsonResponse({
			'message': {
				'text': "문제가 발생하였습니다. 다음 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': ['정보 입력', '건강 관리', '건강정보 제공', '개발자에게 하고 싶은 이야기']
			}
		})

	elif return_str == '데이터 입력 성공':
		return JsonResponse({
			'message': {
				'text': "데이터 입력에 성공하였습니다. 다음 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': ['정보 입력', '건강 관리', '건강정보 제공', '개발자에게 하고 싶은 이야기']
			}
		})

	elif return_str == '개발자에게 하고 싶은 이야기':
		return JsonResponse({
			'message': {
				'text': "개발자에게 한 마디 입력해주세요. (ex : 한 마디/정보 입력이 잘 되지 않아요)"
			},
			'keyboard': {
				'type': 'text'
			}
		})

	else: # for print
		return JsonResponse({
			'message': {
				'text': '지정된 형식을 지켜주시면 감사하겠습니다.'
			},
			'keyboard': {
				'type': 'text'
			}
		})

@csrf_exempt
def message(request):
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']
	user_name = return_json_str['user_key']
	data_list = return_str.split('/')

	if len(data_list) > 1 and data_list[0] == '입력':
		name = data_list[1]
		date = data_list[2]
		gender = data_list[3]
		h = data_list[4]

		u = User(u_id=user_name)
		u.name = name
		u.birth_date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
		u.gender = gender
		u.height = float(h)

		try:
			obj = User.objects.get(pk=user_name)
			data_list[0] = 'already object exist'
		except User.DoesNotExist:
			u.save()
			data_list[0] = '데이터 입력 성공'

	if data_list[0] == '한 마디':
		f = open(os.path.join(os.path.dirname(__file__),'c_log.txt'),'w',encoding='utf-8')
		text = user_name + '(' + str(datetime.datetime.now()) + ') : ' + data_list[1]
		f.write(text)
		f.close()
		data_list[0] = '수고하셨습니다.'
		get_json_data = get_json(data_list[0], True)
		return get_json_data

	get_json_data = get_json(data_list[0], False)
	return get_json_data

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
