#!/usr/bin/env python3

import logging
import os.path
import pickle
import sys

import flask
import numpy as np
import pandas as pd

APP = flask.Flask(__name__)

RNG = np.random.default_rng()


def choice(memory, previous=None):
    correct = np.empty(len(memory["table"]))
    incorrect = np.empty(len(memory["table"]))
    for i in range(len(memory["table"])):
        correct[i] = sum(memory["results"][i])
        incorrect[i] = len(memory["results"][i]) - correct[i]

    weights = (incorrect + 1) / (correct + incorrect + 1)
    weights[memory["mask"] :] = 0

    if previous is not None:
        weights[memory["index"][previous]] = 0

    weights **= 4
    weights /= weights.sum()

    snapshot = pd.DataFrame(
        {
            "question": [item["question"] for item in memory["table"]],
            "correct": correct,
            "incorrect": incorrect,
            "streak": memory["streak"],
        },
    )
    snapshot["total"] = snapshot.correct + snapshot.incorrect
    snapshot["rate"] = snapshot.correct / snapshot.total
    snapshot["weight"] = weights

    snapshot.to_csv(os.path.join("out", "snapshot.csv"))

    return RNG.choice(memory["table"], size=1, p=weights, shuffle=False)[0]


@APP.route("/next", methods=["POST"])
def next():
    body = flask.request.get_json()

    path = os.path.join("data", f"{sys.argv[1]}.pkl")

    with open(path, "rb") as file:
        memory = pickle.load(file)

    if body is None:
        return choice(memory)

    if body["response"] is None:
        memory["results"][memory["index"][body["previous"]]].append(True)
        memory["streak"][memory["index"][body["previous"]]] += 1
    else:
        memory["results"][memory["index"][body["previous"]]].append(False)
        memory["streak"][memory["index"][body["previous"]]] = 0

    if np.all(3 <= memory["streak"][: memory["mask"]]):
        memory["mask"] += 10

    with open(path, "wb") as file:
        pickle.dump(memory, file)

    return choice(memory, body["previous"])


@APP.route("/")
def home():
    return flask.render_template("home.html")


def main():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    APP.run(host="0.0.0.0", port="8000", debug=False)


if __name__ == "__main__":
    main()
