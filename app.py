from flask import Flask, request
from pymessenger import Element, Button
from bot import Bot
from wit import Wit
import os

app = Flask(__name__)
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
VERIFY_TOKEN = os.environ['VERIFY_TOKEN']
WIT_TOKEN = os.environ['WIT_TOKEN']
LOGO_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV8492KOEEG_mbIplp-C2uumsRq3hfO2oz7f5Dt6BnciOgS1ZjtmXi3-frSEQCQq0rVMXlgqi4qg5eWyaEqciJMajkECd2pkw-lt6a1NQCV7RK5TSlRNDKYCGCmDk1PB6qVVDDKwBRKQ7O9-bQI5kwc5ShFKCiOdIGmK-1rWs5PTCXHLQzZ1URgr3Ssm28Mh1YC-mX47NGC22P2l20jpDLGorP-nwUf7o9ZVLIeJ6ygxg52rL_mM-7ZFpAK-zi1WrhoKZDDy3Sh6aFwkNiIfFLOoJJaBrLoS213AkbxNLPzCfN3wcEEQ-R70XywZ1Af7zjq7vcyVF6FWp7UVIENx07Si4FShC3RG3LkUpdZLv-aRK417tv3sScW6hFwxLupxmXZh_R6A1rJyfFaAsC-WiE_lU2IKmwX_ePI3tereYmGsdZLeHMhvTKnpzqPOT7swn-i4iDH08Ay2JFSfGnH_r42bD912CZjVEyVdawCNk9arqCI4uXqMdbo1zO8xuz_jbgnqSTqITJmV-hPZNWvK4h3Cp4BjYEqojggcRDNsx_9Ryb8yBvTl-RuRr5NoEBNNN3SFpM7CVe2ard8QtBI6Cee_nzQ51uSjtnw0g9_rrG_nSC-11ZpfoclKy7imXiexz55tUd9hDZIzJuLzlZzyfp0gRmk2Zh5aemo6xGJryqzy7y2ckFnlnAC92xCFvJcqxpHX87AnCDk1lD-WG_60Xe9iSCm5cy5gywRJeM7rDdkL-WI1P4G08gyLOQRONc-fFWLE8lLpe6dJWeauvF3ge28ebjHn6cMXORoUqV4T15cDwgtQ4p7a3jQftdjlP6UFcHsGIFOHVFRW2HYhQ0pedb8wPo0o0kEZ8btvpVntCMlik1uNUO8gyQJjr_XD7UMu9gg=w1000-no-tmp.jpg'
MENU_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV86Y6hOo7s6GLdb-9EBifeLCP4g3Sv7mk3AWtK0vEq5cvDXNmwzK7X4qU1weWbpL-zzFSUQepOFQavRgMKyrczbWoe81nOKh3Rwkw5HgK9muxMMfbYjYjf53K8ty-z86OJym1lX5IWut8htdT4NW3uVf4UvMmQHw-z5j12EkMiy4iETAr4KEwenhFZ-7-Hh-Zsy-iaT6oxgf_TGbZ7nnNkxMXf2NGuxtpwLAFEMXNNT_NADAiOLvf7RTPuuQyLC3LwklQqGzj-8pLcKhmQtRc6llw6DckU_IFew2_GOPkwd8cijjlCYkHowVG9QSUB1pZNim2kVIRA1mWnMrUK4H0cfmYF2TfkKPmoNrAXtmJrOv5KVQ4CRbTNTtdHaCi_0T2fc0hPRzQOl-hpRRGGO-qiBZReTNyNaPnnLbg5_1mcmGPjeCkb-frkcLuIAjLEEONRBGrqSJlIMKD-yhhu3eA-XB9RUyRnedeMORlB0cEZyz2VA1IDnKpnQQFjbuavqt77erL--r0dowqTk05pWpJkpM1GBEi7ZCCoOrmrxhrZFDm9ZO1tFwvSccfh9JwYpBke_F75iAjwo9MYn3wNxZLKDtx1GztdUoavFim98zMw5K_muT0lqzwgKl2b-hqZ1JGjGi4oRJzu54gpBubYk-F-TIgYOKeeP7kgcpanF2U0OtAdQZZci7Z203Q0ip6a2tjofwOyav_TYmIcPCUt3LXmpb5zuB7pfjc7dhHJvXi-ePV5Mpc0DJhOugrHrSu7QEZRRNYk3RLvkjLyZt95a1XRWscViA1qTUTilikuJcZAH-ZQ6PbVV-WaBfO5LICp4Al_gDDaLA7E7VmpfSvc7De7-MDmBuxSdW75OxKxa3Ba6rWWprlGLPi3pwl3vh1puKyQ=w1000-no-tmp.jpg'
CAFE_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV84sO-oEIDHcmMtoa3fFIQ_GkdaInosB0g2SfupepuntUabbOUivFPrD-nmJ0ygBlGKV9cYs_Z4dxXHZl9NjBjo9sT0D8Sy-kIHWHndwwpFXXpKh503KhG6xvWsezTe-V4Uvx9BTmQo0voycGZrTH3IoBiJqQKGCQiXHaXn8_zDl0pNLCOYLedCO-x5LhDDrJe9Ysy7-azXp5rNI5c5OK_Ss6cPVzmdO2XB0OTC7dH7iCCyEDP_TK_L4MewFDUkowTG1qbxV-kNTRQLMLFW9aFuajTl7F9ULp0OTTvc8w4BwlFsnUtFKY7QQRJ55oblWPpeoUGTd6vW6_-PFnGwydxFkw06s83fsnpevUiOHXZd7YRXW-pAGO2c29_aUI8Nq6IldvWYYEa9iDyP7QFNKgfakl5EoB3_1MXOdARfZJxI6h8WaMxY8iXjah9wnMorD2ZWg_hohJFUJPC2t6HxZ2UQ7dGLJ0yTteGe-0n6IraPHha5txwZVhyndrZCUTjKNDDqFxMykMWSKtkY7j84fWwG8I_vKIR1YHv4wFfjA_UaRBISKBONklq6YTIKeRoEYuk1TDIS7iQUeoWiiZuFrB5_baNqZJKkPkMNF5_CupPwQKLbsoVCh5SO8GLyiBEVvDRxmioaafBz5bluUOR692fedaGsbLzTiqZzIdkaFF1poyydfZO5ZnWUbZaQ3ibQxdzPzZG_m92YB0_DSLMI1jflqIyjknfQOnOOWJvh_GUHYsXxA_tRaYjXpCEAFle6_CXk9EjrJ5gIfUqzuBSenQ5DYqiMncv9YTHWVDoO6U6gYTFoInp7SCVEq5conIqUHlac25j5WxN8F3gmg1N_lyh8npLP4Uu3DFsh8OGt1O1uy5ENO4J8L20G3i9bc2wEn5g=w1000-no-tmp.jpg'
TRASUA_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV84z77rSJFHqhvoYTfeH4ZogYmhRHTceq9QuPn9MlhFuIJbY2WRAr6fOHOHvp_i4zKQc8_Jw-aQM6B4635pv3Y-Y2xogu33eB0iGpDcPiwRR3-ELwuXt09GucO-cNHWRikf6VMT-oz9FxeEB600PDh28q15GNNurHuG-Lh4hHJtZnu6VMqasgHv6ZBmOaFvcy3JPsHq80W-ewI4T7OQ-pbp3qfeOtL4Mz48lpZFIxV67ewAn6MSqoaTEhBxJTihBNum0aeBZW92BZbzANon2QM5NwQ0tC3rXYluuBu6BQyp3psjIkXQnrKJhx0zUKL8AoBfRWcKKA-DF69iRdNtvi9pb1HdDvzNpI1B1kHGG1SLq_HJQQvl4gSw_4hlw3hDQL6YGU6_tVgRKGLvFltrXUsKooUQpqBFXduc67lwtPNtH1Z4YEgBqzH9jOn_Us1TYCoel02TI3JT2bxPQhOzr_mBWISikm6hPkqJlvJIi27BC6f_EdZdYhaQwlz_20BfpFgmFENvCxtzJHlDV3b5fkoJ0fuQRzKoX2YdoLCuYZ-rJkp1fvyDojLBP6nnbmBlhNeljbOqCsi6yiMJOs1bfeC1M3ZSVCvpGsPkphNy2GI5q5lWr9Hmvc_GLWMahTFeHnNeaQ3jLIje8qIkJXGVZM2kZH0twAv2cZm42zrhAzppVK2-LkxEfKPBgmWphsKDCxgpR1eJvaXctQUlapEnHSoInXDaVgCr6xqADpXTOsS1edzfdzafNbaa_5ixy5KC8x5gFONSh3gb8tTbi_NUHQqLghTgSaG5ZbAs8P17wogXCxvnqRTm4LgugA7t2IxfnIeBLUjZWNSAsj8JdC_EJfWQ-riFJqcKipd1R62MT1MsH9eI77am-lu2nu-uEHoqqKg=w1000-no-tmp.jpg'
YOGURT_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV85VErxPLNGXz8UaeEgC8qkfKWbqYiLSwwOKr0CgtUy92o4tnblatxNJkOOWKsp8uewi96xKmuLRpQ633t6OYLxV1DQc5BcWbTIj7lEUwNsgDkkUZlRp5nTTgRaTz5jjj3J8Sngc3NPgQgeyH9_tL1zIpEbNzmKW4k9b-1Ffw2_8fiOI9Ukl7p__O0q1wBoTfBcepMZlK6jLRMAXdQWvvsTE4uV6pm08Wk3IYoH3CesEH9gPS6ob8okRLNLP_9hrJ3vyICgwuR2Tt0C7RksR8N09iyeCiSPcjf8tMNk5SJRF65EpAHD3Ca5YNFU8TtUmlYILtbSlNPb4GcWuzf6lhP64z0zxT1PNMHjUGa84ORM3KlQ6WUySwb2BHmwzCR7E0UDoqBVpKBW29aTYbToYYwXqtV4TJRyCiI-xyh9pP3LFpq1Bb-HH99iGA0w49idmMcvbmhfHZ1HCQfe1wdQw7AwU4xB1ZpBvOCz10F_1Yb8k8XOWFj1oyy3XZ0u-TPI9h_mUbNAGDGBiW3dcpHrtdL0ZCW9Cp5N2_n8QbvHMADobhgHL_kGxX6gzdlONF7mQVej9FO_X9QW0ZnOnV3pLrC-NYrityCJJHeIeY_mMAihZv1f1mrwaCu0GR81t7SDJq0TCDSvxdXz-Z1uhH0Tram5IyJJYggkBT27f564OaBle4z7Z4cZqKnXlRXG_K8FG9sZaZfFZr3sE3IizLS64c-UVE1IiZDxKx-ZdnSfhdipVQ_ZV001sYE74vKcaMDiXUZh9uxHE1XMnnrcwJPD1kWdo3z6l9D3cKShSZqJN0rVLNdtvhITieCCCm6wNBj_z6hwMy-tmkiQVTfIg5zqimdROv6ewBv-UXzzZd7CNMKF02bVaWgjXFXSwW3HUNWuluA=w1000-no-tmp.jpg'
TRA_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV8737f7pkzmBpiH0VmCCNVDqBhaErgnFETS6h4CfkNPtkjZd07rRmXbz1KEe9ARjcTN1EdJnDgnvi2TGDg3vuGfoehenHyOLeYiJW9wstboIxVyhZSE1PcKZdcdvQnnq_tsEptcsrv2oM2HLUPUXnB1Lu2LytyZfNqBnQKFDbqeC-kWzrHy24cccMKTWUOlPnocQPN5-IphfIj7yVB4OeNGONxvVfT1HnyGhIBhIHmwLdeqWOC6fvFljG8IsA-qaSjHvRNqJL5zjEImYe9oqWisqYaL4jZ-N1fZUWwUtFhjGfVPISpvybUkgUwZpoPjBaV-UuP-x3vwe5_xS9rLHR5fMJvlonAVypZLOk6MkpbCubYy7H7A_o-eZ2ZjuVF0QNtqu9dMQ-M2s2FXXWPCQPGKozF647CZqiVC92GRELYEZbOw4sYLQorogiLG9XZpOzdc5e_ZGNHxq1Lq0nTeiX5FNI-Uou9iwp3f6M4xRUYHLZXENmCzGKA34mK51Qd5MtC0OdzY-BZ2mRD_JZRO33XhYKDAqAgU7xPr1IOCDZy-YVbzd3fu0TIK1PkYUHR29iDQur8EXgZJJLxZZHZdnMrL5qgrlmYRDyfk8WRciejjtyEGqMsbKuE1sU3OaBav7VqZYXD5wocdeS6xqd4Rqv9plN73S5pA_jYQ2kNNVMLvQi0WrMSyVPZYBPh7VeuvGcsQ7d38fhM80PM9XugMnAAK0yui5jwuevogYLq2rrRia1u0fS6A2Lg7K4J1XRljxe-4OYL03ZpvkxdJ7ctX4y-f59BBXzhtaUIIcQpWWFeWByPKZHkmgj8URIl1Ze8lNjhRH_Yzovmy3TN_H2Ehvf8oImU_xAu478HF_hqeOm_SF0qnOGqTqJIu97RIiylujwg=w1000-no-tmp.jpg'
SODA_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV840OPjmnlWdawsfRKoGj6ELcKOItBdsBL9hKNTluN5zL4lC3Q8uZ9pnz2FdZ_FGLWDWb3ZiSFziXxNvjBFaV1d4GFPBzj8mP_IplwgcYIwiNHwG5T0yMMr3vbs5_QzcyNKCZagH5N8r3XNjtrqe0b1eOTaP5MU_HYORJ6QYZLQsaTw9uTg1MBuVv60NGBvaP8HOf6WcmyT7Tu0Ch9c4Fc04MULdvyHFW7ohuuEudsDyLWZCPL9g01TonXXm05KUGa5C-hQ2RzUDoahGW0UL7ipzUFY7dSj-pHWRQlrwPjxlXtf6UKjIkBoAyu2DtudT5l62OYTmJw3HPwiDX3ixxB4KBR4lW9PAZOcCh6w5pfC_DZW8MOD4P64ftAKRWyx-skqoMtdMZ0OTnrqqt9qC0BVOX7C6rkopDWbm4cC2u8-v23lQYQFnqiX0I2FwNFUAT6eUSTr1WQVP3IZ6Y64NFMiKHb1botLySJmJboZ6tzpZniqb6jQVpMflE1Ko85kPKV0q9eOLYU0My593XYZqnegFZcEmbj9w24Zpy8ZvSuNF8nSSt0BM0azWPJVbqc9oMYWYypvDoqhrBjYH6wZrDD9_VBZjBZ7E5z2QESkUUG5yW92IHoBkGTIq26dC0AEGZB2KxmsqF0jYtxqt4VDLxh-VWvBM8jTRnjgDgnJJ1kbpu8Ipu5bJNr6ER12MUAnfHRkOY5BBIVV837nnfL-It7_7UG8tlSQGpssOgTVCX1itPg-xICNE4EibpCKTKrQNpiLu_PrU1AWNqvP3yz1XAEIlMwF_VJF8Yz0dX8jl0wzjeE1Pshgs5yn7SrExjfmmw7ANWwYLbZ1H09A2LsOWB54KtDcJXCkD8oDIL5siLLToaKlLduikR-fCBawQ8omJTQ=w1000-no-tmp.jpg'
NUOCEP_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV85jfJIV_3MIVEAVQBJPG2H5Cn7XwtiYnwWwdqd7cG6_iRcf09MyA3wqRWXeq0Lmw810mxpkva8_ZObqE9Xmrq5RdeX5TjwCNffK4nCn6r1RWlTd85ito-cW0zgoWzv4nONq3rbCBb0vlKPyou2ZpPlnQKMANeOD5Q0ZJ3YlP4jHNQM8utOK4GyYz9sNX0BqM5RcljFOfl7RYMiFURuEx6ZkfG-d0AAMJ1k9sP0p9AWDugSEIMc6OvAgqkNDAknQ2sZQfFhc-tfpwAXnEZz5igj1H8f57q6ZMu5QKQN7dUP-5EztTdqU7CLt60f7oyendstiMBX1vdJ8EYaSHmKVvozg5emCwryY0FyBCHp9dH9DZtB7WA9hynaNrQIsKk5TOPpDvRFU5JqprjmAXZ-c-lnIWSXiYlvrZM_0STITkGh59dUdWz1_gB3m0uKVg0VwtFX-H2H4bHGwDpAeOZbmJTQgjO1fJP6u9eTP51djDzD-PaBM_HxiuKCkCmIPISpxGykq2FtETeEfnkew_1d2tENWEf4FlYEVPLVw1lTfa8uHAdbsHBnsB3mKSDCDUBDn02l87uRMdpO-8xfBfE_jEjLfA9sYgOnSHNrGysOhpcnu210R4J4fzfdrCWJ1b4iWNc57OeYi9G0UcH3G4BoB4oyVN9XH7uzN8nmpk0sqy37KjxKeFL3KHXDE6_wixkcs2WlFRCpLL_tAmsAFnepFR4hvs5veCWuBnEAJLOBX_kw8pymWIDK6EBZEEyM2j1rF05ogz1skRK67LP7-G0i1cEDY9ZkpFEJlNt4K8AquPAdbi_4iZ05ITj38NPnIEbOJanH5aj1ios0FWVWBok8Z4ioCqBDSuuNh10fcxps0UO44kXPMUTHs8VSOg5sUuFsq1A=w1000-no-tmp.jpg'
TOPPING_CAFE167 = 'https://lh3.googleusercontent.com/pw/ABLVV84uux-IW2bIbmL3Ik6-ORfPtw65Dbjz77RS2FpmGy20eGLoKLCUnsBz7-R0xu78NRTx8y0gZMygZR3HAididV-opOdjj1yas-cLgKTQZj0z_Vu8y-qOzTaca3M8yalwllJKwkQmYXNDsPkxe8y-ykfSbjo_ItYhrCbIoFSRGgCZl-zhG4VC1yboLbsNRYnlwNUV31IodnOmIDhLzmw7ctEYmCuWOOUH-Cy1ReaQqD1jBaj71whj2za8OrflnL5ctd4kU08vSJys29MgFHy_7n-ndpagiFf7y4n2zaZl9OjpySGltP4D8JA1Wf2Az8_MhJzOxKnIVI5KG-SH4d5Ekh2twIYRswb5iT-ru9fFNG7ovyWgyz2n7s06wjwoVCAd10NG60Y-oCYDpeyQeasgoCMKiYiG3G_fs4QlvhMdfx8E87RUgyZPuRnYwg_kb1xx5zvvs6Tt8o9nCizUmd9YNJgWg2oeJDzAn71Mc3hT5MBMw4zFafAFEH-i6y_rttch-kKnLXkFc25VWoR1AihGVy9R97OKb4KH4OHDILiKVa15usmR9T--kqMLC3jnP-iOsiE9WDI5gNU7-YOFu1sOu4qc158w-Df5beli4c0eahuOpWCjctzaACltbWOjmJMTfxMg4kq7ypL-UMIUQmxNZdrBFSYtv4AlPCrM7pQrnBRk99sv4fN1haPaLB4ej7yXjkz7--f4-1l-jCHv0zAdHn23DUE-HV68jbh--VR_A2HEKzmp0p9dnkijvOvXCwIbH19liw9xow7JchXYPLTqU4KkueBC-S9tIBFPm3zpHYH1rBHJF65EnVksiPr6zgqR-j_5qsiZ4A7ZJlBUwxm1wnOOq7RmmxGliTcu72idQVEY-U9TEDtzkC_Tuan6u5NawA=w1000-no-tmp.jpg'
SHOPEEFOOD = "https://shopeefood.vn/ho-chi-minh/167-cafe-hoang-sa"
GRABFOOD = 'https://food.grab.com/vn/vi/restaurant/cafe-tea-167-delivery/5-C6AVGNUDV8A1L6?'
GOFOOD = "https://gofood.link/a/KjNGP5d"
MENU_ONLINE_LINK = [
				{
					"title": "Cafe167 - Mua hàng online",
					"image_url": LOGO_CAFE167,
					"subtitle": "Hân hạnh được phục vụ quý khách",
					"buttons": [
					{
						"type": "web_url",
						"url": SHOPEEFOOD,
						"title": "Shopee Food"
					},{
						"type": "web_url",
						"url": GRABFOOD,
						"title": "Grab Food"
					},{
						"type": "web_url",
						"url": GOFOOD,
						"title": "Go Food"
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
			response_sent_image = MENU_CAFE167
			image_send(recipient_id, response_sent_image)
			element_send(recipient_id, MENU_ONLINE_LINK)
		elif intents == 'ket_thuc':
			response_sent_text = F"Xin cảm ơn {user_first_name} đã ủng hộ Cafe167. Hẹn gặp lại quý khách."
			message_send(recipient_id, response_sent_text)
		elif intents == 'muon_mua':
			response_sent_text = F"Xin cảm ơn {user_first_name} đã ủng hộ. Vui lòng để lại số điện thoại để quán liên hệ giao hàng, hoặc đặt hàng tại Cafe167 Online"
			message_send(recipient_id, response_sent_text)
			element_send(recipient_id, MENU_ONLINE_LINK)
		elif intents == 'loai_hang_hoa':
			if response['entities']:
				entities = response['entities']
				bPrint = False
				for item  in entities:
					if entities[item][0]['role'] == 'hang_dac_biet':
						response_sent_text = "Đây là các món signature của quán: Trà chanh giã tay, Marble bơ cà phê, Trà sữa ngọc trai lá nếp."		
						message_send(recipient_id, response_sent_text)
						element_send(recipient_id, MENU_ONLINE_LINK)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'cafe':
						response_sent_text = "Đây là menu cafe của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = CAFE_CAFE167		
						image_send(recipient_id, response_sent_image)
						element_send(recipient_id, MENU_ONLINE_LINK)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'tra':
						response_sent_text = "Đây là menu trà của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = TRA_CAFE167		
						image_send(recipient_id, response_sent_image)
						element_send(recipient_id, MENU_ONLINE_LINK)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'tra_sua':
						response_sent_text = "Đây là menu trà sữa của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = TRASUA_CAFE167
						image_send(recipient_id, response_sent_image)
						element_send(recipient_id, MENU_ONLINE_LINK)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'soda':
						response_sent_text = "Đây là menu soda của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = SODA_CAFE167	
						image_send(recipient_id, response_sent_image)
						element_send(recipient_id, MENU_ONLINE_LINK)	
						bPrint = True	
						break	
					elif entities[item][0]['role'] == 'yogurt':
						response_sent_text = "Đây là menu yogurt của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = YOGURT_CAFE167	
						image_send(recipient_id, response_sent_image)
						element_send(recipient_id, MENU_ONLINE_LINK)	
						bPrint = True	
						break
					elif entities[item][0]['role'] == 'nuoc_ep':
						response_sent_text = "Đây là menu nước ép của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = NUOCEP_CAFE167	
						image_send(recipient_id, response_sent_image)
						element_send(recipient_id, MENU_ONLINE_LINK)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'topping':
						response_sent_text = "Đây là menu topping của quán."
						message_send(recipient_id, response_sent_text)
						response_sent_image = TOPPING_CAFE167		
						image_send(recipient_id, response_sent_image)
						element_send(recipient_id, MENU_ONLINE_LINK)	
						bPrint = True
						break
				if bPrint == False:
						response_sent_text = "Vui lòng để lại tên, số điện thoại, Cafe167 sẽ liên hệ hỗ trợ bạn ngay."
						message_send(recipient_id, response_sent_text)
						element_send(recipient_id, MENU_ONLINE_LINK)
			else:
				response_sent_text = "Vui lòng để lại tên, số điện thoại, Cafe167 sẽ liên hệ hỗ trợ bạn ngay."
				message_send(recipient_id, response_sent_text)
				element_send(recipient_id, MENU_ONLINE_LINK)
		elif intents == 'thong_tin':
			if response['entities']:
				entities = response['entities']
				bPrint = False
				for item  in entities:
					if entities[item][0]['role'] == 'hang_dac_biet':
						response_sent_text = f"Xin gửi đến {user_first_name} chương trình khuyến mãi đặc biệt tại Cafe167 Online"
						message_send(recipient_id, response_sent_text)
						element_send(recipient_id, MENU_ONLINE_LINK)
						bPrint = True
						break
					elif entities[item][0]['role'] == 'muon_mua':
						element_send(recipient_id, MENU_ONLINE_LINK)
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
		response_sent_text = f"Xin cảm ơn {user_first_name} đã quan tâm đến Cafe167, chúc quý khách một ngày tốt lành."
		message_send(recipient_id, response_sent_text)


# if __name__ == '__main__':
# 	app.run()