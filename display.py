import PySimpleGUI as sg

sg.theme('Black')
sg.SetOptions(font=("Monaco", 24), element_size=(100,1))

settings_column = [
  [
    sg.Text("BUDGET (£)", relief='flat', pad=(30,0)),
    sg.Slider((5,50), 15, 1, pad=(0,20), size=(18,15), orientation="h", key="budget")
  ],
  [
    sg.Radio("ALL", "radio_1", pad=(35,0), key="all", default=True, text_color='red', enable_events=True), 
    sg.Radio("UNIQUE", "radio_1", pad=(35,0), key="unique", enable_events=True), 
    sg.Radio("NEW", "radio_1", pad=(35,0), key="new", enable_events=True)
  ],
  [
    sg.OptionMenu(
      values=["I'm Feelin' Lucky", " Meals Only", ' Vegetarian'], 
      size=(30, 100), 
      key="option")
  ],
]
button_column = [
  [sg.Button("Generate Order", pad=(30,5), use_ttk_buttons=True, enable_events=True, key='generate')],
  [sg.Button("Reset", pad=(0,5), use_ttk_buttons=True, disabled=True, enable_events=True, key='reset')],
]

layout = [
  [ 
    sg.Column(settings_column),
    sg.VSeperator(),
    sg.Column(button_column, element_justification='center'),
    sg.VSeperator(),
    sg.Image(filename='logo.png',size=(144,144), pad=(15,0))
  ],
  [sg.HorizontalSeparator()],
  [sg.Text("Awaiting Order...", 	size=(17, 1), key='order_text'), sg.Text("", 	size=(45, 1), key='budget_text')],
  [sg.Output(size=(63, 10), echo_stdout_stderr=True, key='output_text')]
  ]

class GUI:
  def __init__(self, menu, func):
    # Create the window
    self.window = sg.Window("Random Order Generator", layout, alpha_channel=.8)
    self.menu = menu
    self.process = func
    self.run()

  def run(self):
    while True:
      event, values = self.window.read()
      if event == sg.WIN_CLOSED:
        break

      if event in ['all', 'unique', 'new']:
        for radio in ['all', 'unique', 'new']:
          self.window[radio].update(text_color="white")
        self.window[event].update(text_color="red")

      if event == 'generate':
        budget = int(values['budget'])
        option = values['option']
        if values['unique']:
          custom = 1
        elif values['new']:
          custom = 2
        else:
          custom = 0
        self.generate(budget,option, custom)
        

      if event == 'reset':
        self.reset()
    
    self.window.close()

  def generate(self, budget, option, custom):
    self.window['generate'].update(disabled=True)
    self.window['reset'].update(disabled=False)
    self.window['order_text'].update('Order:')
    self.window['budget_text'].update(f'Budget: £{budget}\tOption: {option}')
    self.window['output_text'].update('')
    self.process(budget,option, custom)

  def reset(self):
    self.window['generate'].update(disabled=False)
    self.window['reset'].update(disabled=True)
    self.window['order_text'].update('Awaiting Order...')
    self.window['budget_text'].update('')
    self.window['output_text'].update('')

  
