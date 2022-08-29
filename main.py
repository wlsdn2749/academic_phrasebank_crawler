from cmath import e
import enum
from re import sub
import requests
from bs4 import BeautifulSoup
import json
import re

def phraseBank_parser(url_name):
    url = f'https://www.phrasebank.manchester.ac.uk/{url_name}/'

    #requests.get() 함수를 사용하여 해당 url을 사용친화적으로 만듬
    req = requests.get(url)

    #requests.text 함수를 이용하여 현재 접속된 url를 html로 bs에 넘김
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    # site_json = json.loads(soup.text)

    # find all ' h5 class=et_pb_toggle_title ' 
    num = 0
    res = []
    while(True):
        if num > 30:
            break
        try:
            subtitles = soup.find_all('div', attrs={'class': f'et_pb_toggle et_pb_module et_pb_accordion_item et_pb_accordion_item_{num} et_pb_toggle_open'})
            num = num + 1
        except:
            break

        # iterate class
        for subtitle in subtitles:
            # title tag and p tag
            title = subtitle.find('h5', attrs={'class': 'et_pb_toggle_title'}).text
            try:    
                p = subtitle.find_all('p')
                p_lst = []
                for i in p:
                    p_lst.append(i.find_all(text=True))
            except:
                pass
            # td is table tag targeted..
            try:
                td = subtitle.find_all('td', attrs={'style': 'border: 1px solid #cccccc;padding: 12px'})
                td_lst = []
                for i in td:
                    td_lst.append(i.find_all(text=True))
            except:
                pass

            try:
                print(title + "\n", p_lst , td_lst)
            except NameError:
                print(title + "\n", p_lst)

            data = {'title': title

            }
            
            toggle = False
            nbsp = "\xa0"

            real_p_lst = []
            real_real_p_lst = []
            temp_data = ""

            for p_list in p_lst:
                for p_tag in p_list:
                    if p_tag.startswith(nbsp):
                        if p_tag == nbsp:
                            continue
                        real_p_lst[-1] += p_tag.lstrip(nbsp)
                        continue
                    if p_tag.endswith(nbsp):
                        if p_tag == nbsp:
                            continue
                        temp_data += p_tag.rstrip(nbsp)
                        continue
                    temp_data += p_tag
                    real_p_lst.append(temp_data)
                    temp_data = ""
                real_real_p_lst.append(real_p_lst)

            for p_tag_idx, p_tag in enumerate(real_real_p_lst):
                for idx, p_t in enumerate(p_tag):
                    # if p_t.startswith(nbsp) and idx >= 2:
                    #     data[f'p{p_tag_idx}-{idx-2}'] = data[f'p{p_tag_idx}-{idx-1}'] + p_t.lstrip(nbsp)
                    #     continue
                    # if p_t.endswith(nbsp):
                    #     data[f'p{p_tag_idx}-{idx}'] = p_t.rstrip(nbsp)
                    #     toggle = True
                    #     continue
                    # if toggle == True:
                    #     data[f'p{p_tag_idx}-{idx-1}'] = data[f'p{p_tag_idx}-{idx-1}'] + p_t
                    #     toggle = False
                    #     continue
                    if p_t.startswith("\n"):
                        p_t = p_t.lstrip("\n")
                    data[f'p{p_tag_idx}-{idx}'] = p_t

            for td_tag_idx, td_tag in enumerate(td_lst):
                for idx, td_t in enumerate(td_tag):
                    if td_t.startswith("\n"):
                        td_t = td_t.lstrip("\n")
                    data[f'td{td_tag_idx}-{idx}'] = td_t    
            res.append(data)

    with open (f'{url_name}.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=8, ensure_ascii=False)
    print(f"Created Json File {url}")


if __name__ == "__main__":
    phraseBank_list = ["introducing-work", "referring-to-sources", "describing-methods",
                       "reporting-results", "discussing-findings", "writing-conclusions"]

    for page in phraseBank_list:
        phraseBank_parser(page)
    # dummy = '\xa0for all variables.\n'
    # print (dummy.startswith("\xa0"))
    # print (dummy.lstrip("\xa0"))
    # print (dummy.lstrip("\xa0").rstrip("\n"))
