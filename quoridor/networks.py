import logging, os
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import os
from tensorflow.keras.layers import (Dense, Activation, Input, Conv2D, Add, LeakyReLU,
                                     BatchNormalization, GlobalAveragePooling2D,
                                     )
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.regularizers import l2
import tensorflow.keras.backend as K
from tensorflow.keras.callbacks import LearningRateScheduler, LambdaCallback
from logs import Log
import config


class Network:
    '''

    Attribute
    ----------
    input_shape : tupple
        Network's input shape.
    output_shape : int
        Network's output shape
    filters : int, list
        Conv2d's filter(s).
    kernel_sizes : int, list
        Conv2d's kernel_size(s).
    strides : int, list
        Conv2d's stride(s).
    initializers : int, list
        Conv2d's initializer(s).
    regularizers : int, list
        Conv2d's regularizer(s).
    res_num : int
        ResNet's layer num.
    args : dict
        This network's attribute names.
    log : Log
        Logging class.
    model : tensorflow.keras.model.Model
        Network's model.
    cwd : str
        Current directory string.

    '''
    def __init__(self,
                 load = False,
                 load_file = 'best_network.h5',
                 cwd = None,
                 ):
        '''

        Attribute
        ----------
        res_num : int
            ResNet's layer num.
        load : bool
            Load model already exists.
        load_file : str
            Model's Paramator file name.
        cwd : int
            Current dirctory.

        '''
        self.input_shape = config.INPUT_SHAPE
        self.output_shape = config.OUTPUT_SHAPE
        self.filters = config.FILTER
        self.kernel_sizes = config.KERNEL
        self.strides = config.STRIDE
        self.initializers = config.INITIALIZER
        self.regularizers = config.REGULARIZER
        self.res_num = config.RES_NUM
        self.cwd = cwd
        self.args = set((
            'input_shape',
            'output_shape',
            'filters',
            'kernel_sizes',
            'strides',
            'initializers',
            'regularizers',
            'res_num',
            ))
        self.log = Log()

        if load:
            self.load_network(filename=load_file)
        else:
            self._num2list()
            self._build_model()
            self.clean()

    def _build_model(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        if self.cwd is None:
            path = os.path.abspath(os.path.join('networks', 'best_network.h5'))
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'networks', 'best_network.h5'))

        if os.path.exists(path):
            print('The Network is already exist. Try Loading.')
            self.load_network()
            return

        inputs = Input(shape=self.input_shape, name='Network_Input', )
        x = Conv2D(
            self.filters[0],
            self.kernel_sizes[0],
            strides=self.strides[0],
            padding='same',
            use_bias=False,
            kernel_initializer=self.initializers[0],
            kernel_regularizer=l2(self.regularizers[0]),
            )(inputs)
        x = BatchNormalization()(x)
        x = LeakyReLU(alpha=0.2)(x)

        for i in range(self.res_num):
            short_cut = x
            x = Conv2D(
                self.filters[i],
                self.kernel_sizes[i],
                strides=self.strides[i],
                padding='same',
                use_bias=False,
                kernel_initializer=self.initializers[i],
                kernel_regularizer=l2(self.regularizers[i]),
                )(x)
            x = BatchNormalization()(x)
            x = LeakyReLU(alpha=0.2)(x)
            x = Conv2D(
                self.filters[i],
                self.kernel_sizes[i],
                strides=self.strides[i],
                padding='same',
                use_bias=False,
                kernel_initializer=self.initializers[i],
                kernel_regularizer=l2(self.regularizers[i]),
                )(x)
            x = BatchNormalization()(x)
            x = Add()([x, short_cut])
            x = LeakyReLU(alpha=0.2)(x)

        x = GlobalAveragePooling2D()(x)
        policy = Dense(
            self.output_shape,
            kernel_regularizer=l2(self.regularizers[-1]),
            )(x)
        policy = Activation(
            'softmax',
            name='Policy_Output',
            )(policy)

        value = Dense(
            1,
            kernel_regularizer=l2(self.regularizers[-1]),
            )(x)
        value = Activation(
            'tanh',
            name='Value_Output',
            )(value)

        self.model = Model(inputs=inputs, outputs=[policy, value])
        self.model.compile(
            optimizer='adam',
            loss=['categorical_crossentropy', 'mse'],
            )

        if self.cwd is None:
            path = os.path.abspath('networks')
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'networks'))
        os.makedirs(path, exist_ok=True)
        self.save_network()

    def _num2list(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        args = set((
            'filters',
            'kernel_sizes',
            'strides',
            'initializers',
            'regularizers',
            ))
        for key in self.__dict__.keys():
            member = getattr(self, key)
            if isinstance(member, (list, tuple, np.ndarray)) or key not in args:
                continue
            setattr(self, key, [member] * (self.res_num + 1))

    def _load_history(self, epoch):
        '''

        Parameters
        ----------
        e : int
            History file's index.

        Returns
        -------
        None.

        '''
        if self.cwd is None:
            path_i = os.path.abspath(os.path.join('histories_input', str(epoch)))
            path_p = os.path.abspath(os.path.join('histories_policy', str(epoch)))
            path_v = os.path.abspath(os.path.join('histories_value', str(epoch)))
        else:
            path_i = os.path.abspath(os.path.join(self.cwd, 'histories_input', str(epoch)))
            path_p = os.path.abspath(os.path.join(self.cwd, 'histories_policy', str(epoch)))
            path_v = os.path.abspath(os.path.join(self.cwd, 'histories_value', str(epoch)))

        for i in range(config.SELFMATCH):
            if i == 0:
                self.history_input = np.load(os.path.join(path_i, '{}.npy'.format(i)))
                self.history_policy = np.load(os.path.join(path_p, '{}.npy'.format(i)))
                self.history_value = np.load(os.path.join(path_v, '{}.npy'.format(i)))
            else:
                load_i = np.load(os.path.join(path_i, '{}.npy'.format(i)))
                load_p = np.load(os.path.join(path_p, '{}.npy'.format(i)))
                load_v = np.load(os.path.join(path_v, '{}.npy'.format(i)))
                self.history_input = np.vstack([self.history_input, load_i])
                self.history_policy = np.vstack([self.history_policy, load_p])
                self.history_value = np.append(self.history_value, load_v)

    def clean(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        K.clear_session()
        self.model = None

    def train(self, cycle_epoch):
        '''

        Parameters
        ----------
        cycle_epoch : int
            How many epochs done for overall training.

        Returns
        -------
        None.

        '''
        def decay(e):
            if e < int(config.EPOCHS * 0.5):
                lr = 0.02
            elif e < int(config.EPOCHS * 0.8):
                lr = 0.002
            else:
                lr = 0.0002

            return lr

        lr_decay = LearningRateScheduler(decay)
        print_callback = LambdaCallback(
            on_epoch_begin = lambda epoch, logs: print('\rTrain: {}/{}'.format(epoch + 1, config.EPOCHS), end='')
        )

        self.load_network()
        self._load_history(cycle_epoch)
        hist = self.model.fit(
            self.history_input,
            [self.history_policy, self.history_value],
            batch_size = config.BATCH_SIZE,
            epochs = config.EPOCHS,
            verbose = False,
            callbacks = [lr_decay, print_callback],
        )
        print()
        self.log.log_loss(hist, cycle_epoch)
        self.save_network(filename='current_network.h5')

    def save_network(self, filename='best_network.h5'):
        '''

        Parameters
        ----------
        filename : str
            Model file's name. This should be 'best_network.h5' or 'current_network.h5'.

        Returns
        -------
        None.

        '''
        if self.cwd is None:
            path = os.path.abspath(os.path.join('networks', filename))
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'networks', filename))

        if self.model:
            self.model.save(path)

    def load_network(self, filename='best_network.h5',):
        '''

        Parameters
        ----------
        filename : str
            Model file's name. This should be 'best_network.h5' or 'current_network.h5'.

        Returns
        -------
        None.

        '''
        if self.cwd is None:
            path = os.path.abspath(os.path.join('networks', filename))
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'networks', filename))
        self.model = load_model(path)
