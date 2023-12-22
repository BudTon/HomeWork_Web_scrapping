import json
from pprint import pprint
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

def find_all_url_vacancy(number_of_pages):
    headers_generator = Headers(os='win', browser='chrom')
    url_list = []
    for page in range(number_of_pages):
        url = f'https://spb.hh.ru/search/vacancy?L_save_area=true&text=python&excluded_text=&area=2&area=1&salary=&currency_code=RUR&experience=doesNotMatter&order_by=relevance&search_period=0&items_on_page=20&page={page}'
        response = requests.get(url, headers=headers_generator.generate())
        main_html_data = response.text
        main_soup = BeautifulSoup(main_html_data, 'lxml')
        vacancy_list = main_soup.find('main', class_="vacancy-serp-content")
        vacancy = vacancy_list.find_all('div', class_='vacancy-serp-item__layout')
        for vacancy_tag in vacancy:
            vacancy_url_tag = vacancy_tag.find('a', class_='serp-item__title')
            vacancy_url = vacancy_url_tag['href']
            url_list.append(vacancy_url)
    url_date = list(set(url_list))
    return url_date

def result_vacancy_data(url_date):
    headers_generator = Headers(os='win', browser='chrom')
    vacancy_data = []
    for url in url_date:
        response = requests.get(url, headers=headers_generator.generate())
        main_html_data = response.text
        main_soup = BeautifulSoup(main_html_data, 'lxml')
        vacancy = main_soup.find_all('div', class_='bloko-column bloko-column_container bloko-column_xs-4 bloko-column_s-8 bloko-column_m-12 bloko-column_l-10')
        vacancy_tag = vacancy[0]
        vacancy_description_tag = vacancy_tag.find('div', {'data-qa': 'vacancy-description'})
        vacancy_description = vacancy_description_tag.text.strip()
        if 'Django' and 'Flask' in vacancy_description:
            vacancy_name_tag = vacancy_tag.find('h1', {'data-qa': 'vacancy-title'})
            vacancy_name = vacancy_name_tag.text.strip()
            vacancy_salary_tag = vacancy_tag.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'})
            vacancy_adress_tag =vacancy_tag.find('span', {'data-qa': 'vacancy-view-raw-address'})
            if vacancy_adress_tag == None:
                vacancy_adress = vacancy_adress_tag
            else:
                vacancy_adress = vacancy_adress_tag.text
            vacancy_сompany_name_tag = vacancy_tag.find('span', {'data-qa': 'bloko-header-2'})
            vacancy_сompany_name = vacancy_сompany_name_tag.text.strip()
            if vacancy_salary_tag == None:
                vacancy_salary = vacancy_salary_tag
            else:
                vacancy_salary = vacancy_salary_tag.text
            vacancy_data.append({
                'vacancy_name': vacancy_name,
                'url': url,
                'salary': vacancy_salary,
                'сompany_name': vacancy_сompany_name,
                'vacancy_adress': vacancy_adress
            })
    return vacancy_data

def result_vacancy_data_usd(url_date):
    headers_generator = Headers(os='win', browser='chrom')
    vacancy_data_usd = []
    for url in url_date:
        response = requests.get(url, headers=headers_generator.generate())
        main_html_data = response.text
        main_soup = BeautifulSoup(main_html_data, 'lxml')
        vacancy = main_soup.find_all('div', class_='bloko-column bloko-column_container bloko-column_xs-4 bloko-column_s-8 bloko-column_m-12 bloko-column_l-10')
        vacancy_tag = vacancy[0]
        vacancy_salary_tag = vacancy_tag.find('span', {'data-qa': 'vacancy-salary-compensation-type-net'})
        if vacancy_salary_tag != None:
            vacancy_salary = vacancy_salary_tag.text
            if ('$' in vacancy_salary
                    or '€' in vacancy_salary
                    or 'USD' in vacancy_salary
                    or 'Usd' in vacancy_salary
                    or 'usd' in vacancy_salary):
                vacancy_name_tag = vacancy_tag.find('h1', {'data-qa': 'vacancy-title'})
                vacancy_name = vacancy_name_tag.text.strip()
                vacancy_adress_tag =vacancy_tag.find('span', {'data-qa': 'vacancy-view-raw-address'})
                if vacancy_adress_tag == None:
                    vacancy_adress = vacancy_adress_tag
                else:
                    vacancy_adress = vacancy_adress_tag.text
                vacancy_сompany_name_tag = vacancy_tag.find('span', {'data-qa': 'bloko-header-2'})
                vacancy_сompany_name = vacancy_сompany_name_tag.text.strip()
                vacancy_data_usd.append({
                    'vacancy_name': vacancy_name,
                    'url': url,
                    'salary': vacancy_salary,
                    'сompany_name': vacancy_сompany_name,
                    'vacancy_adress': vacancy_adress
                })
    return vacancy_data_usd
def load_in_json(name_file, date):
    with open(f'{name_file}', 'w', encoding='utf8') as f:
        json.dump(date, f)


if __name__ == '__main__':
    number_of_pages = 2
    url_date = find_all_url_vacancy(number_of_pages)
    result_date = result_vacancy_data(url_date)
    pprint(result_date)
    print(len(result_date))
    vacancy_data_usd = result_vacancy_data_usd(url_date)
    pprint(vacancy_data_usd)
    print(len(vacancy_data_usd))
    load_in_json('vacancy_data.json', result_date)
    load_in_json('vacancy_salary_usd.json',vacancy_data_usd)
#
#
#
#
