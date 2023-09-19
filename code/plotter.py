import matplotlib.pyplot as plt
import numpy as np

def plot(scores, epsilons, filename, real_scores, lines=None):
    plt.figure(figsize=(10, 5))
    fig, ax1 = plt.subplots()

    # Plot epsilon on the first y-axis (left)
    color = 'tab:blue'
    ax1.set_xlabel("Number of Games")
    ax1.set_ylabel("Exploitation", color=color)
    ax1.plot(epsilons, color=color)
    ax1.tick_params(axis='y', labelcolor=color)

    # Create a second y-axis (right) for the score
    ax2 = ax1.twinx()
    color = 'tab:red'
    ax2.set_ylabel('Score', color=color)
    
    N = len(scores)
    running_avg = np.empty(N)
    for t in range(N):
        running_avg[t] = np.mean(scores[max(0, t - 100):(t + 1)])
    
    ax2.scatter(range(N), running_avg, color=color, s=5)  # Use s parameter to set the dot size
    ax2.tick_params(axis='y', labelcolor=color)

    if lines is not None:
        for line in lines:
            ax1.axvline(x=line)

    # Save the plot as a PNG image
    plt.savefig(filename+'.png')

    # Create a new plot for real scores
    plt.figure(figsize=(10, 5))

    # Plot real scores
    plt.plot(range(len(real_scores)), real_scores, color='green')
    plt.xlabel("Millions of frames")
    plt.ylabel("Average Real Score")

    # Save the real scores plot as a separate PNG image
    plt.savefig(filename + '_real.png')

    # Close all figures
    plt.close('all')

