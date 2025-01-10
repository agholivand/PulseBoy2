import sys
sys.path.append('C:\\Users\\amirr\\Py\\PulseBoy2')
sys.path.append('C:\\Users\\amirr\\Py\\PulseBoy2\\PulseBoy')
sys.path.append('C:\\Users\\amirr\\Py\\PulseBoy2\\PyPulse')

from PyPulse import PulseInterface
import numpy as np
from PyQt5 import QtWidgets
import Models.Experiment as Experiment
from Controllers import QueueControl, QueueControl
from multiprocessing import Queue, Process, Manager
from Designs import mainDesign
from Models import PBWidgets
try:
    from vipulse import StreamNSave
except ImportError:
    print('No camera!')
import pickle as pickle
import os.path
import daqface.DAQ as daq


# noinspection PyBroadException
class MainApp(QtWidgets.QMainWindow, mainDesign.Ui_MainWindow):
    def __init__(self):
        super(self.__class__, self).__init__()
        self.setupUi(self)

        # Setup Experiment Data / Controller
        self.trialBankModel = Experiment.ExperimentModel(self)
        self.trialBankTable.setModel(self.trialBankModel)

        self.queue_controller = QueueControl.QueueController(self.trialBankModel,
                                                             self.get_global_params,
                                                             self.get_hardware_params,
                                                             self.get_export_params,
                                                             self.triggerWaitCheckBox)

        # self.triggerWaitCheckBox.isChecked()

        if os.path.exists('params.config'):
            try:
                self.load_config_data()
            except:
                pass

        # Setup Button Bindings
        self.addValveButton.clicked.connect(lambda f: self.add_valve(v_type=self.valveTypeCombo.currentText()))

        self.addTrialButton.clicked.connect(self.add_trial)
        self.updateTrialButton.clicked.connect(self.update_trial)
        self.removeTrialButton.clicked.connect(self.remove_trial)
        self.moveUpButton.clicked.connect(self.move_trial_up)
        self.moveDownButton.clicked.connect(self.move_trial_down)
        self.randomiseTrialsButton.clicked.connect(self.randomise_trials)

        self.actionSave.triggered.connect(self.save)
        self.actionLoad.triggered.connect(self.load)
        self.actionSave_Configuration.triggered.connect(self.save_config_data)
        self.exportPathDirButton.clicked.connect(self.set_export_path)

        self.trialBankTable.selectionModel().selectionChanged.connect(self.trial_selected)
        self.queue_controller.trial_start.connect(self.select_current_trial)
        # self.queue_controller.trial_job.trial_end.connect(self.plot_analog_data) - TODO, needs DAQ to test

        self.startQueueButton.clicked.connect(self.queue_controller.start)
        self.stopQueueButton.clicked.connect(self.queue_controller.stop)
        self.pauseQueueButton.clicked.connect(self.queue_controller.pause)
        self.runSelectedButton.clicked.connect(lambda x: self.queue_controller.run_selected(self.trialBankTable.selectionModel().selectedRows()[0].row()))
        self.startQueueFromSelectedButton.clicked.connect(lambda x: self.queue_controller.run_from_selected(self.trialBankTable.selectionModel().selectedRows()[0].row()))

        ## Camera code
        # camera_params = Manager().dict()
        # self.cameraParams = camera_params
        # self.launchCameraButton.clicked.connect(self.startStream)

        # self.get_camera_params()
        # self.closeCamerasButton.clicked.connect(self.terminateCameraStream)
        # self.updateCamerasButton.clicked.connect(self.get_camera_params)
        # self.closeValvesButton.clicked.connect(self.reset_all_chans)


    def add_valve(self, v_type='Simple', params=None):
        position = len(self.valveBankContents.children()) - 1
        if v_type == 'Simple':
            new_valve = PBWidgets.SimpleValveWidget(self.valveBankContents, position)
        elif v_type == 'Noise':
            new_valve = PBWidgets.NoiseValveWidget(self.valveBankContents, position)
        elif v_type == 'Plume':
            new_valve = PBWidgets.PlumeValveWidget(self.valveBankContents, position)
        elif v_type == 'Anti Plume':
            new_valve = PBWidgets.AntiPlumeValveWidget(self.valveBankContents, position)
        elif v_type == 'Binary':
            new_valve = PBWidgets.BinaryPlumeValveWidget(self.valveBankContents, position)
        else:
            new_valve = PBWidgets.SimpleValveWidget(self.valveBankContents, position)

        if params is not None:
            new_valve.set_parameters(params)
        self.valveBankContents.layout().addWidget(new_valve)

    def reset_all_chans(self):
        daq.closeValves(self.get_hardware_params()['digital_dev'])

    def add_trial(self):
        n_valves = 0
        all_params = list()
        trial_name = self.trialNameEdit.text()
        for valve in self.valveBankContents.children():
            if hasattr(valve, 'get_parameters'):
                params = valve.get_parameters()
                all_params.append(params)
                n_valves += 1

        if n_valves > 0:
            self.trialBankModel.append_row([n_valves, all_params, trial_name])

    def update_trial(self):
        selected_trial = self.trialBankTable.selectionModel().selectedRows()[0].row()
        n_valves = 0
        all_params = list()
        trial_name = self.trialNameEdit.text()
        for valve in self.valveBankContents.children():
            if hasattr(valve, 'get_parameters'):
                params = valve.get_parameters()
                all_params.append(params)
                n_valves += 1

        if n_valves > 0:
            self.trialBankModel.update_row(selected_trial, [n_valves, all_params, trial_name])

    def remove_trial(self):
        try:
            selected_trial = self.trialBankTable.selectionModel().selectedRows()[0].row()
            self.trialBankModel.remove_row(selected_trial)
        except:
            print('No trial selected')
            pass

    def move_trial_up(self):
        idx = self.trialBankTable.selectionModel().selectedRows()[0].row()
        self.trialBankModel.move_trial_up(idx)
        if idx > 0:
            self.select_trial(idx - 1)

    def move_trial_down(self):
        idx = self.trialBankTable.selectionModel().selectedRows()[0].row()
        self.trialBankModel.move_trial_down(idx)
        if idx < len(self.trialBankModel.arraydata):
            self.select_trial(idx + 1)

    def randomise_trials(self):
        glob_params = self.get_global_params()
        self.trialBankModel.randomise_trials(glob_params)

    def trial_selected(self):
        try:
            selected_trial = self.trialBankTable.selectionModel().selectedRows()[0].row()
        except:
            selected_trial = 0

        trial_params = self.trialBankModel.arraydata[selected_trial][1]
        invert_valves = []
        if self.invertBlankcheckBox.isChecked():
            try:
                invert_valves = [int(i) for i in self.blankValveEdit.text().split(',')]
            except ValueError:
                print('Unable to invert channels, did not understand input "%s' % self.blankValveEdit.text())
        
        pulses, t = PulseInterface.make_pulse(float(self.sampRateEdit.text()),
                                              float(self.globalOnsetEdit.text()),
                                              float(self.globalOffsetEdit.text()), trial_params, invert_chan_list=invert_valves)

        self.graphicsView.plotItem.clear()
        for p, pulse in enumerate(pulses):
            self.graphicsView.plotItem.plot(t, np.array(pulse) - (p * 1.1))

        self.trialNameEdit.setText(self.trialBankModel.arraydata[selected_trial][2])

        self.update_valve_bank(selected_trial)

    def select_current_trial(self):
        self.trialBankTable.selectRow(self.trialBankModel.current_trial)

    def select_trial(self, trial_n):
        self.trialBankTable.selectRow(trial_n)

    def update_valve_bank(self, trial_idx):
        for widget in self.valveBankContents.children():
            if hasattr(widget, 'get_parameters'):
                widget.remove_from_parent()

        for valve in self.trialBankModel.arraydata[trial_idx][1]:
            self.add_valve(v_type=valve['type'], params=valve)

    def plot_analog_data(self):
        self.analogView.plotItem.clear()
        for a, analog in enumerate(self.queue_controller.thread.analog_data):
            t = np.arange(len(analog)) / int(self.sampRateEdit.text())
            self.analogView.plotItem.plot(t, np.array(analog) - (a * 1.1))

    def save(self):
        fname, suff = QtWidgets.QFileDialog.getSaveFileName(self, "Save File", "", "Trial Bank (*.trialbank)")
        fname, suff = fname.split('.')
        suff = '.' + suff
        self.trialBankModel.save_arraydata((fname, suff))

    def load(self):
        fname, suff = QtWidgets.QFileDialog.getOpenFileName(self, "Open File", '', '*.trialbank')
        print(fname)
        self.trialBankModel.load_arraydata(fname)
        self.queue_controller.trial_list = self.trialBankModel.arraydata

    def save_config_data(self):
        config = {'hardware_params': self.get_hardware_params(),
                  'global_params': self.get_global_params(),
                  'export_params': self.get_export_params()}

        with open('params.config', 'wb') as fn:
            pickle.dump(config, fn)

    def load_config_data(self):
        with open('params.config', 'rb') as fn:
            config = pickle.load(fn)

        hardware_params = config['hardware_params']
        global_params = config['global_params']
        export_params = config['export_params']

        #self.analogInDevEdit.setText(hardware_params['analog_dev'])
        #self.analogChannelsEdit.setText(str(hardware_params['analog_channels']))
        self.digitalOutDevEdit.setText(hardware_params['digital_dev'])
        self.digitalChannelsEdit.setText(str(hardware_params['digital_channels']))
        self.syncClockEdit.setText(hardware_params['sync_clock'])
        self.sampRateEdit.setText(str(int(hardware_params['samp_rate'])))
        self.triggerInEdit.setText(str(hardware_params['trigger_source']))

        self.globalOnsetEdit.setText(str(global_params['global_onset']))
        self.globalOffsetEdit.setText(str(global_params['global_offset']))

        self.exportPathEdit.setText(export_params['export_path'])
        self.exportSuffixEdit.setText(export_params['export_suffix'])

    def get_hardware_params(self):
        params = dict()
        #params['analog_dev'] = self.analogInDevEdit.text()
        #params['analog_channels'] = int(self.analogChannelsEdit.text())
        params['digital_dev'] = self.digitalOutDevEdit.text()
        params['digital_channels'] = int(self.digitalChannelsEdit.text())
        params['sync_clock'] = self.syncClockEdit.text()
        #params['sync_clock'] = "OnboardClock"  # Replace with the desired clock source
        params['samp_rate'] = float(self.sampRateEdit.text())
        params['trigger_source'] = self.triggerInEdit.text()

        return params

    def get_global_params(self):
        params = dict()
        params['global_onset'] = float(self.globalOnsetEdit.text())
        params['global_offset'] = float(self.globalOffsetEdit.text())
        params['repeats'] = float(self.repeatsBox.text())
        #params['repeats_done'] = 0
        params['shuffle_repeats'] = bool(self.shuffleRepeatsBox.isChecked())
        params['inverted_blank_off_state'] = bool(self.invertBlankcheckBox.isChecked())
        if params['inverted_blank_off_state']:
            params['inverted_blank_valves'] = [int(i) for i in self.blankValveEdit.text().split(',')]
        else:
            params['inverted_blank_valves'] = None

        params['shuffle_offset'] = int(self.shuffleOffsetlineEdit.text())
        params['shuffle_group_size'] = int(self.shuffleGrouplineEdit.text())
        return params

    def get_export_params(self):
        params = dict()
        params['save_names'] = bool(self.trialNameCheckBox.isChecked())
        params['save_pulses'] = bool(self.pulseCheckBox.isChecked())
        params['export_path'] = str(self.exportPathEdit.text())
        params['pulse_suffix'] = str(self.pulseSuffixEdit.text())
        params['trial_suffix'] = str(self.trialNameSuffixEdit.text())

        return params

    def set_export_path(self):
        path = QtWidgets.QFileDialog.getExistingDirectory(self, "Choose Export Path")
        self.exportPathEdit.setText(path + '/')
    

    # def startStream(self):
    #     self.get_camera_params()
    #     self.cameraParams['runStream'] = True
    #     self.cameraProcess = Process(target=StreamNSave.stream_and_save, 
    #                                  args=(self.cameraParams,))
    #     self.cameraProcess.daemon = True
    #     self.cameraProcess.start()
    # def terminateCameraStream(self):
    #     self.cameraParams['runStream'] = False
    #     #self.cameraProcess.terminate()

    # def get_camera_params(self):
    #     self.cameraParams['saveStream'] = bool(self.saveCameraVideocheckBox.isChecked())
    #     self.cameraParams['showStream'] = bool(self.showStreamcheckBox.isChecked())
    #     self.cameraParams['outDir'] = str(self.exportPathEdit.text())
    #     self.cameraParams['cams'] = int(self.numberCamerasEdit.text())
    #     self.cameraParams['cameraSuffix'] = str(self.cameraSuffixEdit.text())
    #     self.cameraParams['inter_stream_interval'] = float(self.cameraSaveIntervalEdit.text())
    #     self.cameraParams['recording_ind'] = bool(self.cameraSaveIconBox.isChecked())


# Back up the reference to the exceptionhook
sys._excepthook = sys.excepthook


def my_exception_hook(exctype, value, traceback):
    # Print the error and traceback
    print(exctype, value, traceback)
    # Call the normal Exception hook after
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)

# Set the exception hook to our wrapping function
sys.excepthook = my_exception_hook


def main():
    app = QtWidgets.QApplication(sys.argv)
    form = MainApp()
    form.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
