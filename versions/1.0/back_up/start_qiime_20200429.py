import PySimpleGUI as sg
import os

sg.theme('LightBlue2')   # Add a touch of color sg.theme('DarkAmber') 
# All the stuff inside your window.
layout = [  [sg.Text('Step 1: Open 2 sessions within MobaXterm')],
            [sg.Text('Step 2: Check/change filenames; example given')],
            [sg.Text('             1) PVEE_01_20200226@metadata.txt')],
            [sg.Text('             2) PVEE_01_20200226@*_R1_*.fastq.gz')],
            [sg.Text('             3) PVEE_01_20200226@*_R2_*.fastq.gz')],
            [sg.Text('Step 3: Check qiime settings')],            
            [sg.Text('Step 4: Create a subset for a testrun (default = 10000')],
            [sg.Text('Step 5: Create bash-scripts')],
            [sg.Text('Step 6: Run subset bash-script 01 in other session (sbatch *kseq_*.sh)')],
            [sg.Text('Step 7: Optimize qiime settings and create bash-scripts')],
            [sg.Text('Step 8: Run bash-script full 01 in the other session (sbatch *01*.sh)')],
            [sg.Text('Step 9: Run bash-script full 02 in the other session (sbatch *02*.sh)')],
            [sg.Button('qiime settings'), sg.Button('Create subset'), sg.Button('Create bash'), sg.Button('Close window')] ]

# Create the Window
window = sg.Window('Start Qiime', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (True, 'qiime settings'):   # if user closes window or clicks cancel
        os.system("gedit " + "/export2/home/microlab/microlab/python_scripts/qiime/qiime_settings.ini")
    if event in (True, 'Create subset'):   # if user closes window or clicks cancel
        os.system("python3.7 " + "/export2/home/microlab/microlab/python_scripts/qiime/qiime2_step01_subsampling_quality_check.py")
    if event in (True, 'Create bash'):   # if user closes window or clicks cancel
        os.system("python3.7 " + "/export2/home/microlab/microlab/python_scripts/qiime/qiime2_step02_automatic_script_bashcmd.py")
    if event in (True, 'Close window'):   # if user closes window or clicks cancel
        exit()             #window.close()
    else:
        continue#print('You entered ', values[0])

#window.close()

#RBAR_04_20200213@metadata.txt
#RBAR_04_20200213@*_R1_*.fastq.gz
#RBAR_04_20200213@*_R2_*.fastq.gz

#layout = [  [sg.Text('Some text on Row 1')],
#           [sg.Text('Enter something on Row 2'), sg.InputText()],
#            [sg.Button('Ok'), sg.Button('Program')] ]
