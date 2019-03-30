import vk_api
import passwords

# Фунция на получение id группы/паблика
def get_id(vk_session):
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

# Функция на получения списка постов по id группы/паблика
def main():
	login, password = passwords.login, passwords.password
	vk_session = vk_api.VkApi(login, password)
	try:
		vk_session.auth(token_only=True)
	except vk_api.AuthError as error_msg:
		print(error_msg)
		return

	tools = vk_api.VkTools(vk_session)
	
	all_posts=[]
	
	posts = tools.get_all('wall.get', 100, {'owner_id': get_id(vk_session), 'filter': 'owner'})
	for elements in posts["items"]:
		all_posts.append(elements.get("text"))
	print('\n\n'.join(all_posts))


if __name__ == "__main__":
	main()

