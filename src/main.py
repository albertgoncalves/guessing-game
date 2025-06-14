#!/usr/bin/env python3

import logging
import os.path
import sys

import flask
import numpy as np
import pandas as pd

APP = flask.Flask(__name__)

RNG = np.random.default_rng()


def choice(memory, previous=None):
    memory["weight"] = 0.0

    if previous is not None:
        memory.loc[memory.question == previous, "mask"] = False

    cohorts = np.sort(memory.streak.unique())

    w = 1
    for n in np.flip(cohorts):
        rows = (memory.streak == n) & memory["mask"]
        k = rows.sum()
        if k == 0:
            continue
        memory.loc[rows, "weight"] = w / k
        w *= 1.5

    memory.weight /= memory.weight.sum()
    memory.to_csv(os.path.join("out", "snapshot.csv"), index=False)

    if previous is not None:
        memory.loc[memory.question == previous, "mask"] = True

    print(
        memory.loc[
            memory.streak.isin(cohorts[:3]) & memory["mask"],
            [
                "question",
                "streak",
                "weight",
            ],
        ].sort_values("streak"),
    )

    selected = memory.iloc[RNG.choice(len(memory), size=1, p=memory.weight, shuffle=False)[0]]
    return {
        "question": selected.question,
        "answer": selected.answer,
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

    if body["response"] is None:
        memory.loc[rows, "streak"] += 1
    else:
        memory.loc[rows, "streak"] = 0

    if (not (memory["mask"].all())) and (3 <= memory.loc[memory["mask"], "streak"]).all():
        memory["mask"].values[: memory["mask"].sum() + 10] = True

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
