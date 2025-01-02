# region [Import]
from unittest import TestCase
import PyDAQmx
import DAQ
import numpy


class TestDigitalInput(TestCase):
    def test_connected_device(self):
        self_test = PyDAQmx.DAQmxSelfTestDevice('cDAQ1')

        self.assertEqual(self_test, 0)

    def test_digital_input(self):
        di = DAQ.DigitalInput('cDAQ1Mod2/port0/line0', 1, 1000, 1)
        di.DoTask()

        self.assertEqual(numpy.sum(di.digitalData[0]), 0)

    def test_digital_data_shape(self):
        di = DAQ.DigitalInput('cDAQ1Mod2/port0/line0:1', 2, 1000, 3)
        di.DoTask()

        print(di.digitalData.shape)

        self.assertEqual(di.digitalData.shape[0] * di.digitalData.shape[1], 2*1000*3)

