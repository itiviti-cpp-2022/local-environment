# Local Environment
A replica of Github CI environment for testing hw projects on a local machine

## Использование
Так как это окружение основано в частности на использовании Docker-контейнера, для начала необходимо установить его себе на компьютер.
Скачиваем Docker для своей ОС здесь - [Get Docker](https://docs.docker.com/get-docker/), тут же слева есть небольшой туториал, чтобы было, с чего начать.
После установки Docker особо никаких дальнейших взаимодействий с ним вручную производить не нужно (кроме как запустить его),
всё управление делается с помощью двух файлов в этом репозитории - **build.py** и **run.py**.

### 1. Запускаем build.py:
```bash
python3 build.py # Или же python build.py, или же ./build.py
```
Этот скрипт соберёт контейнер **cpp-env**, окружение которого совпадает тем, что у Github CI. В нём же и будет проходить компиляция и тесты.

### Не забываем запустить build.py при обновлении (git pull)!!!

### 2. Натравляем run.py на наш выполненный проект (репозиторий):
```bash
python3 run.py test /локальный/путь/к/репозиторию # естественно это заменяем на локальный путь до того репозитория, где выполнили проект
```
Конкретнее, например:
```bash
python3 run.py test ~/itmo/cpp/monte-carlo
```
Это запустит Docker контейнер cpp-env, который скомпилирует код в вашем репозитории и запустит тесты. 

## Функционал
Любое использование скрипта **run.py** после сборки Docker-контейнера с помощью **build.py** выглядит как:
```bash
python3 run.py {команда} {путь к репозиторию
```
Где команда это одно из:
1. **test** - компилирует проект без санитайзеров, с ASAN ([address sanitizer](https://clang.llvm.org/docs/AddressSanitizer.html)), USAN ([undefined behaviour sanitizer](https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html))
2. **build** - просто проверит компиляцию проекта без санитайзеров
3. **fmt** - отформатирует проект под .clang-format, указанный в репозитории (обычно это общий формат кода для конкретного задания, часто несоблюдение формата вызовет ошибку при пуше кода на гитхаб)  
   Дополнительно указав путь до другого файла .clang-format можно отформатировать в свой формат:
   ```bash
   python3 run.py fmt ../.my-clang-format ../lfru-buddy
   ```
5. **checkfmt** - проверит, соответствует ли код формату, указанному в .clang-format репозитория
6. **send** - прогонит тесты, отформатирует код, после чего запушит его на гитхаб в ту ветку, в которой на данной момент находится локальный репозиторий

## Зачем
У организаций на github (например, itiviti-cpp-2021) есть ограниченное кол-во минут, которые израсходуются каждый раз,
когда вы загружаете свой код в данный репозиторий и запускается долгий процесс компиляции и тестирования. Для этого **обязательно** всегда тестируйте сначала локально, с помощью этого окружения.

Только после успешного прохождения **всех тестов и проверки форматирования** стоит push'ить свой локальный репозиторий в github.
