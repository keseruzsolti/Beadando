import math

from data.project.model import RentalDataset
import numpy as np
import matplotlib.pyplot as plt


def hany_kulonbozo(dataset: RentalDataset) -> None:
    properties = ["Person.age", "Job.job"]
    values = [
        [person.age for person in dataset.people],
        [job.job for job in dataset.jobs]

    ]

    total_length = [len(value) for value in values]
    unique_length = [len(set(value)) for value in values]

    x = np.arange(len(properties))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    series_total = ax.bar(x - width / 2, total_length, width, label="Total")
    series_unique = ax.bar(x + width / 2, unique_length, width, label="Unique")

    ax.set_ylabel("Number of entities")
    ax.set_title("Number of total and unique values")
    ax.set_xticks(x)
    ax.set_xticklabels(properties)
    ax.legend()

    ax.bar_label(series_total, padding=3)
    ax.bar_label(series_unique, padding=3)

    fig.tight_layout()

    plt.show()


def emberek_koronkent(dataset: RentalDataset) -> None:
    ages = list({person.age for person in dataset.people})
    values = [0 for _ in ages]
    for person in dataset.people:
        values[ages.index(person.age)] += 1

    x = np.arange(len(ages))  # the label locations
    width = 0.35  # the width of the bars

    fig, ax = plt.subplots()
    series = ax.bar(x - width / 2, values, width)

    # Add some text for labels, title and custom x-axis tick labels, etc.
    ax.set_ylabel("Number of people")
    ax.set_title("Number of people per ages")
    ax.set_xticks(x)
    ax.set_xticklabels(ages, rotation=90)
    ax.bar_label(series)

    ax.tick_params(axis="both", which="major", labelsize=10)

    fig.tight_layout()

    plt.show()


def distances_by_types(dataset: RentalDataset) -> None:
    types = list({address.address for address in dataset.addresses})
    values = [0 for _ in types]
    for transaction in dataset.transactions:
        values[types.index(transaction.address)] += 1

    fig1, ax = plt.subplots()
    ax.pie(values, labels=types, autopct="%1.1f%%", startangle=90, rotatelabels=True, pctdistance=0.7)
    ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.

    ax.tick_params(axis="both", which="major", labelsize=8)

    plt.show()


