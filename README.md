Вот пример файла `README.md` для вашего проекта:

```markdown
# Pomodoro Timer

Pomodoro Timer — это инструмент для повышения продуктивности, основанный на методике Pomodoro. Программа помогает пользователям организовать свои рабочие сессии с чередованием работы и отдыха. Также предусмотрена возможность сбора и анализа статистики.

## Установка

1. Убедитесь, что у вас установлен Python версии 3.7 или выше.
2. Клонируйте репозиторий проекта:
   ```bash
   git clone <URL вашего репозитория>
   ```
3. Перейдите в папку проекта:
   ```bash
   cd <папка_с_проектом>
   ```
4. Установите проект с помощью `pip`:
   ```bash
   pip install .
   ```

## Использование

После установки, команда `pomodoro` будет доступна в командной строке. Ниже приведены основные параметры и команды.

### Запуск таймера

Запустите базовый таймер:
```bash
pomodoro -r {hours}:{minutes}
```

Пример:
```bash
pomodoro -r 1:30
```
Это начнет 1 час 30 минут работы, разбитые на сессии с использованием стандартных настроек (25 минут работы, 5 минут отдыха, 15 минут длинного перерыва).

### Изменение настроек таймера

Чтобы изменить базовые настройки таймера:
```bash
pomodoro -r 1:30 -m
```

Вы сможете задать длину рабочих и отдыхательных сессий, а также настроить большую паузу и указать целевую активность.

### Статистика

1. **За последнюю неделю:**
   ```bash
   pomodoro --stats last_week
   ```

2. **По дате:**
   ```bash
   pomodoro --stats date --stats_mode date
   ```
   Вас попросят ввести дату в формате `YYYY-MM-DD`.

3. **За период:**
   ```bash
   pomodoro --stats period --stats_mode activity
   ```
   Вас попросят указать начальную и конечную дату.

