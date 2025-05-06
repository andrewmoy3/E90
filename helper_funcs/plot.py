import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import plotly.express as px

plt.style.use("dark_background")
plt.rcParams.update({
    'font.size': 10,
    'font.family': 'JetBrains Mono',
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'text.color': 'white',
    'axes.labelcolor': 'white',
    'xtick.color': 'white',
    'ytick.color': 'white',
    'axes.edgecolor': 'white',
    'axes.titlecolor': 'white'
})

def plot(outputs, profits, budgets, title, filepath, ylabel=None):
    budget_idx, bucket_numbers = np.where(outputs == 1)
    x_coordinates = [budgets[i] for i in budget_idx]

    fig, ax = plt.subplots(figsize=(12, 6))
    plt.subplots_adjust(left=0.25, bottom=0.1, top=0.95)
    fig.patch.set_facecolor('#37474f')

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_frame_on(False)
    ax.grid(False)

    plt.ylabel("Buckets Chosen")
    plt.tick_params(axis='both', which='major', labelsize=10)

    ys = np.arange(len(ylabel)) 
    ax.hlines(y=ys, xmin=min(budgets), xmax=max(budgets),
            colors='white', linestyles='dashed', linewidth=1, alpha=0.2)
    plt.xlabel("Budget (Hundred Millions of $)")
    ax.set_title("Maximize " + title, loc='left', pad=10, color='white', fontsize=16)

    if ylabel:
        plt.yticks(ticks=np.arange(len(ylabel)) , labels=ylabel)
        plt.subplots_adjust(bottom=0.1, top=0.95)
        plt.ylim(-0.5, len(ylabel) - 0.5)
    plt.tight_layout()
    n_buckets = len(ylabel)
    marker_size = max(50, 500 / n_buckets)  

    plt.scatter(x_coordinates, bucket_numbers,  marker='s', s=marker_size, color='skyblue')
    # plt.scatter(x_coordinates, bucket_numbers,  marker='s', s=marker_size, color='#83c9ff')
    inset = 0.002  # try 0.002–0.005 for a fine-tuned fit
    fig.patches.append(
        patches.Rectangle(
            (0 + inset, 0 + inset), 1 - 2*inset, 1 - 2*inset,
            transform=fig.transFigure,
            facecolor='none',
            edgecolor='white',
            linewidth=2,
            zorder=1000
        )
    )
    plt.savefig(f'{filepath}.png')  
    plt.close('all')
    # plt.show()

def plot_bar_chart(bar_chart, dorm_names, title, filepath):
    plt.clf()
    fig, ax = plt.subplots()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_frame_on(False)
    ax.grid(False)
    fig.patch.set_facecolor('#37474f')
    bar_positions = range(len(bar_chart))
    plt.bar(bar_positions, bar_chart, color='skyblue', edgecolor='white')
    numeric_labels = [str(i + 1) for i in bar_positions]
    plt.xticks(ticks=bar_positions, labels=numeric_labels)
    plt.title(title, loc='left')

    legend_labels = [f"{i + 1}: {name}" for i, name in enumerate(dorm_names)]
    legend_text = "\n".join(legend_labels)
    plt.xlabel('Dorm')
    plt.ylabel('Frequency')
    props = dict(boxstyle='round', facecolor='#263238', edgecolor='white', alpha=0.9)
    ax.text(1.02, .8, legend_text, transform=ax.transAxes,
            fontsize=10, va='top', ha='left', bbox=props, color='white')
    fig.patches.append(
        patches.Rectangle(
            (0, 0), 1, 1,   
            transform=fig.transFigure,
            facecolor='none',
            edgecolor='white',
            linewidth=2,
            zorder=1000
        )
    )
    plt.tight_layout()
    plt.savefig(filepath, dpi=300)
    plt.close()

def plot_line_chart(item_values, items, budgets):
    # x = np.arange(len(item_values[0]))
    plt.clf()
    fig, ax = plt.subplots()
    fig.patch.set_facecolor('#37474f')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.set_frame_on(False)
    ax.grid(False)

    max_budget = budgets[-1]        
    xticks = np.arange(0, max(budgets), 0.25*100000000)
    plt.xticks(xticks, [f"{x/100000000}" for x in xticks])
    fig.patches.append(
        patches.Rectangle(
            (0, 0), 1, 1,
            transform=fig.transFigure,
            facecolor='none',
            edgecolor='white',
            linewidth=2,
            zorder=1000
        )
    )

    for row in item_values:
        #normalize row
        row = row / np.max(row)
        plt.plot(budgets, row)
    plt.xlabel("Budget (Hundred Millions of $)")
    plt.ylabel("Value")
    plt.title("Line Graph of Savings")
    plt.legend([f"{items[i]} Savings" for i in range(len(item_values))])
    plt.grid(True)
    plt.savefig("./outputs/line_graph.png")