# voley_bet_3_set
parsing/predict_model/autobet

#название файлов рабочее, так как делал все для себя, особой красоты не наводил 


#1.Программа состоит из 3 блоков: 
- парсинг: парсит игры в лайве с сайтов букмекеров 
- прогнозотор(делает предикт на какую команду ставить) - на основе ранее подготовленной модели (модель на базе тестового датасета на основе рельных игр в количестве 8000 штук)
- автоставка: делает ставку на тот исход, который выдал прогнозатор
- Все в сборе запускается в следующей очередности: 
1) парсер
2) прогнозатор
3) автоставка 
Все файлы находятся в папке voley_set. Тренировочная модель в корне проекта 
В папке voley_set/test_model_result  - находятся файлы которые проверяют результат работы модели на рельных данных.

#2. Чтобы запустить парсер нужно запустить файл sound1508.py

#3 Чтобы запустить прогнозотор нужно запустить файл to_bet.py

#4. Чтобы запустить автоставку нужно запустить файл 3_7

№5. Чтобы проверить результат работы прогнозатора нужно запустить файлы из voley_set/test_model_result в порядке нумерации в начале названия файла. Данный блок не обязательный, сделан чтобы можно было проверить результат оперативно

