from sre_constants import _NamedIntConstant

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from ditas.models import User, Food, News, Weight, Meal
from django.db import connection
from django.db.utils import OperationalError
from django.db.models.query import prefetch_related_objects
from django.conf import settings
import json, datetime, os
import MySQLdb
# Create your views here.

choice_list = ['개인정보 입력','개인정보 확인','식단 검색','건강 관리','건강정보 제공','개발자에게 하고 싶은 이야기']

def index(request):
	return HttpResponse("Hello, world. Welcome to DiTAS WebSite")

def keyboard(request):
	global choice_list
	return JsonResponse({
		'type' : 'buttons',
		'buttons' : choice_list
	})

def get_food_ins(food_param):

	foods_all = Food.objects.all()
	food = None

	for food_ins in foods_all:
		food_str = food_ins.f_name.split('/')
		bFind_sub = False
		bFind_real = False

		for food_name in food_str:
			if food_param == food_ins.f_name:
				bFind_real = True
				break

			if food_param in food_ins.f_name:
				bFind_sub = True
				break

		if bFind_real == True:
			food = food_ins
			break

		if bFind_sub == True:
			food = food_ins

	return food

def get_json_text(return_str):
	return JsonResponse({
		'message': {
			'text': return_str
		},
		'keyboard': {
			'type': 'text',
		},
	})

def get_json(return_str, bPrint):
	global choice_list
	if bPrint == True:
		return JsonResponse({
			'message': {
				'text': return_str
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': choice_list
			},
		})

	if return_str == '개인정보 입력':
		return JsonResponse({
			'message': {
				'text': "고객의 이름, 생년월일(ex.1993-10-04), 성(남,여), 키 입력해주세요. (ex. 입력/당순이/2018-05-21/남/180.0) "
			},
			'keyboard': {
				'type': 'text'
			},
		})

	elif return_str == '식단 검색':
		return JsonResponse({
			'message': {
				'text': "먹은 식단에 대해서 다음과 같은 형태로 입력해주세요. (ex. 식단/꿀홍삼)"
			},
			'keyboard': {
				'type': 'text'
			}
		})

	elif return_str == '건강 관리':
		return JsonResponse({
			'message': {
				'text': "몸무게 입력 혹은 식단 입력 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': ['몸무게 입력', '식단 입력', '메인으로 복귀']
			}
		})

	elif return_str == '몸무게 입력':
		return JsonResponse({
			'message': {
				'text': "다음과 같은 형식으로 입력해주세요. ex. 몸무게/75.5"
			},
			'keyboard': {
				'type': 'text'
			}
		})

	elif return_str == '식단 입력':
		return JsonResponse({
			'message': {
				'text': "다음과 같은 형식으로 입력해주세요. ex. 식단 입력/밥,김치,꿀홍삼"
			},
			'keyboard': {
				'type': 'text'
			}
		})

	elif return_str == '건강정보 제공':
		# 최신 건강정보 뉴스를 포함한 링크를 전송함.
		n = News.objects.order_by('news_date')
		for x in n:
			news_url = x.news_url
		return JsonResponse({
			'message': {
				'text': news_url
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': choice_list
			},
		})

	elif return_str == '메인으로 복귀':
		return JsonResponse({
			'message': {
				'text': "다음 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': choice_list
			}
		})

	elif return_str == '문제 발생':
		return JsonResponse({
			'message': {
				'text': "문제가 발생하였습니다. 다음 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': choice_list
			}
		})

	elif return_str == '데이터 입력 성공':
		return JsonResponse({
			'message': {
				'text': "데이터 입력에 성공하였습니다. 다음 버튼 중 하나를 클릭해주십시오."
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': choice_list
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
				'type': 'buttons',
				'buttons': choice_list
			}
		})

@csrf_exempt
def message(request):
	message = ((request.body).decode('utf-8'))
	return_json_str = json.loads(message)
	return_str = return_json_str['content']
	user_name = return_json_str['user_key']
	data_list = return_str.split('/')
	bPrint = False

	# 개인정보 입력
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
			obj.name = name
			obj.birth_date = datetime.datetime.strptime(date,'%Y-%m-%d').date()
			obj.gender = gender
			obj.height = float(h)
			data_list[0] = '유저 정보를 수정하였습니다.'
			bPrint = True
		except User.DoesNotExist:
			u.save()
			data_list[0] = '데이터 입력 성공'


	# 건강 관리 정보 입력(몸무게)
	if len(data_list) > 1 and data_list[0] == '몸무게':
		try:
			wei = float(data_list[1])

		except ValueError:
			data_list[0] = '해당 부분에는 숫자만 입력해주세요'
			bPrint = True
			return get_json(data_list[0],bPrint)

		try:
			user_ins = User.objects.get(pk=user_name) # user search
			weight = Weight.objects.get(user=user_ins,kg_date=datetime.datetime.today().date()) # weight search

			if weight == None:
				w = Weight()
				w.user = user_ins
				w.kg_date = datetime.datetime.today().date()
				w.kg_value = wei
				w.save()

			else: # Database에 당일 몸무게를 기록한 경우
				weight.kg_value = wei
				weight.save()

		except User.DoesNotExist:
			data_list[0] = '먼저 정보 입력을 해주세요.'
			bPrint = True

	# 건강 관리 정보 입력(식단)
	if len(data_list) > 1 and data_list[0] == '식단 입력':
		food_list = data_list[1].split(',')

		try:
			user_ins = User.objects.get(pk=user_name)  # user search

			for food in food_list:
				meal = Meal()
				meal.user = user_ins
				food_ins = get_food_ins(food)
				meal.food = food_ins
				meal.f_time = datetime.datetime.now() # 여기서 에러 발생 (서버에서 datetime.datetime.now() 시간 부분 저장은 문제 없지만, Mysql 서버에는 9시간 이전 시간으로 저장됨)
				meal.save()

			data_list[0] = '식단 정보가 입력되었습니다.'
			bPrint = True

		except Food.DoesNotExist:
			data_list[0] = '입력한 음식이 데이터베이스 상에서 존재하지 않습니다.'
			bPrint = True

	# 개인정보 확인
	if len(data_list) == 1 and data_list[0] == '개인정보 확인':
		try:
			obj = User.objects.get(pk=user_name)
			data_list[0] = '이름 : ' + obj.name + '\n' + '생년월일 : ' + str(obj.birth_date) + '\n' + '성별 : ' + obj.gender + '\n' + \
						   '키 : ' + str(obj.height)
			bPrint = True

		except User.DoesNotExist:
			data_list[0] = '먼저 정보 입력을 해주세요.'
			bPrint = True

	# 식단 체크
	if len(data_list) > 1 and data_list[0] == '식단':
		try:
			foods_all = Food.objects.all()
			food = None
			food = get_food_ins(data_list[1])

			if food is not None:
				data_list[0] = '섭취한 음식의 정보(' + food.f_name + ')는 다음과 같습니다.\n'
				data_list[0] += '탄수화물 : ' + str(food.f_car) + '(g)\n' + '단백질 : ' + str(food.f_pro) + '(g)\n' + \
							   '지방 : ' + str(food.f_fat) + '(g)\n' + '당 : ' + str(food.f_dang) + '(g)\n' + \
							   '나트륨 : ' + str(food.f_ntr) + '(mg)\n' + '콜레스트롤 : ' + str(food.f_chol) + '(mg)'
				bPrint = True

			else:
				data_list[0] = '입력한 음식이 데이터베이스 상에서 존재하지 않습니다.'
				bPrint = True

		except Food.DoesNotExist:
			data_list[0] = '입력한 음식이 데이터베이스 상에서 존재하지 않습니다.'
			bPrint = True

		except ValueError:
			data_list[0] = 'Value Error'
			bPrint = True

	# 개발자 한 마디
	if data_list[0] == '한 마디':
		f = open(os.path.join(os.path.dirname(__file__),'c_log.txt'),'w',encoding='utf-8')
		text = user_name + '(' + str(datetime.datetime.now()) + ') : ' + data_list[1]
		f.write(text)
		f.close()
		data_list[0] = '감사합니다. 개발에 잘 반영하겠습니다.'
		bPrint = True

	get_json_data = get_json(data_list[0], bPrint)
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
