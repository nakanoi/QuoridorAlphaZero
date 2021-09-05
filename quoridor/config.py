'''
Hyper Paramators
'''
LENGTH = 9
WALLS = 10
BREAK = 96
INPUT_SHAPE = (LENGTH, LENGTH, 4 + WALLS * 2)
OUTPUT_SHAPE = 8 + 2 * (LENGTH - 1) * (LENGTH - 1)
# Train epoch for one cycle.
EPOCHS = 200 # Training epoch number
BATCH_SIZE = 256
FILTER = 256
KERNEL = 3
STRIDE = 1
INITIALIZER = 'he_normal'
REGULARIZER = 0.0005
RES_NUM = 19
# simulation times per one prediction.
SIMULATIONS = 300 #1600
GAMMA = 1.0
# self match times.
SELFMATCH = 200 # 25000
CYCLES = 200
PARALLEL_MATCH = 10
# Evaluation times per one evaluation
EVAL_MATCH = 10 # 400
C_PUT = 1.0
ALPHA = 0.35
EPS = 0.25
