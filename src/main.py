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
        weight *= 1.75

    weights = pd.DataFrame(weights)
    for column in ["weight", "size"]:
        weights[column] /= weights[column].sum()

    memory.weight /= memory.weight.sum()
    memory.to_csv(os.path.join("out", "snapshot.csv"), index=False)

    if previous is not None:
        memory.loc[memory.question == previous, "mask"] = True

    print(
        memory.loc[
            memory.consec.isin(consecs[:3]) & memory["mask"],
            [
                "question",
                "consec",
                "weight",
            ],
        ].sort_values("consec"),
    )

    selected = memory.iloc[RNG.choice(len(memory), size=1, p=memory.weight, shuffle=False)[0]]
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

    if body["response"] is None:
        memory.loc[rows, "consec"] += 1
    else:
        memory.loc[rows, "consec"] = 0

    if (not (memory["mask"].all())) and (3 <= memory.loc[memory["mask"], "consec"]).all():
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
