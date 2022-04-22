import PySimpleGUI as sg
import model

ZERO_PAD = ((0, 0), (0, 0))


class ProgramWindow():

    def __init__(self):

        self.programs = self.get_all()
        self.selected_program = None

        self.layout = [
            [sg.Text('Type', size=(10, 1), justification='right'), sg.Combo(['Undergraduate', 'Postgraduate'],
                                                                            key='--PROGRAM-TYPE-', size=(35, 1))],
            [sg.Text('Title', size=(10, 1), justification='right'), sg.Input(
                key='-IN-PROGRAM-TITLE-', size=(35, 1))],
            [sg.Button('Save', size=(45, 1))],
            [sg.Button('Delete', size=(45, 1))],
            [sg.Button('Close', key="-CLOSE-", size=(45, 1))],
            [sg.HSeparator(pad=ZERO_PAD)],
            [sg.Listbox(values=self.programs, select_mode='extended',
                        key='-LIST-', size=(50, 20), enable_events=True)],
        ]

        self.window = sg.Window('Programs', self.layout, size=(300, 350))

    def reset(self):
        self.selected_program = None
        self.window.find_element('-IN-PROGRAM-TITLE-').update('')
        self.window.find_element('--PROGRAM-TYPE-').update('')
        self.programs = self.get_all()
        self.window.find_element('-LIST-').update(self.programs)

    def save(self, values):
        if values['-IN-PROGRAM-TITLE-'] and values['--PROGRAM-TYPE-']:

            if self.selected_program:
                self.selected_program.title = values['-IN-PROGRAM-TITLE-']
                self.selected_program.type = values['--PROGRAM-TYPE-']
                model.Programs.update(self.selected_program)

            else:
                program = model.Programs(
                    title=values['-IN-PROGRAM-TITLE-'], type=values['--PROGRAM-TYPE-'])

                exists = [program for program in self.programs if program.title ==
                          values['-IN-PROGRAM-TITLE-']]

                if len(exists) == 0:
                    model.Programs.insert(program)

            self.reset()

    def delete(self):
        if self.selected_program:
            model.Programs.delete(self.selected_program.id)
            self.reset()

    def get_all(self):
        return model.Programs.get_all()

    def set_selected_program(self, values):
        selected = str(values['-LIST-'][0]).split(' - ')
        self.selected_program = [
            program for program in self.programs if program.id == int(selected[0])][0]
        self.window.find_element(
            '-IN-PROGRAM-TITLE-').update(self.selected_program.title)
        self.window.find_element(
            '--PROGRAM-TYPE-').update(self.selected_program.type)

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if event == 'Save':
                self.save(values)

            if event == 'Delete':
                self.delete()

            if event == '-LIST-':
                self.set_selected_program(values)

            if event in (sg.WIN_CLOSED, '-CLOSE-'):
                break

        self.window.close()
