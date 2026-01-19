#!/usr/bin/env python3

import logging
import os
import sys

import flask
import numpy as np
import pandas as pd

APP = flask.Flask(__name__)

RNG = np.random.default_rng()

WEIGHT_RATE = float(sys.argv[2])
assert 1.0 < WEIGHT_RATE, WEIGHT_RATE

CORRECT_STEP = int(sys.argv[3])
assert 0 < CORRECT_STEP, CORRECT_STEP

CONSEC_REQ = int(sys.argv[4])
assert 0 < CONSEC_REQ, CONSEC_REQ

VISITED = []


def choice(memory):
    if len(VISITED) == 0:
        rows = memory["mask"]
    else:
        rows = memory["mask"] & (memory.question != VISITED[-1])

    consecs = np.flip(np.sort(memory.loc[rows, "consec"].unique()))

    weights = np.cumprod(np.full(len(consecs), WEIGHT_RATE))
    weights /= np.sum(weights)

    subset = memory.loc[(memory.consec == RNG.choice(consecs, 1, p=weights)[0]) & rows].copy()
    assert 0 < len(subset)

    subset["visited"] = False

    for question in VISITED[-2::-1]:
        if (~subset.visited).sum() == 1:
            break

        subset.visited |= subset.question == question

    selected = subset.loc[~subset.visited].sample(n=1, random_state=RNG).iloc[0]

    try:
        VISITED.pop(VISITED.index(selected.question))
    except ValueError:
        pass

    VISITED.append(selected.question)
    assert len(VISITED) == len(set(VISITED))

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
    assert memory.notnull().values.all()

    if len(VISITED) == 0:
        return choice(memory)

    rows = memory.question == VISITED[-1]
    assert rows.sum() == 1, VISITED[-1]

    if body is None:
        pass

    elif body["answer"] is None:
        memory.loc[rows, "consec"] += 1

        rows = CONSEC_REQ <= memory.consec
        memory.loc[rows, "consec"] = memory.loc[rows, "consec"].map(
            {
                consec: min((CONSEC_REQ * 2) + 1, i + CONSEC_REQ)
                for i, consec in enumerate(np.sort(memory.loc[rows, "consec"].unique()))
            },
        )

        if (not (memory["mask"].all())) and (
            CONSEC_REQ <= memory.loc[memory["mask"], "consec"]
        ).all():
            memory["mask"].values[: memory["mask"].sum() + CORRECT_STEP] = True

    else:
        assert isinstance(body["answer"], str), body
        memory.loc[rows | (memory["mask"] & (memory.answer == body["answer"])), "consec"] = 0

    memory.to_csv(path, index=False)

    return choice(memory)


@APP.route("/")
def home():
    return flask.render_template("home.html")


def main():
    logging.getLogger("werkzeug").setLevel(logging.ERROR)
    APP.run(host="0.0.0.0", port="8000", debug=False)


if __name__ == "__main__":
    main()
