#  `datalang`
## Data-Oriented Programming Language (EDS)

(c) Dmitry Ponyatov <<dponyatov@gmail.com>> 2020 MIT

github: https://github.com/ponyatov/datalang


* dynamic language over Executable Data Structures
    * metaprogramming as the main method
    * homoiconic interpreter
    * weak dynamic typing
* oriented for ML and data processing
    * implemented in Python due to a huge amount of off-the-shelf libraries
    * interactive session via web interface
        * console -> Jupyter-like cell editor -> full-size web layouting
* `DataWeb` platform
    * tiny web client (mobile optimized)
    * full web interface for the server-side system (distributed cloud in mind)
    * web representation is data, programs are data, everything is self-evaluatable data
    * targets on dynamic web sites with internal data processing (web+apps+storage)
* `todo`
    * port to Erlang/Elixir runtime stack
    * Lispy dynamic language


## три & 1/2 пункта trueъ языка программирования

1. способен ли язык работать с программами на самом себе напрямую, без
   построенния тонны промежуточных слоев? (типа парсеров и reflection)
2. способен ли язык расширять собственную *семантику* не выходя за границы
   синтаксиса? (макросы)
3. содержит ли ядро языка средства расширения *синтаксиса*, позволящие
   **ввести** в систему код на любом другом языке?
    * содержит ли язык достаточно богатые средства форматированного **вывода**,
      чтобы получить код на любом другом языке?


### Code as Data

* Николай Рыжиков
    [Clojure Data DSL's для web разработки](https://www.youtube.com/watch?v=urQ5o754TU4)

* [SICP] Харольд Абельсон, Джеральд Джей Сассман
    [Структура и Интерпретация Компьютерных Программ](https://www.ozon.ru/product/struktura-i-interpretatsiya-kompyuternyh-programm-5322055)

* [red book]
    [Программирование в Clojure: Практика применения Lisp в мире Java](https://www.ozon.ru/product/programmirovanie-v-clojure-praktika-primeneniya-lisp-v-mire-java-142702699)

* Faraz Haider
    [Writing Lispex, a Lisp interpreter in Elixir](https://medium.com/@sfhrizvi/writing-lispex-a-lisp-interpreter-in-elixir-423cd2c439ac)


### Persistent Languages

* https://en.wikipedia.org/wiki/Persistent_programming_language
* **OS Phantom** (by) Дмитрий Завалишин
    * [ОС Фантом с ортогональной персистентностью](https://www.youtube.com/watch?v=ocqyZO-5VsA)


### Python

#### Flask/SQLite

* Мигель Гринберг
    [Разработка веб-приложений с использованием Flask на языке Python](https://www.ozon.ru/context/detail/id/139907958)
* [Изучение Flask / #3 - Работа с базой данных SQLite](https://www.youtube.com/watch?v=G-si1WbtNeM)
* https://flask-sqlalchemy.palletsprojects.com/en/2.x/quickstart/

#### Django hell

* [Архитектура ПО, MVC и бизнес-логика. Критика Django](https://www.youtube.com/watch?v=HpL6ymFEuu4)

#### aiohttp

*  Okumy
    [Курс: асинхронный Python](https://www.youtube.com/playlist?list=PLyUvGavKi98XpdrC92SDQGCKrGpT5ieWw)


### Erlang/Elixir

* [urich] Саша Юрич
    [Elixir в действии](https://www.ozon.ru/product/elixir-v-deystvii-164833016)
* Joe Armstrong
    [Programming Erlang](https://gangrel.files.wordpress.com/2015/08/programming-erlang-2nd-edition.pdf)
    Software for a Concurrent World /2nd ed/
* [green book] Франческо Чезарини, Симон Томпсон
    [Программирование в Erlang](https://www.ozon.ru/context/detail/id/148770389)
* [OTP] Франческо Чезарини, Стивен Виноски
    [Проектирование масштабируемых систем с помощью Erlang/OTP](https://www.ozon.ru/context/detail/id/140152220)
* [The Erlang Runtime System](https://exote.ch/~aseigo/beam-book/beam-book-2017-04-08.pdf)
* Vincenzo Nicosia
    [Towards Hard Real–Time Erlang](http://erlang.org/workshop/2007/proceedings/05nicosi.pdf)

#### Cowboy

* https://habr.com/ru/post/173595/


### DataFlow programming

* https://grgv.xyz/aflow/
* https://www.youtube.com/c/Nodes_io/videos

#### JavaScript libs for interactive 2D

* http://www.draw2d.org/draw2d_touch/jsdoc/#!/guide
* https://bpmn.io/toolkit/bpmn-js/

## BPMN/UML

### Camunda

* https://camunda.com/why-camunda/
    * [Getting Started with Camunda](https://www.youtube.com/playlist?list=PLJG25HlmvsOUnCziyJBWzcNh7RM5quTmv)
* Reunico [Camunda BPM для начинающих](https://www.youtube.com/playlist?list=PLmLqPF63bMozWwyXeyclGi48kxbFcDBFL)

## misc

* https://t.me/proelixir/176600
    * «Нормальное ТЗ» для программиста -- это миф, придуманный людьми, которые
      не хотят вовлекаться в то, зачем вообще нужно программирование. А бизнес
      меняется, как и его восприятие.
        * явный признак, что не хватает какого-то мощного, но очень динамичного
          средства прототипирования (язык + среда), в котором заказчик (*)
          способен нарисовать действующую модель продукта, и передать её
          нормальным программистам для фиксации в полноценную реализацию<br> (*)
          пара человек в штате, которые в теме, и при этом кое-как-то могут в
          программирование
        * что-то а-ля Smalltalk возможно, как интерактивная среда -- рисовать
          элементы интерфейса (просто мышью тык квадратик на экран), вешать на
          них события, для событий прописывать методы обработки на чем-то
          питоноподобном...
        * в ЕСПД-мире для этого было попугайское называние "эскизное
          проектирование" -- система "RADОСть"
