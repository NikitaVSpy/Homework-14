from bs4 import BeautifulSoup as BS
import requests
import csv

URL = "https://metarankings.ru/best-pc-games/"
CSV = "game.csv"

def get_html(url, params=""):
	response = requests.get(url, params="")
	return response


def get_content(html):
	soup = BS(html, "html.parser")
	items = soup.find_all("div", class_="post clear")
	game = []

	for item in items:
		game.append(
			{
			"name":item.find("a", class_="name").get_text(),
			"platform":item.find("div", class_="post-meta").get_text(),
			"rating":item.select(".small-score")[1].text.replace(".", ",")
			}
		)
	return game


def save_doc(items, path):
	with open(path, "w", newline="") as file:
		writer = csv.writer(file, delimiter=";")
		writer.writerow(["Название игры", "Платформа", "Рейтинг"])
		for item in items:
			writer.writerow( [item["name"], item["platform"], item["rating"]] )


def parser():
	PAGES = 5
	html = get_html(URL)
	if html.status_code == 200:
		game = []
		for page in range(1, PAGES+1):
			print(f"Парсим страницу № {page}")
			html = get_html(URL+f"page/{page}/")
			game.extend(get_content(html.text))
			save_doc(game, CSV)
	else:
		print("Error")


parser()