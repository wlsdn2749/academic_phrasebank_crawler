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
                # td_fst = td[0].find_all(text=True)
                # td_sec = td[1].find_all(text=True)
            except:
                pass

            try:
                print(title + "\n", p_lst , td_lst)
            except NameError:
                print(title + "\n", p_lst)

            data = {'title': title

            }
            for p_tag_idx, p_tag in enumerate(p_lst):
                for idx, p_t in enumerate(p_tag):
                    data[f'p{p_tag_idx}-{idx}'] = p_t

            for td_tag_idx, td_tag in enumerate(td_lst):
                for idx, td_t in enumerate(td_tag):
                    data[f'td{td_tag_idx}-{idx}'] = td_t    
            res.append(data)

    with open (f'{url_name}.json', 'w', encoding='utf-8') as f:
        json.dump(res, f, indent=8, ensure_ascii=False)
    print(f"Created Json File {url}")
# subtitles = soup.find_all('div', attrs={'class': 'et_pb_row_inner et_pb_row_inner_1'})

# for subtitle in subtitles:
#     titles = subtitle.find_all('h5', attrs={'class': 'et_pb_toggle_title'})
#     datas = subtitle.find_all('p')
#     data_set = []
#     p = re.compile('\W')

#     for idx, data in enumerate(datas):
#         real_data = data.find_all(text=True)
#         if p.match(real_data[0]) == None:
#             data_set.append(real_data)
    
#     for title, data in zip(titles, data_set):
#         print("title is = " , title.text)
#         print("data is = ", data)

        

    
    # print(title + "\n", data)

    #et_pb_toggle et_pb_module et_pb_accordion_item et_pb_accordion_item_1 et_pb_toggle_open
    #et_pb_toggle et_pb_module et_pb_accordion_item et_pb_accordion_item_0 et_pb_toggle_open

    
if __name__ == "__main__":
    phraseBank_list = ["introducing-work", "referring-to-sources", "describing-methods",
                       "reporting-results", "discussing-findings", "writing-conclusions"]

    for page in phraseBank_list:
        phraseBank_parser(page)
    
