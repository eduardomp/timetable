
import PySimpleGUI as sg
import textwrap
import model

ZERO_PAD = ((0, 0), (0, 0))


class TimetableWindow():

    def __init__(self, selected_program):

        self.programs = model.Programs.get_all()
        self.selected_program = selected_program

        sg.theme('Material2')

        self.tables = self.generate_tables()

        self.layout = [[sg.Column(self.tables,
                                  expand_y=True,
                                  expand_x=True,
                                  pad=ZERO_PAD,
                                  scrollable=True,
                                  vertical_scroll_only=True,
                                  size=(850, 690),
                                  key='-TABLES-')]]

        self.window = sg.Window(
            'Timetable', self.layout, size=(900, 700),)

    def generate_cell(self, year, term, day_of_week, hour):

        activity = model.Activities.get_by_program_year_term(
            self.selected_program, year, term, day_of_week, hour)

        if activity:

            time = f'{activity.start} - {activity.finish}'

            return [
                [sg.Text('\n'.join(textwrap.wrap(
                    f'{activity.title}', 20)), size=(20, None))],
                [sg.Text(f'{time}')],
                [sg.Button('EDIT',
                           size=(10, 1), pad=(0, 0), key='-EDIT-'),
                 sg.Button('DELETE',
                           size=(10, 1), pad=(0, 0), key='-DELETE-')]
            ]

        return [[sg.Text('', size=(20, None))]]

    def generate_row(self, hour, year, term):

        return [
            sg.Column([], size=(30, None)),
            sg.VSeparator(pad=(0, 0)),

            sg.Column(self.generate_cell(year, term, 'Monday',
                      f'{hour}:00'), size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(self.generate_cell(year, term, 'Tuesday',
                      f'{hour}:00'), size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(self.generate_cell(year, term, 'Wednesday',
                      f'{hour}:00'), size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(self.generate_cell(year, term, 'Thursday',
                      f'{hour}:00'), size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(self.generate_cell(year, term, 'Friday',
                      f'{hour}:00'), size=(150, None)),

            sg.VSeparator(pad=ZERO_PAD)

        ]

    def generate_rows(self, parent_layout, year, term):

        for i in range(9, 21):
            parent_layout.append([sg.Text(f'{i}:00', pad=((0, 10), (0, 0))),
                                  sg.HSeparator(pad=ZERO_PAD)]),
            parent_layout.append(self.generate_row(i, year, term))

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

        parent_layout = self.generate_rows(parent_layout, year, term)

        return parent_layout

    def generate_tables(self):

        layout = []

        if self.selected_program:

            if self.selected_program.type == 'Undergraduate':
                print("Undergraduate")
                layout = self.generate_table(layout, 1, 1)
                layout = self.generate_table(layout, 1, 2)
                layout = self.generate_table(layout, 2, 1)
                layout = self.generate_table(layout, 2, 2)
                layout = self.generate_table(layout, 3, 1)
                layout = self.generate_table(layout, 3, 2)

            if self.selected_program.type == 'Postgraduate':
                layout = self.generate_table(layout, 1, 1)
                layout = self.generate_table(layout, 1, 2)

        return layout

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

        self.window.close()
