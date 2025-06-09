#!/usr/bin/env python3

from collections import deque

import os.path
import pickle
import sys

import numpy as np
import pykakasi


def init_jp():
    kakasi = pykakasi.kakasi()

    table = []
    index = {}

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

        for key in ["hira", "kana"]:
            question = result[0][key]
            assert question not in index.keys(), question
            index[question] = len(table)
            table.append({"question": question, "answer": result[0]["hepburn"]})

    return {
        "table": table,
        "index": index,
        "results": [deque(maxlen=10) for _ in range(len(table))],
        "streak": np.zeros(len(table)),
        "mask": 10,
    }


def init_pt():
    table = []
    index = {}

    for question, answer in [
        ("falo", "I speak"),
        ("falas", "you speak (fam. sing.)"),
        ("ele fala", "he speaks"),
        ("você fala", "you speak (polite sing.)"),
        ("falamos", "we speak"),
        ("eles falam", "they speak"),
        ("vocês falam", "you speak (polite pl.)"),
        ("vendo", "I sell"),
        ("vendes", "you sell (fam. sing.)"),
        ("ele vende", "he sells"),
        ("você vende", "you sell (polite sing.)"),
        ("vendemos (presente)", "we sell"),
        ("eles vendem", "they sell"),
        ("vocês vendem", "you sell (polite pl.)"),
        ("parto", "I depart"),
        ("partes", "you depart (fam. sing.)"),
        ("ele parte", "he departs"),
        ("você parte", "you depart (polite sing.)"),
        ("partimos (presente)", "we depart"),
        ("eles partem", "they depart"),
        ("vocês partem", "you depart (polite pl.)"),
        ("fale", "speak! (polite sing.)"),
        ("falem", "speak! (polite pl.)"),
        ("venda", "sell! (polite sing.)"),
        ("vendam", "sell! (polite pl.)"),
        ("parta", "depart! (polite sing.)"),
        ("partam", "depart! (polite pl.)"),
        ("falemos", "let's speak"),
        ("vendamos", "let's sell"),
        ("partamos", "let's depart"),
        ("falei", "I spoke"),
        ("falaste", "you spoke (fam. sing.)"),
        ("ele falou", "he spoke"),
        ("você falou", "you spoke (polite sing.)"),
        ("falámos", "we spoke"),
        ("eles falaram", "they spoke"),
        ("vocês falaram", "you spoke (polite pl.)"),
        ("vendi", "I sold"),
        ("vendeste", "you sold (fam. sing.)"),
        ("ele vendeu", "he sold"),
        ("você vendeu", "you sold (polite sing.)"),
        ("vendemos (pretérito perfeito)", "we sold"),
        ("eles venderam", "they sold"),
        ("vocês venderam", "you sold (polite pl.)"),
        ("parti", "I departed"),
        ("partiste", "you departed (fam. sing.)"),
        ("ele partiu", "he departed"),
        ("você partiu", "you departed (polite sing.)"),
        ("partimos (pretérito perfeito)", "we departed"),
        ("eles partiram", "they departed"),
        ("vocês partiram", "you departed (polite pl.)"),
        ("eu falava", "I was speaking"),
        ("falavas", "you were speaking (fam. sing.)"),
        ("ele falava", "he was speaking"),
        ("você falava", "you were speaking (polite sing.)"),
        ("falávamos", "we were speaking"),
        ("eles falavam", "they were speaking"),
        ("vocês falavam", "you were speaking (polite pl.)"),
        ("eu vendia", "I was selling"),
        ("vendias", "you were selling (fam. sing.)"),
        ("ele vendia", "he was selling"),
        ("você vendia", "you were selling (polite sing.)"),
        ("vendíamos", "we were selling"),
        ("eles vendiam", "they were selling"),
        ("vocês vendiam", "you were selling (polite pl.)"),
        ("eu partia", "I was departing"),
        ("partias", "you were departing (fam. sing.)"),
        ("ele partia", "he was departing"),
        ("você partia", "you were departing (polite sing.)"),
        ("partíamos", "we were departing"),
        ("eles partiam", "they were departing"),
        ("vocês partiam", "you were departing (polite pl.)"),
        ("falarei", "I shall speak"),
        ("falarás", "you will speak (fam. sing.)"),
        ("ele falará", "he will speak"),
        ("você falará", "you will speak (polite sing.)"),
        ("falaremos", "we shall speak"),
        ("eles falarão", "they will speak"),
        ("vocês falarão", "you will speak (polite pl.)"),
        ("venderi", "I shall sell"),
        ("venderás", "you will sell (fam. sing.)"),
        ("ele venderá", "he will sell"),
        ("você venderá", "you will sell (polite sing.)"),
        ("venderemos", "we shall sell"),
        ("eles venderão", "they will sell"),
        ("vocês venderão", "you will sell (polite pl.)"),
        ("partirei", "I shall depart"),
        ("partirás", "you will depart (fam. sing.)"),
        ("ele partirá", "he will depart"),
        ("você partirá", "you will depart (polite sing.)"),
        ("partiremos", "we shall depart"),
        ("eles partirão", "they will depart"),
        ("vocês partirão", "you will depart (polite pl.)"),
        ("procurá-lo-ei", "I shall look for it"),
        ("procurá-lo-ás", "you will look for it (fam. sing.)"),
        ("ele procurá-lo-á", "he will look for it"),
        ("você procurá-lo-á", "you will look for it (polite sing.)"),
        ("procurá-lo-emos", "we will look for it"),
        ("eles procurá-lo-ão", "they will look for it"),
        ("vocês procurá-lo-ão", "you will look for it (polite pl.)"),
        ("falar-lhe-ei", "I shall speak to him"),
        ("falar-lhe-ás", "you will speak to him (fam. sing.)"),
        ("ele falar-lhe-á", "he will speak to him"),
        ("você falar-lhe-á", "you will speak to him (polite sing.)"),
        ("falar-lhe-emos", "we will speak to him"),
        ("eles falar-lhe-ão", "they will speak to him"),
        ("vocês falar-lhe-ão", "you will speak to him (polite pl.)"),
        ("eu falaria", "I would speak"),
        ("falarias", "you would speak (fam. sing.)"),
        ("ele falaria", "he would speak"),
        ("você falaria", "you would speak (polite sing.)"),
        ("falaríamos", "we would speak"),
        ("eles falariam", "they would speak"),
        ("vocês falariam", "you would speak (polite pl.)"),
        ("deito-me", "I lie down"),
        ("deitas-te", "you lie down (fam. sing.)"),
        ("ele deita-se", "he lies down"),
        ("você deita-se", "you lie down (polite sing.)"),
        ("deitamos-nos", "we lie down"),
        ("eles deitam-se", "they lie down"),
        ("vocês deitam-se", "you lie down (polite pl.)"),
        ("deitei-me", "I lay down"),
        ("deitava-me", "I was lying down"),
        ("tinha-me deitado", "I had lain down"),
        ("deitar-me-ei", "I shall lie down"),
        ("deitar-me-ia", "I would lie down"),
        ("deite-se", "lie down!"),
        ("fui", "I went, I was (ser, pretérito perfeito)"),
        ("eu ia", "I was going"),
        ("estive", "I was (estar, pretérito perfeito)"),
        ("eu estava", "I was (estar, pretérito imperfeito)"),
        ("tive", "I had"),
    ]:
        for key in [question, answer]:
            assert key not in index.keys(), key

        index[question] = len(table)
        table.append({"question": question, "answer": answer})

        index[answer] = len(table)
        table.append({"question": answer, "answer": question})

    return {
        "table": table,
        "index": index,
        "results": [deque(maxlen=10) for _ in range(len(table))],
        "streak": np.zeros(len(table)),
        "mask": 10,
    }


def update(old, new):
    for item in new["table"]:
        if item["question"] in old["index"].keys():
            continue

        print(item)

        old["index"][item["question"]] = len(old["table"])
        old["table"].append(item)
        old["results"].append(deque(maxlen=10))

    streak = np.zeros(len(old["table"]))
    streak[: len(old["streak"])] = old["streak"]
    old["streak"] = streak

    assert len(old["table"]) == len(old["index"])
    assert len(old["table"]) == len(old["results"])
    assert len(old["table"]) == len(old["streak"])


def main():
    path = os.path.join("data", f"{sys.argv[1]}.pkl")

    if sys.argv[1] == "jp":
        init = init_jp
    elif sys.argv[1] == "pt":
        init = init_pt
    else:
        assert False, sys.argv[1]

    if not os.path.exists(path):
        with open(path, "wb") as file:
            pickle.dump(init(), file)
    else:
        with open(path, "rb") as file:
            old = pickle.load(file)

        new = init()
        update(old, new)

        with open(path, "wb") as file:
            pickle.dump(old, file)


if __name__ == "__main__":
    main()
