#!/usr/bin/env python3

import os.path
import pickle

import flask
import numpy as np
import pandas as pd
import pykakasi

APP = flask.Flask(__name__)

RNG = np.random.default_rng()


def init():
    kakasi = pykakasi.kakasi()

    table = []
    index = {}

    key = "kana"

    for i, hiragana in enumerate(
        # fmt: off
        [
            "あ", "い", "う", "え", "お",

            "か", "き", "く", "け", "こ",
            "きゃ", "きゅ", "きょ",

            "さ", "し", "す", "せ", "そ",
            "しゃ", "しゅ", "しょ",

            "た", "ち", "つ", "て", "と",
            "ちゃ", "ちゅ", "ちょ",

            "な", "に", "ぬ", "ね", "の",
            "にゃ", "にゅ", "にょ",

            "は", "ひ", "ふ", "へ", "ほ",
            "ひゃ", "ひゅ", "ひょ",

            "ま", "み", "む", "め", "も",
            "みゃ", "みゅ", "みょ",

            "や", "ゆ", "よ",

            "ら", "り", "る", "れ", "ろ",
            "りゃ", "りゅ", "りょ",

            "わ", "を",

            "が", "ぎ", "ぐ", "げ", "ご",
            "ぎゃ", "ぎゅ", "ぎょ",

            "ざ", "じ", "ず", "ぜ", "ぞ",
            "じゃ", "じゅ", "じょ",

            "だ", "ぢ", "づ", "で", "ど",
            "ぢゃ", "ぢゅ", "ぢょ",

            "ば", "び", "ぶ", "べ", "ぼ",
            "びゃ", "びゅ", "びょ",

            "ぱ", "ぴ", "ぷ", "ぺ", "ぽ",
            "ぴゃ", "ぴゅ", "ぴょ",

            "ん",
        ],  # fmt: on:
    ):
        result = kakasi.convert(hiragana)
        assert len(result) == 1, result
        table.append({"question": result[0][key], "answer": result[0]["hepburn"]})
        index[result[0][key]] = i

    return {
        "table": table,
        "index": index,
        "correct": np.zeros(len(table)),
        "incorrect": np.zeros(len(table)),
        "streak": 0,
        "mask": 10,
    }


PATH = os.path.join("data", "memory.pkl")

if os.path.exists(PATH):
    with open(PATH, "rb") as file:
        MEMORY = pickle.load(file)
else:
    MEMORY = init()
    with open(PATH, "wb") as file:
        pickle.dump(MEMORY, file)


def choice(previous=None):
    incorrect = MEMORY["incorrect"] + 1

    weights = incorrect / (MEMORY["correct"] + incorrect)
    weights[MEMORY["mask"] :] = 0

    if previous is not None:
        weights[MEMORY["index"][previous]] = 0

    weights **= 2
    weights /= weights.sum()

    snapshot = pd.DataFrame(
        {
            "question": [item["question"] for item in MEMORY["table"]],
            "correct": MEMORY["correct"],
            "incorrect": MEMORY["incorrect"],
        },
    )
    snapshot["total"] = snapshot.correct + snapshot.incorrect
    snapshot["rate"] = snapshot.correct / snapshot.total
    snapshot["weight"] = weights

    snapshot.to_csv(os.path.join("out", "snapshot.csv"))

    return RNG.choice(MEMORY["table"], size=1, p=weights, shuffle=False)[0]


@APP.route("/next", methods=["POST"])
def next():
    body = flask.request.get_json()

    if body is None:
        return choice()

    if body["response"] is None:
        MEMORY["correct"][MEMORY["index"][body["previous"]]] += 1
        MEMORY["streak"] += 1
    else:
        MEMORY["incorrect"][MEMORY["index"][body["previous"]]] += 1
        MEMORY["streak"] = 0

    if 15 < MEMORY["streak"]:
        MEMORY["mask"] += 3
        MEMORY["streak"] = 0

    with open(PATH, "wb") as file:
        pickle.dump(MEMORY, file)

    return choice(body["previous"])


@APP.route("/")
def home():
    return flask.render_template("home.html")


def main():
    APP.run(host="0.0.0.0", port="8000", debug=True)


if __name__ == "__main__":
    main()
