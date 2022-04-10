import PySimpleGUI as sg

sg.theme('Material2')

top_bar = [
    sg.Text('Login'),
    sg.Input(key='-LOGIN-', size=(20, 1)),
    sg.Text('Password'),
    sg.Input(key='-PASS-', size=(20, 1)),
]

column_left = [
    [sg.Button('Calendar')],
    [sg.Button('Calendar 2')],
    [sg.Button('Calendar 3')]
]

column_right = [
    [sg.Text("Timetable")]
]

layout = [[
    [top_bar, sg.HSeparator()],
    sg.Column(column_left),
    sg.VSeparator(),
    sg.Column(column_right)
]]

window = sg.Window('Timetable', layout, size=(1000, 700))

while True:
    event, values = window.read()

    print(event, values)

    if event in (sg.WIN_CLOSED, 'Exit'):
        break

window.close()
