import PySimpleGUI as sg
import os

sg.theme('LightBlue2')   # Add a touch of color sg.theme('DarkAmber') 
# All the stuff inside your window.
layout = [  [sg.Frame('Qiime2 analysis',[

            [sg.Text('Step 01: Open 2 sessions within MobaXterm with the account "microlab"')],
            [sg.Text('Step 02: Upload the fastq.gz-files and the barcode-file to "/export2/home/microlab/microlab/qiime/illumina_data/"')],            
            [sg.Text('Step 03: Check/rename filenames; Addition of similar identifiers followed by "@" in front of the filenames')],
            [sg.Text('         Syntax = Initials + "_" + Quotenumber + "_" + Gene + "_" + Primerset + "_" + Date(yyyymmdd) + "@". See example below')],
            [sg.Text('         1) CSCH_Q12946_16S_515F926R_20201113@metadata.txt')],
            [sg.Text('         2) CSCH_Q12946_16S_515F926R_20201113@*_R1_*.fastq.gz')],
            [sg.Text('         3) CSCH_Q12946_16S_515F926R_20201113@*_R2_*.fastq.gz')],
            [sg.Text('Step 04: Check qiime settings     '), sg.Button('qiime settings 0')],
            [sg.Text('         Default: U515F: GTGYCAGCMGCCGCGGTAA; BAC926R: CCGYCAATTYMTTTRAGTTT; Find info in *@metadata.txt')],
            [sg.Text('         Default: trim_forward = 5; trim_reverse = 5; length_forward = 240; length_reverse = 200')],
            [sg.Text('         Default: size_subsample = 10000')],

            [sg.Frame('Estimation of length_forward and length_reverse settings; Check quality; Create subset',[
            [sg.Text('Step 4a: Create bash-script   '), sg.Button('Create bash 0')],
            [sg.Text('Step 4b: Run bash-script 00 in the other session (sbatch *identifier*_bash_step_00_qiime_quality.sh)')],
            [sg.Text('Step 4c: Update settings based on output "CHECK_quality_scores_datasets.txt"   '),sg.Button('qiime settings 1')],
            [sg.Text('Step 4d: Continue with step 05')]])],            

            [sg.Text('Step 05: Create bash-scripts      '), sg.Button('Create bash 1')],
            [sg.Text('Step 06: Run bash-script 01 in other session (sbatch *identifier*_bash_step_01_qiime_scripts.sh)')],
            [sg.Text('Step 07: Check qiime settings     '), sg.Button('qiime settings 2')],
            [sg.Text('         Check quality settings (length_forward and length_reverse with "CHECK_quality_scores_datasets.txt")')],
            [sg.Text('         Check efficiency QIIME2 analysis ("CHECK_*identifier*_stats.tsv")')],
            [sg.Text('         If used quality settings or the efficiencies were not ok:')],
            [sg.Text('             --> Repeat from Step 4 with adapted settings!')],
            [sg.Text('         If used quality settings and the efficiencies were ok, update sampling_depth')],
            [sg.Text('             --> Sampling_depth = lowest amount of the second last column in "CHECK_*identifier*_stats.tsv"')],
            [sg.Text('Step 08: Optimize qiime settings for the sampling_depth and create bash-scripts'), sg.Button('Create bash 2')],
            [sg.Text('Step 09: Run bash-script 02 in the other session (sbatch *identifier*_bash_step_02_qiime_graphs.sh)')],
            [sg.Text('Step 10: If the run was succesful, please move the data from the wetrock cluster to another location')]])],
            [sg.Button('Close window')] ]

    #[sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3)),
     #sg.Frame('Labelled Group',[[
     #sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25, tick_interval=25),
     #sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
     #sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
     #sg.Column(column1, background_color='lightblue')]])],
    #[sg.Text('_' * 80)],
 

#RPEI_20200605_BGEU_bash_step_01_qiime_scripts_all_in_1.sh


#RPEI_20200605_BGEU_bash_step_02_qiime_graphs.sh




# Create the Window
window = sg.Window('Start Qiime Analysis', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event in (True, 'Create bash 0'):   # if user closes window or clicks cancel
        os.system("python3.7 " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime2_step00_bash_quality_20211028.py")
    if event in (True, 'Create bash 1'):   # if user closes window or clicks cancel
        os.system("python3.7 " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime2_step01_bash_qiime2_20211028.py")
    if event in (True, 'Create bash 2'):   # if user closes window or clicks cancel
        os.system("python3.7 " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime2_step02_bash_graphs_20211028.py")
    if event in (True, 'qiime settings 0'):   # if user closes window or clicks cancel
        os.system("gedit " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini")
    if event in (True, 'qiime settings 1'):   # if user closes window or clicks cancel
        os.system("gedit " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini")
    if event in (True, 'qiime settings '):   # if user closes window or clicks cancel
        os.system("gedit " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini")        
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


#path = /export2/home/microlab/microlab/qiime/illumina_data/

#size_subsample = 10000

#path_python = /export2/home/microlab/microlab/python_scripts/qiime/
#path_qiime = ~/miniconda3/envs/qiime2-2019.10 

#nodes = 1
#ntasks_per_node = 1
#cpus_per_task = 16
#qiime_version = qiime2-2019.10

#forward_barcodes_file = metadata.txt
#forward_barcodes_column = BarcodeSequence

#forward_primer = GTGYCAGCMGCCGCGGTAA
#reverse_primer = CCGYCAATTYMTTTRAGTTT

#trim_forward = 5
#trim_reverse = 5
#length_forward = 240
#length_reverse = 200

#min_depth = 100
#max_depth = 10000
#sampling_depth = 39417

#path_classifier = /export2/home/microlab/microlab/qiime_classifiers/
#classifier = NB_classifier_SILVA_132_99_16S_515F-926R_QIIME2-2019.10.qza



#sg.theme('LightBlue2')   # Add a touch of color sg.theme('DarkAmber') 
# All the stuff inside your window.
#layout = [  [sg.Text('Step 1: Search for genes in the NCBI nucleotide')],
            #[sg.Text('Step 2: Download the accession number as a file')],
            #[sg.Text('Step 3: Check qiime settings')],
            #[sg.Text('Enter something on Row 2'), sg.InputText()],            
            #[sg.Text('Step 4: Create a subset for a testrun (default = 10000')],
            #[sg.Text('Step 5: Create bash-scripts')],
            #[sg.Text('Your typed chars appear here:'), sg.InputText(size=(64,1))],
            
            #[sg.Text('Step 6: Run subset bash-script 01 in other session (sbatch *kseq_*.sh)')],
            #[sg.Text('Step 7: Optimize qiime settings and create bash-scripts')],
            #[sg.Text('Step 8: Run bash-script full 01 in the other session (sbatch *01*.sh)')],
            #[sg.Text('Step 9: Run bash-script full 02 in the other session (sbatch *02*.sh)')],
            #[sg.Button('PDT settings'), sg.Button('Step 1: Fetch genbank-files'), sg.Button('Create bash'), sg.Button('Close window')] ,
            #[sg.Button('PDT settings'), sg.Button('Step 1: Fetch genbank-files'), sg.Button('Create bash'), sg.Button('Close window')] ]

# Create the Window
#window = sg.Window('Start PDT Functional genes', layout)
# Event Loop to process "events" and get the "values" of the inputs
#while True:
    #event, values = window.read()
    #if event in (True, 'PDT settings'):   # if user closes window or clicks cancel
        #os.system("gedit " + "/export2/home/microlab/microlab/python_scripts/qiime/pdt_settings.ini")
    #if event in (True, 'Step 1: Fetch genbank-files'):   # if user closes window or clicks cancel
        #os.system("python3.7 " + "/export2/home/microlab/microlab/python_scripts/qiime/qiime2_step01_subsampling_quality_check.py")
    #if event in (True, 'Create bash'):   # if user closes window or clicks cancel
        #os.system("python3.7 " + "/export2/home/microlab/microlab/python_scripts/qiime/qiime2_step02_automatic_script_bashcmd.py")
    #if event in (True, 'Close window'):   # if user closes window or clicks cancel
        #exit()             #window.close()
    #else:
        #continue#print('You entered ', values[0])


    #layout += [sg.Text(f'{i}. '), sg.In(key=i)],

#import PySimpleGUI as sg

#layout  = [[sg.Text(f'{i}. '), sg.In(key=i)] for i in range(1,6)] + [[sg.Button('Save'), sg.Button('Exit')]]

#window = sg.Window('To Do List Example', layout)

#event, values = window.read()



#sg.ChangeLookAndFeel('GreenTan')

# ------ Menu Definition ------ #
#menu_def = [['&File', ['&Open', '&Save', 'E&xit', 'Properties']],
            #['&Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
            #['&Help', '&About...'], ]

# ------ Column Definition ------ #
#column1 = [[sg.Text('Column 1', background_color='lightblue', justification='center', size=(10, 1))],
           #[sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
           #[sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
           #[sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

#layout = [
    #[sg.Menu(menu_def, tearoff=True)],
    #[sg.Text('(Almost) All widgets in one Window!', size=(30, 1), justification='center', font=("Helvetica", 25), relief=sg.RELIEF_RIDGE)],
    #[sg.Text('Here is some text.... and a place to enter text')],
    #[sg.InputText('This is my text')],
    #[sg.Frame(layout=[
    #[sg.Checkbox('Checkbox', size=(10,1)),  sg.Checkbox('My second checkbox!', default=True)],
    #[sg.Radio('My first Radio!     ', "RADIO1", default=True, size=(10,1)), sg.Radio('My second Radio!', "RADIO1")]], title='Options',title_color='red', relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
    #[sg.Multiline(default_text='This is the default Text should you decide not to type anything', size=(35, 3)),
     #sg.Multiline(default_text='A second multi-line', size=(35, 3))],
    #[sg.InputCombo(('Combobox 1', 'Combobox 2'), size=(20, 1)),
     #sg.Slider(range=(1, 100), orientation='h', size=(34, 20), default_value=85)],
    #[sg.InputOptionMenu(('Menu Option 1', 'Menu Option 2', 'Menu Option 3'))],
    #[sg.Listbox(values=('Listbox 1', 'Listbox 2', 'Listbox 3'), size=(30, 3)),
     #sg.Frame('Labelled Group',[[
     #sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=25, tick_interval=25),
     #sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=75),
     #sg.Slider(range=(1, 100), orientation='v', size=(5, 20), default_value=10),
     #sg.Column(column1, background_color='lightblue')]])],
    #[sg.Text('_' * 80)],
    #[sg.Text('Choose A Folder', size=(35, 1))],
    #[sg.Text('Your Folder', size=(15, 1), auto_size_text=False, justification='right'),
     #sg.InputText('Default Folder'), sg.FolderBrowse()],
    #[sg.Submit(tooltip='Click to submit this form'), sg.Cancel()]]

#window = sg.Window('Everything bagel', layout, default_element_size=(40, 1), grab_anywhere=False)
#event, values = window.read()
#window.close()

#sg.Popup('Title',
#         'The results of the window.',
#         'The button clicked was "{}"'.format(event),
#         'The values are', values)





