import datetime


def start(config):
    ans = {}
    about = 'Курс: ' + config['course_name'] + '\n'
    about += config['description'] + '\n'
    about += 'Даты проведения: ' + config['start_date'] + ' - ' + config['finish_date'] + '\n'
    about += 'Литература: ' + '\n'
    for elem in config['resources']:
        about += elem + '\n'
    ans['about'] = about
    curr_date = datetime.date.today()
    start_date = datetime.datetime.strptime(config['start_date'], '%Y-%m-%d').date()
    finish_date = datetime.datetime.strptime(config['finish_date'], '%Y-%m-%d').date()
    info = ''
    if curr_date < start_date:
        info = 'Курс ещё не начался. Запись возможна с ' + config['start_date']
    elif curr_date > finish_date:
        info = 'Курс завершен.'
    elif (curr_date - start_date).days > int(config['days_after']):
        info = 'Запись завершена.'
    else:
        info = 'Вы можете записаться.\nДо конца регистрации осталось: ' + str(
            int(config['days_after']) - (curr_date - start_date).days)
    ans['info'] = info
    return ans

# if __name__=='__main__':
#     config = {
#         "course_name": "Название курса",
#         "start_date": "2018-04-08",
#         "finish_date": "2018-05-25",
#         "days_after": "21",
#         "description": "Описание курса",
#         "resources": [
#             "лит-ра1",
#             "лит-ра2",
#             "ресурс1"
#         ]
#     }
#     print(*start(config).values())
