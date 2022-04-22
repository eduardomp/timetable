
import PySimpleGUI as sg
import model


class ActivitiesWindow():

    def __init__(self):

        self.programs = list(
            map(lambda p: f'{p.id} - {p.title} ({p.type})', model.Programs.get_all()))

        self.modules = list(
            map(lambda m: f'{m.id} - {m.title}', model.Modules.get_all()))

        self.day_of_week = ['Monday',
                            'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.start = '',
        self.finish = '',
        self.hours = ['09:00', '10:00', '11:00', '12:00', '13:00', '14:00',
                      '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']

        self.layout = [
            [sg.Text('Program', size=(10, 1), justification='right'), sg.Combo(self.programs,
                                                                               key='-PROGRAM-', enable_events=True, size=(30, 1))],
            [sg.Text('Module', size=(10, 1), justification='right'), sg.Combo(self.modules,
                                                                              key='-MODULE-', disabled=True, size=(30, 1))],
            [sg.Text('Day of Week', size=(10, 1), justification='right'), sg.Combo(self.day_of_week,
                                                                                   key='-DAY-', disabled=True, size=(30, 1))],
            [sg.Text('Start', size=(10, 1), justification='right'), sg.Combo(self.hours,
                                                                             key='-START-', disabled=True, size=(30, 1))],
            [sg.Text('Finish', size=(10, 1), justification='right'), sg.Combo(self.hours,
                                                                              key='-FINISH-', disabled=True, size=(30, 1))],
            [sg.Button('Add', disabled=True, size=(45, 1))],
            [sg.Button('Close', key="-CLOSE-", size=(45, 1))]
        ]

        self.window = sg.Window('Activities', self.layout, size=(300, 250))

    def reset(self):
        self.window.find_element('-PROGRAM-').update('')
        self.window.find_element('-MODULE-').update('', disabled=True)
        self.window.find_element('-DAY-').update('', disabled=True)
        self.window.find_element('-START-').update('', disabled=True)
        self.window.find_element('-FINISH-').update('', disabled=True)
        self.window.find_element('Add').update(disabled=True)

    def save(self, values):
        if values['-PROGRAM-'] and values['-MODULE-'] and values['-DAY-'] and values['-START-'] and values['-FINISH-']:

            activity = model.Activities(
                module=values['-MODULE-'], day_of_week=values['-DAY-'], start=values['-START-'], finish=values['-FINISH-'])

            exists = model.Activities.count(activity)

            if exists == 0:
                model.Activities.insert(activity)

            self.reset()

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if event == '-PROGRAM-':
                self.modules = list(
                    map(lambda m: f'{m.id} - {m.title}', model.Modules.get_by_program_id(
                        values['-PROGRAM-'].split(' - ')[0])))

                print(f'>>> {self.modules} ')

                self.window.find_element('-MODULE-').update(
                    self.modules, disabled=False)

            if event == 'Add':
                self.save(values)

            if event in (sg.WIN_CLOSED, '-CLOSE-'):
                break

        self.window.close()
