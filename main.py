
import PySimpleGUI as sg
import model
import program
import modules
import activities
import timetable

ZERO_PAD = ((0, 0), (0, 0))

LOGIN = "admin"
PASSWORD = "admin"


class MainWindow():

    def __init__(self):

        self.authenticated = False

        self.programs = model.Programs.get_all()
        self.selected_program = None

        sg.theme('Material2')

        self.top_bar = [
            [sg.Text('Login',  size=(10, 1), justification='right'),
             sg.Input(key='-LOGIN-', size=(35, 1))],
            [sg.Text('Password',  size=(10, 1), justification='right'),
             sg.Input(key='-PASS-', size=(35, 1), password_char='*')],
            [sg.Button('Login', key='-LOGIN-BTN-', size=(45, 1))]
        ]

        self.buttons = [
            [sg.Button('Programs', key='-PROGRAMS-',
                       size=(45, 1), visible=self.authenticated)],
            [sg.Button('Modules', key='-MODULES-', size=(45, 1),
                       visible=self.authenticated)],
            [sg.Button('Activities', key='-ACTIVITIES-',
                       size=(45, 1), visible=self.authenticated)],
        ]

        self.combo_programs = [
            [sg.Text('Select a program to generate the timetable:',
                     justification='center', key='-SELECTED-PROGRAM-LABEL-', visible=self.authenticated)],
            [sg.Combo(self.programs, key='-SELECTED-PROGRAM-',
                      enable_events=True, size=(45, 1), visible=self.authenticated)],
        ]

        self.layout = [[
            [self.top_bar, sg.HSeparator()],
            [self.buttons],
            [self.combo_programs]
        ]]

        self.window = sg.Window('Timetable', self.layout, size=(300, 250))

    def set_selected_program(self, values):
        self.selected_program = values['-SELECTED-PROGRAM-']

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if event == '-PROGRAMS-':
                program.ProgramWindow().render()

            if event == '-MODULES-':
                modules.ModulesWindow().render()

            if event == '-ACTIVITIES-':
                activities.ActivitiesWindow().render()

            if event == '-SELECTED-PROGRAM-':
                self.set_selected_program(values)
                timetable.TimetableWindow(self.selected_program).render()

            if event == '-LOGIN-BTN-':
                if values['-LOGIN-'] == LOGIN and values['-PASS-'] == PASSWORD:
                    print("ok")
                    self.window.find_element('-PROGRAMS-').update(visible=True)
                    self.window.find_element('-MODULES-').update(visible=True)
                    self.window.find_element(
                        '-ACTIVITIES-').update(visible=True)
                    self.window.find_element(
                        '-SELECTED-PROGRAM-').update(visible=True)
                    self.window.find_element(
                        '-SELECTED-PROGRAM-LABEL-').update(visible=True)
                    self.authenticated = True

                else:
                    sg.popup('Wrong login or password!')

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

        self.window.close()


if __name__ == '__main__':
    MainWindow().render()
