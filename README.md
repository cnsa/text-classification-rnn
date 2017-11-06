# Text-classification on Keras Tensorflow with LSTM and word2vector models.

Prepare python:

```shell
pip install -r ./requirements.txt
```

Train model:
```shell
python ./model.py
```

Evaluate saved model:
```shell
python ./eval.py
```

Run Tensorboard
```
make tensorboard
```
http://localhost:6006/#scalars


# DATA

### FACTOR ID MAP

Факторы используются под уникальными кодовыми именами.

Возьмем за основу числовой набор 1-N.
Это позволит сократить размер нашей коллекции данных.

Query представляет собой запрос для веб-интерфейса.

Если Query = `-`, значит оно соответствует значению в колонке Factor.

| Id  | Factor | Query |
| --- | ---- | --- |
| 0 | Рост числа туристов | - |
| 1 | Рост времени пребывания туристов | - |
| 2 | Увеличение среднего чека | - |
| 3 | Повышение прямой доходности от турпотока | - |
| 4 | Увеличение числа КСР | Увеличение числа коллективных средств размещения |
| 5 | Создание специализированных шоппинг-центров | - |
| 6 | Увеличение числа событийных мероприятий | - |
| 7 | Создание специализированных въездных туроператоров (облегченный визовый въезд) | `[Создание специализированных въездных туроператоров, облегченный визовый въезд]` |
| 8 | Повышение качества экскурсионного обслуживания | - |
| 9 | Повышение качества навигации и транспортного обслуживания | - |
| 10 | Создание туристских кластеров и точек потребления | - |
| 11 | PR продвижение Москвы в СМИ и Соцсетях | - |
| 12 | Реклама туристских возможностей среди выездных туроператоров за рубежом | - |
