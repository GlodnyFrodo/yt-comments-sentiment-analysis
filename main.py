import PySimpleGUI as sg
from sentiment_analysis_comments_visualization import visual_analysis
from comments_scraper import *

# Main application window
layout = [[sg.Text('Podaj link do filmu na YouTube:'), sg.Input(key='-URL-')],
          [sg.Text('Podaj nazwę pliku do zapisu komentarzy:'), sg.Input(key='-FILENAME-'), sg.Button('Wybierz')],
          [sg.Button('Pobierz komentarze'), sg.Button('Wyjdź')]]

window = sg.Window('Analiza sentymentu komentarzy na YouTube', layout)


# Event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Wyjdź':
        break
    elif event == 'Wybierz':
        filename = sg.popup_get_file('Wybierz plik do zapisu komentarzy', save_as=True,
                                     file_types=(('JSON files', '*.json'),))
        window['-FILENAME-'].update(filename)
    elif event == 'Pobierz komentarze':
        url = values['-URL-']
        filename = values['-FILENAME-']
        if not filename.endswith('.json'):
            filename += '.json'

        get_comments(url, filename)
        sg.popup('Komentarze zostały pobrane i zapisane do pliku JSON.')

        # Run vizualization
        visual_analysis(filename)

window.close()
