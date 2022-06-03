import re
import time
import requests
import xlsxwriter
from bs4 import BeautifulSoup


def get_data(url):
    result = {}
    page = 0
    while True:
        current_page = requests.get(url + f'?page={page}')
        soup = BeautifulSoup(current_page.text, 'lxml')
        if not soup.find_all('div', class_='container-item'):
            break
        else:
            all_a_links = soup.find_all('a', class_='link')
            titles = {i.text: i.get('href') for i in all_a_links}
            for title in titles:
                result[title] = []
                response = requests.get(url + titles[title])
                soup2 = BeautifulSoup(response.text, 'lxml')
                date = soup2.find_all('a', class_='text-reply-items', string=re.compile('Дата'))
                text_reply = soup2.find_all('a', class_='text-reply')
                for i, k in zip(date, text_reply):
                    result[title].append([i.text, k.text.replace('\r', '').replace('\n', '').strip()])
            page += 1

    workbook = xlsxwriter.Workbook('file.xlsx')
    for title in result:
        worksheet = workbook.add_worksheet(name=title[:30])
        for pos, (date, comment) in enumerate(result[title], start=1):
            worksheet.write(f'A{pos}', date)
            worksheet.write(f'B{pos}', comment)
    workbook.close()


if __name__ == '__main__':
    print('Получаю данные...')
    get_data(url='https://lainelir2.pythonanywhere.com/')
    print('Данные успешно получены и сохранены.')
    time.sleep(3)
