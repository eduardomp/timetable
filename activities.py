
import PySimpleGUI as sg
import model


class ActivitiesWindow():

    def __init__(self, selected_activity=None):

        self.selected_activity = selected_activity

        module_disabled = False if self.selected_activity else True

        self.programs = list(
            map(lambda p: f'{p.id} - {p.title} ({p.type})', model.Programs.get_all()))

        self.modules = list(
            map(lambda m: f'{m.id} - {m.title}', model.Modules.get_all()))

        self.day_of_week = ['Monday',
                            'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        self.start = '',
        self.finish = '',
        self.hours = ['9:00', '10:00', '11:00', '12:00', '13:00', '14:00',
                      '15:00', '16:00', '17:00', '18:00', '19:00', '20:00', '21:00']

        self.layout = [
            [sg.Text('Program', size=(10, 1), justification='right'), sg.Combo(self.programs,
                                                                               key='-PROGRAM-', enable_events=True, size=(30, 1))],
            [sg.Text('Module', size=(10, 1), justification='right'), sg.Combo(self.modules,
                                                                              key='-MODULE-', disabled=module_disabled, size=(30, 1))],
            [sg.Text('Day of Week', size=(10, 1), justification='right'), sg.Combo(self.day_of_week,
                                                                                   key='-DAY-', size=(30, 1))],
            [sg.Text('Start', size=(10, 1), justification='right'), sg.Combo(self.hours,
                                                                             key='-START-', size=(30, 1))],
            [sg.Text('Finish', size=(10, 1), justification='right'), sg.Combo(self.hours,
                                                                              key='-FINISH-', size=(30, 1))],
            [sg.Button('Save', size=(45, 1))],
            [sg.Button('Close', key="-CLOSE-", size=(45, 1))]
        ]

        self.window = sg.Window('Activities', self.layout, size=(300, 250))

    def reset(self):
        self.selected_activity = None
        self.window.find_element('-PROGRAM-').update('')
        self.window.find_element('-MODULE-').update('', disabled=True)
        self.window.find_element('-DAY-').update('')
        self.window.find_element('-START-').update('')
        self.window.find_element('-FINISH-').update('')

    def save(self, values):
        if values['-PROGRAM-'] and values['-MODULE-'] and values['-DAY-'] and values['-START-'] and values['-FINISH-']:

            if self.selected_activity:
                self.selected_activity.module_id = values['-MODULE-'].id
                self.selected_activity.day_of_week = values['-DAY-']
                self.selected_activity.start = values['-START-'].split(':')[0]
                self.selected_activity.finish = \
                    values['-FINISH-'].split(':')[0]

                model.Activities.update(self.selected_activity)

            else:

                activity = model.Activities(
                    module_id=values['-MODULE-'].id,
                    day_of_week=values['-DAY-'],
                    start=values['-START-'].split(':')[0],
                    finish=values['-FINISH-'].split(':')[0])

                exists = model.Activities.count(activity)

                if exists == 0:
                    model.Activities.insert(activity)

            self.reset()

    def set_selected_activity(self):
        module = model.Modules.get_by_id(self.selected_activity.module_id)

        program = model.Programs.get_by_id(module.program_id)

        self.window.find_element(
            '-PROGRAM-').update(f'{program.id} - {program.title} ({program.type})')

        self.window.find_element(
            '-MODULE-').update(f'{module.id} - {module.title}', disabled=False)

        self.window.find_element(
            '-DAY-').update(self.selected_activity.day_of_week)

        self.window.find_element(
            '-START-').update(f'{self.selected_activity.start}:00')

        self.window.find_element(
            '-FINISH-').update(f'{self.selected_activity.finish}:00')

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if(self.selected_activity):
                self.set_selected_activity()
                self.window.refresh()

            if event == '-PROGRAM-':
                self.modules = model.Modules.get_by_program_id(
                    values['-PROGRAM-'].split(' - ')[0])

                self.window.find_element(
                    '-MODULE-').update(value='', values=self.modules, disabled=False)

            if event == 'Save':
                self.save(values)

            if event in (sg.WIN_CLOSED, '-CLOSE-'):
                break

        self.window.close()
