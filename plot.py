import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
def plot(outputs, profits, budgets, title, ylabel=None):
    budget_idx, bucket_numbers = np.where(outputs == 1)
    x_coordinates = [budgets[i] for i in budget_idx]
    plt.figure(figsize=(12, 6))
    plt.xlabel("Budget ($)")
    plt.ylabel("Buckets Chosen")
    if ylabel:
        plt.yticks(ticks=np.arange(len(ylabel)) , labels=ylabel)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1, top=0.95)
        plt.ylim(-0.5, len(ylabel) - 0.5)
    plt.scatter(x_coordinates, bucket_numbers)
    plt.savefig(f'outputs/{title}.png')
    # plt.show()