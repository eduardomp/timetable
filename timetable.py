
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

    def generate_cell(self, activities, hour):

        cell = []

        if activities:
            for activity in activities:

                if hour == int(activity.start):
                    time = f'{activity.start} - {activity.finish}'
                    cell.append([sg.Text('\n'.join(textwrap.wrap(
                        f'{activity.modules.title}', 20)), size=(20, None))])
                    cell.append([sg.Text(f'{time}')])

                if hour > int(activity.start) and hour < int(activity.finish):
                    cell.append([sg.Text('', size=(20, None))])

                if (hour + 1) == int(activity.finish):
                    cell.append([sg.Button('EDIT',
                                           size=(10, 1), pad=(0, 0), key='-EDIT-'),
                                sg.Button('DELETE',
                                          size=(10, 1), pad=(0, 0), key='-DELETE-')])
            return cell

        return [[sg.Text('', size=(20, None))]]

    def generate_row(self, hour, year, term):

        activities = model.Activities.get_by_program_year_term(
            self.selected_program, year, term, hour)

        monday_activity = list(filter(
            lambda a: a.day_of_week == 'Monday', activities))
        tuesday_activity = list(filter(
            lambda a: a.day_of_week == 'Tuesday', activities))
        wednesday_activity = list(filter(
            lambda a: a.day_of_week == 'Wednesday', activities))
        thursday_activity = list(filter(
            lambda a: a.day_of_week == 'Thursday', activities))
        friday_activity = list(filter(
            lambda a: a.day_of_week == 'Friday', activities))

        monday_cell = self.generate_cell(monday_activity, hour)
        tuesday_cell = self.generate_cell(tuesday_activity, hour)
        wednesday_cell = self.generate_cell(wednesday_activity, hour)
        thursday_cell = self.generate_cell(thursday_activity, hour)
        friday_cell = self.generate_cell(friday_activity, hour)

        monday_color = 'blue' if len(monday_activity) > 0 else None
        tuesday_color = 'blue' if len(tuesday_activity) > 0 else None
        wednesday_color = 'blue' if len(wednesday_activity) > 0 else None
        thursday_color = 'blue' if len(thursday_activity) > 0 else None
        friday_color = 'blue' if len(friday_activity) > 0 else None

        return [
            sg.Column([], size=(30, 80), pad=ZERO_PAD),

            sg.VSeparator(pad=(0, 0)),

            sg.Column(monday_cell,
                      size=(150, 80),
                      pad=ZERO_PAD,
                      key=f'-MONDAY-{year}-{term}-{hour}-',
                      background_color=monday_color),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(tuesday_cell,
                      size=(150, 80),
                      pad=ZERO_PAD,
                      key=f'-TUESDAY-{year}-{term}-{hour}-',
                      background_color=tuesday_color),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(wednesday_cell,
                      size=(150, 80),
                      pad=ZERO_PAD,
                      key=f'-WEDNESDAY-{year}-{term}-{hour}-',
                      background_color=wednesday_color),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(thursday_cell,
                      size=(150, 80),
                      pad=ZERO_PAD,
                      key=f'-THURSDAY-{year}-{term}-{hour}-',
                      background_color=thursday_color),

            sg.VSeparator(pad=ZERO_PAD),

            sg.Column(friday_cell,
                      size=(150, 80),
                      pad=ZERO_PAD,
                      key=f'-FRIDAY-{year}-{term}-{hour}-',
                      background_color=friday_color),

            sg.VSeparator(pad=ZERO_PAD)

        ]

    def generate_rows(self, parent_layout, year, term):

        hour_font = ('Helvetica bold', 8)

        for i in range(9, 21):
            parent_layout.append([sg.Text(f'{i}:00', font=hour_font, pad=((0, 10), (0, 0))),
                                  sg.HSeparator(pad=ZERO_PAD)])
            parent_layout.append(self.generate_row(i, year, term))

        parent_layout.append([sg.Text(f'21:00', font=hour_font, pad=((0, 10), (0, 0))),
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
