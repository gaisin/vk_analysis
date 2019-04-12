from vk_api import VkApi, VkTools

import settings


def get_all_comments(input_url, tools):
    '''function returns all posts comments in list'''
    all_comments =[]
    
    owner_id, post_id = input_url[19:].split('_')
    comments = tools.get_all('wall.getComments',  100, {'owner_id' : owner_id, 'post_id' : post_id, 'need_likes' : 1})
    
    for comment in comments['items']:
        text = comment['text']
        likes_count = comment['likes']['count']
        comment_id = comment['id']
        all_comments.append( (input_url, comment_id, text, likes_count) )
    
    return all_comments


def main():
    vk_session = VkApi(settings.LOGIN, settings.PASSWORD, scope='wall')
    vk_session.auth(token_only=True)
    tools = VkTools(vk_session)
    input_url = input('Введите ссылку на пост: ')

    all_comments = get_all_comments(input_url, tools)
    print('\n'.join(all_comments))

if __name__ == "__main__":
    main()