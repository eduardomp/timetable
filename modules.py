import PySimpleGUI as sg
import model

ZERO_PAD = ((0, 0), (0, 0))


class ModulesWindow():

    def __init__(self):
        self.programs = model.Programs.get_all()
        self.modules = self.get_all()
        self.selected_module = None

        self.years = ['1', '2', '3']
        self.terms = ['1', '2']

        self.layout = [
            [sg.Text('Title', size=(10, 1), justification='right'),
             sg.Input(key='-IN-TITLE-', size=(35, 1))],
            [sg.Text('Program', size=(10, 1), justification='right'),
                sg.Combo(self.programs,
                         key='-PROGRAM-', size=(35, 1))],
            [sg.Text('Year', size=(10, 1), justification='right'),
             sg.Combo(self.years, key='-YEAR-', size=(35, 1))],
            [sg.Text('Term', size=(10, 1), justification='right'),
             sg.Combo(self.terms, key='-TERM-', size=(35, 1))],
            [sg.Text('Optional', size=(10, 1), justification='right'),
             sg.Checkbox('', key='-OPTIONAL-')],
            [sg.Button('Save', size=(45, 1))],
            [sg.Button('Delete', size=(45, 1))],
            [sg.Button('Close', key="-CLOSE-", size=(45, 1))],
            [sg.HSeparator(pad=ZERO_PAD)],
            [sg.Listbox(values=self.modules, select_mode='extended',
                        key='-LIST-MODULES-', size=(120, 20), enable_events=True)],
        ]

        self.window = sg.Window('Modules', self.layout, size=(300, 350))

    def reset(self):
        self.selected_module = None
        self.window.find_element('-IN-TITLE-').update('')
        self.window.find_element('-PROGRAM-').update('')
        self.window.find_element('-YEAR-').update('')
        self.window.find_element('-TERM-').update('')
        self.window.find_element('-OPTIONAL-').update(False)
        self.modules = self.get_all()
        self.window.find_element('-LIST-MODULES-').update(self.modules)

    def save(self, values):
        if values['-IN-TITLE-'] and values['-PROGRAM-'] and values['-YEAR-'] and values['-TERM-']:

            if self.selected_module:
                self.selected_module.title = values['-IN-TITLE-']
                self.selected_module.program_id = values['-PROGRAM-'].id
                self.selected_module.year = values['-YEAR-']
                self.selected_module.term = values['-TERM-']
                self.selected_module.optional = values['-OPTIONAL-']

                model.Modules.update(self.selected_module)
                sg.popup('Activity updated!', title='Success')

            else:
                module = model.Modules(
                    title=values['-IN-TITLE-'],
                    program_id=values['-PROGRAM-'].id,
                    year=values['-YEAR-'],
                    term=values['-TERM-'],
                    optional=values['-OPTIONAL-'])

                exists = [module for module in self.modules if module.title ==
                          values['-IN-TITLE-']]

                if len(exists) == 0:
                    model.Modules.insert(module)
                    sg.popup('Activity created!', title='Success')

            self.reset()

    def delete(self):
        if self.selected_module:
            model.Modules.delete(self.selected_module.id)
            self.reset()

    def get_all(self):
        return model.Modules.get_all()

    def set_selected_module(self, values):
        selected = str(values['-LIST-MODULES-'][0]).split(' - ')
        self.selected_module = [
            module for module in self.modules if module.id == int(selected[0])][0]
        self.window.find_element(
            '-IN-TITLE-').update(self.selected_module.title)
        self.window.find_element(
            '-PROGRAM-').update(self.selected_module.programs)
        self.window.find_element(
            '-YEAR-').update(self.selected_module.year)
        self.window.find_element(
            '-TERM-').update(self.selected_module.term)
        self.window.find_element(
            '-OPTIONAL-').update(self.selected_module.optional)

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if event == 'Save':
                self.save(values)

            if event == 'Delete':
                self.delete()

            if event == '-LIST-MODULES-':
                self.set_selected_module(values)

            if event in (sg.WIN_CLOSED, '-CLOSE-'):
                break

        self.window.close()
