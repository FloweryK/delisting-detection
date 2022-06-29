import os
import re
import utils
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from config import *


if __name__ == '__main__':
    # prepare metadata
    model = None
    targets = None

    # prepare empty metric list
    stat = {}

    # load stat
    fnames = os.listdir(TEST_ROOT)
    for fname in fnames:
        trial = int(re.findall('[0-9]+', fname)[0])
        file = utils.load(os.path.join(TEST_ROOT, fname))

        if (model is None) and (targets is None):
            model = file['model']
            targets = file['targets']

        epochs = file['log']
        for epoch, metrics in epochs.items():
            for metric, value in metrics.items():
                if metric in ('epoch', 'confusion_matrix'):
                    continue
                if metric not in stat:
                    stat[metric] = [[0 for _ in range(len(epochs))] for _ in range(len(fnames))]
                stat[metric][trial][int(epoch)] = value

    # prepare figure
    fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(2, 2, figsize=(10, 8))
    fig.suptitle('model=' + model)

    # ax1: plot loss
    train_loss = np.nanmean(stat['train_loss'], axis=0)
    test_loss = np.nanmean(stat['test_loss'], axis=0)

    ax1.plot(train_loss, label='loss (train)', c='tab:blue')
    ax1.plot(test_loss, label='loss (test)', c='tab:orange')

    ax1.set_title('BCE loss (100 Trials mean)')
    ax1.set_xlabel('epoch')
    ax1.grid()
    ax1.legend()

    # ax2: plot performance metrics
    precision = np.nanmean(stat['precision'], axis=0)
    recall = np.nanmean(stat['recall'], axis=0)
    f1 = np.nanmean(stat['f1'], axis=0)
    best_f1_idx, best_f1 = np.argmax(f1), np.max(f1)

    ax2.plot(precision, label='precision')
    ax2.plot(recall, label='recall')
    ax2.plot(f1, label='f1 score')
    ax2.plot(best_f1_idx, best_f1, 'ro')
    ax2.text(best_f1_idx, best_f1 + 0.025, 'maximum f1 = %.3f' % best_f1, c='red')

    ax2.set_title('performance metrics (100 Trials mean)')
    ax2.set_xlabel('epoch')
    ax2.set_yticks(np.arange(0, 1.05, 0.1))
    ax2.set_yticks(np.arange(0, 1.05, 0.025), minor=True)
    ax2.grid(which='minor', alpha=0.5)
    ax2.grid(which='major', alpha=1)
    ax2.set(ylim=[0.5, 1.05])
    ax2.legend(loc='lower right')

    # error histogram
    error = np.array(stat['error'])
    error = np.concatenate(error, axis=1)
    error = error

    ax3.set_title('error histogram (100 Trials Stack)')
    ax3.set_xlabel('absolute error (= |predict - label|)')
    ax3.set_xticks(np.arange(0, 1.0, 0.1), minor=True)
    ax3.set_yticks(np.arange(0, error.shape[1], error.shape[1] // 10))
    ax3.set_yticks(np.arange(0, error.shape[1], error.shape[1] // 20), minor=True)
    ax3.grid(which='minor', alpha=0.5)
    ax3.grid(which='major', alpha=1)
    hist = ax3.hist(error[0], range=(0, 1), bins=20)
    ax3.set(xlim=[0, 1], ylim=[0, error.shape[1]])

    # animation options
    # dot animation
    ax1_dot1 = ax1.plot([0], [train_loss[0]], marker='o', c='tab:blue')[0]
    ax1_dot2 = ax1.plot([0], [test_loss[0]], marker='o', c='tab:orange')[0]
    ax2_dot1 = ax2.plot([0], [precision[0]], marker='o', c='tab:blue')[0]
    ax2_dot2 = ax2.plot([0], [recall[0]], marker='o', c='tab:orange')[0]
    ax2_dot3 = ax2.plot([0], [f1[0]], marker='o', c='tab:green')[0]

    # animation step
    def animate(i):
        ax1_dot1.set_data([i], [train_loss[i]])
        ax1_dot2.set_data([i], [test_loss[i]])

        ax2_dot1.set_data([i], [precision[i]])
        ax2_dot2.set_data([i], [recall[i]])
        ax2_dot3.set_data([i], [f1[i]])

        ax3.cla()
        ax3.set_title('error histogram (100 Trials Stack)')
        ax3.set_xlabel('absolute error (= |predict - label|)')
        ax3.set_xticks(np.arange(0, 1.0, 0.1), minor=True)
        ax3.set_yticks(np.arange(0, error.shape[1], error.shape[1] // 10))
        ax3.set_yticks(np.arange(0, error.shape[1], error.shape[1] // 20), minor=True)
        ax3.grid(which='minor', alpha=0.4)
        ax3.grid(which='major', alpha=1)
        ax3.hist(error[i], range=(0, 1), bins=20)
        ax3.set(xlim=[0, 1], ylim=[0, error.shape[1]])

    anim = animation.FuncAnimation(fig, animate, interval=50, frames=error.shape[0])

    # show
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    # plt.show()

    # save animation
    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=60, metadata=dict(artist='Me'), bitrate=1800)
    os.makedirs(SUMMARY_DIR, exist_ok=True)
    anim.save(SUMMARY_DIR + '/' + TEST_ROOT.split('/')[-1] + '_total.mp4')



