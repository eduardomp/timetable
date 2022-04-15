import PySimpleGUI as sg


def generate_row(row_num, row_data):
    return [
        sg.Text("         "),
        sg.Button('', size=(12, 4), key=(
            f"-cell-{row_num}-1-"), pad=(0, 0)),
        sg.Button('', size=(12, 4), key=(
            f"-cell-{row_num}-2-"), pad=(0, 0)),
        sg.Button('', size=(12, 4), key=(
            f"-cell-{row_num}-3-"), pad=(0, 0)),
        sg.Button('', size=(12, 4), key=(
            f"-cell-{row_num}-4-"), pad=(0, 0)),
        sg.Button('', size=(12, 4), key=(
            f"-cell-{row_num}-5-"), pad=(0, 0))
    ]


def generate_rows():
    rows = [[sg.Text("Timetable")]]
    for i in range(0, 24):
        rows.append([sg.Text(f"{i}:00"), sg.HSeparator()]),
        rows.append(generate_row(i, []))
    return rows


sg.theme('Material2')

top_bar = [
    sg.Text('Login'),
    sg.Input(key='-LOGIN-', size=(20, 1)),
    sg.Text('Password'),
    sg.Input(key='-PASS-', size=(20, 1), password_char='*'),
    sg.Button('Login', key='-LOGIN-BUTTON-')
]

column_left = [
    [sg.Button('Calendar')],
    [sg.Button('Calendar 2')],
    [sg.Button('Calendar 3')]
]

column_right = generate_rows()

layout = [[
    [top_bar, sg.HSeparator()],
    sg.Column(column_left, expand_y=True, expand_x=True, size=(100, 680)),
    sg.VSeparator(),
    sg.Column(column_right,
              expand_y=True,
              expand_x=True,
              scrollable=True,
              vertical_scroll_only=True,
              size=(890, 680))
]]

window = sg.Window('Timetable', layout, size=(1000, 700))

while True:
    event, values = window.read()

    print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
