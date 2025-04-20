import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
def plot(outputs, profits, budgets, ylabel=None):
    # figure, axis = plt.subplots(1, 1)
    # figure, axes = plt.figure(figsize=(10, 5))

    # plot cost savings vs budget (dollars saved (per unit time) as a function of budget)
    # axis[0, 0].plot(budgets, profits)
    # axis[0, 0].set_title("Annual Energy Cost vs Minimum Spending")

    # plot energy savings vs budget (BTUS saved (per unit time) as a function of budget)
    # axis[0, 1].plot(budgets, profits / cost_per_btu)
    # axis[0, 1].set_title("Energy Savings vs Budget")

    # plot chosen upgrades vs budget (upgrades chosen as a function of budget)
    budget_idx, bucket_numbers = np.where(outputs == 1)
    x_coordinates = [budgets[i] for i in budget_idx]
    # print(len(x_coordinates), len(rows), len(budgets), len(cols))
    # plt.xticks(ticks=budgets, rotation=90)  # force all ticks (warning: will clutter)

    plt.figure(figsize=(12, 6))
    # sns.heatmap(outputs, cmap="Greys", cbar=False)

    plt.xlabel("Budget ($)")
    plt.ylabel("Buckets Chosen")

    if ylabel:
        plt.yticks(ticks=np.arange(len(ylabel)) , labels=ylabel)
        plt.tight_layout()
        plt.subplots_adjust(bottom=0.1, top=0.95)
        plt.ylim(-0.5, len(ylabel) - 0.5)

        # plt.subplots_adjust(left=0.1)  


    plt.scatter(x_coordinates, bucket_numbers)

    # plt.show()
    plt.savefig('plot.png')