import PySimpleGUI as sg
import serial
from pandas import DataFrame
from datetime import datetime
import time
TEXT_WIDTH = 20

#start of window 1 layout
frame_layout1 = [
    [sg.Combo(["Form", "Set", "Reset"], key='-FIRST_CHOICE-', enable_events=True)],
    [sg.Text('Time (uS):           ', key='-TIME_UNIT1-'), sg.InputText('', size=(TEXT_WIDTH,10), key='-TIME1-', enable_events=True)],
    [sg.Text('Voltage (V):         '), sg.InputText('', size=(TEXT_WIDTH,10), key='-VOLTAGE1-', enable_events=True)],
    [sg.Text('Blank Period (uS):'), sg.InputText('', size=(TEXT_WIDTH,10), key='-BLANK1-', enable_events=True)]
]

frame_layout2 = [
    [sg.Combo(["Read", "Stop"], key='-SECOND_CHOICE-', enable_events=True)],
    [sg.Text('Time (uS):           '), sg.InputText('', size=(TEXT_WIDTH,10), key='-TIME2-', enable_events=True)],
    [sg.Text('Voltage (V):         '), sg.InputText('', size=(TEXT_WIDTH,10), key='-VOLTAGE2-', enable_events=True)],
    [sg.Text('Blank Period (uS):'), sg.InputText('', size=(TEXT_WIDTH,10), key='-BLANK2-', enable_events=True)]
]

frame_layout3 = [
    [sg.Combo(["Set", "Reset"], key='-THIRD_CHOICE-', enable_events=True)],
    [sg.Text('Time (uS):           ', key='-TIME_UNIT3-'), sg.InputText('', size=(TEXT_WIDTH,10), key='-TIME3-', enable_events=True)],
    [sg.Text('Voltage (V):         '), sg.InputText('', size=(TEXT_WIDTH,10), key='-VOLTAGE3-', enable_events=True)],
    [sg.Text('Blank Period (uS):'), sg.InputText('', size=(TEXT_WIDTH,10), key='-BLANK3-', enable_events=True)]
]

frame_layout4 = [
    [sg.Combo(["Read", "Stop"], key='-FOURTH_CHOICE-', enable_events=True)],
    [sg.Text('Time (uS):           '), sg.InputText('', size=(TEXT_WIDTH,10), key='-TIME4-', enable_events=True)],
    [sg.Text('Voltage (V):         '), sg.InputText('', size=(TEXT_WIDTH,10), key='-VOLTAGE4-', enable_events=True)],
    [sg.Text('Blank Period (uS):'), sg.InputText('', size=(TEXT_WIDTH,10), key='-BLANK4-', enable_events=True)]
]

layout = [
    [sg.Frame('First Stage', frame_layout1), sg.VSeparator(), sg.Frame('Second Stage', frame_layout2)],
    [sg.Frame('Third Stage', frame_layout3), sg.VSeparator(), sg.Frame('Fourth Stage', frame_layout4)],
    [sg.Text('_'*75)],
    [sg.Text('Row: '), sg.Combo(['1','2','3','4','5','6','7','8'], key='-ROW-'), sg.Text('Column: '), sg.Combo(['1','2','3','4','5','6','7','8'], key='-COLUMN-')],
    [sg.Text('Number of Repetitions: '), sg.InputText('', size=(TEXT_WIDTH, 10), key='-REPETITIONS-')],
    [sg.Submit(key='Submit')]
]
#end of window 1 layout

#start of menu layout
menu_layout = [
    [sg.Text("Select your option for the desired protocol: ")],
    [sg.Combo(['SINGLE DEVICE PROGRAMMING', 'SINGLE COLUMN PROGRAMMING'], key='-PROTOCOL-', size=(150,10))],
    [sg.Submit(key='Submit1')]
]
#end of menu layout

#start of window 2 layout
set_reset1 = [
    [sg.Text('Time (uS):           '), sg.InputText('', size=(TEXT_WIDTH,10), key='-SET_TIME-', enable_events=True)],
    [sg.Text('Set Voltage (V):   '), sg.InputText('', size=(TEXT_WIDTH,10), key='-SET_VOLTAGE-', enable_events=True)],
    [sg.Text('Reset Voltage (V):'), sg.InputText('', size=(TEXT_WIDTH,10), key='-RESET_VOLTAGE-', enable_events=True)],
    [sg.Text('Blank Period (uS):'), sg.InputText('', size=(TEXT_WIDTH,10), key='-SET_BLANK-', enable_events=True)]
]

read1 = [
    [sg.Text('Time (uS):           '), sg.InputText('', size=(TEXT_WIDTH,10), key='-READ_TIME-', enable_events=True)],
    [sg.Text('Voltage (V):         '), sg.InputText('', size=(TEXT_WIDTH,10), key='-READ_VOLTAGE-', enable_events=True)],
    [sg.Text('Blank Period (uS):'), sg.InputText('', size=(TEXT_WIDTH,10), key='-READ_BLANK-', enable_events=True)]
]

layout2 = [
    [sg.Frame('SET/RESET', set_reset1), sg.VSeparator(), sg.Frame('READ', read1)],
    [sg.Text('_'*75)],
    [
        sg.Text('Row 1-8 Bit Data: '), sg.Combo(['0','1'], key='Row1'), sg.Combo(['0','1'], key='Row2'),
        sg.Combo(['0','1'], key='Row3'), sg.Combo(['0','1'], key='Row4'), sg.Combo(['0','1'], key='Row5'),
        sg.Combo(['0','1'], key='Row6'), sg.Combo(['0','1'], key='Row7'), sg.Combo(['0','1'], key='Row8')
    ],
    [sg.Text('Column: '), sg.Combo(['1','2','3','4','5','6','7','8'], key='-COL-'), sg.Text('Row: 0')],
    [sg.Submit(key='Sub')]
]
#end of window 2 layout

#instruction conversion string-to-int
conversion = {
    'Stop': 0,
    'Form': 1,
    'Set': 2,
    'Reset': 3,
    'Read': 4
}

#hexadecimal mappings for -1 to -25
#just used as a reference
negatives = {
    -1: '0xFF',
    -2: '0xFE',
    -3: '0xFD',
    -4: '0xFC',
    -5: '0xFB',
    -6: '0xFA',
    -7: '0xF9',
    -8: '0xF8',
    -9: '0xF7',
    -10:'0xF6',
    -11:'0xF5',
    -12:'0xF4',
    -13:'0xF3',
    -14:'0xF2',
    -15:'0xF1',
    -16:'0xF0',
    -17:'0xEF',
    -18:'0xEE',
    -19:'0xED',
    -20:'0xEC',
    -21:'0xEB',
    -22:'0xEA',
    -23:'0xE9',
    -24:'0xE8',
    -25:'0xE7'
}

"""
This method generates a dictionary with all the necessary information from
window 1, where row!=0.

Parameter values: must be of type dict with all the values from the GUI
Returns dict of information
"""
def generateInfo(values):
    for key in values:
        if(len(values[key])==0):
            values[key]='0'
    information = {
        1: (0 if values['-FIRST_CHOICE-']=='0' else conversion[values['-FIRST_CHOICE-']], int(values['-TIME1-']), int(round(float(values['-VOLTAGE1-'])/0.1)), int(values['-BLANK1-'])),
        2: (0 if values['-SECOND_CHOICE-']=='0' else conversion[values['-SECOND_CHOICE-']],  int(values['-TIME2-']), int(round(float(values['-VOLTAGE2-'])/0.1)), int(values['-BLANK2-'])),
        3: (0 if values['-THIRD_CHOICE-']=='0' else conversion[values['-THIRD_CHOICE-']],  int(values['-TIME3-']), int(round(float(values['-VOLTAGE3-'])/0.1)), int(values['-BLANK3-'])),
        4: (0 if values['-FOURTH_CHOICE-']=='0' else conversion[values['-FOURTH_CHOICE-']],  int(values['-TIME4-']), int(round(float(values['-VOLTAGE4-'])/0.1)), int(values['-BLANK4-'])),
        'Position': (int(values['-ROW-']), int(values['-COLUMN-'])),
        'Reps': int(values['-REPETITIONS-'])
    }
    return information

"""
This method generates a dictionary with all the necessary information from
window 2, where row==0.

Parameter values: must be of type dict with all the values from the GUI
Returns dict of information
"""
def generateInfo2(values):
    information = {
        1: (0 if len(values['-SET_TIME-'])==0 else int(values['-SET_TIME-']), 0 if len(values['-SET_VOLTAGE-'])==0 else int(round(float(values['-SET_VOLTAGE-'])/0.1)), 0 if len(values['-RESET_VOLTAGE-'])==0 else int(round(float(values['-RESET_VOLTAGE-'])/0.1)), 0 if len(values['-SET_BLANK-'])==0 else int(values['-SET_BLANK-'])),
        2: (0 if len(values['-READ_TIME-'])==0 else int(values['-READ_TIME-']), 0 if len(values['-READ_VOLTAGE-'])==0 else int(round(float(values['-READ_VOLTAGE-'])/0.1)), 0 if len(values['-READ_BLANK-'])==0 else int(values['-READ_BLANK-'])),
        'ROW1': int(values['Row1']),
        'ROW2': int(values['Row2']),
        'ROW3': int(values['Row3']),
        'ROW4': int(values['Row4']),
        'ROW5': int(values['Row5']),
        'ROW6': int(values['Row6']),
        'ROW7': int(values['Row7']),
        'ROW8': int(values['Row8']),
        'Column': int(values['-COL-'])
    }
    return information

"""
This is a helper method to assert correct values were inputted for 
each stage of the process.

Parameter data: dict of information
Parameter stage: int for the stage of the process to check
"""
def assertStage(data, stage):
    assert data[stage][1]>=1 and data[stage][1]<=125, "Time inputted in stage " + str(stage) + " was out of the accepted 1-125 range."
    if data[stage][0]==1:
        assert data[stage][2]==33, "Forming Voltage must be 3.3V."
    elif data[stage][0]==4:
        assert data[stage][2]>=-25 and data[stage][2]<=0, "Voltage at stage " + str(stage) + " was out of the accepted -2.5V to 0V range." 
    else:
        assert data[stage][2]>=-25 and data[stage][2]<=25, "Voltage at stage " + str(stage) + " was out of the accepted -2.5V to 2.5V range."
    assert data[stage][3]>=1 and data[stage][3]<=125, "Time inputted in stage " + str(stage) + " for the blank period was out of the accepted 1-125 range."

"""
Asserts the inputted values were in the correct range.
(Window 1)

Parameter data: dict of information
Returns an array representations of the data in the correct byte order
"""
def assertRanges(data):
    assert type(data)==dict, "There was an incorrectly inputted value."
    array = [128]

    #First stage assertions
    assert data[1][0] in [1, 2, 3], "Stage 1 was not form, set, or reset."
    assertStage(data, 1)
    for i in range(4):
        append = (data[1][i])
        if(data[1][i]<0):
                append = 255 + data[1][i]
        array.append(append)

    #Second stage assertions
    if(data[2][0]==0):
        for i in range(4):
            array.append(0)
    else:
        assert data[2][0] in [0, 4], "Stage 2 was not read or stop."
        assertStage(data, 2)
        for i in range(4):
            append = (data[2][i])
            if(data[2][i]<0):
                append = 255 + data[2][i]
            array.append(append)

    #Third stage assertions
    if(data[3][0]==0):
        for i in range(4):
            array.append(0)
    else:
        assert data[3][0] in [2, 3], "Stage 3 was not set or reset."
        assertStage(data, 3)
        for i in range(4):
            append = (data[3][i])
            if(data[3][i]<0):
                append = 255 + data[3][i]
            array.append(append)

    #Fourth stage assertions
    if(data[4][0]==0):
        for i in range(4):
            array.append(0)
    else:
        assert data[4][0] in [0, 4], "Stage 4 was not read or stop."
        assertStage(data, 4)
        for i in range(4):
            append = (data[4][i])
            if(data[4][i]<0):
                append = 255 + data[4][i]
            array.append(append)

    #Cycles assertion
    if(data['Reps']==0):
        data['Reps']=1
    assert data['Reps']>=1 and data['Reps']<=125, "Repetitions were not within the accepted range of 1-125."
    append = (data['Reps'])
    array.append(append)

    #Position assertions
    assert data['Position'][0]>=1 and data['Position'][0]<=8, "Row was not in 1-8."
    assert data['Position'][1]>=1 and data['Position'][1]<=8, "Column was not in 1-8."
    append1 = (data['Position'][1])
    append2 = (data['Position'][0])
    array.append(append1)
    array.append(append2)
    array.append(129)

    return array

"""
Asserts the inputted values were in the correct range.
(Window 2)

Parameter data: dict of information
Returns an array representations of the data in the correct byte order
"""
def assertRanges2(data):
    array = [128]
    assert type(data)==dict, "There was an incorrectly inputted value."
    
    assert data[1][0]>=1 and data[1][0]<=125, "Set/Reset time was not in the accepted range."
    assert data[1][1]>=-25 and data[1][1]<=25, "Set voltage was not in the accepted range."
    assert data[1][2]>=-25 and data[1][2]<=25, "Reset voltage was not in the accepted range."
    assert data[1][3]>=1 and data[1][3]<=125, "Set/Reset blank period time was not in the accepted range."

    for i in range(4):
        append = (data[1][i])
        if(data[1][i]<0):
                append = 255 + data[1][i]
        array.append(append)

    assert data[2][0]>=1 and data[2][0]<=125 or data[2][0]==0, "Read time was not in the accepted range."
    assert data[2][1]>=-25 and data[2][1]<=0 or data[2][1]==0, "Read voltage was not in the accepted range."
    assert data[2][2]>=1 and data[2][2]<=125 or data[2][2]==0, "Read blank period time was not in the accepted range."

    for i in range(3):
        append = (data[2][i])
        if(data[2][i]<0):
                append = 255 + data[2][i]
        array.append(append)

    for i in range(1,9):
        string = 'ROW'+str(i)
        assert data[string] in [0,1], "Bit data at row " + str(i) + " was not 0 or 1."
        append = (data[string])
        array.append(append)

    array.append(0)
    array.append(0)

    assert data['Column']>=1 and data['Column']<=8, "Column was not 1-8."
    append = (data['Column'])
    array.append(append)

    array.append(0)
    array.append(129)

    return array
    
#creates the first menu to select the desired protocol to be run,
#which opens a new GUI for that protocol.
protocol = ''
first_menu = sg.Window("Protocol Selection", menu_layout, size=(300,100))
while True:
    event1, values1 = first_menu.read()
    if event1 == "Exit" or event1 == sg.WIN_CLOSED:
        break
    if event1 == 'Submit1':
        if values1['-PROTOCOL-']=='SINGLE COLUMN PROGRAMMING':
            protocol = 'Row=0'
        elif values1['-PROTOCOL-']=='SINGLE DEVICE PROGRAMMING':
            protocol = '1<=Row<=8'
        break
first_menu.close()

"""
This method retrieves the resistance values being thrown out to serial when the program is run.
It saves the data to an excel file under the header "Resistance Values."

Parameter numReads: number of times a read cycle occurs
"""
def retrieveData(numReads):
    listData = []
    for i in range(numReads*2+3):
        data = ser.readline().decode('ascii')
        print(data)
        if data:
            listData.append(data)
    df = DataFrame({'Resistance Values':listData})
    print(df)
    
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    current_date = str(datetime.date.today().month) + '_' + str(datetime.date.today().day) + '_' + str(datetime.date.today().year)
    df.to_excel(current_date+'_Resistances_'+current_time+'.xlsx',sheet_name='sheet1', index=False)

"""
This method retrieves the resistance values being thrown out to serial when the program is run.
It saves the data to an excel file under the header "Resistance Values."

Parameter numReads: number of times a read cycle occurs
"""
def retrieveData2(numReads):
    listData = []
    for i in range(8*2+2):
        data = ser.readline().decode('ascii')
        print(data)
        if data:
            listData.append(data)
    df = DataFrame({'Resistance Values':listData})
    print(df)
    
    now = datetime.now()
    current_time = now.strftime("%H_%M_%S")
    current_date = str(datetime.date.today().month) + '_' + str(datetime.date.today().day) + '_' + str(datetime.date.today().year)
    df.to_excel(current_date+'_Resistances_'+current_time+'.xlsx',sheet_name='sheet1', index=False)


"""
Opens up window 1, which is when the row selected is between 1-8.
Returns the resulting string of hexadecimal values that were inputted.
"""
def window1():
    window = sg.Window("Single Device Programming", layout, size=(600,400), finalize=True)
    data = ''
    resultArray = ''
    window['-SECOND_CHOICE-'].update('Read')
    window['-FOURTH_CHOICE-'].update('Read')
    while True:
        resultArray = ''
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == "-FIRST_CHOICE-":
            choice = values["-FIRST_CHOICE-"]
            if choice == 'Form':
                window['-TIME1-'].update(1)
                window['-VOLTAGE1-'].update(3.3)
                window['-BLANK1-'].update('')
                window['-TIME_UNIT1-'].update('Time (mS):           ')
            else:
                window['-TIME1-'].update('')
                window['-VOLTAGE1-'].update('')
                window['-BLANK1-'].update('')
                window['-TIME_UNIT1-'].update('Time (uS):           ')
        if event == 'Submit':
            try:
                data = generateInfo(values)
            except:
                print('One or more field was missing or incorrectly entered.')
            resultArray= assertRanges(data)
            print(resultArray)
            if(len(resultArray)>0):
                numReads = 0
                if(data[2][0]==4):
                    numReads=numReads+1
                if(data[4][0]==4):
                    numReads=numReads+1
                numReads = numReads*data['Reps']
                #Send serial data and then retrieve resistances
                ser.write(bytearray(resultArray))
                time.sleep(1)
                retrieveData(numReads)
    window.close()
    return resultArray

"""
Opens up window 2, which is when row=0 is selected.
Returns the resulting string of hexadecimal values that were inputted.  
"""
def window2():
    window = sg.Window("Single Column Programming", layout2, size=(600,300), finalize=True)
    data = ''
    resultArray = ''
    for i in range(1,9):
        window['Row'+str(i)].update(1)
    while True:
        event, values = window.read()
        if event == "Exit" or event == sg.WIN_CLOSED:
            break
        if event == 'Sub':
            try:
                data = generateInfo2(values)
            except:
                print('One or more field was missing.')
            resultArray = assertRanges2(data)
            print(resultArray)
            if(len(resultArray)>0):
                numReads = 1
                #Send serial data and then retrieve resistances
                ser.write(bytearray(resultArray))
                time.sleep(1)
                retrieveData2(numReads)
    window.close()
    return resultArray

ser = serial.Serial('COM9',baudrate=115200,bytesize=8, parity = serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
ser.timeout=.5

#Code below here runs the program
opened = ''
if protocol == '1<=Row<=8':
    opened = window1()
    print(opened)
elif protocol == 'Row=0':
    opened = window2()
    print(opened)
else:
    print('Invalid protocol')

ser.close()

"""
if(len(opened)>0):
    #Open serial port and send "opened" variable to the microcontroller
    ser = serial.Serial('COM9',baudrate=115200,bytesize=8, parity = serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE)
    ser.timeout=.5
    ser.write(bytearray(opened))
    ser.close()
"""



