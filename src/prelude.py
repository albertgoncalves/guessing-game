#!/usr/bin/env python3

import gzip
import os.path
import sys
import xml.etree.ElementTree as et

import numpy as np
import pandas as pd
import pykakasi


def init_jp():
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
    ]:  # fmt: on:
        result = kakasi.convert(hiragana)
        assert len(result) == 1, result

        for key in ["hira", "kana"]:
            data.append({"question": result[0][key], "answer": result[0]["hepburn"]})

    data = pd.DataFrame(data)
    assert data.question.duplicated().sum() == 0

    return data


def init_pt():
    data = []

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
        ("falarei", "I will speak"),
        ("falarás", "you will speak (fam. sing.)"),
        ("ele falará", "he will speak"),
        ("você falará", "you will speak (polite sing.)"),
        ("falaremos", "we will speak"),
        ("eles falarão", "they will speak"),
        ("vocês falarão", "you will speak (polite pl.)"),
        ("venderei", "I will sell"),
        ("venderás", "you will sell (fam. sing.)"),
        ("ele venderá", "he will sell"),
        ("você venderá", "you will sell (polite sing.)"),
        ("venderemos", "we will sell"),
        ("eles venderão", "they will sell"),
        ("vocês venderão", "you will sell (polite pl.)"),
        ("partirei", "I will depart"),
        ("partirás", "you will depart (fam. sing.)"),
        ("ele partirá", "he will depart"),
        ("você partirá", "you will depart (polite sing.)"),
        ("partiremos", "we will depart"),
        ("eles partirão", "they will depart"),
        ("vocês partirão", "you will depart (polite pl.)"),
        ("procurá-lo-ei", "I will look for it"),
        ("procurá-lo-ás", "you will look for it (fam. sing.)"),
        ("ele procurá-lo-á", "he will look for it"),
        ("você procurá-lo-á", "you will look for it (polite sing.)"),
        ("procurá-lo-emos", "we will look for it"),
        ("eles procurá-lo-ão", "they will look for it"),
        ("vocês procurá-lo-ão", "you will look for it (polite pl.)"),
        ("falar-lhe-ei", "I will speak to him"),
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
        ("deitamo-nos", "we lie down"),
        ("eles deitam-se", "they lie down"),
        ("vocês deitam-se", "you lie down (polite pl.)"),
        ("deitei-me", "I lay down"),
        ("deitava-me", "I was lying down"),
        ("tinha-me deitado", "I had lain down (spoken)"),
        ("deitar-me-ei", "I will lie down"),
        ("deitar-me-ia", "I would lie down"),
        ("deite-se", "lie down! (polite sing.)"),
        ("fui", "I went, I was (ser, pretérito perfeito)"),
        ("eu ia", "I was going"),
        ("estive", "I was (estar, pretérito perfeito)"),
        ("eu estava", "I was (estar, pretérito imperfeito)"),
        ("tive", "I had"),
        ("eles dão", "they give"),
        ("eles davam", "they were giving"),
        ("eles deram", "they gave"),
        ("faço", "I do"),
        ("eu fazia", "I was doing"),
        ("fiz", "I did"),
        ("ele fez", "he did"),
        ("eu seria", "I would be (ser)"),
        ("eu estaria", "I would be (estar)"),
        ("eu escrevera", "I had written (literary)"),
        ("ver", "to see"),
        ("vir", "to come"),
        ("venho", "I come"),
        ("eu vinha", "I was coming"),
        ("vim", "I came"),
        ("ele veio", "he came"),
        ("vínhamos", "we were coming"),
        ("vimos (presente)", "we come"),
        ("viemos", "we came"),
        ("ele vê", "he sees"),
        ("ele via", "he was seeing"),
        ("ele viu", "he saw"),
        ("vimos (pretérito perfeito)", "we saw"),
        ("vemos", "we see"),
        ("vejo", "I see"),
        ("vi", "I saw"),
        ("eu via", "I was seeing"),
        ("eles veem", "they see"),
        ("eles viram", "they saw"),
        ("eles viam", "they were seeing"),
        ("eles vieram", "they came"),
        ("eles vinham", "they were coming"),
        ("eles vêm", "they come"),
        ("dou", "I give"),
        ("dás", "you give (fam. sing.)"),
        ("ele dá", "he gives"),
        ("damos", "we give"),
        ("eu dava", "I was giving"),
        ("davas", "you were giving (fam. sing.)"),
        ("ele dava", "he was giving"),
        ("dávamos", "we were giving"),
        ("dei", "I gave"),
        ("deste", "you gave (fam. sing.)"),
        ("ele deu", "he gave"),
        ("demos", "we gave, let's give"),
        ("dê", "give! (polite sing.)"),
        ("deem", "give! (polite pl.)"),
        ("ele faz", "he does"),
        ("fazemos", "we do"),
        ("eles fazem", "they do"),
        ("fazes", "you do (fam. sing.)"),
        ("fizeste", "you did (fam. sing.)"),
        ("fizemos", "we did"),
        ("eles fizeram", "they did, they had done (literary)"),
        ("eu faria", "I would do"),
        ("farei", "I will do"),
        ("farás", "you will do (fam. sing.)"),
        ("ele fará", "he will do"),
        ("faremos", "we will do"),
        ("eles farão", "they will do"),
        ("fiquei", "I stayed"),
        ("fico", "I stay"),
        ("ele ficou", "he stayed"),
        ("ele fica", "he stays"),
        ("você fica", "you stay (polite sing.)"),
        ("ponho", "I put (presente)"),
        ("pões", "you put (fam. sing., presente)"),
        ("ele põe", "he put (presente)"),
        ("pomos", "we put (presente)"),
        ("eles põem", "they put (presente)"),
        ("pus", "I put (pretérito perfeito)"),
        ("puseste", "you put (fam. sing., pretérito perfeito)"),
        ("ele pôs", "he put (pretérito perfeito)"),
        ("pusemos", "we put (pretérito perfeito)"),
        ("eles puseram", "they put (pretérito perfeito)"),
        ("eu punha", "I was putting"),
        ("punhas", "you were putting (fam. sing.)"),
        ("ele punha", "he was putting"),
        ("púnhamos", "we were putting"),
        ("eles punham", "they were putting"),
        ("posso", "I can"),
        ("podes", "you can (fam. sing.)"),
        ("ele pode", "he can"),
        ("podemos", "we can"),
        ("eles podem", "they can"),
        ("pude", "I was able (pretérito perfeito)"),
        ("pudeste", "you were able (fam. sing., pretérito perfeito)"),
        ("ele pôde", "he was able (pretérito perfeito)"),
        ("pudemos", "we were able (pretérito perfeito)"),
        ("eles puderam", "they were able (pretérito perfeito), they had been able (literary)"),
        ("vou", "I go"),
        ("vais", "you go (fam. sing.)"),
        ("ele vai", "he goes"),
        ("vamos", "we go"),
        ("eles vão", "they go"),
        ("ele ia", "he was going"),
        ("ias", "you were going (fam. sing.)"),
        ("íamos", "we were going"),
        ("eles iam", "they were going"),
        ("foste", "you went, you were (fam. sing., ser, pretérito perfeito)"),
        ("ele foi", "he went, he was (ser, pretérito perfeito)"),
        ("fomos", "we went, we were (ser, pretérito perfeito)"),
        (
            "eles foram",
            "they went, they were (ser, pretérito perfeito), they had been (ser, literary)",
        ),
        ("ele esteve", "he was (estar, pretérito perfeito)"),
        ("sou", "I am (ser)"),
        ("és", "you are (fam. sing., ser)"),
        ("ele é", "he is (ser)"),
        ("somos", "we are (ser)"),
        ("eles são", "they are (ser)"),
        ("eu era", "I was (ser, pretérito imperfeito)"),
        ("eras", "you were (fam. sing., ser, pretérito imperfeito)"),
        ("ele era", "he was (ser, pretérito imperfeito)"),
        ("éramos", "we were (ser, pretérito imperfeito)"),
        ("eles eram", "they were (ser, pretérito imperfeito)"),
        ("estou", "I am (estar)"),
        ("estás", "you are (fam. sing., estar)"),
        ("ele está", "he is (estar)"),
        ("estamos", "we are (estar)"),
        ("eles estão", "they are (estar)"),
        ("estiveste", "you were (fam. sing., estar, pretérito perfeito)"),
        ("estivemos", "we were (estar, pretérito perfeito)"),
        ("eles estiveram", "they were (estar, pretérito perfeito)"),
        ("tenho", "I have"),
        ("tens", "you have (fam. sing.)"),
        ("ele tem", "he has"),
        ("temos", "we have"),
        ("eles têm", "they have"),
        ("eu tinha", "I was having"),
        ("tinhas", "you were having (fam. sing.)"),
        ("ele tinha", "he was having"),
        ("tínhamos", "we were having"),
        ("eles tinham", "they were having"),
        ("tiveste", "you had (fam. sing.)"),
        ("ele teve", "he had"),
        ("tivemos", "we had"),
        ("eles tiveram", "they had"),
        ("sei", "I know"),
        ("eu sabia", "I was knowing"),
        ("eu soube", "I knew"),
        ("soubeste", "you knew (fam. sing.)"),
        ("ele soube", "he knew"),
        ("soubemos", "we knew"),
        ("eles souberam", "they knew"),
        ("digo", "I say"),
        ("dizes", "you say (fam. sing.)"),
        ("ele diz", "he says"),
        ("dizemos", "we say"),
        ("eles dizem", "they say"),
        ("eu disse", "I said"),
        ("disseste", "you said (fam. sing.)"),
        ("ele disse", "he said"),
        ("dissemos", "we said"),
        ("eles disseram", "they said"),
        ("diga", "say! (polite sing.)"),
        ("digamos", "let's say"),
        ("digam", "say! (polite pl.)"),
        ("trago", "I bring"),
        ("ele traz", "he brings"),
        ("eu trazia", "I was bringing"),
        ("eu trouxe", "I brought"),
        ("trouxeste", "you brought (fam. sing.)"),
        ("ele trouxe", "he brought"),
        ("trouxemos", "we brought"),
        ("eles trouxeram", "they brought"),
        ("traga", "bring! (polite sing.)"),
        ("tragamos", "let's bring"),
        ("tragam", "bring! (polite pl.)"),
        ("levo", "I take"),
        ("levas", "you take (fam. sing.)"),
        ("ele leva", "he takes"),
        ("levamos", "we take, we took"),
        ("eles levam", "they take"),
        ("levei", "I took"),
        ("levaste", "you took (fam. sing.)"),
        ("ele levou", "he took"),
        ("eles levaram", "they took"),
        ("leve", "take! (polite sing.)"),
        ("levemos", "let's take"),
        ("levem", "take! (polite pl.)"),
        ("quero", "I want"),
        ("queres", "you want (fam. sing.)"),
        ("ele quer", "he wants"),
        ("queremos", "we want"),
        ("eles querem", "they want"),
        ("eu queria", "I was wanting"),
        ("eu quisera", "I had wanted (literary)"),
        ("eu quereria", "I would want"),
        ("quererei", "I will want"),
        ("eu quis", "I wanted"),
        ("quiseste", "you wanted (fam. sing.)"),
        ("ele quis", "he wanted"),
        ("quisemos", "we wanted"),
        ("eles quiseram", "they wanted"),
        ("viste", "you saw (fam. sing.)"),
        ("vias", "you were seeing (fam. sing.)"),
        ("vês", "you see (fam. sing.)"),
        ("o feriado", "holiday"),
        ("as férias", "vacation"),
        ("eu soubera", "I had known (literary)"),
        ("saio", "I exit"),
        ("sais", "you exit (fam. sing.)"),
        ("ele sai", "he exits"),
        ("saímos", "we exit, we exited"),
        ("eles saem", "they exit"),
        ("saí", "I exited"),
        ("saíste", "you exited (fam. sing.)"),
        ("ele saiu", "he exited"),
        ("eles saíram", "they exited"),
        ("eu saía", "I was exiting"),
        ("saías", "you were exiting (fam. sing.)"),
        ("ele saía", "he was exiting"),
        ("saíamos", "we were exiting"),
        ("eles saíam", "they were exiting"),
        ("faça", "do! (polite sing.)"),
        ("façam", "do! (polite pl.)"),
        ("façamos", "let's do"),
        ("eu fora", "I had went (literary), I had been (ser, literary)"),
        ("foras", "you had went (fam. sing., literary), you had been (fam. sing., ser, literary)"),
        ("ele fora", "he had went (literary), he had been (ser, literary)"),
        ("fôramos", "we had went (literary), we had been (ser, literary)"),
    ]:
        data.append({"question": question, "answer": answer})
        data.append({"question": answer, "answer": question})

    data = pd.DataFrame(data)
    assert data.question.duplicated().sum() == 0
    assert data.answer.duplicated().sum() == 0

    return data


# NOTE: See `https://www.edrdg.org/kanjidic/kanjd2index_legacy.html`.
# NOTE: See `https://github.com/davidluzgouveia/kanji-data/blob/master/tools/kanjidic.py`.
def init_kanjidic():
    with open(os.path.join("data", "kanjidic2.xml.gz"), "rb") as file:
        xml = gzip.decompress(file.read()).decode("utf-8")

    with open(os.path.join("out", "kanjidic2.xml"), "w") as file:
        file.write(xml)

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

    data.sort_values(
        ["stroke_count", "freq"],
        ascending=[True, True],
        ignore_index=True,
        inplace=True,
    )

    data.to_csv("kanjidic2.csv", index=False)

    data["question"] = data.literal
    data["answer"] = data.meaning_pt.map(lambda meaning: meaning[0])
    return data.loc[data.freq.notnull(), ["question", "answer"]].copy()


def main():
    path = os.path.join("data", f"{sys.argv[1]}.csv")

    if sys.argv[1] == "jp":
        init = init_jp
    elif sys.argv[1] == "pt":
        init = init_pt
    elif sys.argv[1] == "kanjidic":
        init = init_kanjidic
    else:
        assert False, sys.argv[1]

    if not os.path.exists(path):
        memory = init()

        memory["consec"] = 0

        mask = np.zeros(len(memory), dtype=np.bool)
        mask[:10] = True

        memory["mask"] = mask

        memory.to_csv(path, index=False)
    else:
        old = pd.read_csv(path)
        new = init()

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


if __name__ == "__main__":
    main()
