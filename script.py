from datacenter.models import Schoolkid
from datacenter.models import Chastisement
from datacenter.models import Mark
from datacenter.models import Lesson
from datacenter.models import Commendation
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned
import random


praises = ['Молодец!', 'Отлично!', 'Великолепно!', 'Прекрасно!', 'Талантливо!']


def fix_marks(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    marks = Mark.objects.filter(schoolkid=child, points__in=[2, 3])
    for mark in marks:
        mark.points = '5'
        mark.save()


def remove_chastisements(schoolkid):
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    sements = Chastisement.objects.filter(schoolkid=child)
    for sement in sements:
        sement.delete()


def create_commendation(schoolkid, subject):
    praise = random.choice(praises)
    child = Schoolkid.objects.get(full_name__contains=schoolkid)
    less = Lesson.objects.get(year_of_study=child.year_of_study,
                              group_letter=child.group_letter, subject__title__contains=subject).first()
    Commendation.objects.create(schoolkid=child, text=praise, created=less.date,
                                teacher=less.teacher, subject=less.subject)


def run(*args):
    print(args[0])
    try:
        if len(args) == 1:
            fix_marks(args[0])
            remove_chastisements(args[0])
        else:
            create_commendation(args[0], args[1])
    except ObjectDoesNotExist:
        print('Опечатка. Или ученика с таким именем нет в базе. Программа Завершена.')
    except MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем, уточните запрос. Программа завершена')










