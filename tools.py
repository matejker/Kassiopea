import numpy as np


def plot_roc(good_pdf, bad_pdf, ax, x, plot_random=True):
    total_bad = np.sum(bad_pdf)
    total_good = np.sum(good_pdf)

    cum_TP = 0
    cum_FP = 0

    TPR_list = [0]
    FPR_list = [0]

    for i in range(len(x)):
        # if bad_pdf[i] > 0:
        cum_TP += bad_pdf[len(x) - 1 - i]
        cum_FP += good_pdf[len(x) - 1 - i]
        FPR = cum_FP / total_good
        TPR = cum_TP / total_bad
        TPR_list.append(TPR)
        FPR_list.append(FPR)

    # Plotting final ROC curve
    ax.plot(FPR_list, TPR_list)

    if plot_random:
        ax.plot(x, x, "--")

    ax.set_xlim([0, 1])
    ax.set_ylim([0, 1])
    ax.set_title("ROC Curve", fontsize=14)
    ax.set_ylabel('TPR', fontsize=12)
    ax.set_xlabel('FPR', fontsize=12)
    ax.grid()


def plot_pdf(good_pdf, bad_pdf, ax, x):
    ax.plot(x, good_pdf, "r", alpha=0.5)
    ax.plot(x, bad_pdf, "g", alpha=0.5)
    ax.set_xlim([0, 1])
    ax.set_ylim([0, 7.5])
    ax.set_title("Probability Distribution", fontsize=14)
    ax.set_ylabel("Counts", fontsize=12)
    ax.set_xlabel("P(X='bad')", fontsize=12)
    ax.legend(["Blacklisted", "Whitelisted"])


def round_acc(x):
    return round((x + 1.) / 2, 1)


def round_acc2(x):
    x = round(x, 1)
    if x == 0.5:
        return 0.5
    else:
        return round(x, 0)