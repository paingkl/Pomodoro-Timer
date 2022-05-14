import tkinter as tk
from tkinter import messagebox
import sys
import keyboard
import threading


def init_form(root, fields):
    """
    Initialise the form UI. Return a list of entry widgets.
    """
    entries = []

    # Display welcome message
    message = tk.Label(root, text='Welcome to PomodoroTimer!')
    message.pack()

    # Display input fields
    for field in fields:
        # Wrap field label and entry in one row
        row = tk.Frame(root)
        label = tk.Label(row, width=10, text=field, anchor='w')
        entry = tk.Entry(row)
        row.pack(side='top', fill='x', padx=5, pady=5)
        label.pack(side='left')
        entry.pack(side='right', fill='x', expand=1)
        entries.append(entry)
    
    return entries


def fetch(entries):
    """
    Get user inputs from entry widgets. If all inputs are valid times, run the timer.
    """
    times = []
    try:
        for entry in entries:
            time = int(entry.get())
            if time < 0:
                messagebox.showerror(title='Error', message='Time must be non-negative integer only, please try again.')
                clear(entries)
                return
            else:
                times.append(time)
    except ValueError:
        messagebox.showerror(title='Error', message='Time must be non-negative integer only, please try again.')
        clear(entries)
        return
    else:
        run_timer(times)


def clear(entries):
    """
    Clear all entry widgets.
    """
    for entry in entries:
        entry.delete(0, 'end')


def run_timer(times):
    """
    Run the pomodoro timer. Stop the timer immediately once force quit is invoked.
    """
    forcequit.clear()  # Reset flag just in case
    work, rest = times
    count = 0
    suffix = ''
    while True:
        if count+1 % 10 == 1:
            suffix = 'st'
        elif count+1 % 10 == 2:
            suffix = 'nd'
        elif count+1 % 10 == 3:
            suffix = 'rd'
        else:
            suffix = 'th'

        # Start pomodoro
        messagebox.showinfo(title='Pomodoro Started!', 
            message=f'Work time set for {work} mins.\nCurrently in {count+1}{suffix} pomodoro.')
        root.withdraw()  # Hide main window
        forcequit.wait(timeout=work*60)
        if forcequit.is_set():
            break
        messagebox.showinfo(title='Break Started!', 
            message=f'Break time set for {rest} mins.\nCurrently in {count+1}{suffix} pomodoro.')
        forcequit.wait(timeout=rest*60)
        if forcequit.is_set():
            break
        count += 1  # End of 1 pomodoro

        root.deiconify()  # Bring back main window
        if not messagebox.askyesno(title='Pomodoro Ended!', message='Do you want to start another pomodoro?'):
            messagebox.showinfo(title='Good Job!', message=f'You have completed {count} pomodoros in this sitting.')
            return
    
    # Force quit invoked
    root.deiconify()
    quit()


def quit():
    """
    Terminate the PomodoroTimer App.
    """
    if messagebox.askyesno(title='Quit', message='Are you sure you want to quit?'):
        root.destroy()
        sys.exit()


if __name__ == '__main__':
    forcequit = threading.Event()

    # Main window
    root = tk.Tk()
    root.title('PomodoroTimer')
    root.attributes('-topmost', True)  # Bring to frontmost

    # Form
    fields = ['Work (mins):', 'Break (mins):']
    entries = init_form(root, fields)

    # Buttons
    btn_row = tk.Frame(root)
    start_btn = tk.Button(btn_row, text='Start', command=(lambda e=entries: fetch(e)))
    quit_btn = tk.Button(btn_row, text='Quit', command=quit)
    btn_row.pack(side='top', fill='x', pady=5)
    quit_btn.pack(side='right', padx=5, ipadx=10)
    start_btn.pack(side='right', ipadx=10)

    # Keyboard event (Win + `) to force quit during an ongoing pomodoro
    keyboard.add_hotkey('win+`', lambda: forcequit.set())
    
    root.mainloop()
