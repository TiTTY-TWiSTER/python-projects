import requests
from bs4 import BeautifulSoup
import csv 
def get_html(url):
	r = requests.get(url) 
	return r.text

def get_total_pages(html): # функция возвращает колличество всех страниц с запросом
	soup = BeautifulSoup(html,'lxml')
	# находим из переданного html то что нас интересует - ссылку на все страницы, которая укказанна в последней ссылке цифрой в href
	pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href') # последняя ссылка
	total_pages = pages.split('=') # разбиваем полученную строку в список
	total_pages[1].split('&')[0] # нас интересует второй элемент списка который еще нужно разбить что бы забрать только число в строке
	total_pages = pages.split('=')[1].split('&')[0] # запомнили

	return int(total_pages)

def write_csv (data):
	with open('avito.csv', 'a') as f:
		writer = csv.writer(f)
		writer.writerow(
			(data['title'],
				data['price'],
				data['metro'],
					data['url'])
			)


def get_page_data(html): # парсим конкретно что нам надо из блока
	soup = BeautifulSoup(html,'lxml')

	ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table') # находим блок с описанием
	for ad in ads: # перебираем блок и достаем из него что нужно нам
		name = ad.find('div', class_='description').find('h3').text.strip().lower() #приводим к нижнему регистру
		if 'apple' in name: # если в названии есть apple(тем самым отсекаем рекламу, например РСЯ)

			try:   #title about data - название цена метро
				title = ad.find('div', class_='description').find('h3').text.strip() # обрезаем пустоту
			except:
				title = ""
			try:
				url = 'https://www.avito.ru' + ad.find('div', class_='description').find('h3').find('a').get('href')
			except:
				url = ""
			try:
				price = ad.find('span', class_='price').text.strip().split(' ₽')[0]
			except:
				price = ""
			try:
				metro = ad.find('div', class_='data').find_all('p')[-1].text.strip()
			except:
				metro = ''

			data = { # записываем полученные данные в словарь
				'title': title,
				'price': price,
				'metro': metro,
				'url': url
				}
			write_csv(data) # записываем в файл
		else:
			continue

def main():
	url =  "https://www.avito.ru/sankt-peterburg/noutbuki?p=1&q=apple+macbook"
	base_url = 'https://www.avito.ru/sankt-peterburg/noutbuki?'
	page_part = 'p=' #сюда подставляем цифры номера страниц
	query_part = '&q=apple+macbook'

	total_pages = get_total_pages(get_html(url))

	for i in range(1, 3):  # страницы с первой по 3ю
		url_gen  = base_url + str(i) + query_part # i в данном случае число.Цикл проходит от 1 до конца числа полученного в функции def get_total_pages
		#print(url_gen)
		html = get_html(url_gen)
		get_page_data(html)


if __name__ == '__main__' :
	main()