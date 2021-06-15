from collections import Counter

from django.shortcuts import render

# Для отладки механизма ab-тестирования используйте эти счетчики
# в качестве хранилища количества показов и количества переходов.
# но помните, что в реальных проектах так не стоит делать
# так как при перезапуске приложения они обнулятся


counter_show = Counter()
counter_click = Counter()


def index(request):
    # Реализуйте логику подсчета количества переходов с лендига по GET параметру from-landing
    from_landing = request.GET.get('from-landing')
    counter_click[from_landing] += 1
    return render(request, 'index.html')


def landing(request):
    # Реализуйте дополнительное отображение по шаблону app/landing_alternate.html
    # в зависимости от GET параметра ab-test-arg
    # который может принимать значения original и test
    # Так же реализуйте логику подсчета количества показов
    ab_test_arg = request.GET.get('ab-test-arg')
    if ab_test_arg == 'original':
        landing = 'landing.html'
    elif ab_test_arg == 'test':
        landing = 'landing_alternate.html'
    counter_show[ab_test_arg] += 1
    return render(request, landing)


def stats(request):
    # Реализуйте логику подсчета отношения количества переходов к количеству показов страницы
    # Для вывода результат передайте в следующем формате:

    try:
        test_conversion = counter_click['test'] / counter_show['test']
    except ZeroDivisionError:
        click_test = counter_click['test']
        show_test = counter_show['test']
        test_conversion = f'{click_test} / {show_test}'
    try:
        original_conversion = counter_click['original'] / counter_show['original']
    except ZeroDivisionError:
        click_original = counter_click['original']
        show_original = counter_show['original']
        original_conversion = f'{click_original} / {show_original}'

    return render(request, 'stats.html', context={
        'test_conversion': test_conversion,
        'original_conversion': original_conversion,
    })
