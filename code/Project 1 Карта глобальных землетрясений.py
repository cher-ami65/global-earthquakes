import json    # импортируем модуль json

from plotly.graph_objs import Scattergeo, Layout  # импортируем тип диаграмм Scattergeo и класс Layout
from plotly import offline       # импорт модуля offline для вывода карты

# Нанесение данных на карту.
filename = '/content/sample_data/1.0_month.geojson.json'
with open(filename) as f:
    all_data = json.load(f)   # преобразование и сохранение данных в переменной all_data

all_dicts = all_data['features']  # сохранение данных, связанных с ключом 'features' в переменной all_dicts

mags, lons, lats, cover_notes = [], [], [], []  # создание пустых списков для хранения нужных извлекаемых данных
for eq_dict in all_dicts:                       # цикл для перебора словаря all_dicts с записью в словарь eq_dict
    mag = eq_dict['properties']['mag']         # извлечение магнитуды из секции 'properties' с ключом 'mag'
    lon = eq_dict['geometry']['coordinates'][0]  # извлечение долготы из секции 'geometry' с ключом 'coordinates' и с индексом 0
    lat = eq_dict['geometry']['coordinates'][1]  # извлечение широты из секции 'geometry' с ключом 'coordinates' и с индексом 1
    title = eq_dict['properties']['title']   # извлечение текстовых описаний магнитуд
    mags.append(mag)   # присоединение к списку mags значений магнитуд
    lons.append(lon)   # присоединение к списку lons значений долготы
    lats.append(lat)   # присоединение к списку lats значений широты
    cover_notes.append(title)  # присоединение к списку cover_notes текстовых описаний значений магнитуд

# Карта землетрясений.
data = [{                      # формирование списка с набором данных для построения диаграммы в форме пар
    'type': 'scattergeo',      # "ключ-значение" в словаре
    'lon': lons,
    'lat': lats,
    'text': cover_notes,
    'marker': {              # использование ключа 'marker' для определения маркеров на карте
        'size': [3*mag for mag in mags],  # использование масштабного коэффициента для увеличения размера маркера
        'color': mags,                  # использование значения mags для определения местоположения на цветовой шкале
        'colorscale': 'Hot',           # использование цветовой шкалы Hot
        'reversescale': True,          # светло-жёлтый цвет для малых значений, тёмно-коричневый для сильных землетрясений
        'colorbar': {'title': 'Магнитуда'},   # определение внешнего вида боковой полоски
    },
}]

my_layout = Layout(title='Глобальные землетрясения за прошедший месяц')  # создаём заголовок диаграммы

fig = {'data': data, 'layout': my_layout}   # создаём словарь, содержащий данные и макет
offline.plot(fig, filename='глобальные землетрясения.html')  # передаём словарь fig функции plot() с именем выходного файла