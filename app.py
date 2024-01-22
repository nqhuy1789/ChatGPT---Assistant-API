from flask import Flask, request
from pymessenger import Element, Button
from bot import Bot
from wit import Wit
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
WIT_TOKEN = os.environ['WIT_TOKEN']
MENU_CAFE167 = 'https://photos.app.goo.gl/aamf4RfbptRmCP1Z6'
MENU_ONLINE_LINK = [
				{
					"title": "Menu Cafe167",
					"subtitle": "Hân hạnh được phục vụ quý khách",
					"image_url": MENU_CAFE167,
					"buttons": [
					{
						"type": "web_url",
						"url": "https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa",
						"title": "ShopeeFood"
					}],
				}]
				
			
			
bot = Bot(ACCESS_TOKEN)
client = Wit(access_token=WIT_TOKEN)

@app.route('/', methods = ['GET', 'POST'])
def webhook():
	if (request.method == 'GET'):
		token = request.args.get("hub.verify_token")
		return verify_token(token)
	elif (request.method == 'POST'):
		output = request.get_json()
		for event in output['entry']:
			messaging = event['messaging']
			for message in messaging:
				if message.get('message'):
					recipient_id = message['sender']['id']
					sendTypingOn(recipient_id)
					text = message['message'].get('text')
					if text: 
						user_profile = bot.get_user_info(recipient_id)
						if user_profile:
							user_first_name = user_profile['first_name']
						else:
							user_first_name = 'bạn'
						generate_message(text,recipient_id, user_first_name)
					sendTypingOff(recipient_id)
	return '200 OK HTTPS.'

def verify_token(token):
	if token == VERIFY_TOKEN:
		return request.args.get("hub.challenge")
	return 'Lỗi sai mã kết nối'

def image_send(recipient_id, image_path):
	bot.send_image_url(recipient_id, image_path)
	return "success"

def message_send(recipient_id, response):
	bot.send_text_message(recipient_id, response)
	return "success"

def element_send(recipient_id, elements):
	bot.send_generic_message(recipient_id, elements)
	return "success"

def sendTypingOn(recipient_id):
	bot.send_action(recipient_id, action='typing_on')
	return "success"

def sendTypingOff(recipient_id):
	bot.send_action(recipient_id, action='typing_off')
	return "success"

def generate_message(text, recipient_id, user_first_name):
	response_sent_text = ''
	response_sent_image = ''
	intents = ''
	entities = list()
	response = client.message(text)
	if response['intents']:
		intents = response['intents'][0]['name']
		if intents == 'mo_dau':
			response_sent_text = f"Xin chào {user_first_name} đã ghé thăm Fanpage Cafe167. Đây là menu của quán, chúc {user_first_name} chọn được thức uống vừa ý!"
			message_send(recipient_id, response_sent_text)
			element_send(recipient_id, MENU_ONLINE_LINK)
			# elements = []
			# element = Element(title="Menu Cafe167", image_url=MENU_CAFE167, subtitle="ShopeeFood", item_url="https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa")
			# elements.append(element)
			# element_send(recipient_id, elements)
			# response_sent_image = MENU_CAFE167
			# image_send(recipient_id, response_sent_image)
			# response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
			# message_send(recipient_id, response_sent_text)
		elif intents == 'ket_thuc':
			response_sent_text = "Xin cảm ơn quý khách đã ủng hộ Cafe167. Hẹn gặp lại quý khách."
			message_send(recipient_id, response_sent_text)
		elif intents == 'muon_mua':
			response_sent_text = "Xin cảm ơn quý khách đã ủng hộ. Vui lòng để lại tên và số điện thoại để quán liên hệ giao hàng, hoặc click vào link để đặt hàng online : https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
			message_send(recipient_id, response_sent_text)
		elif intents == 'loai_hang_hoa':
			if response['entities']:
				entities = response['entities']
				bPrint = False
				for item  in entities:
					if entities[item][0]['role'] == 'hang_dac_biet':
						response_sent_text = "Đây là các món signature của quán: Trà chanh giã tay, Marble bơ cà phê, Trà sữa ngọc trai lá nếp. Click vào link để đặt hàng online : https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"		
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'cafe':
						response_sent_text = "Đây là menu cafe của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/420041016_122108902460177774_7165810135327767889_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeHnol4fWr1KTlD3Q7mH1ElHKm3HWY3iKVMqbcdZjeIpUzLyyDxzWtSoAr8rhzHmVqPIGrAQsxl-r_-Ks5rs-rOn&_nc_ohc=RVFWmLROoTAAX_2bdJs&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfCdtvstYno9mn0Zex3Uz_oxgGy3Vw1n3XtO3bAEZoU3zg&oe=65AD88BB'		
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'tra':
						response_sent_text = "Đây là menu trà của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/420035116_122108902502177774_6314051225205981823_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeGJAIBoDDGT34m0mc19qAl_jJlh3-TFKk-MmWHf5MUqT1xcVm61c2usKBEnxRApCFL_5SxWQb5igaxlM1JAH12L&_nc_ohc=Y3D1xeWekD0AX9qz3iy&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfDqHxFfGuCij-5ewpNoVmS1lrQDzfJTxUGE9NzFBY4o8w&oe=65ABE509'		
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'tra_sua':
						response_sent_text = "Đây là menu trà sữa của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/419735467_122108902514177774_3911680859865134942_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeFkVyU8Tyel44nMH0dijzKoppGwXaZOEKqmkbBdpk4QqhFc3rpCtsgJnTTZdTxSqzPMV635xZwMEQ2I517CJxEW&_nc_ohc=xoAwQ2yQi9kAX_1YU3l&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfDMb0HpbEdEgFgb3ajsKB9VQ_FWRA6AzerKa04Sf9_2OA&oe=65AC599B'		
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'soda':
						response_sent_text = "Đây là menu soda của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/420018215_122108902484177774_2849894979951740486_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeGWC8h3GuUdxKHvLdwNCgzMG4uiypgyIrEbi6LKmDIisb1ZTdaZ6gGbMZBN-09w5rWcswVwhGRXZDyd1gSVUlCX&_nc_ohc=lK221N6FemgAX9LIFBg&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfAEgDaKdcmt3fWKVOhPL2RJjN6SSciwMX0vuTyS7V3V3w&oe=65AD7C56'		
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)	
						bPrint = True	
						break	
					elif entities[item][0]['role'] == 'yogurt':
						response_sent_text = "Đây là menu yogurt của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/420459779_122108902418177774_8067036978686612593_n.jpg?_nc_cat=108&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeECAgaH1FY1AiAoqpS_7TeOmf5eaEgGzCWZ_l5oSAbMJSFa_cvlRrUDiw3cgNobeodiuFJRS9wk5HENBzGu7tc_&_nc_ohc=pPT0UygrqO0AX_zkOTs&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfC_iH30KGceRRCfONFy8P9DLIgo0lqChyXmnt21WaD9AA&oe=65AC2059'		
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)	
						bPrint = True	
						break
					elif entities[item][0]['role'] == 'nuoc_ep':
						response_sent_text = "Đây là menu nước ép của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/420024139_122108902478177774_5047453647158816145_n.jpg?_nc_cat=103&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeFVaZm7rVt0NPTI3I06-T1ixjAOmUiCi9jGMA6ZSIKL2G-63uhXpzEUAEdYD7eYSE4L2On5OSOZAAiTG9dJMnsU&_nc_ohc=N6IICDDiZnQAX-zZdpC&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfD0CLyiig_3V8FbbdYFaopWn1egAZTlX0mdr5ZqXR6Ptw&oe=65ACEA34'		
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)	
						bPrint = True
						break
					elif entities[item][0]['role'] == 'topping':
						response_sent_text = "Đây là menu topping của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/420021642_122108902490177774_5161320864997202696_n.jpg?_nc_cat=106&ccb=1-7&_nc_sid=3635dc&_nc_eui2=AeEctNvp0DWDbfzZ_Lj4Lqq6fYyxCF146zt9jLEIXXjrO5y5cl5_onM6Z7Y8qSKtNsOV5HaNKiExt0Ch4jtdm-Rp&_nc_ohc=Bj9xxh8WZ8QAX_i9EvI&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfD8pxubjqRHERHWBRPpKoaTY3u-nP-HJCQg4LKc0Xg4Mg&oe=65AD6C24'		
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)	
						bPrint = True
						break
				if bPrint == False:
						response_sent_text = "Đây là menu của quán. Vui lòng để lại tên, số điện thoại, Cafe167 sẽ liên hệ hỗ trợ bạn ngay."
						message_send(recipient_id, response_sent_text)
						response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/418514395_122107255376177774_7917820904535141587_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=dd5e9f&_nc_eui2=AeGXT2cWi6vGNGi7xMLuzaWMgS8vYg4irqmBLy9iDiKuqYgNUkdi72ZaGsaof3kiKBiSsmUey7KfjYafZJMT5UG4&_nc_ohc=QL8l34ozMv0AX8x-zC6&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfDwwlyuQTjQyxl2-vWfPo7S3oZciBvKImxKsZK9X8GSsA&oe=65AD0DB6'
						image_send(recipient_id, response_sent_image)
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)
			else:
				response_sent_text = "Đây là menu của quán. Vui lòng để lại tên, số điện thoại, Cafe167 sẽ liên hệ hỗ trợ bạn ngay."
				message_send(recipient_id, response_sent_text)
				response_sent_image = 'https://scontent.fsgn1-1.fna.fbcdn.net/v/t39.30808-6/418514395_122107255376177774_7917820904535141587_n.jpg?_nc_cat=102&ccb=1-7&_nc_sid=dd5e9f&_nc_eui2=AeGXT2cWi6vGNGi7xMLuzaWMgS8vYg4irqmBLy9iDiKuqYgNUkdi72ZaGsaof3kiKBiSsmUey7KfjYafZJMT5UG4&_nc_ohc=QL8l34ozMv0AX8x-zC6&_nc_ht=scontent.fsgn1-1.fna&oh=00_AfDwwlyuQTjQyxl2-vWfPo7S3oZciBvKImxKsZK9X8GSsA&oe=65AD0DB6'
				image_send(recipient_id, response_sent_image)
				response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
				message_send(recipient_id, response_sent_text)
		elif intents == 'thong_tin':
			if response['entities']:
				entities = response['entities']
				bPrint = False
				for item  in entities:
					if entities[item][0]['role'] == 'hang_dac_biet':
						response_sent_text = "Cafe167 xin gửi đến bạn chương trình khuyến mãi đặc biệt tại địa chỉ: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'muon_mua':
						response_sent_text = "Đặt hàng online tại: https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'gio':
						response_sent_text = "Cafe167 mở cửa từ 7h - 22h mỗi ngày"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'do_an':
						response_sent_text = "Hiện nay quán không bán đồ ăn. Mong bạn thông cảm!"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'dia_chi':
						response_sent_text = "Địa chỉ của quán là 167bis Hoàng Sa, phường Tân Định, quận 1. Bạn đi theo Google map này nhé: https://maps.app.goo.gl/heazVACbVuWSEjqo8"
						message_send(recipient_id, response_sent_text)
						bPrint = True
						break
				if bPrint == False:
					response_sent_text = "Vui lòng để lại tên và số điện thoại, Cafe167 sẽ liên hệ hỗ trợ bạn ngay."
					message_send(recipient_id, response_sent_text)
	else:
		response_sent_text = "Xin cảm ơn quý khách đã quan tâm đến Cafe167, chúc quý khách một ngày tốt lành."
		message_send(recipient_id, response_sent_text)


# if __name__ == '__main__':
# 	app.run()