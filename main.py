
import PySimpleGUI as sg
import textwrap
import model

ZERO_PAD = ((0, 0), (0, 0))


class ProgramWindow():

    def __init__(self):

        self.programs = self.get_all()
        self.selected_program = None

        self.layout = [
            [sg.Text('Type', size=(10, 1), justification='right'), sg.Combo(['Undergraduate', 'Postgraduate'],
                                                                            key='--PROGRAM-TYPE-', size=(30, 1))],
            [sg.Text('Title', size=(10, 1), justification='right'), sg.Input(
                key='-IN-PROGRAM-TITLE-', size=(30, 1))],
            [sg.Button('Save', size=(10, 1), pad=(10, None)), sg.Button('Delete', size=(
                10, 1)), sg.Button('Close', key="-CLOSE-", size=(10, 1))],
            [sg.HSeparator(pad=ZERO_PAD)],
            [sg.Listbox(values=self.programs, select_mode='extended',
                        key='-LIST-', size=(120, 20), enable_events=True)],
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


class ModulesWindow():

    def __init__(self):
        self.list = model.Programs.get_all()
        self.programs = list(
            map(lambda p: f'{p.id} - {p.title} ({p.type})', self.list))
        self.modules = self.get_all()
        self.selected_module = None

        self.years = ['1', '2', '3']
        self.terms = ['1', '2']

        self.layout = [
            [sg.Text('Title', size=(20, 1), justification='right'),
             sg.Input(key='-IN-TITLE-', size=(20, 1))],
            [sg.Text('Program', size=(20, 1), justification='right'), sg.Combo(self.programs,
                                                                               key='-PROGRAM-', size=(20, 1))],
            [sg.Text('Year', size=(20, 1), justification='right'),
             sg.Combo(self.years, key='-YEAR-', size=(20, 1))],
            [sg.Text('Term', size=(20, 1), justification='right'),
             sg.Combo(self.terms, key='-TERM-', size=(20, 1))],
            [sg.Text('Optional', size=(20, 1), justification='right'),
             sg.Checkbox('', key='-OPTIONAL-')],
            [sg.Button('Save', size=(10, 1), pad=(10, None)), sg.Button('Delete', size=(
                10, 1)), sg.Button('Close', key="-CLOSE-", size=(10, 1))],
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
                self.selected_module.program = values['-PROGRAM-']
                self.selected_module.year = values['-YEAR-']
                self.selected_module.term = values['-TERM-']
                self.selected_module.optional = values['-OPTIONAL-']

                model.Modules.update(self.selected_module)

            else:
                module = model.Modules(
                    title=values['-IN-TITLE-'], program=values['-PROGRAM-'], year=values['-YEAR-'], term=values['-TERM-'], optional=values['-OPTIONAL-'])

                exists = [module for module in self.modules if module.title ==
                          values['-IN-TITLE-']]

                if len(exists) == 0:
                    model.Modules.insert(module)

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
            '-PROGRAM-').update(self.selected_module.program)
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
            [sg.Button('Add', disabled=True, size=(10, 1)), sg.Button(
                'Close', key="-CLOSE-", size=(20, 1))],
        ]

        self.window = sg.Window('Activities', self.layout, size=(300, 150))

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


class MainWindow():

    def generate_cell(self, title=None, time=None):
        if title == None or time == None:
            return [[sg.Text('', size=(20, None))]]

        return [
            [sg.Text('\n'.join(textwrap.wrap(
                f'{title}', 20)), size=(20, None))],
            [sg.Text(f'{time}')],
            [sg.Button('EDIT',
                       size=(10, 1), pad=(0, 0), key='-EDIT-'),
             sg.Button('DELETE',
                       size=(10, 1), pad=(0, 0), key='-DELETE-')]
        ]

    def generate_row(self, row_num, row_data):

        mock_text = '''Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam urna tortor, suscipit in ullamcorper ut, dapibus in felis. Integer ac augue risus. Pra.'''

        return [
            sg.Column([], size=(30, None)),
            sg.VSeparator(pad=(0, 0)),

            sg.Column(self.generate_cell(mock_text,
                      '09:00AM - 10:00AM'), size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(self.generate_cell(), size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column([
                [sg.Text('\n'.join(textwrap.wrap(
                    f'{mock_text}', 20)), size=(20, None))],
                [sg.Text('09:00AM - 10:00AM')]
            ], size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column([
                [sg.Text('\n'.join(textwrap.wrap(
                    f'{mock_text}', 20)), size=(20, None))],
                [sg.Text('09:00AM - 10:00AM')]
            ], size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column([
                [sg.Text('\n'.join(textwrap.wrap(
                    f'{mock_text}', 20)), size=(20, None))],
                [sg.Text('09:00AM - 10:00AM')]
            ], size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD)

        ]

    def generate_rows(self, parent_layout):

        for i in range(9, 21):
            parent_layout.append([sg.Text(f'{i}:00', pad=((0, 10), (0, 0))),
                                  sg.HSeparator(pad=ZERO_PAD)]),
            parent_layout.append(self.generate_row(i, []))

        parent_layout.append([sg.Text(f'21:00', pad=((0, 10), (0, 0))),
                              sg.HSeparator(pad=ZERO_PAD)])

        return parent_layout

    def generate_table(self, parent_layout, year, term):

        title_font = ('Helvetica bold', 20)
        subtitle_font = ('Helvetica bold', 15)
        header_font = ('Helvetica bold', 12)

        title = [sg.Text(f'Program: {self.selected_program.title}', font=title_font,
                         justification='center')]
        subtitle = [
            sg.Text(f'Year: {year}', font=subtitle_font),
            sg.Text(f'Term: {term}', font=subtitle_font)
        ]

        header = [
            sg.Text('Monday', font=header_font, pad=((100, 70), (10, 2))),
            sg.Text('Tuesday', font=header_font, pad=((50, 50), (10, 2))),
            sg.Text('Wednesday', font=header_font,
                    pad=((50, 60), (10, 2))),
            sg.Text('Thursday', font=header_font, pad=((50, 60), (10, 2))),
            sg.Text('Friday', font=header_font, pad=((50, 60), (10, 2)))
        ]

        parent_layout.append(title)
        parent_layout.append(subtitle)
        parent_layout.append(header)

        parent_layout = self.generate_rows(parent_layout)

        return parent_layout

    def generate_tables(self, parent_layout):
        print(f'self.selected_program ====== {self.selected_program}')
        if self.selected_program:

            if self.selected_program.type == 'Undergraduate':
                print("Undergraduate")
                parent_layout = self.generate_table(parent_layout, 1, 1)
                parent_layout = self.generate_table(parent_layout, 1, 2)
                parent_layout = self.generate_table(parent_layout, 2, 1)
                parent_layout = self.generate_table(parent_layout, 2, 2)
                parent_layout = self.generate_table(parent_layout, 3, 1)
                parent_layout = self.generate_table(parent_layout, 3, 2)

            if self.selected_program.type == 'Postgraduate':
                parent_layout = self.generate_table(parent_layout, 1, 1)
                parent_layout = self.generate_table(parent_layout, 2, 1)

        return parent_layout

    def generate_right_column(self):
        print("GENERATING RIGHT COLUMN")
        layout = []

        combo_programs = [
            sg.Text('Program selected: ', justification='center'),
            sg.Combo(self.programs, key='-SELECTED-PROGRAM-', enable_events=True, size=(30, 1))]

        layout.append(combo_programs)

        layout = self.generate_tables(layout)

        return layout

    def __init__(self):

        self.programs = model.Programs.get_all()
        self.selected_program = self.programs[0]

        sg.theme('Material2')

        self.top_bar = [
            sg.Text('Login'),
            sg.Input(key='-LOGIN-', size=(20, 1)),
            sg.Text('Password'),
            sg.Input(key='-PASS-', size=(20, 1), password_char='*'),
            sg.Button('Login', key='-LOGIN-', size=(20, 1))
        ]

        self.column_left = [
            [sg.Button('Programs', key='-PROGRAMS-', size=(20, 1))],
            [sg.Button('Modules', key='-MODULES-', size=(20, 1))],
            [sg.Button('Activities', key='-ACTIVITIES-', size=(20, 1))],
        ]

        self.column_right = self.generate_right_column()

        self.layout = [[
            [self.top_bar, sg.HSeparator()],
            sg.Column(self.column_left, expand_y=True,
                      expand_x=True, size=(100, 680)),
            sg.VSeparator(),
            sg.Column(self.column_right,
                      expand_y=True,
                      expand_x=True,
                      pad=ZERO_PAD,
                      scrollable=True,
                      vertical_scroll_only=True,
                      size=(850, 690),
                      key='-RIGHT-COLUMN-')
        ]]

        self.window = sg.Window('Timetable', self.layout, size=(1200, 700))

    def set_selected_program(self, values):
        self.selected_program = values['-SELECTED-PROGRAM-']

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if event == '-PROGRAMS-':
                ProgramWindow().render()

            if event == '-MODULES-':
                ModulesWindow().render()

            if event == '-ACTIVITIES-':
                ActivitiesWindow().render()

            if event == '-SELECTED-PROGRAM-':
                self.set_selected_program(values)

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

        self.window.close()


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.render()
