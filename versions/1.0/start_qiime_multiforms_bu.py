import PySimpleGUI as sg
import os
#import qiime2_step03_bash_merge_20211117 as bash03




def qiime2_start_form_0_base():
    sg.theme('LightBlue2')   
    
    layout = [  [sg.Frame('Start Form Qiime2' ,[
                [sg.Text('  ')],
                [sg.Button('Step 1: Upload and rename files', font=("Helvetica", 12))],
                [sg.Button('Step 2: Settings and quality control', font=("Helvetica", 12))],
                [sg.Button('Step 3: Qiime2 pipeline', font=("Helvetica", 12))],
                [sg.Text('  ')],
                [sg.Button('Step 4a: Data and graphs', font=("Helvetica", 12))],
                [sg.Text('     or    ', font=("Helvetica", 12))],
                [sg.Button('Step 4b: Merge datasets, data and graphs', font=("Helvetica", 12))],
                [sg.Text('  ')],], font=("Helvetica", 16))],
                [sg.Text('  ')],
                [sg.Button('Exit', font=("Helvetica", 12))],]
    window_0 = sg.Window('Start Qiime2 Analysis', layout, finalize=True)
    return window_0



def qiime2_start_form_1_files():
    sg.theme('LightBlue2')   
    
    layout = [  [sg.Frame('Step 1 Qiime2 --> Upload and rename files',[
                [sg.Text('  ')],
                [sg.Text('Step 1.1: Open 2 sessions within MobaXterm with the account "microlab"', font=("Helvetica", 11))],
                [sg.Text('Step 1.2: Upload the fastq.gz-files and the barcode-file to "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/raw_illumina_data_gz/"', font=("Helvetica", 11))],            
                [sg.Text('Step 1.3: Check/rename filenames; Addition of similar identifiers followed by "@" in front of the filenames', font=("Helvetica", 11))],
                [sg.Text('         Syntax = Initials + "_" + Quotenumber + "_" + Gene + "_" + Primerset + "_" + Date(yyyymmdd) + "@". See example below', font=("Helvetica", 11))],
                [sg.Text('         1) CSCH_Q12946_16S_515F926R_20201113@metadata.txt', font=("Helvetica", 11))],
                [sg.Text('         2) CSCH_Q12946_16S_515F926R_20201113@*_R1_*.fastq.gz', font=("Helvetica", 11))],
                [sg.Text('         3) CSCH_Q12946_16S_515F926R_20201113@*_R2_*.fastq.gz', font=("Helvetica", 11))],
                [sg.Text('  ')],], font=("Helvetica", 14))],
                [sg.Text('  ')],
                [sg.Button('Next step', font=("Helvetica", 12))],]
    window_1 = sg.Window('Qiime Analysis 1', layout, finalize=True)
    return window_1

def qiime2_start_form_2_quality():

    sg.theme('LightBlue2')   
    
    layout = [  [sg.Frame('Step 2 Qiime2 --> Check Qiime2 settings and quality control',[
                [sg.Text('  ')],
                [sg.Text('Step 2.1: Check qiime settings     ', font=("Helvetica", 11)), sg.Button('qiime settings', font=("Helvetica", 12))],
                [sg.Text('          Default/standard values are (Find primer info in *@metadata.txt):', font=("Helvetica", 11))],
                [sg.Text('          U515F: GTGYCAGCMGCCGCGGTAA', font=("Helvetica", 11))],
                [sg.Text('          BAC926R: CCGYCAATTYMTTTRAGTTT', font=("Helvetica", 11))],
                [sg.Text('          size_subsample = 10000', font=("Helvetica", 11))],
                [sg.Text('Step 2.2: Create bash-script   ', font=("Helvetica", 11)), sg.Button('Create bash-script 00', font=("Helvetica", 11))],
                [sg.Text('          Bash-script 00 was created in folder: "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/raw_illumina_data_gz/"', font=("Helvetica", 11))],
                [sg.Text('Step 2.3: Run bash-script 00 in the other Mobaxterm session (sbatch *identifier*_bash_step_00_qiime_quality.sh)', font=("Helvetica", 11))],
                [sg.Text('  ')],], font=("Helvetica", 14))],
                [sg.Text('  ')],
                [sg.Button('Next step', font=("Helvetica", 12)),],]
    window_2 = sg.Window('Qiime Analysis 2', layout, finalize=True)
    return window_2

def qiime2_start_form_3_qiime2():

    sg.theme('LightBlue2')   
    
    layout = [  [sg.Frame('Step 3 Qiime2 --> Qiime2 pipeline',[
                [sg.Text('  ')],
                [sg.Text('Step 3.1: Check qiime settings     ', font=("Helvetica", 11)), sg.Button('qiime settings', font=("Helvetica", 12))],
                [sg.Text('          Default/standard values are:', font=("Helvetica", 11))],
                [sg.Text('          trim_forward = 5', font=("Helvetica", 11))],
                [sg.Text('          trim_reverse = 5', font=("Helvetica", 11))],
                [sg.Text('          length_forward = 200', font=("Helvetica", 11)), sg.Text('          Check "CHECK_quality_scores_datasets.txt" in output-folder', font=("Helvetica", 11))], 
                [sg.Text('          length_reverse = 190', font=("Helvetica", 11)), sg.Text('          Check "CHECK_quality_scores_datasets.txt" in output-folder', font=("Helvetica", 11))],
                [sg.Text('Step 3.2: Create bash-script 01    ', font=("Helvetica", 11)), sg.Button('Create bash-script 01', font=("Helvetica", 12))],
                [sg.Text('          Bash-script 01 was created in folder: "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/raw_illumina_data_gz/"', font=("Helvetica", 11))],
                [sg.Text('Step 3.3: Run bash-script 01in the other Mobaxterm session (sbatch *identifier*_bash_step_01_qiime_quality.sh)', font=("Helvetica", 11))],
                [sg.Text('  ')],], font=("Helvetica", 14))],
                [sg.Text('  ')],
                [sg.Button('Next step', font=("Helvetica", 12)),],]
    window_3 = sg.Window('Qiime Analysis 3', layout, finalize=True)
    return window_3

def qiime2_start_form_4a_graphs_data():

    sg.theme('LightBlue2')   
    
    layout = [  [sg.Frame('Step 4a Qiime2 --> Data and graphs',[
                [sg.Text('  ')],
                [sg.Text('If merging is not needed', font=("Helvetica", 11))],            
                [sg.Text('Step 4a.1: Check qiime settings     ', font=("Helvetica", 11)), sg.Button('qiime settings', font=("Helvetica", 12))],
                [sg.Text('          Sampling_depth = lowest amount of the second last column in "CHECK_*identifier*_stats.tsv"', font=("Helvetica", 11))],
                [sg.Text('Step 4a.2: Create bash-script 02    ', font=("Helvetica", 11)), sg.Button('Create bash-script 02', font=("Helvetica", 12))],
                [sg.Text('          Bash-script 02 was created in folder: "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/raw_illumina_data_gz/"', font=("Helvetica", 11))],
                [sg.Text('Step 4a.3: Run bash-script 02 in the other Mobaxterm session (sbatch *identifier*_bash_step_02_qiime_graphs.sh)', font=("Helvetica", 11))],
                [sg.Text('  ')],], font=("Helvetica", 14))],
                [sg.Text('  ')],
                [sg.Button('Next step', font=("Helvetica", 12)),],]
    window_4a = sg.Window('Qiime Analysis 4a', layout, finalize=True)
    return window_4a


def qiime2_start_form_4b_merge_graphs_data():
    sg.theme('LightBlue2')   
    
    layout = [  [sg.Frame('Step 4b Qiime2 --> Merge datasets, data and graphs',[
                [sg.Text('  ')],
                [sg.Text('If merging needed', font=("Helvetica", 13))],            
                [sg.Text('Step 4b.1: Check qiime settings     ', font=("Helvetica", 11)), sg.Button('qiime settings', font=("Helvetica", 12))],
                [sg.Text('Step 4b.2: Create bash-script 03    ', font=("Helvetica", 11)), sg.Button('Create bash-script 03', font=("Helvetica", 12))],
                [sg.Text('          Bash-script 03 was created in folder: "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/raw_illumina_data_gz/"', font=("Helvetica", 11))],
                [sg.Text('Step 4b.3: Check qiime settings     ', font=("Helvetica", 11))],
                [sg.Text('          Sampling_depth = lowest amount of the second last columns in "CHECK_*identifier*_stats.tsv" LOWEST VALUE FROM FILES, WHICH WILL BE COMBINED!!!', font=("Helvetica", 11))],
                [sg.Text('Step 4b.4: Run bash-script 03 in the other Mobaxterm session (sbatch *identifier*_bash_step_03_qiime_merge.sh)', font=("Helvetica", 11))],
                [sg.Text('  ')],], font=("Helvetica", 12))],
                [sg.Text('  ')],
                [sg.Button('Next step', font=("Helvetica", 12))],]

    window_4b = sg.Window('Start Qiime Analysis 4b', layout, finalize=True)
    return window_4b


def main():

    window_0 = qiime2_start_form_0_base()
    window_1 = None
    window_2 = None
    window_3 = None
    window_4a = None
    window_4b = None

    while True:
        window, event, values = sg.read_all_windows()
        
        if window == window_0 and (event in (sg.WIN_CLOSED, 'Exit')):
            break


        if event == 'Step 1: Upload and rename files' and not window_1:
            window_1 = qiime2_start_form_1_files()
            window_0.hide()

        if event == 'Step 2: Settings and quality control' and not window_2:
            window_2 = qiime2_start_form_2_quality()
            window_0.hide()

        if event == 'Step 3: Qiime2 pipeline' and not window_3:
            window_3 = qiime2_start_form_3_qiime2()
            window_0.hide()

        if event == 'Step 4a: Data and graphs' and not window_4a:
            window_4a = qiime2_start_form_4a_graphs_data()
            window_0.hide()

        if event == 'Step 4b: Merge datasets, data and graphs' and not window_4b:
            window_4b = qiime2_start_form_4b_merge_graphs_data()
            window_0.hide()


        if window == window_1 and (event in (sg.WIN_CLOSED, 'Next step')):
            window_1.close()
            window_1 = None
            window_0.un_hide()
        if window == window_2 and (event in (sg.WIN_CLOSED, 'Next step')):
            window_2.close()
            window_2 = None
            window_0.un_hide()
        if window == window_3 and (event in (sg.WIN_CLOSED, 'Next step')):
            window_3.close()
            window_3 = None
            window_0.un_hide()
        if window == window_4a and (event in (sg.WIN_CLOSED, 'Next step')):
            window_4a.close()
            window_4a = None
            window_0.un_hide()
        if window == window_4b and (event in (sg.WIN_CLOSED, 'Next step')):
            window_4b.close()
            window_4b = None
            window_0.un_hide()

        if window == window_2 and event == 'qiime settings':
            os.system("gedit " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini")

        if window == window_3 and event == 'qiime settings':
            os.system("gedit " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini")

        if window == window_4a and event == 'qiime settings':
            os.system("gedit " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini")

        if window == window_4b and event == 'qiime settings':
            os.system("gedit " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime_settings.ini")



        if window == window_2 and event == 'Create bash-script 00':
            os.system("python3.7 " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime2_step00_bash_quality_20211028.py")

        if window == window_3 and event == 'Create bash-script 01':
            os.system("python3.7 " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime2_step01_bash_qiime2_20211028.py")

        if window == window_4a and event == 'Create bash-script 02':
            os.system("python3.7 " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime2_step02_bash_graphs_20211028.py")

        if window == window_4b and event == 'Create bash-script 03':
            os.system("python3.7 " + "/export2/home/microlab/qiime2/pipeline_qiime2-2019-10/python_scripts/qiime2_step03_bash_merge_20211117.py")


            
        else:
            continue

    window_0.close()


if __name__ == '__main__':
    main()


