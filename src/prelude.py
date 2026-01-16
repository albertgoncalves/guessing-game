#!/usr/bin/env python3

import gzip
import os
import sys
import xml.etree.ElementTree as et

import bs4
import numpy as np
import pandas as pd
import pykakasi

NOTES = "ABCDEFG"
PITCHES = {"A": 9, "B": 11, "C": 0, "D": 2, "E": 4, "F": 5, "G": 7}
INTERVALS = {"m3": (2, 3), "M3": (2, 4), "P4": (3, 5), "P5": (4, 7), "m6": (5, 8), "M6": (5, 9)}

MASK_MIN = 10


def jp():
    kakasi = pykakasi.kakasi()

    data = []

    # fmt: off
    for hiragana in [
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

        "っし", "っち",
    ]:  # fmt: on:
        result = kakasi.convert(hiragana)
        assert len(result) == 1, (hiragana, result)

        for key in ["hira", "kana"]:
            data.append({"question": result[0][key], "answer": result[0]["hepburn"]})

    # fmt: off
    for katakana in [
        "ヴ", "ヴァ", "ヴィ", "ヴェ", "ヴォ",
        "ディ",
        "ファ", "フィ", "フェ", "フォ",
    ]:  # fmt: on:
        result = kakasi.convert(katakana)
        assert len(result) == 1, (katakana, result)

        data.append({"question": result[0]["kana"], "answer": result[0]["hepburn"]})

    with open(os.path.join("assets", "jp.txt"), "r") as file:
        for line in file.readlines():
            word = line.strip()

            result = kakasi.convert(word)
            assert len(result) == 1, result

            data.append({"question": word, "answer": result[0]["hepburn"]})

    data = pd.DataFrame(data)
    assert data.question.duplicated().sum() == 0

    return data


def pt():
    data = []

    with open(os.path.join("assets", "pt.txt"), "r") as file:
        for line in file.readlines():
            (question, answer) = line.strip().split(", ", 1)
            data.append({"question": question, "answer": answer})
            data.append({"question": answer, "answer": question})

    data = pd.DataFrame(data)
    assert data.question.duplicated().sum() == 0
    assert data.answer.duplicated().sum() == 0

    return data


# NOTE: See `https://www.edrdg.org/kanjidic/kanjd2index_legacy.html`.
# NOTE: See `https://github.com/davidluzgouveia/kanji-data/blob/master/tools/kanjidic.py`.
def kanjidic():
    with open(os.path.join("assets", "kanjidic2.xml.gz"), "rb") as file:
        xml = gzip.decompress(file.read()).decode("utf-8")

    data = []
    for character in et.fromstring(xml).iter("character"):
        misc = character.find("misc")
        if misc is None:
            continue

        reading_meaning = character.find("reading_meaning")
        if reading_meaning is None:
            continue

        rmgroup = reading_meaning.find("rmgroup")
        if rmgroup is None:
            continue

        meaning_en = []
        meaning_pt = []
        for meaning in rmgroup.iter("meaning"):
            m_lang = meaning.attrib.get("m_lang")
            if m_lang is None:
                meaning_en.append(meaning.text.strip().lower())
            elif m_lang == "pt":
                if meaning.text.strip().lower() == "waº":
                    continue
                meaning_pt.append(meaning.text.strip().lower())

        if (len(meaning_en) == 0) or (len(meaning_pt) == 0):
            continue

        grade = misc.find("grade")
        freq = misc.find("freq")

        data.append(
            {
                "literal": character.find("literal").text,
                "meaning_en": meaning_en,
                "meaning_pt": meaning_pt,
                "grade": None if grade is None else grade.text,
                "stroke_count": int(misc.find("stroke_count").text),
                "freq": None if freq is None else freq.text,
            },
        )

    data = pd.DataFrame(data).astype({"grade": "Int64", "freq": "Int64"})

    data.sort_values(["freq"], ascending=[True], ignore_index=True, inplace=True)

    data["question"] = data.literal
    data["answer"] = data.meaning_pt.map(lambda meaning: meaning[0])

    for question, answer in [
        ("弦", "corda (arco violão)"),
        ("皿", "prato (tipo)"),
        ("親", "parente"),
        ("再", "segundo tempo"),
        ("又", "além disso"),
        ("資", "recursos"),
        ("済", "terminar"),
        ("決", "decidir"),
    ]:
        rows = data.question == question
        assert rows.sum() == 1
        data.loc[rows, "answer"] = answer

    return data.loc[data.freq.notnull(), ["question", "answer"]].copy()


# NOTE: See `https://www3.nhk.or.jp/nhkworld/lesson/pt/lessons/`.
def kaishi():
    kakasi = pykakasi.kakasi()

    data = []

    def tokenize(text):
        i = 0

        tokens = []

        while True:
            assert text[i] == '"', (text[i], i)
            i += 1
            j = i

            if (i + 1) == len(text):
                break

            while True:
                j += 1

                if (text[j] == '"') and (text[j + 1] == '"'):
                    j += 1
                    continue

                if (text[j] == '"') and (text[j + 1] != '"'):
                    break

            token = text[i:j].replace('""', '"').strip()
            if token != "":
                tokens.append(token)

            i = j

        return tokens

    with open(os.path.join("assets", "Kaishi 1.5k.txt"), "r") as file:
        lines = file.read()
        text = lines.split("\n", 2)[-1]
        for i, token in enumerate(tokenize(text)[2:]):
            if (i % 2) == 0:
                continue

            div = bs4.BeautifulSoup(token, "lxml").find("div", {"lang": "ja"})

            question = []
            answer = div.find("div")
            kana = []

            for element in [
                element
                for element in answer.previous_siblings
                if not isinstance(element, bs4.element.Comment)
            ][::-1]:
                if element.text.strip() == "":
                    continue
                if element.name == "ruby":
                    children = element.children
                    while True:
                        try:
                            rb = next(children)
                        except StopIteration:
                            break

                        rt = next(children)
                        assert (rb.name == "rb") and (rt.name == "rt"), element

                        kana.append(rt.text.strip())
                        question.append(f"<ruby>{rb.text.strip()}<rt>{rt.text.strip()}</rt></ruby>")
                else:
                    assert isinstance(element, bs4.element.NavigableString), element
                    element = element.strip()
                    if element == "":
                        continue
                    question.append(element)
                    kana.append(element)

            results = kakasi.convert("".join(kana))
            assert len(results) == 1, results

            data.append(
                {
                    "question": "".join(question),
                    "answer": f"{results[0]['hepburn']} - {answer.text.strip()}",
                }
            )

    data = pd.DataFrame(data)
    data.drop_duplicates("question", keep="first", ignore_index=True, inplace=True)

    for question, answer, replacement in [
        (
            "<ruby>友<rt>とも</rt></ruby><ruby>達<rt>だち</rt></ruby>",
            "tomodachi - Amigo, companhia.",
            "tomodachi - amigo, companhia",
        ),
        (
            "<ruby>私<rt>わたし</rt></ruby>",
            "watashi - eu (formal, uso geral)",
            "watashi - eu (forma formal, uso geral)",
        ),
        ("はい", "hai - sim (formal)", "hai - sim (forma formal)"),
        ("いいえ", "iie - não (formal)", "iie - não (forma formal)"),
        (
            "ありがとうございます",
            "arigatougozaimasu - obrigado (formal)",
            "arigatougozaimasu - obrigado (forma formal)",
        ),
        (
            "<ruby>我<rt>われ</rt></ruby><ruby>々<rt>われ</rt></ruby>",
            "wareware - nós (formal)",
            "wareware - nós (forma formal)",
        ),
        ("お<ruby>茶<rt>ちゃ</rt></ruby>", "ocha - chá (formal)", "ocha - chá (forma formal)"),
    ]:
        rows = data.question == question
        assert rows.sum() == 1
        assert (data.loc[rows, "answer"] == answer).all()
        data.loc[rows, "answer"] = replacement

    assert data.question.duplicated().sum() == 0

    return data


def note_to_pitch(note):
    pitch = PITCHES[note[0]]

    for accidental in note[1:]:
        if accidental == "b":
            pitch -= 1
        elif accidental == "#":
            pitch += 1
        else:
            assert False, accidental

    return pitch % 12


def transpose(note_from, interval):
    (steps, semitones) = INTERVALS[interval]

    note_to = NOTES[(NOTES.index(note_from[0]) + steps) % len(NOTES)]
    pitch_from = note_to_pitch(note_from)
    pitch_to = (pitch_from + semitones) % 12

    if pitch_to < PITCHES[note_to]:
        pitch_to += 12

    above = (PITCHES[note_to] + 12) - pitch_to
    below = pitch_to - PITCHES[note_to]

    if above <= below:
        note_to += "b" * above
    else:
        note_to += "#" * below

    assert (pitch_to % 12) == note_to_pitch(note_to), (note_from, interval, note_to)

    return note_to


def intervals():
    data = pd.DataFrame(
        [
            {
                "question": f"{note + accidentals} + {interval}",
                "answer": transpose(note + accidentals, interval),
            }
            for interval in INTERVALS.keys()
            for accidentals in ["", "b", "#"]
            for note in NOTES
        ],
    )
    assert data.question.duplicated().sum() == 0
    return data


def main():
    path = os.path.join("data", f"{sys.argv[1]}.csv")

    if not os.path.exists(path):
        memory = eval(sys.argv[1])()

        memory["consec"] = 0

        mask = np.zeros(len(memory), dtype=np.bool)
        mask[:MASK_MIN] = True

        memory["mask"] = mask

        memory.to_csv(path, index=False)
        print(f"Created {len(memory)} new question(s)! ({path})")
    else:
        old = pd.read_csv(path)
        new = eval(sys.argv[1])()

        missing = new.loc[~new.question.isin(old.question)].copy()
        if len(missing) == 0:
            print("Nothing to do!")
            return

        missing["consec"] = 0
        missing["mask"] = np.zeros(len(missing), dtype=np.bool)

        combined = pd.concat([old, missing], ignore_index=True)
        assert combined.question.duplicated().sum() == 0

        if sys.argv[1] == "pt":
            assert combined.answer.duplicated().sum() == 0

        combined.to_csv(path, index=False)
        print(f"Added {len(missing)} new question(s)! ({path})")


if __name__ == "__main__":
    main()
