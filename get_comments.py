from vk_api import VkApi, VkTools

import settings

vk_session = VkApi(settings.LOGIN, settings.PASSWORD, scope='wall')
vk_session.auth(token_only=True)

def get_all_comments(input_url):  #function returns all posts comments in list
    tools = VkTools(vk_session)
    all_comments =[]
    
    owner_id, post_id = input_url[19:].split('_')
    comments = tools.get_all('wall.getComments',  100, {'owner_id' : owner_id, 'post_id' : post_id})
    
    for comment in comments['items']:
        all_comments.append(comment['text'])
    
    return all_comments

def main():
    input_url = input('Введите ссылку на пост: ')

    all_comments = get_all_comments(input_url)
    print('\n'.join(all_comments))

if __name__ == "__main__":
    main()



