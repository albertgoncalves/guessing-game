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

    if previous is not None:
        memory.loc[memory.question == previous, "mask"] = False

    consecs = np.sort(memory.loc[memory["mask"], "consec"].unique())

    weights = []
    weight = 1
    for consec in np.flip(consecs):
        rows = (memory.consec == consec) & memory["mask"]
        size = rows.sum()
        assert size != 0, consec
        memory.loc[rows, "weight"] = weight / size
        weights.append(
            {
                "consec": consec,
                "weight": weight,
                "size": size,
            },
        )
        weight *= WEIGHT_RATE

    weights = pd.DataFrame(weights)
    for column in ["weight", "size"]:
        weights[column] /= weights[column].sum()

    memory.weight /= memory.weight.sum()

    if previous is not None:
        memory.loc[memory.question == previous, "mask"] = True

    print(
        memory.loc[
            memory.consec.isin(consecs[consecs < CONSEC_REQ]) & memory["mask"],
            [
                "question",
                "consec",
                "weight",
            ],
        ]
        .sort_values("consec")
        .to_string(index=False),
    )

    k = memory["mask"].sum()
    print(
        round((CONSEC_REQ <= memory.loc[memory["mask"], "consec"]).sum() / k, 3),
        k,
        round(k / len(memory), 3),
    )

    selected = memory.sample(n=1, weights=memory.weight, random_state=RNG).iloc[0]
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
