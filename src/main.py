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
assert 1.0 < WEIGHT_RATE, WEIGHT_RATE

CORRECT_STEP = int(sys.argv[3])
assert 0 < CORRECT_STEP, CORRECT_STEP

INCORRECT_STEP = CORRECT_STEP * 3

CONSEC_REQ = int(sys.argv[4])
assert 0 < CONSEC_REQ, CONSEC_REQ

HISTORY_CAP = 10
assert 0 < HISTORY_CAP, HISTORY_CAP

HISTORY_MIN = 6
assert 0 < HISTORY_MIN, HISTORY_MIN

HISTORY_PENALTY = 0.1
assert HISTORY_PENALTY < 0.5, HISTORY_PENALTY

HISTORY = []


def choice(memory, previous=None):
    if previous is None:
        rows = memory["mask"]
    else:
        rows = memory["mask"] & (memory.question != previous)

    consecs = np.flip(np.sort(memory.loc[rows, "consec"].unique()))
    weights = np.empty(len(consecs))

    weight = 1
    for i in range(len(consecs)):
        weights[i] = weight
        weight *= WEIGHT_RATE

    weights /= sum(weights)

    subset = memory.loc[(memory.consec == RNG.choice(consecs, 1, p=weights)[0]) & rows].copy()
    subset["in_history"] = subset.question.isin([pair[0] for pair in HISTORY])

    if subset.in_history.nunique() == 1:
        selected = subset.sample(n=1, random_state=RNG).iloc[0]
    else:
        subset_weights = subset.groupby("in_history", as_index=False).agg(
            freq=("question", "nunique"),
        )
        subset_weights["weight"] = subset_weights.in_history.map(
            lambda in_history: HISTORY_PENALTY if in_history else 1.0 - HISTORY_PENALTY,
        )
        subset_weights.weight /= subset_weights.freq
        subset = subset.merge(subset_weights, on="in_history", how="left", validate="m:1")
        selected = subset.sample(n=1, weights=subset.weight, random_state=RNG).iloc[0]

    weights = (
        memory.loc[rows]
        .groupby("consec", as_index=False)
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

    HISTORY.insert(0, (body["previous"], correct))

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

        if (len(HISTORY) == HISTORY_CAP) and (sum([pair[1] for pair in HISTORY]) < HISTORY_MIN):
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
