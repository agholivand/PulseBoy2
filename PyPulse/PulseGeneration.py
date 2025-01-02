import scipy.signal as signal
import numpy as np
import scipy.io as sio


def square_pulse(sampling_rate, duration, frequency, duty, inverted=False):
    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    square_pulse = (np.array(signal.square(2 * np.pi * frequency * t, duty=duty)) / 2) + 0.5
    if inverted:
        square_pulse = -square_pulse + 1
    return  square_pulse, t


def extended_square_pulse(sampling_rate, duration, frequency, duty):
    # extension direction: 1 = forwards, -1 = backwards
    t = np.linspace(0, duration, sampling_rate * duration, endpoint=False)
    pulse = (np.array(signal.square(2 * np.pi * frequency * t, duty=duty)) / 2) + 0.5

    distance = ((1.0 / frequency) * duty) * sampling_rate
    extender = np.ones((int(distance)))

    pulse = np.append(extender, pulse)

    new_duration = duration+((1.0 / frequency) * duty)
    t = np.linspace(0, new_duration, int(sampling_rate * new_duration), endpoint=False)

    return pulse, t


def shatter_pulse(sampling_rate, duration, frequency, duty, shatter_frequency, shatter_duty, inverted=False):

    if shatter_frequency < frequency:
        raise ValueError('Shatter frequency must not be lower than major frequency.')

    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)
    if inverted:
        shatter_duty = 1-shatter_duty
    guide_pulse, _ = square_pulse(sampling_rate, duration, frequency, duty, inverted=False)
    shattered_pulse = (np.array(signal.square(2 * np.pi * shatter_frequency * t, duty=shatter_duty)) / 2) + 0.5
    out_pulse = guide_pulse * shattered_pulse
    if inverted:
        out_pulse = out_pulse * -1 + 1
    return out_pulse, t


def random_shatter_pulse(sampling_rate, duration, frequency, duty, shatter_frequency, target_duty, amp_min, amp_max, extend=False):
    # this function generates a shattered pulse based on major pulse frequency and duty, as well as shatter frequency.
    # The function will generate standard pulse and then shatter it, with the duty
    # of each shattered pulse randomised. The function will aim to keep the integral of the pulse at duty * target duty
    if shatter_frequency < frequency:
        raise ValueError('Shatter frequency must not be lower than major frequency.')

    if extend:
        guide_pulse, _ = extended_square_pulse(sampling_rate, duration, frequency, duty)
        duration = len(guide_pulse) / sampling_rate
    else:
        guide_pulse, _ = square_pulse(sampling_rate, duration, frequency, duty)

    t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

    if target_duty == 1.0:
        return guide_pulse, t

    # calculate shatter duty bounds
    if (target_duty - amp_min) < (amp_max - target_duty):
        lower_duty_bound = amp_min
        upper_duty_bound = target_duty + (target_duty - amp_min)
    else:
        upper_duty_bound = amp_max
        lower_duty_bound = target_duty - (amp_max - target_duty)

    shattered_guide = []
    while len(shattered_guide) < len(t):
        rand_param = np.random.uniform(lower_duty_bound, upper_duty_bound)
        shattered_guide = np.hstack((shattered_guide, np.ones(int(sampling_rate / shatter_frequency)) * rand_param))

    shattered_guide = shattered_guide[0:int(sampling_rate*duration)]
    shattered_pulse = (np.array(signal.square(2 * np.pi * shatter_frequency * t, duty=shattered_guide)) / 2) + 0.5

    return guide_pulse * shattered_pulse, t


def random_simple_pulse(sampling_rate, params):
    # Build main portion of pulse
    if params['fromDuty']:
        frequency = params['frequency']
        duty = params['duty']
    else:
        assert params['fromValues']
        frequency = 1.0 / (params['pulse_width'] + params['pulse_delay'])
        duty = params['pulse_width'] / (params['pulse_width'] + params['pulse_delay'])

    if params['fromLength']:
        duration = params['length']
    else:
        assert params['fromRepeats']
        if params['fromValues']:
            duration = (params['pulse_width'] + params['pulse_delay']) * params['repeats']
        else:
            assert params['fromDuty']
            duration = (1.0 / frequency) * params['repeats']

    if duration > 0.0:
        if 'extend' in params.keys():
            pulse, t = random_shatter_pulse(sampling_rate, duration, frequency, duty, params['shatter_frequency'],
                                            params['target_duty'], params['amp_min'], params['amp_max'],
                                            extend=params['extend'])
            duration = len(t) / sampling_rate
        else:
            pulse, t = random_shatter_pulse(sampling_rate, duration, frequency, duty, params['shatter_frequency'],
                                        params['target_duty'], params['amp_min'], params['amp_max'])
    else:
        pulse, t = square_pulse(sampling_rate, duration, frequency, duty)

    # Attach onset and offset
    if params['inversion']:
        onset = np.ones(int(sampling_rate * params['onset']))
        offset = np.ones(int(sampling_rate * params['offset']))
    else:
        onset = np.zeros(int(sampling_rate * params['onset']))
        offset = np.zeros(int(sampling_rate * params['offset']))

    # if we want to shadow the pulse, add this in here (repeat the pulse at a compensating duty)
    if params['shadow']:
        pulse_on = (1.0 / frequency) * duty
        shadow, _ = random_shatter_pulse(sampling_rate, duration - pulse_on, frequency, duty,
                                         params['shatter_frequency'], 0.5-params['target_duty'], params['amp_min'],
                                         params['amp_max'])
        shadow = np.hstack((np.zeros(int(pulse_on * sampling_rate)), shadow))
        if len(shadow) < len(pulse):
            size_diff = len(pulse) - len(shadow)
            shadow = np.hstack((shadow, np.zeros(size_diff)))

        pulse = pulse + shadow

        pulse[np.where(pulse > 1.0)] = 1.0

    total_length = round(duration + params['onset'] + params['offset'],
                         10)  # N.B. Have to round here due to floating point representation problem

    return np.hstack((onset, pulse, offset)), np.linspace(0, total_length, int(total_length * sampling_rate))


def spec_time_pulse(sampling_rate, params):
    # Initial parameters
    frequency = params['frequency']
    p_times = params['pulse_times']
    p_length = params['pulse_length']
    target_duty = params['target_duty']
    amp_min = params['amp_min']
    amp_max = params['amp_max']
    shatter_frequency = params['shatter_frequency']

    if len(p_times) > 0:
        duration = np.max(p_times) + (p_length * 2.0)
    else:
        duration = 0.0

    # Generate guide clean pulse
    pulse = np.zeros(int(duration*sampling_rate))
    for pt in p_times:
        s = int(pt*sampling_rate)
        e = int((pt+p_length)*sampling_rate)
        pulse[s:e] = 1.0

    if params['invert']:
        pulse = 1.0 - pulse

    # Generate shattering guide
    t = np.linspace(0, duration, int(duration * sampling_rate))
    if (target_duty - amp_min) < (amp_max - target_duty):
        lower_duty_bound = amp_min
        upper_duty_bound = target_duty + (target_duty - amp_min)
    else:
        upper_duty_bound = amp_max
        lower_duty_bound = target_duty - (amp_max - target_duty)

    shattered_guide = []
    while len(shattered_guide) < len(pulse):
        rand_param = np.random.uniform(lower_duty_bound, upper_duty_bound)
        shattered_guide = np.hstack((shattered_guide, np.ones(int(sampling_rate / shatter_frequency)) * rand_param))

    shattered_guide = shattered_guide[0:int(sampling_rate*duration)]
    shattered_pulse = (np.array(signal.square(2 * np.pi * shatter_frequency * t, duty=shattered_guide)) / 2) + 0.5

    # Apply to guide clean pulse
    pulse = pulse * shattered_pulse
    if params['reverse']:
        pulse = pulse[::-1]

    # Attach onset and offset
    if params['inversion']:
        onset = np.ones(int(sampling_rate * params['onset']))
        offset = np.ones(int(sampling_rate * params['offset']))
    else:
        onset = np.zeros(int(sampling_rate * params['onset']))
        offset = np.zeros(int(sampling_rate * params['offset']))

    pulse = np.hstack((onset, pulse, offset))

    total_length = round(duration + params['onset'] + params['offset'], 10)
    t = np.linspace(0, total_length, int(total_length * sampling_rate))

    return pulse, t


def simple_pulse(sampling_rate, params):
    # Build main portion of pulse
    if params['fromDuty']:
        frequency = params['frequency']
        duty = params['duty']
    else:
        assert params['fromValues']
        frequency = 1.0 / (params['pulse_width'] + params['pulse_delay'])
        duty = params['pulse_width'] / (params['pulse_width'] + params['pulse_delay'])

    if params['fromLength']:
        duration = params['length']
    else:
        assert params['fromRepeats']
        if params['fromValues']:
            duration = (params['pulse_width'] + params['pulse_delay']) * params['repeats']
        else:
            assert params['fromDuty']
            duration = (1.0 / frequency) * params['repeats']

    if params['isClean']:
        pulse, t = square_pulse(sampling_rate, duration, frequency, duty, inverted=params['inversion'])
    else:
        assert params['isShatter']
        pulse, t = shatter_pulse(sampling_rate, duration, frequency, duty, params['shatter_frequency'],
                                 params['shatter_duty'], inverted=params['inversion'])

    # Attach onset and offset
    if params['inversion']:
        onset = np.ones(int(int(sampling_rate * params['onset'])))
        offset = np.ones(int(int(sampling_rate * params['offset'])))
    else:
        onset = np.zeros(int(int(sampling_rate * params['onset'])))
        offset = np.zeros(int(int(sampling_rate * params['offset'])))

    pulse = np.hstack((onset, pulse, offset))

    total_length = round(duration + params['onset'] + params['offset'], 10) # N.B. Have to round here due to floating point representation problem

    return pulse, np.linspace(0, total_length, int(total_length*sampling_rate))


def multi_simple_pulse(sampling_rate, global_onset, global_offset, params_list):
    longest_t = []
    pulses = list()

    for params in params_list:
        this_pulse, t = simple_pulse(sampling_rate, params)
        pulses.append(this_pulse)
        if len(t) > len(longest_t):
            longest_t = t

    pulse_matrix = np.zeros((len(pulses), len(longest_t) + (global_onset + global_offset) * sampling_rate))

    for p, pulse in enumerate(pulses):
        pulse_matrix[p][(global_onset * sampling_rate):(global_onset * sampling_rate)+len(pulse)] = pulse

    t = np.linspace(0, pulse_matrix.shape[1] / sampling_rate, pulse_matrix.shape[1])

    return pulse_matrix, t


def noise_pulse(sampling_rate, params):
    # Build main portion of pulse
    pulse_length = int(sampling_rate / params['frequency'])
    if params['fromLength']:
        duration = params['length']
    else:
        assert params['fromRepeats']
        duration = (params['repeats'] * pulse_length) / sampling_rate

    guide_pulse = []

    seed = params['seed']
    amp_min = params['amp_min']
    amp_max = params['amp_max']

    t = np.linspace(0, duration, int(sampling_rate * duration))
    np.random.seed(int(params['seed']))
    while len(guide_pulse) < len(t):
        rand_param = np.random.uniform(amp_min, amp_max)
        guide_pulse = np.hstack((guide_pulse, np.ones(pulse_length) * rand_param))

    guide_pulse = guide_pulse[0:int(sampling_rate*duration)]

    pulse = (np.array(signal.square(2 * np.pi * params['shatter_frequency'] * t, duty=guide_pulse)) / 2) + 0.5

    # Attach onset and offset
    if params['inversion']:
        onset = np.ones(int(sampling_rate * params['onset']))
        offset = np.ones(int(sampling_rate * params['offset']))
    else:
        onset = np.zeros(int(sampling_rate * params['onset']))
        offset = np.zeros(int(sampling_rate * params['offset']))

    total_length = round(duration + params['onset'] + params['offset'], 10)
    return np.hstack((onset, pulse, offset)), np.linspace(0, total_length, total_length * sampling_rate)


def plume_pulse(sampling_rate, params):
    plume = sio.loadmat(params['data_path'])
    plume = plume['plume'][0]

    # resample to match sampling rate
    resampled = signal.resample(plume, int(len(plume)*(sampling_rate / params['data_fs'])))
    # zero out negative values
    resampled[resampled < 0] = 0
    # normalise
    resampled = (resampled - min(resampled)) / (max(resampled) - min(resampled))
    resampled = resampled * params['target_max']

    duration = len(resampled) / sampling_rate
    t = np.linspace(0, duration, int(sampling_rate * duration))
    pulse = (np.array(signal.square(2 * np.pi * params['shatter_frequency'] * t, duty=resampled)) / 2) + 0.5

    # Attach onset and offset
    if params['inversion']:
        onset = np.ones(int(sampling_rate * params['onset']))
        offset = np.ones(int(sampling_rate * params['offset']))
    else:
        onset = np.zeros(int(sampling_rate * params['onset']))
        offset = np.zeros(int(sampling_rate * params['offset']))

    total_length = round(params['onset'] + params['offset'] + len(pulse) / sampling_rate, 10)
    return np.hstack((onset, pulse, offset)), np.linspace(0, total_length, int(total_length * sampling_rate))

def anti_plume_pulse(sampling_rate, params):
    plume = sio.loadmat(params['data_path'])
    plume = plume['plume'][0]

    # resample to match sampling rate
    resampled = signal.resample(plume, int(len(plume)*(sampling_rate / params['data_fs'])))
    # zero out negative values
    resampled[resampled < 0] = 0
    # normalise
    resampled = (resampled - min(resampled)) / (max(resampled) - min(resampled))
    resampled = resampled * params['target_max']

    duration = len(resampled) / sampling_rate
    t = np.linspace(0, duration, int(sampling_rate * duration))
    pulse = (np.array(signal.square(2 * np.pi * params['shatter_frequency'] * t, duty=resampled)) / 2) + 0.5
    anti_pulse = [1 - i for i in pulse]

    # Attach onset and offset
    if params['inversion']:
        onset = np.ones(int(int(sampling_rate * params['onset'])))
        offset = np.ones(int(int(sampling_rate * params['offset'])))
    else:
        onset = np.zeros(int(int(sampling_rate * params['onset'])))
        offset = np.zeros(int(int(sampling_rate * params['offset'])))

    total_length = round(params['onset'] + params['offset'] + len(pulse) / sampling_rate, 10)
    return np.hstack((onset, anti_pulse, offset)), np.linspace(0, total_length, int(total_length * sampling_rate))


def binary_pulse(sampling_rate, params):
    '''
    Creates a pulse from a value passed to it
    '''

    binary = params['value_to_binarise']

    assert binary >= 0, 'Binary minimum should be zero'
    assert binary <= 2**params['num_of_bins'] - 1, 'Binary maximum should be less than %s' % str(2**params['num_of_bins'])
    bin_width = params['bin_size']*sampling_rate
    binned = bin(binary)[2:]
    while len(binned) < params['num_of_bins']:
        binned = '0' + binned
    bin_output = []
    bin_pulse = [int(i) for i in binned for j in range(int(bin_width))]


    duration = len(bin_pulse) / sampling_rate
    t = np.linspace(0, duration, int(sampling_rate * duration))

    if 'isShatter' in params:
        if params['isShatter'] is True:
            if params['inversion']:
                shatter_duty = 1 - params['shatter_duty']
            else:
                shatter_duty = params['shatter_duty']
            shattered_pulse = (np.array(signal.square(2 * np.pi * params["shatter_frequency"] * t, duty=shatter_duty)) / 2) + 0.5
            bin_pulse = bin_pulse * shattered_pulse

    bin_pulse = np.array(bin_pulse)
    if params['inversion']:
        onset = np.ones(int(sampling_rate * params['onset']))
        offset = np.ones(int(sampling_rate * params['offset']))
        bin_pulse = bin_pulse * -1 + 1
    else:
        onset = np.zeros(int(sampling_rate * params['onset']))
        offset = np.zeros(int(sampling_rate * params['offset']))

    total_length = round(params['onset'] + params['offset'] + len(bin_pulse)/sampling_rate, 10)
    return np.hstack((onset, bin_pulse, offset)), np.linspace(0, total_length, int(total_length * sampling_rate))


def dummy_noise_pulse(sampling_rate, params):
    # Build main portion of pulse
    pulse_length = int(sampling_rate / params['frequency'])
    if params['fromLength']:
        duration = params['length']
    else:
        assert params['fromRepeats']
        duration = (params['repeats'] * pulse_length) / sampling_rate

    guide_pulse = []

    seed = params['seed']
    amp_min = params['amp_min']
    amp_max = params['amp_max']

    t = np.linspace(0, duration, int(sampling_rate * duration))

    guide_pulse = np.ones(sampling_rate*duration)

    pulse = (np.array(signal.square(2 * np.pi * params['shatter_frequency'] * t, duty=guide_pulse)) / 2) + 0.5

    # Attach onset and offset
    if params['inversion']:
        onset = np.ones(int(sampling_rate * params['onset']))
        offset = np.ones(int(sampling_rate * params['offset']))
    else:
        onset = np.zeros(int(sampling_rate * params['onset']))
        offset = np.zeros(int(sampling_rate * params['offset']))

    total_length = round(duration + params['onset'] + params['offset'], 10)
    return np.hstack((onset, pulse, offset)), np.linspace(0, total_length, int(total_length * sampling_rate))


def multi_noise_pulse(sampling_rate, global_onset, global_offset, params_list):
    longest_t = []
    pulses = list()

    for params in params_list:
        this_pulse, t = noise_pulse(sampling_rate, params)
        pulses.append(this_pulse)
        if len(t) > len(longest_t):
            longest_t = t

    pulse_matrix = np.zeros((len(pulses), len(longest_t) + (global_onset + global_offset) * sampling_rate))

    for p, pulse in enumerate(pulses):
        pulse_matrix[p][(global_onset * sampling_rate):(global_onset * sampling_rate) + len(pulse)] = pulse

    t = np.linspace(0, pulse_matrix.shape[1] / sampling_rate, pulse_matrix.shape[1])

    return pulse_matrix, t


# params = {'fromLength': True, 'fromRepeats': False, 'frequency': 20, 'repeats': 5, 'seed': 1, 'amp_min': 0.1,
#           'amp_max': 0.9, 'shatter_frequency': 500, 'length': 1, 'onset': 0.1, 'offset': 0.1}
#
# pulse, t = dummy_noise_pulse(10000, params)

# plt.plot(t, pulse)
# plt.show()

# Testing - random shatter
# pulse, t = random_shatter_pulse(20000.0, 2.0, 5.0, 0.5, 200.0, 1.0, 0.1, 0.9)
# print(sum(pulse) / len(pulse))
# plt.plot(t, pulse)
# plt.xlim((-0.1, 2.1))
# plt.ylim((-0.1, 1.1))
# plt.show()
