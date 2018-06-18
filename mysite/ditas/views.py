from sre_constants import _NamedIntConstant

from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.utils import timezone
from ditas.models import User, Food, News, Weight, Meal, Blood
from django.db import connection
from django.db.utils import OperationalError
from django.db.models.query import prefetch_related_objects
from django.conf import settings
import json, datetime, os
import MySQLdb
# Create your views here.

global yes_sign, no_sign, choice_list
yes_sign = ['응', '맞아']
no_sign = ['아니', '틀렸어']
choice_list = ['개인정보 입력','개인정보 확인','식단 검색','건강 관리','최근 1주 기록','건강정보 제공', '개발자에게 하고 싶은 이야기', '챗봇 정보 확인']

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
				'text': "고객의 이름, 생년월일(ex.1995-10-03), 성(남,여), 키 입력해주세요. (ex. 입력/당순이/1995-10-03/여/182.0) "
			},
			'keyboard': {
				'type': 'text'
			},
		})

	elif return_str == '식단 입력':
		return JsonResponse({
			'message': {
				'text': "먹은 식단에 대해서 다음과 같은 형태로 입력해주세요. ex. 먹은식단/밥,김치찌개,어묵조림,김치,꿀홍삼"
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
				'buttons': ['몸무게 입력', '식단 입력', '혈당 입력', '메인으로 복귀']
			}
		})

	elif return_str == '몸무게 입력':
		return JsonResponse({
			'message': {
				'text': "다음 형식으로 입력해주세요. ex. 몸무게/75.5"
			},
			'keyboard': {
				'type': 'text'
			}
		})

	elif return_str == '혈당 입력':
		return JsonResponse({
			'message': {
				'text': "다음 형식으로 입력해주세요.(식사 2시간 이후에 당 수치 기준) \n 식사 2시간 이후에 당 수치를 기록해주세요. ex. 혈당/130"
			},
			'keyboard': {
				'type': 'text'
			}
		})

	elif return_str == '식단 검색':
		return JsonResponse({
			'message': {
				'text': "다음 형식으로 입력해주세요. ex. 식단/꿀홍삼"
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
				'text': "개발자에게 한 마디 입력해주세요. (ex : 한마디/정보 입력이 잘 되지 않아요)"
			},
			'keyboard': {
				'type': 'text'
			}
		})

	elif return_str == '챗봇 정보 확인':
		return JsonResponse({
			'message': {
				'text': show_list()
			},
			'keyboard': {
				'type': 'buttons',
				'buttons': choice_list
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
	global user_name, q_obj
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
			obj.save()
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
			weight.kg_value = wei
			weight.save()

			data_list[0] = '오늘 하루 몸무게 정보가 수정되었습니다.'
			bPrint = True

		except User.DoesNotExist:
			data_list[0] = '먼저 정보 입력을 해주세요.'
			bPrint = True

		except Weight.DoesNotExist:
			w = Weight()
			w.user = user_ins
			w.kg_date = datetime.datetime.today().date()
			w.kg_value = wei
			w.save()
			data_list[0] = '오늘 하루 몸무게 정보가 입력되었습니다.'
			bPrint = True

	# 건강 관리 정보 입력(식단)
	if len(data_list) > 1 and data_list[0] == '먹은식단':
		# food_list = data_list[1].split(',')

		try:
			user_ins = User.objects.get(pk=user_name)  # user search

			# 입력 식품 리스트 별로 공공 식품 데이터에서 조회되지 않는 경우가 발생하여 텍스트 그대로 저장
			meal = Meal()
			meal.user = user_ins
			meal.food = None
			meal.food_list = data_list[1]
			meal.f_time = datetime.datetime.now() # 여기서 에러 발생 (서버에서 datetime.datetime.now() 시간 부분 저장은 문제 없지만, Mysql 서버에는 9시간 이전 시간으로 저장됨)
			meal.save()

			f_list = data_list[1].split(',')


			data_list[0] = '식단 정보가 입력되었습니다.'
			bPrint = True

		except Food.DoesNotExist:
			data_list[0] = '입력한 음식이 데이터베이스 상에서 존재하지 않습니다.'
			bPrint = True

	# 건강 관리 정보 입력(혈당)
	if len(data_list) > 1 and data_list[0] == '혈당':
		try:
			user_ins = User.objects.get(pk=user_name)  # user search

			# 입력 식품 리스트 별로 공공 식품 데이터에서 조회되지 않는 경우가 발생하여 텍스트 그대로 저장
			blood = Blood()
			blood.user = user_ins
			blood.bld_time = datetime.datetime.now() # 여기서 에러 발생 (서버에서 datetime.datetime.now() 시간 부분 저장은 문제 없지만, Mysql 서버에는 9시간 이전 시간으로 저장됨)
			blood.bld_data = float(data_list[1])
			blood.save()

			data_list[0] = '혈당 정보가 입력되었습니다.'
			bPrint = True

		except User.DoesNotExist:
			data_list[0] = '먼저 정보 입력을 해주세요.'
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
				data_list[0] = '입력하신 음식의 정보(' + data_list[1] + ')는 다음과 같습니다.\n'
				data_list[0] += '탄수화물 : ' + str(food.f_car) + '(g)\n' + '단백질 : ' + str(food.f_pro) + '(g)\n' + \
							   '지방 : ' + str(food.f_fat) + '(g)\n' + '당 : ' + str(food.f_dang) + '(g)\n' + \
							   '나트륨 : ' + str(food.f_ntr) + '(mg)\n' + '콜레스트롤 : ' + str(food.f_chol) + '(mg)'

				# 당 비율이 높은 음식은 주의 문구를 추가로 보내도록 한다. (0.05 이상)
				dang_per = float(food.f_dang / food.f_sz)
				if dang_per >= 0.05:
					data_list[0] += '\n' + data_list[1] + "은 당이 높습니다. 주의를 요합니다."

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

	# 유저의 최근 1주일 간 기록(몸무게, 혈당)
	if len(data_list) == 1 and data_list[0] == '최근 1주 기록':

		try:
			user_ins = User.objects.get(pk=user_name)  # user search

			weight_all = Weight.objects.filter(user = user_ins)
			meal_all = Meal.objects.filter(user = user_ins)
			blood_all = Blood.objects.filter(user = user_ins)

			max_weight = 0.0
			min_weight = 1000.0
			max_blood = 0.0
			min_blood = 1000.0

			for weight in weight_all:
				delta = datetime.datetime.now().date() - weight.kg_date
				if delta.days <= int(7):
					max_weight = max(max_weight,weight.kg_value)
					min_weight = min(min_weight, weight.kg_value)

			for blood in blood_all:
				delta = datetime.datetime.now().date() - blood.bld_time.date()
				if delta.days <= int(7):
					max_blood = max(max_blood,blood.bld_data)
					min_blood = min(min_blood,blood.bld_data)

			data_list[0] = user_ins.name + "님의 최근 1주일이에요. \n"

			if max_weight > 0.0:
				data_list[0] += "최고 몸무게는 " + str(max_weight) + "(kg)\n"

			else:
				data_list[0] += "최근 1주일 간 몸무게 기록이 없습니다. \n"


			if min_weight < 1000.0:
				data_list[0] += "최저 몸무게는 " + str(min_weight) + "(kg)\n"

			if max_blood > 0.0:
				data_list[0] += "최고 혈당은 " + str(max_blood) + "(mg/dl)\n"

			else:
				data_list[0] += "최근 1주일 간 혈당 기록이 없습니다. \n"


			if min_blood < 1000.0:
				data_list[0] += "최저 혈당은 " + str(min_blood) + "(mg/dl)"

			if max_blood > 200:
				data_list[0] += "\n 현재 당뇨 관리가 시급합니다. 당이 많이 든 음식은 최대한 자제해주시길 바랍니다."

			elif max_blood > 140:
				data_list[0] += "\n 당뇨 위기 단계에 속합니다. 지속적인 식단 관리가 필요합니다."

			else:
				data_list[0] += "\n 당 수치가 정상입니다. 그렇지만 주기적인 식단 관리는 DiTAS와 함께 해주세요~"

			bPrint = True

		except User.DoesNotExist:
			data_list[0] = '먼저 정보 입력을 해주세요.'
			bPrint = True

	# 개발자 한 마디
	if data_list[0] == '한마디':
		f = open(os.path.join(os.path.dirname(__file__),'c_log.txt'),'a',encoding='utf-8') # c_log.txt = 로그 파일
		text = user_name + '(' + str(datetime.datetime.now()) + ') : ' + data_list[1] + '\n'
		f.write(text)
		f.close()
		data_list[0] = '감사합니다. 개발에 잘 반영하겠습니다.'
		bPrint = True

	get_json_data = get_json(data_list[0], bPrint)
	return get_json_data

####################################
# new function 180617
####################################
def show_list():
	_message = '안녕하세요. 저는 당신의 당뇨 관리를 위한 생활 비서 Ditas입니다. \n' \
				'저는 아래 내용에 대해서 당신께 도움을 드릴 수 있어요! \n' \
				'1. 개인정보 입력 및 수정 \n' \
				'2. 개인정보 확인 \n' \
			   	'3. 식단 검색 \n' \
			   	'4. 건강 관리(몸무게, 식단, 혈당 입력)\n' \
			   	'5. 최근 1주일 간 몸무게 및 혈당 기록\n' \
			   	'6. 당뇨병 관련 정보 받기\n' \
				'7. 개발자에게 하고 싶은 이야기\n' \
				'Ditas는 항상 당신께 더 좋은 도움을 드리기 위해 개발 중입니다! 많은 관심 부탁드려요!'

	return _message

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
