import os
import itertools
import json
import requests
import shutil

headers = {
            'Content-Type' : 'application/json',
            'Authorization' : 'Bearer <API KEY>'
        }

template = "<TEMPLATE>"

modification_list = []

def read_as_list(file):
    my_file = open(file, "r")
    content_list = my_file.readlines()
    final_list.append(content_list)

    modification_name = os.path.splitext(file)[0]
    modification_list.append(modification_name)

def create_modifications(creative_dict):
    modifications = []
    main_dict = {}
    for x,y in creative_dict.items():
        if 'img' in x:
            empty_dict = {}
            empty_dict['name'] = x
            empty_dict['image_url'] = y
            main_dict.update(empty_dict)
        elif 'text' in x:
            empty_dict = {}
            empty_dict['name'] = x
            empty_dict['text'] = y
            main_dict.update(empty_dict)
        elif 'color' in x:
            empty_dict = {}
            empty_dict['name'] = x
            empty_dict['color'] = y
            main_dict.update(empty_dict)
        else:
            pass
    modifications.append(main_dict)

    for mod in modifications:
        create_image(mod)


def create_image(modifications):
    img_data_dict = {
    "template": template,
    "modifications": modifications
   }

    print(img_data_dict)
    print("--------------")
    url = "https://api.bannerbear.com/v2/images"
    r = requests.post(url, data=json.dumps(img_data_dict), headers=headers)
    list_all_images()

def list_all_images():
    headers = {
                'Authorization' : 'Bearer <API KEY>'
            }

    url = "https://api.bannerbear.com/v2/images"    
    r = requests.get(url, headers=headers).json()

    for x in r:
        print(x['template'])
        if x['template'] == template:
            retrieve_image(str(x['uid']))
        else:
            continue

def retrieve_image(uid):
    headers = {
                'Authorization' : 'Bearer <API KEY>'
              }
    url = f"https://api.bannerbear.com/v2/images/{uid}"
    r = requests.get(url, headers = headers).json()
    img_data = requests.get(r["image_url_png"]).content
    with open(f'{uid}.png', 'wb') as handler:
        handler.write(img_data)

final_list = []

for filename in os.listdir(os.getcwd()):
    if filename.endswith(".txt"): 
        read_as_list(filename)
        continue
    else:
        continue

all_combinations = list(itertools.product(*final_list))

comb_list = []

for combination in all_combinations:
    comb_dict = {}
    num = 0
    for mod in range(len(modification_list)):
            comb_dict[modification_list[num]] = combination[num]
            num += 1
    comb_list.append(comb_dict)

for creative in comb_list:
    create_modifications(creative)
