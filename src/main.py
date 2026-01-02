#!/usr/bin/env python3

import logging
import os
import sys

import flask
import numpy as np
import pandas as pd

from prelude import MASK_MIN

APP = flask.Flask(__name__)

RNG = np.random.default_rng()

WEIGHT_RATE = float(sys.argv[2])

CORRECT_STEP = int(sys.argv[3])
INCORRECT_STEP = CORRECT_STEP * 3

CONSEC_REQ = int(sys.argv[4])

HISTORY = []

HISTORY_CAP = 10
HISTORY_MIN = 6


def choice(memory, previous=None):
    memory["weight"] = 0.0

    rows = memory["mask"]

    if previous is not None:
        rows &= memory.question != previous

    consecs = np.flip(np.sort(memory.loc[rows, "consec"].unique()))
    weights = np.empty(len(consecs))

    weight = 1
    for i in range(len(consecs)):
        weights[i] = weight
        weight *= WEIGHT_RATE

    weights /= sum(weights)

    selected = (
        memory.loc[(memory.consec == RNG.choice(consecs, 1, p=weights)[0]) & rows]
        .sample(n=1, random_state=RNG)
        .iloc[0]
    )

    weights = (
        memory.loc[rows]
        .groupby("consec")
        .agg(size=("question", "count"))
        .merge(
            pd.DataFrame({"consec": consecs, "weight": weights}),
            on="consec",
            how="right",
            validate="1:1",
        )
    )
    assert weights.notnull().values.all()

    weights["size"] /= weights["size"].sum()

    print()
    print(
        memory.loc[(memory.consec < CONSEC_REQ) & memory["mask"], ["question", "consec"]]
        .sort_values("consec")
        .to_string(index=False),
    )

    k = memory["mask"].sum()
    print(
        round((CONSEC_REQ <= memory.loc[memory["mask"], "consec"]).sum() / k, 3),
        k,
        round(k / len(memory), 3),
    )

    return {
        "question": selected.question,
        "answer": selected.answer,
        "consec": int(selected.consec),
        "weights": weights.to_dict(orient="records"),
    }


@APP.route("/next", methods=["POST"])
def next():
    body = flask.request.get_json()

    path = os.path.join("data", f"{sys.argv[1]}.csv")
    memory = pd.read_csv(path)

    if body is None:
        return choice(memory)

    rows = memory.question == body["previous"]
    assert rows.sum() == 1, body["previous"]

    correct = body["response"] is None

    HISTORY.insert(0, correct)

    if HISTORY_CAP < len(HISTORY):
        HISTORY.pop()
        assert len(HISTORY) == HISTORY_CAP, HISTORY

    if correct:
        memory.loc[rows, "consec"] += 1

        rows = CONSEC_REQ <= memory.consec
        memory.loc[rows, "consec"] = memory.loc[rows, "consec"].map(
            {
                consec: i + CONSEC_REQ
                for i, consec in enumerate(np.sort(memory.loc[rows, "consec"].unique()))
            },
        )

        if (not (memory["mask"].all())) and (
            CONSEC_REQ <= memory.loc[memory["mask"], "consec"]
        ).all():
            memory["mask"].values[: memory["mask"].sum() + CORRECT_STEP] = True

    else:
        memory.loc[rows | (memory["mask"] & (memory.answer == body["response"])), "consec"] = 0

        if (len(HISTORY) == HISTORY_CAP) and (sum(HISTORY) < HISTORY_MIN):
            HISTORY.clear()
            memory["mask"].values[max(MASK_MIN, memory["mask"].sum() - INCORRECT_STEP) :] = False

    memory.to_csv(path, index=False)

    return choice(memory, body["previous"])


@APP.route("/")
def home():
    return flask.render_template("home.html")


def main():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    APP.run(host="0.0.0.0", port="8000", debug=False)


if __name__ == "__main__":
    main()
