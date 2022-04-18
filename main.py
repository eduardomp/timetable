import PySimpleGUI as sg


zero_pad = ((0, 0), (0, 0))


class ProgramWindow():

    def __init__(self):
        pass

    def render(self):
        self.layout = [
            [sg.Text('Type'), sg.Combo(['Undergraduate', 'Postgraduate'],
                                       key='--PROGRAM-TYPE-', size=(20, 1)),
             sg.Text('Title'), sg.Input(
                key='-IN-PROGRAM-TITLE-', size=(20, 1))],
        ]

        self.window = sg.Window('Programs', self.layout, size=(400, 450))

        while True:
            event, values = self.window.read()

            print(event, values)

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

        self.window.close()


class ModulesWindow():

    def __init__(self):
        self.programs = ['Select']
        self.year = ['Select', '1', '2', '3']
        self.term = ['Select', '1', '2']
        self.optional = True
        self.title = ''
        pass

    def render(self):
        self.layout = [
            [sg.Text('Program'), sg.Combo(self.programs,
                                          key='-PROGRAM-', size=(20, 1))],
            [sg.Text('Year'), sg.Combo(self.year, key='-YEAR-', size=(20, 1))],
            [sg.Text('Term'), sg.Combo(self.term, key='-TERM-', size=(20, 1))],
            [sg.Text('Optional'), sg.Checkbox('', key='-OPTIONAL-')],
            [sg.Text('Title'), sg.Input(key='-IN-TITLE-', size=(20, 1))],
            [sg.Button('Add'), sg.Button('Exit')]
        ]

        self.window = sg.Window('Modules', self.layout, size=(400, 450))

        while True:
            event, values = self.window.read()

            print(event, values)

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

        self.window.close()


class MainWindow():

    def generate_row(self, row_num, row_data):
        return [
            sg.Text("         "),
            sg.VSeparator(pad=zero_pad),
            sg.Button('', button_color='#ffffff', size=(12, 4), key=(
                f"-cell-{row_num}-1-"), pad=zero_pad),
            sg.VSeparator(pad=zero_pad),
            sg.Button('', button_color='#ffffff', size=(12, 4), key=(
                f"-cell-{row_num}-2-"), pad=zero_pad),
            sg.VSeparator(pad=zero_pad),
            sg.Button('', button_color='#ffffff', size=(12, 4), key=(
                f"-cell-{row_num}-3-"), pad=zero_pad),
            sg.VSeparator(pad=zero_pad),
            sg.Button('', button_color='#ffffff', size=(12, 4), key=(
                f"-cell-{row_num}-4-"), pad=zero_pad),
            sg.VSeparator(pad=zero_pad),
            sg.Button('', button_color='#ffffff', size=(12, 4), key=(
                f"-cell-{row_num}-5-"), pad=zero_pad),
            sg.VSeparator(pad=zero_pad)

        ]

    def generate_rows(self):
        rows = [
            [sg.Text("Timetable"), sg.Text("", key="-program-choosed-")],
            [
                sg.Text("Monday", pad=((100, 70), (10, 2))),
                sg.Text("Tuesday", pad=((50, 50), (10, 2))),
                sg.Text("Wednesday", pad=((70, 60), (10, 2))),
                sg.Text("Thursday", pad=((60, 60), (10, 2))),
                sg.Text("Friday", pad=((60, 60), (10, 2)))],
        ]
        for i in range(9, 21):
            rows.append([sg.Text(f"{i}:00", pad=((0, 10), (0, 0))),
                        sg.HSeparator(pad=zero_pad)]),
            rows.append(self.generate_row(i, []))

        rows.append([sg.Text(f"21:00", pad=((0, 10), (0, 0))),
                    sg.HSeparator(pad=zero_pad)])

        return rows

    def __init__(self):

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

        self.column_right = self.generate_rows()

        self.layout = [[
            [self.top_bar, sg.HSeparator()],
            sg.Column(self.column_left, expand_y=True,
                      expand_x=True, size=(100, 680)),
            sg.VSeparator(),
            sg.Column(self.column_right,
                      expand_y=True,
                      expand_x=True,
                      pad=zero_pad,
                      scrollable=True,
                      vertical_scroll_only=True,
                      size=(850, 690))
        ]]

        self.programWindow = ProgramWindow()

        self.modulesWindow = ModulesWindow()

        self.window = sg.Window('Timetable', self.layout, size=(1200, 700))

    def render(self):

        while True:
            event, values = self.window.read()

            print(event, values)

            if event == "-PROGRAMS-":
                self.programWindow.render()

            if event == "-MODULES-":
                self.modulesWindow.render()

            if event in (sg.WIN_CLOSED, 'Exit'):
                break

        self.window.close()


if __name__ == '__main__':
    main_window = MainWindow()
    main_window.render()
