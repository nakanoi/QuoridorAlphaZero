import logging, os
logging.disable(logging.WARNING)
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import numpy as np
import os
import pickle
from tensorflow.keras.layers import (Dense, Activation, Input, Conv2D, Add, LeakyReLU,
                                     BatchNormalization, GlobalAveragePooling2D,
                                     )
from tensorflow.keras.models import Model, load_model
from tensorflow.keras.regularizers import l2
import tensorflow.keras.backend as K
from tensorflow.keras.callbacks import LearningRateScheduler, LambdaCallback
from logs import Log


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
                 input_shape = None,
                 output_shape = None,
                 filters = None,
                 kernel_sizes = None,
                 strides = None,
                 initializers = None,
                 regularizers = None,
                 res_num = None,
                 load = False,
                 load_file = 'best_network.h5',
                 cwd = None,
                 ):
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
        load : bool
            Load model already exists.
        load_file : str
            Model's Paramator file name.
        cwd : int
            Current dirctory.

        '''
        self.input_shape = input_shape
        self.output_shape = output_shape
        self.filters = filters
        self.kernel_sizes = kernel_sizes
        self.strides = strides
        self.initializers = initializers
        self.regularizers = regularizers
        self.res_num = res_num
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
            self._load_members()
        else:
            self._num2list()
            self._build_model()
            self._save_members()
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

    def _save_members(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        if self.cwd is None:
            path = os.path.abspath('networks')
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'networks'))
        os.makedirs(path, exist_ok=True)
        members = {}

        for key in self.__dict__.keys():
            member = getattr(self, key)
            if key in self.args:
                members[key] = member

        if self.cwd is None:
            path = os.path.abspath(os.path.join('networks', 'member.h5'))
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'networks', 'member.h5'))

        with open(path, 'wb') as f:
            pickle.dump(members, f)

    def _load_members(self):
        '''

        Parameters
        ----------
        None.

        Returns
        -------
        None.

        '''
        if self.cwd is None:
            path = os.path.abspath(os.path.join('networks', 'member.h5'))
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'networks', 'member.h5'))

        with open(path, 'rb') as f:
            members = pickle.load(f)

        for k, v in members.items():
            setattr(self, k, v)

    def _load_history(self, e):
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
            path = os.path.abspath(os.path.join('histories_input', '{}.history'.format(e)))
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'histories_input', '{}.history'.format(e)))
        with open(path, 'rb') as f:
            self.history_input = pickle.load(f)

        if self.cwd is None:
            path = os.path.abspath(os.path.join('histories_policy_value', '{}.history'.format(e)))
        else:
            path = os.path.abspath(os.path.join(self.cwd, 'histories_policy_value', '{}.history'.format(e)))
        with open(path, 'rb') as f:
            self.history_policy_value = pickle.load(f)

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

    def train(self, epochs, batch_size, cycle_epoch):
        '''

        Parameters
        ----------
        epoches : int
            Training epoch number.
        batch_size : int
            Training batch size.
        cycle_epoch : int
            How many epochs done for overall training.

        Returns
        -------
        None.

        '''
        def decay(epoch):
            if epoch < int(epochs * 0.5):
                lr = 0.02
            elif epoch < int(epochs * 0.8):
                lr = 0.002
            else:
                lr = 0.0002

            return lr

        lr_decay = LearningRateScheduler(decay)
        print_callback = LambdaCallback(
            on_epoch_begin = lambda epoch, logs: print('\rTrain: {}/{}'.format(epoch + 1, epochs), end='')
        )

        self._load_history(cycle_epoch)
        xs = self.history_input
        policy, value = zip(*self.history_policy_value)
        policy = np.array(policy)
        value = np.array(value)

        hist = self.model.fit(
            xs,
            [policy, value],
            batch_size = batch_size,
            epochs = epochs,
            verbose = False,
            callbacks = [lr_decay, print_callback],
        )
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
        self._load_members()
