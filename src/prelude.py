#!/usr/bin/env python3

import os.path
import sys

import numpy as np
import pandas as pd
import pykakasi


def init_jp():
    kakasi = pykakasi.kakasi()

    memory = []

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
            memory.append({"question": result[0][key], "answer": result[0]["hepburn"]})

    memory = pd.DataFrame(memory)
    assert memory.question.duplicated().sum() == 0

    return memory


def init_pt():
    memory = []

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
        ("deitamos-nos", "we lie down"),
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
        ("eles foram", "they went, they were (ser, pretérito perfeito)"),
        ("ele esteve", "he was (estar, pretérito perfeito)"),
    ]:
        memory.append({"question": question, "answer": answer})
        memory.append({"question": answer, "answer": question})

    memory = pd.DataFrame(memory)
    assert memory.question.duplicated().sum() == 0
    assert memory.answer.duplicated().sum() == 0

    return memory


def main():
    path = os.path.join("data", f"{sys.argv[1]}.csv")

    if sys.argv[1] == "jp":
        init = init_jp
    elif sys.argv[1] == "pt":
        init = init_pt
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
