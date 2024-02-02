from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Mark
from datacenter.models import Lesson
from datacenter.models import Commendation
import random


PRAISES = ['Молодец!', 'Отлично!', 'Великолепно!', 'Прекрасно!', 'Талантливо!']


def get_user_data(schoolkid):
    try:
        user_data = Schoolkid.objects.get(full_name__contains=schoolkid)
        return user_data
    except Schoolkid.DoesNotExist:
        print('Опечатка. Или ученика с таким именем нет в базе. Программа завершена.')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем, уточните запрос. Программа завершена.')


def fix_marks(schoolkid):
    Mark.objects.filter(schoolkid=schoolkid, points__in=[2, 3]).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    praise = random.choice(PRAISES)
    try:
        lesson = Lesson.objects.filter(year_of_study=schoolkid.year_of_study,
                                       group_letter=schoolkid.group_letter, subject__title__contains=subject).first()
        Commendation.objects.create(schoolkid=schoolkid, text=praise, created=lesson.date,
                                    teacher=lesson.teacher, subject=lesson.subject)
    except AttributeError:
        print('Опечатка. Или предмета с таким названием нет в базе. Программа завершена.')


def run(*args):
    if len(args) == 0:
        print('Вы ввели пустую строку')
    else:
        child = get_user_data(args[0])
        if len(args) == 1:
            fix_marks(child)
            remove_chastisements(child)
        else:
            subject = args[1]
            create_commendation(child, subject)


if __name__ == '__main__':
    run()