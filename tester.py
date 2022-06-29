import os
import datetime
import utils
import trainer
from config import *


if __name__ == '__main__':
    os.makedirs(TEST_DIR)

    for trial in range(N_TEST):
        print('====== TRIAL: %i ======' % trial)
        history = trainer.run(record=True)
        utils.save(history, os.path.join(TEST_DIR, 'trial_%04i' % trial + '.json'))
