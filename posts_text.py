import vk_api

from get_comments import get_all_comments
import settings

from model import Base, Group, Comment_data, Post_data, Session


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
            save_group_id_to_group(group_data)
            return group_data
        else:
            group_link = str(input('Некорректный ввод. Пожалуйста, введите ссылку на сообщество в следующем формате: https://vk.com/...: '))


def get_posts(tools, vk_session):
    # Функция на получение списка постов по id группы/паблика

    all_posts_url=[]
    group_id = get_id(vk_session)
    posts = tools.get_all('wall.get', 100, {'owner_id': group_id, 'filter': 'owner'})
    for elements in posts["items"]:
        post_id = elements.get("id")
        text = elements.get("text")
        all_posts_url.append( (group_id, (f'https://vk.com/wall{group_id}_{post_id}'), text) )
    save_data_to_post_data(all_posts_url)
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
    all_posts = get_posts(tools, vk_session)
    for urls in all_posts:
        url = urls[1]
        all_comments = get_all_comments(url, tools)
        save_data_to_comment_data(all_comments)

def save_group_id_to_group(group_data):
    # Функция сохранения group_id в таблице group
    session = Session()
    c1 = Group(group_id = group_data)
    session.add(c1)
    session.commit()

def save_data_to_post_data(all_posts_url):
    # Функция сохранения данных в таблице post_data
    session = Session()
    for elements in all_posts_url:
        c1 = Post_data(
            group_id = elements[0],
            post_id = elements[1],
            post_text = elements[2]
        )
        session.add(c1)
    session.commit()

def save_data_to_comment_data(all_comments):
    # Функция сохранения данных в таблице comment_data
    session = Session()
    for elements in all_comments:
        c1 = Comment_data(
            post_id = elements[0],
            comment_id = elements[1],
            comment_text = elements[2],
            likes = elements[3]
        )
        session.add(c1)
    session.commit()

if __name__ == "__main__":
    main()

