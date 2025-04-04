import os
import curses
from pathlib import Path
import subprocess

def main(stdscr):
    curses.curs_set(0)  # Скрыть курсор
    current_dir = Path.cwd()
    selected_idx = 0

    # Настройка цветов
    curses.start_color()
    curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)    # Папки
    curses.init_pair(2, curses.COLOR_YELLOW, curses.COLOR_BLACK)  # Файлы
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)   # Выделенный элемент

    while True:
        stdscr.clear()

        # Заголовок
        stdscr.addstr("↑/↓: Выбор | →: Войти | ←: Назад | Пробел: Выбрать | q: Выход\n", curses.A_DIM)
        stdscr.addstr(f"\n\n\nТекущая папка: {current_dir}\n", curses.A_BOLD | curses.color_pair(3))

        # Получаем содержимое папки
        try:
            entries = list(current_dir.iterdir())
        except PermissionError:
            stdscr.addstr("\nОшибка: Нет доступа!", curses.COLOR_RED)
            stdscr.refresh()
            curses.napms(1000)
            current_dir = current_dir.parent
            continue

        # Сортируем (папки → файлы)
        entries.sort(key=lambda x: (not x.is_dir(), x.name.lower()))

        # Вывод элементов
        for idx, entry in enumerate(entries):
            prefix = "> " if idx == selected_idx else "  "
            name = entry.name + ("/" if entry.is_dir() else "")
            
            if idx == selected_idx:
                attr = curses.color_pair(3) | curses.A_BOLD
            elif entry.is_dir():
                attr = curses.color_pair(1)
            else:
                attr = curses.color_pair(2)

            stdscr.addstr(f"{prefix}{name}\n", attr)

        # Обработка клавиш
        key = stdscr.getch()

        if key == ord('q'):
            break
        elif key == curses.KEY_UP and selected_idx > 0:
            selected_idx -= 1
        elif key == curses.KEY_DOWN and selected_idx < len(entries) - 1:
            selected_idx += 1
        elif key == curses.KEY_RIGHT and selected_idx < len(entries):
            selected_entry = entries[selected_idx]
            if selected_entry.is_dir():
                current_dir = selected_entry
                selected_idx = 0
        elif key == curses.KEY_LEFT:
            current_dir = current_dir.parent
            selected_idx = 0
        elif key == ord(' '):  # Пробел — выбор папки
            selected_entry = entries[selected_idx]
            target_dir = selected_entry if selected_entry.is_dir() else selected_entry.parent
            
            # Меняем директорию в текущем процессе
            os.chdir(target_dir)
            
            # Запускаем новый интерактивный fish-shell в новой директории
            subprocess.run(["clear && fish"], shell=True)
            break  # Выходим из curses

if __name__ == "__main__":
    try:
        curses.wrapper(main)
    except KeyboardInterrupt:
        pass
