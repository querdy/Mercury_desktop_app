# Mercury_desktop_app
Приложение для автоматизации рутины при работе с Меркурием.
Работоспособно при наличии аккаунта с правом доступа "Сертефикация высшего ветеринарного риска" (ГВЭ).

ВАЖНО! Программа не использует оффициальное API по причине того, что в нем не реализована часть функций для ГВЭ (ВСЭ, справки о безопасности молока), как следвствие производится работа через внутренни API сайта, следовательно приложение может внезапно перестать работать. Если не работает логин - достаточно сменить IP(перезапустить роутер). Зато не нужно получать отдельные реквизиты доступа :)

Функции:
1. внесение лабораторных исследований на вырабатываемую продукцию по номеру транзакции (в транзакциях типа переработка/производство, в т.ч. при незавершенном производстве с исключением повторного внесения исследований на одну запись журнала при многократном запуске)
2. внесение ВСЭ на вырабатываемую продукцию по номеру транзакции

В планах:
1. Внесение ВСЭ
2. Формирование транзакций типа переработка/производство по шаблону-заявке (*.xlsx)
3. Формирование транзакций типа перевозка со сменой владельца и без по шаблону-заявке (*.xlsx)
4. Формирование справки о безопасности молока

Краткая инструкция:
При первом запуске:
  - Настройки -> Добавить/изменить пользователя -> вводим логин-пароль -> Добавить. Должно прийти уведомление с подтверждением входа. Логин-пароль сохраняются у ВАС на    компьютере (в открытом виде, файл db.sqlite3 в корне приложения).

Лабораторные исследования:
При первом запуске:
    Настройки -> Зарегистрировать предприятие -> следуем подсказке -> Сохранить
    * - название предприятие - это просто название шаблона. Оно нужно исключительно для удобного выбора набора исследований при запуске.
  
При последующих запусках:
  На вкладке "Исследования" вводим номер транзакции -> выбираем предприятие-шаблон -> "Старт"
  * - если выбрать не то предприятие, на продукцию в указанной транзакции будут внесены исследования, относящиеся выбранному предприятию, будте аккуратны.

ВСЭ:
  При первом запуске:
  - Настройки -> Изменить список предприятий (всэ) -> добавляете удобное для вас название и номер RU (только цифры) -> сохранить
  - Настройки -> Изменить список показателей ВСЭ -> ВАЖНО! Вам нужна транзакция переработки из живой скотины в продукцию, программа сможет подцепить только ту продукцию, которая в этой транзакции есть на остатке (остаток не равен 0). Вводим номер этой транзакции, выбираем площадку, жмем "мобрать данные о продукции"
  - Тут же нажимаем кнопку "Добавить всэ" -> выбираем продукцию, показатель, вводим фактическое значение и заключение (как в самом меркурии) -> сохранить
  - Настройки -> Изменить цели ВСЭ для продукции -> Базово для всех продуктов встает цель "реализация в пищу людям" - если у вас на каких-то продуктах цель другая - указываете из списки -> сохранить
  - Вноситься ВСЭ будут только на ту продкцию, для которой вы указали необходимые параметры на вкладке "Изменить список показателей ВСЭ"
  
  При последующих запусках:
  - На вкладке "ВСЭ" вводим номер транзакции и выбираем предприятие, указанное в настройках на вкладке "Изменить список предприятий (всэ)" -> Старт
  

Стек: Electron, Vue.js, FastAPI, SQLAlchemy, bs4
