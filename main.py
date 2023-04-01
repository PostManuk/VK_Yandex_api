import requests
from pprint import pprint
import json
from tqdm import tqdm,trange
from time import sleep



class VK:

    def __init__(self,acess_token,user_id):
        self.acess_token = acess_token
        self.owner_id= user_id

    def get_photo(self):
        url_vk = requests.get('https://api.vk.com/method/photos.get', params={'owner_id':self.owner_id,
                                                                             'access_token': self.acess_token,
                                                                             'v':'5.131',
                                                                             'album_id': 'profile',
                                                                             'photo_sizes': True,
                                                                             'extended': True,
                                                                             'rev': 1,
                                                                             'count': 10
                                                                             }).json()

        with open('photos_vk.json', 'w') as file :
            json.dump( url_vk, file , indent=2, ensure_ascii=False)


    def write_photo(self,f_name):
        self.f_name = f_name
        images=[]
        photos = json.load(open('photos_vk.json'))['response']['items']
        for photo in photos:
            likes = photo['likes']['count']
            sizes = photo['sizes']
            for size in sizes:
                type = size['type']
                url_photo = size['url']
                if size['type'] == 'z':
                    dict = ([{'file_name': f'{likes}.jpg',
                              'url': url_photo,
                              'size': type
                              }])
                    images.extend(dict)
                    self.images_dict={'photos': images}
                    with open(self.f_name, 'w') as file:
                        json.dump(self.images_dict, file, indent=2, ensure_ascii=False)

    def instance_vk_json(self):
        return self.images_dict


class Yandex:

    host = 'https://cloud-api.yandex.net/'

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        return {'Content_Type': 'application/json', 'Authorization': f'OAuth {self.token}'}

    def create_folder(self, folder_name):
        uri = 'v1/disk/resources/'
        url = self.host + uri
        params = {'path': f'/{folder_name}', 'overwrite': 'true'}
        requests.put(url, headers=self.get_headers(), params=params)


    def upload_files_VK(self, file_url, file_name, folder_name):
        uri = 'v1/disk/resources/upload'
        url = self.host+uri
        params = {'path': f'/{folder_name}/{file_name}',
                  'url': file_url, 'overwrite': 'true'}
        response = requests.post(url, headers=self.get_headers(), params=params)
        if response.status_code == 202:
            for i in trange(len(file_name),desc= f'Loading photo - {file_name}',unit = f' Photo-{file_name} has been uploaded to the {folder_name}'):
                sleep(.1)
        else:
            print('Status code is not accepted')


def upload (instance_vk):
    for i in instance_vk['photos']:
        url_vk = i['url']
        name_vk_photo=i['file_name']
        upload1.upload_files_VK(url_vk,name_vk_photo,'new_folder')
    print()
    pprint('---Loading completed!---')



if __name__ == '__main__':

    with open('VK_token_id.txt.', encoding='utf-8') as file:
        acess_token_vk = file.readline().strip()
        user_id = file.readline().strip()
        yandex_token= file.readline().strip()


    profile_photos1 = VK(acess_token_vk, user_id)
    profile_photos1.get_photo()
    profile_photos1.write_photo('photos_vk_dump.json')

    upload1 = Yandex(yandex_token)
    upload1.get_headers()
    folder_name = 'new_folder'
    upload1.create_folder('new_folder')

    upload(profile_photos1.instance_vk_json())
