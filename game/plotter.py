import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
from IPython import display

plt.ion()

def plot(scores, mean_scores):
    plt.clf()
    plt.title('Training')
    plt.xlabel('Number of games')
    plt.ylabel('Score')
    plt.plot(scores)
    plt.plot(mean_scores)
    plt.ylim(ymin=0)
    plt.text(len(scores)-1, scores[-1], str(scores[-1]))
    plt.text(len(mean_scores)-1, mean_scores[-1], str(mean_scores[-1]))

    ax = plt.gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))


    plt.pause(0.001)