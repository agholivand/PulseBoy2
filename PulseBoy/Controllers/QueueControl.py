from PyQt5 import QtCore
from time import sleep
import daqface.DAQ as daq
from PyPulse import PulseInterface
import scipy.io as sio
import numpy as np
from datetime import datetime
import os


class QueueWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    trial_start = QtCore.pyqtSignal()

    def __init__(self, parent, experiment, get_global_params, get_hardware_params, get_export_params):
        super(self.__class__, self).__init__(None)
        self.parent = parent
        self.experiment = experiment
        self.get_global_params = get_global_params
        self.get_hardware_params = get_hardware_params
        self.get_export_params = get_export_params

    @QtCore.pyqtSlot()
    def trial(self):
        while True:
            sleep(0.05)
            if self.parent.should_run:
                self.trial_start.emit()

                trial_params = self.experiment.arraydata[self.experiment.current_trial][1]
                hardware_params = self.get_hardware_params()
                global_params = self.get_global_params()
                export_params = self.get_export_params()
                invert_valves = []
                if global_params['inverted_blank_off_state']:
                    invert_valves = global_params['inverted_blank_valves']
                pulses, t = PulseInterface.make_pulse(hardware_params['samp_rate'],
                                                      global_params['global_onset'],
                                                      global_params['global_offset'],
                                                      trial_params, invert_chan_list=invert_valves)

                if hardware_params['control_carrier']:
                    while len(pulses) < hardware_params['digital_channels']:
                        pulses = np.append(pulses, np.zeros((1, pulses.shape[1])), axis=0)
                    carrier_control = np.append(np.ones(pulses.shape[1]-0), np.zeros(0))
                    pulses = np.append(pulses, carrier_control[np.newaxis], axis=0)
                # in standard configuration we want to run each trial sequentially
                if not self.parent.trigger_state():
                    if hardware_params['analog_channels'] > 0:
                        self.trial_daq = daq.DoAiMultiTask(hardware_params['analog_dev'], hardware_params['analog_channels'],
                                                           hardware_params['digital_dev'], hardware_params['samp_rate'],
                                                           len(t) / hardware_params['samp_rate'], pulses,
                                                           hardware_params['sync_clock'])

                        self.analog_data = self.trial_daq.DoTask()
                    else:
                        self.trial_daq = daq.DoCoTask(hardware_params['digital_dev'], '', hardware_params['samp_rate'],
                                                      len(t) / hardware_params['samp_rate'], pulses)
                        self.trial_daq.DoTask()
                        # close_valves= daq.DoCoTask(hardware_params['digital_dev'], '', hardware_params['samp_rate'],
                        #                               len(t) / hardware_params['samp_rate'], np.zeros((len(pulses), 10)))
                        # close_valves.DoTask()
                        self.analog_data = []
                # unless the 'wait for trigger' box is checked, in which case we want to wait for our trigger in
                else:
                    if hardware_params['analog_channels'] > 0 :
                        self.trial_daq = daq.DoAiTriggeredMultiTask(hardware_params['analog_dev'],
                                                                hardware_params['analog_channels'],
                                                                hardware_params['digital_dev'],
                                                                hardware_params['samp_rate'],
                                                                len(t) / hardware_params['samp_rate'], pulses,
                                                                hardware_params['sync_clock'],
                                                                hardware_params['trigger_source'])

                        self.analog_data = self.trial_daq.DoTask()
                    else:
                        self.trial_daq= daq.DoTriggeredCoTask(hardware_params['digital_dev'], '', hardware_params['samp_rate'], len(t) / hardware_params['samp_rate'],
                                                              pulses, hardware_params['trigger_source'])
                        self.trial_daq.DoTask()
                        self.analog_data = []

                # Save data
                if export_params['save_pulses']:
                    date = datetime.today().strftime('%Y%m%d')
                    time = datetime.today().strftime('%H%M%S')
                    trialName = self.experiment.arraydata[self.experiment.current_trial][2]
                    
                    if self.experiment.current_trial == 0:
                        trialbankName = export_params['trialbankName']
                        # Adding timestamp to the directory name (trialbankName -> dateTime_trialbankName)
                        newTrialbankName = date+'T'+time+'_'+trialbankName
                        newExportPath = export_params['export_path']+'\\'+newTrialbankName
                        pulses_path = os.path.join(newExportPath, 'pulses')
                        os.makedirs(pulses_path, exist_ok=True)
                    date = datetime.today().strftime('%Y%m%d')
                    time = datetime.today().strftime('%H%M%S')
                    save_string =pulses_path + '\\' + date + 'T' + time + '_' + str(trialName) + '.mat'
                    sio.savemat(save_string, {'pulses': pulses, 't': t})
                    #sio.savemat(save_string, {'analog_data': self.analog_data, 'pulses': pulses, 't': t})
                
                if export_params['save_names']:
                    #names = [i[-1] for i in self.experiment.arraydata] --> this creates a text file at the end of a trialbank, not used anymore |15.07.2024
                    trials_path = os.path.join(newExportPath, 'trials')
                    os.makedirs(trials_path, exist_ok=True) 
                    f = open(trials_path+'\\'+ date + 'T' + time + '_' + str(trialName) + '.txt', 'a')
                    f.write(date+'T'+time)
                    f.write('\n')
                    f.write(trialName)
                    f.close()
                if self.experiment.total_trials() - self.experiment.current_trial == 1:
                    self.experiment.reset_trials()
                    self.parent.repeats_done += 1
                    print('repeats done ', self.parent.repeats_done)
                    if self.parent.repeats_done == global_params['repeats']:
                        self.parent.should_run = False
                        self.parent.repeats_done = 0
                    else:
                        if global_params['shuffle_repeats']:
                            self.experiment.randomise_trials(global_params)

                elif self.parent.should_run:
                    self.experiment.advance_trial()


                self.finished.emit()


class QueueController(QtCore.QObject):
    trial_start = QtCore.pyqtSignal()

    def __init__(self, experiment, get_global_params, get_hardware_params, get_export_params, trigger_control):
        super(self.__class__, self).__init__(None)
        self.experiment = experiment
        self.get_global_params = get_global_params
        self.get_hardware_params = get_hardware_params
        self.get_export_params = get_export_params
        self.prepare_thread()
        self.repeats_done = 0

        self.should_run = False
        self.trigger_control = trigger_control

    def prepare_thread(self):
        self.thread = QtCore.QThread()
        self.worker = QueueWorker(self, self.experiment, self.get_global_params, self.get_hardware_params,
                                  self.get_export_params)
        self.worker.moveToThread(self.thread)
        self.worker.trial_start.connect(self.trial_start.emit)
        self.thread.started.connect(self.worker.trial)

        self.thread.start()

    def start(self):

        if not self.should_run:
            self.should_run = True

    def pause(self):
        if self.should_run:
            self.should_run = False
            self.experiment.advance_trial()

    def stop(self):
        if self.should_run:
            self.should_run = False

        self.experiment.reset_trials()
        self.repeats_done = 0


    def run_selected(self, trial):
        if not self.should_run:
            self.should_run = True
            self.experiment.current_trial = trial
            sleep(0.05)
            self.should_run = False

    def run_from_selected(self, trial):
        if not self.should_run:
            self.should_run = True
            self.experiment.current_trial = trial


    def finished(self):
        print("not implemented")

    def trigger_state(self):
        return self.trigger_control.isChecked()
