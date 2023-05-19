import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import time
import threading
import sys
from playsound import playsound



class GUI(ttk.Frame):
    def __init__(self, contenedor, debug=False):
        super().__init__(contenedor)
        self.debug = debug
        if self.debug:
            print(f'DEBUG:    {self.debug}')

        self.turn = 'work'

        self.listaThreadings = []

        self.initRound = 1
        self.restMinute = 5
        self.minuto = 25
        self.rounds = 4
        self.sleeping = 1

        self.running = False
        self.close = False

        self.display = ''

        self.clock = datetime.fromtimestamp(self.minuto * 60)
        self.restClock = datetime.fromtimestamp(self.restMinute * 60)

        #
        # Construcción del wigdet
        # \/  \/  \/   \/  \/  \/

        style = ttk.Style()
        style.configure('timer.TLabel', font=('Droid Sans', 45, 'bold'))
        self.labelTimer = ttk.Label(self, style='timer.TLabel')
        self.labelTimer['text'] = self.timerDisplay()


        # Frame status
        self.frameStatus = ttk.Frame(self)
        # Frame padre de minutos y ciclos
        self.frameUpDown = ttk.Frame(self)
        # Frames hijos de minutos y ciclo
        self.frameLabelUpDown = ttk.Frame(self.frameUpDown)
        self.frameRoundUpDown = ttk.Frame(self.frameUpDown)
        # Frame panel control
        self.frameControl = ttk.Frame(self)


        style = ttk.Style()
        style.configure('title.TLabel', font=('Droid Sans', 20, 'bold'))
        self.turnLabel = ttk.Label(self.frameStatus, style='title.TLabel')
        self.turnLabel['text'] = 'Work'

        style = ttk.Style()
        style.configure('title.TLabel', font=('Droid Sans', 20, 'bold'))
        self.currentRound = ttk.Label(self.frameStatus, font=('Droid_Sans 11 underline'))
        self.currentRound["text"] = f'Step {self.initRound}'



        # panel control
        self.start = ttk.Button(self.frameControl, text='start', command=self.btnStart)
        # self.start.config(state='disabled')

        self.pause = ttk.Button(self.frameControl, text='pause', command=self.pause)
        self.pause.config(state='disabled')
        self.reset = ttk.Button(self.frameControl, text='reset', command=self.reset)
        self.reset.config(state='disabled')

        # elementos frame minutos
        self.minuteDescribe = ttk.Label(self.frameLabelUpDown, text='Minutos')
        self.labelMinute = ttk.Label(self.frameLabelUpDown)
        self.labelMinute['text'] = self.showMinute()
        self.upMinute = ttk.Button(self.frameLabelUpDown, text='+', command=self.increment)
        self.downMinute = ttk.Button(self.frameLabelUpDown, text='-', command=self.decrement)

        # elementos frame ciclos
        self.roundsDescribe = ttk.Label(self.frameRoundUpDown, text='Rounds')
        self.labelRounds = ttk.Label(self.frameRoundUpDown)
        self.labelRounds['text'] = self.showRound()
        self.upRound = ttk.Button(self.frameRoundUpDown, text='+', command=self.roundIncrement)
        self.downRound = ttk.Button(self.frameRoundUpDown, text='-', command=self.roundDecrement)

        # ###############
        # Grid elementos

        # Frame GRID status
        self.frameStatus.grid(column=0, columnspan=5, row=0)
        self.turnLabel.grid(column=0, columnspan=5, row=1)
        self.currentRound.grid(column=0, columnspan=5, row=2)

        # label grid timer
        self.labelTimer.grid(column=0, columnspan=5, row=1)

        # Frame grid
        self.frameUpDown.grid(column=0, row=4, sticky="NSEW")
        self.frameLabelUpDown.grid(column=0, columnspan=2, row=4, padx=10, sticky="NSEW")
        self.frameRoundUpDown.grid(column=3, columnspan=2, row=4, padx=10, sticky="NSEW")

        # grid frame minutos
        self.minuteDescribe.grid(column=1, columnspan=2, row=1)
        self.labelMinute.grid(column=1, columnspan=2, row=2)
        self.upMinute.grid(column=1, row=3)#, sticky=tk.W)
        self.downMinute.grid(column=2, row=3)#, sticky=tk.W)

        # grid frame rounds
        self.roundsDescribe.grid(column=3, columnspan=2, row=1)
        self.labelRounds.grid(column=3, columnspan=2, row=2)
        self.upRound.grid(column=3, row=3)
        self.downRound.grid(column=4, row=3)

        # grid frame control
        self.frameControl.grid(column=0, columnspan=5, row=5, pady=20)
        self.start.grid(column=1, row=1, sticky="NSEW")
        self.pause.grid(column=2, row=1, sticky="NSEW")
        self.reset.grid(column=3, row=1, sticky="NSEW")

        # frame padre
        self.grid(sticky="NSEW", pady=(10,10))


    def ding(self):
        playsound('sounds/ding.wav')

    def alarm_clock(self):
        playsound('sounds/alarm.mp3')

    def tic_tac_clock(self):
        playsound('sounds/tic.wav')

    def work(self):
        if self.debug:
            print(f'run: {self.running}', f'close?: {self.close}', f'round  {self.rounds}')

        self.upMinute.config(state='disabled')
        self.downMinute.config(state='disabled')
        self.upRound.config(state='disabled')
        self.downRound.config(state='disabled')

        if self.rounds > 0:
            while self.clock.timestamp() >= 0 and self.running:
                if self.close == True:
                    break
                self.display = f'{self.clock.strftime("%M")} : {self.clock.strftime("%S")}'

                if self.debug:
                    print(self.display, self.clock.timestamp())

                self.timerDisplay()
                self.clock = datetime.fromtimestamp(self.clock.timestamp() - 1)

                sound = threading.Thread(target=self.tic_tac_clock)
                sound.start()

                time.sleep(self.sleeping)

                if self.clock.timestamp() == 0 and self.rounds > 0:
                    if self.debug:
                        print('---> 0 miliseconds', f'Round : {self.rounds}')
                    self.close = True
                    self.turn = 'rest'
                    self.turnLabel['text'] = 'Rest'
                    self.restClock = datetime.fromtimestamp(self.restMinute * 60)
                    self.display = f'{self.restClock.strftime("%M")} : {self.restClock.strftime("%S")}'
                    self.labelTimer.config(text=self.display)
                    # self.rest()
                    self.start.config(state='normal')
                    self.pause.config(state='disabled')
                    self.reset.config(state='normal')
                    self.rounds -= 1
                    if self.rounds > 0:
                        sound = threading.Thread(target=self.ding)
                        sound.start()

        if self.rounds <= 0:
            if self.debug:
                print('---_> Aca')
            self.close = True
            self.rounds = 4
            self.minuto = 25
            self.initRound = 1
            self.turn = 'work'
            self.turnLabel['text'] = 'Work'
            self.clock = datetime.fromtimestamp(self.minuto * 60)
            self.display = f'{self.clock.strftime("%M")} : {self.clock.strftime("%S")}'
            self.currentRound.config(text=f'Step {self.initRound}')
            self.labelTimer.config(text=self.display)
            self.labelRounds.config(text=self.rounds)
            self.labelMinute.config(text=self.minuto)
            if self.debug:
                print('DESDE WORK', f'round  {self.rounds}')
                print('FIN DEL TRABAJo')

            alarm = threading.Thread(target=self.alarm_clock)
            alarm.start()

            self.msg = messagebox.showinfo(title="Alert", message='El trabajo ha terminado')



    def rest(self):
        if self.debug:
            print(f'Desde REST, --- {self.rounds}')


        if self.rounds > 0:
            while self.restClock.timestamp() >= 0 and self.running:
                # if self.rounds < 0:
                #     break
                if self.close == True:
                    break
                self.display = f'{self.restClock.strftime("%M")} : {self.restClock.strftime("%S")}'

                if self.debug:
                    print(self.display)

                self.labelTimer.config(text=self.display)
                self.restClock = datetime.fromtimestamp(self.restClock.timestamp() - 1)

                sound = threading.Thread(target=self.tic_tac_clock)
                sound.start()

                time.sleep(self.sleeping)

                if self.restClock.timestamp() == 0:
                    self.initRound += 1
                    self.currentRound.config(text=f'Step {self.initRound}')
                    self.turn = 'work'
                    self.turnLabel['text'] = 'Work'
                    self.close = True
                    self.clock = datetime.fromtimestamp(self.minuto * 60)
                    self.display = f'{self.clock.strftime("%M")} : {self.clock.strftime("%S")}'
                    self.labelTimer.config(text=self.display)
                    self.start.config(state='normal')
                    self.pause.config(state='disabled')
                    self.reset.config(state='normal')

                    sound = threading.Thread(target=self.ding)
                    sound.start()
                    # self.work()


    def btnStart(self):
        if self.debug:
            print(f'Turn ---> {self.turn}')
            print(f'Round ---> {self.rounds}')
            print('running', self.running)

        self.running = True
        self.close = False

        if self.running == True:
            self.start.config(state='disabled')
            self.pause.config(state='normal')
            self.reset.config(state='normal')

        if self.turn == 'work':
            thread = threading.Thread(target=self.work, name='work')
            self.listaThreadings.append(thread)
        elif self.turn == 'rest':
            thread = threading.Thread(target=self.rest, name='rest')
            self.listaThreadings.append(thread)
        thread.start()


    def pause(self):
        self.start.config(state='normal')
        self.pause.config(state='disabled')
        self.reset.config(state='normal')
        self.running = False
        self.close = False

    def reset(self):
        self.start.config(state='normal')
        self.pause.config(state='disabled')
        self.reset.config(state='disabled')

        self.upMinute.config(state='normal')
        self.downMinute.config(state='normal')
        self.upRound.config(state='normal')
        self.downRound.config(state='normal')

        self.close = True
        self.rounds = 4
        self.turn = 'work'
        self.labelRounds.config(text=self.rounds)
        self.clock = datetime.fromtimestamp(self.minuto * 60)
        self.display = f'{self.clock.strftime("%M")} : {self.clock.strftime("%S")}'
        self.timerDisplay()

    def timerDisplay(self):
        self.display = f'{self.clock.strftime("%M")} : {self.clock.strftime("%S")}'
        self.labelTimer.config(text=self.display)

    def increment(self):
        if self.minuto <= 59:
            self.minuto += 1
            self.clock = datetime.fromtimestamp(self.minuto * 60)

            if self.debug:
                print(self.minuto, self.clock)

            self.showMinute()
            self.timerDisplay()

    def decrement(self):
        if self.minuto > 1:
            self.minuto -= 1
            self.clock = datetime.fromtimestamp(self.minuto * 60)

            if self.debug:
                print(self.minuto, self.clock)

            self.showMinute()
            self.timerDisplay()

    def roundIncrement(self):
        if self.rounds < 12:
            self.rounds += 1

            if self.debug:
                print('Round', self.rounds)

            self.showRound()

    def roundDecrement(self):
        if self.rounds > 1:
            self.rounds -= 1

            if self.debug:
                print('Round', self.rounds)

            self.showRound()


    def showMinute(self):
        self.labelMinute.config(text=self.minuto)

    def showRound(self):
        self.labelRounds.config(text=self.rounds)



class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('PyMoDoRo')
        # self.geometry('300x100')
        self.resizable(width=False, height=False)



if __name__ == '__main__':
    debug = False
    args = sys.argv
    if len(args) > 2:
        if args[2] == 'debug':
            debug = True

    g = App()
    # g.protocol('WM_DELETE_WINDOW', '')
    GUI(g, debug)
    g.mainloop()
