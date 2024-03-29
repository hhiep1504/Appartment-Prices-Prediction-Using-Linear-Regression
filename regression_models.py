import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import *
from sklearn.linear_model import *
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import RandomForestRegressor

# import the dataset.
data = pd.read_csv("dataset.csv")
x = data.drop("price", axis=1)
y = data["price"]
# split the dataset in to training and testing set
x_train, x_test, y_train, y_test = train_test_split(
    x, y, test_size=0.2, random_state=28
)


def ridge_regression(x_train, x_test, y_train, y_test, n):
    model = Ridge(alpha=n / 10)

    # train the model
    model.fit(x_train, y_train)

    # calculate the MAPE
    y_pred = model.predict(x_test)
    y_pred_rounded = [round(result, 2) for result in y_pred]
    mape = float(
        "{:.2f}".format(100 * mean_absolute_percentage_error(y_test, y_pred_rounded))
    )

    return y_pred_rounded, mape


def lasso_regression(x_train, x_test, y_train, y_test, n):
    model = Lasso(alpha=n / 10)

    # train the model
    model.fit(x_train, y_train)

    # calculate the MAPE
    y_pred = model.predict(x_test)
    y_pred_rounded = [round(result, 2) for result in y_pred]
    mape = float(
        "{:.2f}".format(100 * mean_absolute_percentage_error(y_test, y_pred_rounded))
    )

    return y_pred_rounded, mape


def k_neighbor_regression_unweighted(x_train, x_test, y_train, y_test, n):
    model = KNeighborsRegressor(n_neighbors=n, weights="uniform")

    # train the model
    model.fit(x_train, y_train)

    # calculate the MAPE
    y_pred = model.predict(x_test)
    y_pred_rounded = [round(result, 2) for result in y_pred]
    mape = float(
        "{:.2f}".format(100 * mean_absolute_percentage_error(y_test, y_pred_rounded))
    )

    return y_pred_rounded, mape


def k_neighbor_regression_weighted(x_train, x_test, y_train, y_test, n):
    model = KNeighborsRegressor(n_neighbors=n, weights="distance")

    # train the model
    model.fit(x_train, y_train)

    # calculate the MAPE
    y_pred = model.predict(x_test)
    y_pred_rounded = [round(result, 2) for result in y_pred]
    mape = float(
        "{:.2f}".format(100 * mean_absolute_percentage_error(y_test, y_pred_rounded))
    )

    return y_pred_rounded, mape


def random_forest_regression(x_train, x_test, y_train, y_test, n):
    model = RandomForestRegressor(max_depth=n)

    # train the model
    model.fit(x_train, y_train)

    # calculate the MAPE
    y_pred = model.predict(x_test)
    y_pred_rounded = [round(result, 2) for result in y_pred]
    mape = float(
        "{:.2f}".format(100 * mean_absolute_percentage_error(y_test, y_pred_rounded))
    )

    return y_pred_rounded, mape


# plot graphs
def lr_graph():
    lr_result = []

    for i in range(1, 21):
        lr_result.append(
            [
                i,
                ridge_regression(x_train, x_test, y_train, y_test, i)[1],
                lasso_regression(x_train, x_test, y_train, y_test, i)[1],
            ]
        )

    constant = [row[0] / 10 for row in lr_result]
    ridge = [row[1] for row in lr_result]
    lasso = [row[2] for row in lr_result]

    plt.plot(constant, ridge, label="Ridge")
    plt.plot(constant, lasso, label="LASSO")
    plt.legend()
    plt.title("Figure 1. Accuracy of Ridge and LASSO regression")
    plt.xlabel("λ")
    plt.ylabel("Mean Absolute Percentage Error (%)")
    plt.show()


def knr_graph():
    knr_result = []

    for i in range(1, 51):
        knr_result.append(
            [
                i,
                k_neighbor_regression_unweighted(x_train, x_test, y_train, y_test, i)[
                    1
                ],
                k_neighbor_regression_weighted(x_train, x_test, y_train, y_test, i)[1],
            ]
        )

    k = [row[0] for row in knr_result]
    knru = [row[1] for row in knr_result]
    knrw = [row[2] for row in knr_result]
    # plot
    plt.plot(k, knru, label="Uniform weight")
    plt.plot(k, knrw, label="Distance weight")
    plt.legend()
    plt.title("Figure 2. Accuracy of k-nearest neighbors regression using Euclidean distance")
    plt.xlabel("k")
    plt.ylabel("Mean Absolute Percentage Error (%)")
    plt.show()


def rfr_graph():
    rfr_result = []

    for i in range(2, 101):
        rfr_result.append(
            [i, random_forest_regression(x_train, x_test, y_train, y_test, i)[1]]
        )

    max_depth = [row[0] for row in rfr_result]
    rfr = [row[1] for row in rfr_result]

    plt.plot(max_depth, rfr)
    plt.title("Figure 3. Accuracy of random forest regression using 100 tree")
    plt.xlabel("Maximum depth of a tree")
    plt.ylabel("Mean Absolute Percentage Error (%)")
    plt.show()


def main():
    a = input(
        "Press a number to see the graph. "
        "[1] Linear Regression; [2] K-nearest Neighbors Regression; [3] Random Forest Regression: "
    )
    if a == "1":
        lr_graph()
    if a == "2":
        knr_graph()
    if a == "3":
        rfr_graph()


main()
