import vk_api

from get_comments import get_all_comments
import settings


def get_id(vk_session):
    # Фунция на получение id группы/паблика

    group_link = str(input('Введите ссылку на сообщество в формате https://vk.com/...: '))
    vk = vk_session.get_api()

    while True:
        if 'https://vk.com/' in group_link:
            if group_link[:21] == 'https://vk.com/public':
                group_data = -int(group_link[21:])
            elif group_link[:19] == 'https://vk.com/club':
                group_data = -int(group_link[19:])
            else:
                group_data = vk.groups.getById(group_id=group_link[15:])
                for elements in group_data:
                    group_data = -int(elements.get("id"))
            return group_data
        else:
            group_link = str(input('Некорректный ввод. Пожалуйста, введите ссылку на сообщество в следующем формате: https://vk.com/...: '))


def get_posts(tools, vk_session):
    # Функция на получения списка постов по id группы/паблика

    all_posts_url=[]
    group_id = get_id(vk_session)
    posts = tools.get_all('wall.get', 100, {'owner_id': group_id, 'filter': 'owner'})
    for elements in posts["items"]:
        post_id = elements.get("id")
        text = elements.get("text")
        all_posts_url.append( ((f'https://vk.com/wall{group_id}_{post_id}'), text) )
    return all_posts_url


def main():
    login, password = settings.LOGIN, settings.PASSWORD
    vk_session = vk_api.VkApi(login, password)
    try:
        vk_session.auth(token_only=True)
    except vk_api.AuthError as error_msg:
        print(error_msg)
        return
    tools = vk_api.VkTools(vk_session)
    all_posts_url = get_posts(tools, vk_session)
    
    for urls in all_posts_url:
        url = urls[0]
        all_comments = get_all_comments(url, tools)
        print('\n'.join(all_comments))

    

if __name__ == "__main__":
    main()

