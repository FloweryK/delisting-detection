import os
import numpy as np
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import random_split
from model import Model
from dataset import CompanyVectorData
from config import *
from torch.utils.tensorboard import SummaryWriter


def run(record=False):

    # TensorBoard
    # After run programs,
    # enter "tensorboard --logdir=runs",
    # and go to "http://localhost:6006/"
    writer = SummaryWriter()

    # dataset preparation
    companydata = CompanyVectorData(PROC_DIR, CACHE_MODEL_DIR)
    n_train = int(len(companydata) * R_TRAIN)
    n_test = len(companydata) - n_train
    trainset, testset = random_split(companydata, [n_train, n_test])

    # for the record
    '''
    history = {
        'model': W2V_MODEL_PATH,
        'targets': companydata.target_list,
        'log': {}
    }'''

    # model, loss, optimizer
    model = Model(companydata.dim, N_HIDDEN)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.00001)

    # train and test
    for epoch in range(N_EPOCH):
        # train
        running_loss = 0

        for i, data in enumerate(trainset):
            vector = data['x']
            label = data['y']

            predict = model(vector)
            loss = criterion(predict, label)
            running_loss += loss.item()

            loss.backward()
            optimizer.step()

        # mean reduction of loss
        running_loss *= 1 / len(trainset)

        # test
        running_loss_test = 0
        C = np.zeros([2, 2])
        error = []

        for data in testset:
            vector = data['x']
            label = data['y']

            predict = model(vector)
            loss = criterion(predict, label)
            running_loss_test += loss.item()

            # update confusion matrix and error
            C[int(round(predict.item() + 1)) - 1][int(label.item())] += 1
            error.append(abs(label.item() - predict.item()))

        # mean reduction of loss
        running_loss_test *= 1 / len(testset)

        # calculate metrics
        precision = C[1, 1] / np.sum(C[1, :])
        recall = C[1, 1] / np.sum(C[:, 1])
        f1 = 2 * (precision * recall) / (precision + recall)
        accuracy = (C[0, 0] + C[1, 1]) / np.sum(C)

        if epoch % 10 == 0:
            print('epoch: %i | loss: %f (train), %f (test)' % (epoch, running_loss, running_loss_test))
            print('confusion matrix:')
            print(C)
            print('precision:', precision)
            print('recall:', recall)
            print('f1 score:', f1)
            print('accuracy:', accuracy)
            print('abs error:', np.mean(error))
            print('')

        # TensorBoard
        writer.add_scalar('Loss/train', running_loss, epoch)
        writer.add_scalar('Loss/test', running_loss_test, epoch)
        writer.add_scalar('Accuracy/accuracy', accuracy, epoch)
        writer.add_scalar('Accuracy/error', np.mean(error), epoch)
        writer.add_scalar('ConfusionMatrix/precision', precision, epoch)
        writer.add_scalar('ConfusionMatrix/recall', recall, epoch)
        writer.add_scalar('ConfusionMatrix/f-score', f1, epoch)

        # for the record
        '''
        history['log'][epoch] = {
            'epoch': epoch,
            'train_loss': running_loss,
            'test_loss': running_loss_test,
            'confusion_matrix': C.tolist(),
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'accuracy': accuracy,
            'error': error
        }
    if record:
        return history'''


if __name__ == '__main__':
    run()