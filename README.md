# ChefList_web
Cайт для составления и хранения списков покупок и рецептов блюд (клон мобильного приложения ChefList).

Этот сайт позволит Вам:
1. Создать список покупок, чтобы не забыть купить в магазине зелёный горошек.
2. Собрать список покупок со всеми необходимыми продуктами для приготовления блюд
    * по собственным рецептам;
    * по имеющимся на сайте рецептам;
    * и даже по рецептам с других сайтов!

**Теперь Вы сможете приготовить всё что хотели и не забьёте при этом холодильник ненужными продуктами!**

## Инструкция по запуску сервера
Выполните в терминале в папке проекта:

**Linux и Mac:** export FLASK_APP=webapp && export FLASK_ENV=development && flask run

**Windows:** set FLASK_APP=webapp && set FLASK_ENV=development && set FLASK_DEBUG=1 && flask run

Или запустите скрипт \_\_init\_\_.py из папки webapp.

## Develop

### Black
*Для использования Black в PyCharm:*
1. Установить black:
```pip install black```
2. Определить путь до папки с утилитой с помощью команды в консоли:
- **Linux и Mac:** ```which black```
- **Windows:** ```where black```
3. Установить в PyCharm расширение **File Watcher**
4. В PyCharm открыть Preferences or Settings -> Tools -> File Watchers и нажать на +
5. Заполнить поля следующим образом:
- Name: Black
- File type: Python
- Scope: Project Files
- Program: <install_location_from_step_2>
- Arguments: \$FilePath$
- Output paths to refresh: \$FilePath$
- Working directory: \$ProjectFileDir$
6. В области Advanced снять чекбоксы “Auto-save edited files to trigger the watcher”, “Trigger the watcher on external changes”.
7. Ok, Ok.
8. Теперь black будет переформатировать файлы в соответствии со своими правилами форматирования при каждом сохранении файлов.

*Для использования Black в VSCode:*
1. Установить расширение **Black Formatter**
2. Открыть страницу настроек и в поиске ввести:
```@id:editor.defaultFormatter @lang:python python formatter```
3. В выпадающем меню выбрать **Black Formatter**
4. Теперь black будет переформатировать файлы в соответствии со своими правилами форматирования при каждом сохранении файлов.


