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
    ]:  # fmt: on:
        result = kakasi.convert(hiragana)
        assert len(result) == 1, (hiragana, result)

        for key in ["hira", "kana"]:
            data.append({"question": result[0][key], "answer": result[0]["hepburn"]})

    # fmt: off
    for katakana in [
        "ヴ", "ヴァ", "ヴィ", "ヴェ", "ヴォ",
        "ファ", "フィ", "フェ", "フォ",
    ]:  # fmt: on:
        result = kakasi.convert(katakana)
        assert len(result) == 1, (katakana, result)

        data.append({"question": result[0]["kana"], "answer": result[0]["hepburn"]})

    for word in [
        "あさ",
        "あめ",
        "いえ",
        "いす",
        "いぬ",
        "おと",
        "かさ",
        "カード",
        "ガイド",
        "カット",
        "カフェ",
        "カレー",
        "キス",
        "クイズ",
        "コース",
        "コート",
        "くま",
        "せみ",
        "とり",
        "ひる",
        "よる",
        "かぎ",
        "ちず",
        "ほん",
        "かめ",
        "かみ",
        "ココア",
        "コスト",
        "コピー",
        "サイズ",
        "サイン",
        "シール",
        "スーツ",
        "セット",
        "タイプ",
        "タイム",
        "まど",
        "もり",
        "ねこ",
        "しお",
        "みせ",
        "うさぎ",
        "おかね",
        "こども",
        "さとう",
        "さかな",
        "タイヤ",
        "タオル",
        "ダンス",
        "チーム",
        "チキン",
        "アイデア",
        "アイドル",
        "アクセス",
        "アパート",
        "イメージ",
        "つくえ",
        "でんき",
        "くるま",
        "りんご",
        "ひつじ",
        "あつい",
        "たぬき",
        "せかい",
        "てんき",
        "せなか",
        "イヤホン",
        "イラスト",
        "インフレ",
        "ウイルス",
        "エアコン",
        "オーブン",
        "ダソリン",
        "カップル",
        "クリップ",
        "クレーム",
        "やさい",
        "すもう",
        "まほう",
        "からい",
        "あまい",
        "かぞく",
        "めがぬ",
        "あたま",
        "たまご",
        "いちご",
        "ケーブル",
        "コーヒー",
        "コメント",
        "サービス",
        "サッカー",
        "サンプル",
        "シャワー",
        "ジュース",
        "スイッチ",
        "スーパー",
        "ともだち",
        "にわとり",
        "こうえん",
        "なっとう",
        "おにぎり",
        "ひこうき",
        "ちかてつ",
        "かんこく",
        "にほんご",
        "ぎんこう",
        "アドバイス",
        "アナウンス",
        "アマチュア",
        "アルバイト",
        "アレルギー",
        "エネルギー",
        "エンジニア",
        "ガードマン",
        "カウンター",
        "カジュアル",
        "かいしゃ",
        "がっこう",
        "だいがく",
        "おとうと",
        "いもうと",
        "どうぶつ",
        "てぶくろ",
        "くつした",
        "たべもの",
        "べんとう",
        "カレンダー",
        "キャンセル",
        "グランド",
        "クラシック",
        "クリスマス",
        "コンテスト",
        "コンテンツ",
        "サインペン",
        "ジャケット",
        "シャンプー",
        "ライフ",
        "ゴーズ",
        "オン",
        "あなた",
        "うみ",
        "えんぴつ",
        "おとこ",
        "さくらんぼ",
        "しんぶん",
        "たけ",
        "ちょう",
        "てがみ",
        "にく",
        "はは",
        "ひと",
        "みず",
        "もも",
        "ゆめ",
        "らいがっき",
        "わたし",
        "さんぽ",
        "へや",
        "まんが",
        "やさしい",
        "バー",
        "バス",
        "カメラ",
        "センター",
        "クリーニング",
        "クラブ",
        "コインロッカー",
        "コラボレーション",
        "コレクション",
        "コントラスト",
        "コーナー",
        "デスティネーション",
        "ダイニング",
        "ディナーブッフェ",
        "エレベーター",
        "エスカレーター",
        "イベント",
        "エクスプレス",
        "ファン",
        "フレンチ",
        "ギャラリー",
        "ガーデン",
        "ギフトセレクション",
        "グルッポ",
        "ホテル",
        "イタリアン",
        "キーボード",
        "レモン",
        "ラウンジ",
        "マシーン",
        "メニュー",
        "パーク",
        "パーキング",
        "ポイント",
        "プライベート",
        "リサイクリング",
        "レストラン",
        "サーモン",
        "サンドウィッチ",
        "ショップ",
        "スポット",
        "ストレッチャー",
        "スーパーマーケット",
        "タイミング",
        "トバク",
        "トイレ",
        "チュリップ",
        "ウイスキー",
        "こんにちは",
        "ありがとう",
        "ごめんなさい",
        "はい",
        "いいえ",
        "おはよう",
        "なに",
        "すごい",
        "たくさん",
    ]:
        result = kakasi.convert(word)
        assert len(result) == 1, result

        data.append({"question": word, "answer": result[0]["hepburn"]})

    data = pd.DataFrame(data)
    assert data.question.duplicated().sum() == 0

    return data


def pt():
    data = []

    # fmt: off
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
        ("vendemos", "we sell, we sold"),
        ("eles vendem", "they sell"),
        ("vocês vendem", "you sell (polite pl.)"),
        ("parto", "I depart"),
        ("partes", "you depart (fam. sing.)"),
        ("ele parte", "he departs"),
        ("você parte", "you depart (polite sing.)"),
        ("partimos", "we depart, we departed"),
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
        ("eles falaram", "they spoke, they had spoken (literary)"),
        ("vocês falaram", "you spoke (polite pl.), you had spoken (polite pl., literary)"),
        ("vendi", "I sold"),
        ("vendeste", "you sold (fam. sing.)"),
        ("ele vendeu", "he sold"),
        ("você vendeu", "you sold (polite sing.)"),
        ("eles venderam", "they sold, they had sold (literary)"),
        ("vocês venderam", "you sold (polite pl.), you had sold (polite pl., literary)"),
        ("parti", "I departed"),
        ("partiste", "you departed (fam. sing.)"),
        ("ele partiu", "he departed"),
        ("você partiu", "you departed (polite sing.)"),
        ("eles partiram", "they departed, they had departed (literary)"),
        ("vocês partiram", "you departed (polite pl.), you had departed (polite pl., literary)"),
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
        ("eles deram", "they gave, they had given (literary)"),
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
        ("vimos", "we come, we saw"),
        ("viemos", "we came"),
        ("ele vê", "he sees"),
        ("ele via", "he was seeing"),
        ("ele viu", "he saw"),
        ("vemos", "we see"),
        ("vejo", "I see"),
        ("vi", "I saw"),
        ("eu via", "I was seeing"),
        ("eles veem", "they see"),
        ("eles viram", "they saw, they had seen (literary)"),
        ("eles viam", "they were seeing"),
        ("eles vieram", "they came, they had come (literary)"),
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
        ("ele põe", "he puts"),
        ("pomos", "we put (presente)"),
        ("eles põem", "they put (presente)"),
        ("pus", "I put (pretérito perfeito)"),
        ("puseste", "you put (fam. sing., pretérito perfeito)"),
        ("ele pôs", "he put"),
        ("pusemos", "we put (pretérito perfeito)"),
        ("eles puseram", "they put (pretérito perfeito), they had put (literary)"),
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
        ("foste", "you went (fam. sing.), you were (fam. sing., ser, pretérito perfeito)"),
        ("ele foi", "he went, he was (ser, pretérito perfeito)"),
        ("fomos", "we went, we were (ser, pretérito perfeito)"),
        ("eles foram", "they went, they had gone (literary), they were (ser, pretérito perfeito), they had been (ser, literary)"),
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
        ("eles estiveram", "they were (estar, pretérito perfeito), they had been (estar, literary)"),
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
        ("eles tiveram", "they had, they had had (literary)"),
        ("sei", "I know"),
        ("eu sabia", "I was knowing"),
        ("eu soube", "I knew"),
        ("soubeste", "you knew (fam. sing.)"),
        ("ele soube", "he knew"),
        ("soubemos", "we knew"),
        ("eles souberam", "they knew, they had known (literary)"),
        ("digo", "I say"),
        ("dizes", "you say (fam. sing.)"),
        ("ele diz", "he says"),
        ("dizemos", "we say"),
        ("eles dizem", "they say"),
        ("eu disse", "I said"),
        ("disseste", "you said (fam. sing.)"),
        ("ele disse", "he said"),
        ("dissemos", "we said"),
        ("eles disseram", "they said, they had said (literary)"),
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
        ("eles trouxeram", "they brought, they had brought (literary)"),
        ("traga", "bring! (polite sing.)"),
        ("tragamos", "let's bring"),
        ("tragam", "bring! (polite pl.)"),
        ("levo", "I take"),
        ("levas", "you take (fam. sing.)"),
        ("ele leva", "he takes"),
        ("levamos", "we take"),
        ("levámos", "we took"),
        ("eles levam", "they take"),
        ("levei", "I took"),
        ("levaste", "you took (fam. sing.)"),
        ("ele levou", "he took"),
        ("eles levaram", "they took, they had taken (literary)"),
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
        ("eles quiseram", "they wanted, they had wanted (literary)"),
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
        ("eles saíram", "they exited, they had exited (literary)"),
        ("eu saía", "I was exiting"),
        ("saías", "you were exiting (fam. sing.)"),
        ("ele saía", "he was exiting"),
        ("saíamos", "we were exiting"),
        ("eles saíam", "they were exiting"),
        ("faça", "do! (polite sing.)"),
        ("façam", "do! (polite pl.)"),
        ("façamos", "let's do"),
        ("eu fora", "I had gone (literary), I had been (ser, literary)"),
        ("foras", "you had gone (fam. sing., literary), you had been (fam. sing., ser, literary)"),
        ("ele fora", "he had gone (literary), he had been (ser, literary)"),
        ("fôramos", "we had gone (literary), we had been (ser, literary)"),
        ("pretender", "to intend"),
        ("cumprir", "to comply, to fulfill"),
        ("meter", "to insert"),
        ("eleger", "to elect"),
        ("retirar", "to remove, to withdraw"),
        ("erguer", "to erect, to raise"),
        ("pegar", "to catch, to grab"),
        ("pagar", "to pay"),
        ("permanecer", "to continue, to remain"),
        ("promover", "to foster, to promote, to sponsor"),
        ("perceber", "to realize"),
        ("conseguir", "to achieve, to acquire"),
        ("surgir", "to arise, to emerge"),
        ("buscar", "to fetch, to search"),
        ("atravessar", "to cross, to traverse"),
        ("montar", "to assemble, to mount"),
        ("manter", "to keep, to maintain"),
        ("mantenho", "I maintain"),
        ("manténs", "you maintain (fam. sing.)"),
        ("ele mantém", "he maintains"),
        ("mantemos", "we maintain"),
        ("eles mantêm", "they maintain"),
        ("mantive", "I maintained"),
        ("mantiveste", "you maintained (fam. sing.)"),
        ("ele manteve", "he maintained"),
        ("mantivemos", "we maintained"),
        ("eles mantiveram", "they maintained, they had maintained (literary)"),
        ("eu mantinha", "I was maintaining"),
        ("mantinhas", "you were maintaining (fam. sing.)"),
        ("ele mantinha", "he was maintaining"),
        ("mantínhamos", "we were maintaining"),
        ("eles mantinham", "they were maintaining"),
        ("eu manteria", "I would maintain"),
        ("manterei", "I will maintain"),
        ("eu mantivera", "I had maintained (literary)"),
        ("mantiveras", "you had maintained (fam. sing., literary)"),
        ("ele mantivera", "he had maintained (literary)"),
        ("mantivéramos", "we had maintained (literary)"),
        ("derreter", "to melt"),
        ("eu podia", "I was able (pretérito imperfeito)"),
        ("podias", "you were able (fam. sing., pretérito imperfeito)"),
        ("ele podia", "he was able (pretérito imperfeito)"),
        ("podíamos", "we were able (pretérito imperfeito)"),
        ("eles podiam", "they were able (pretérito imperfeito)"),
        ("dó bemol", "Cb"),
        ("dó", "C"),
        ("dó sustenido", "C#"),
        ("ré bemol", "Db"),
        ("ré", "D"),
        ("ré sustenido", "D#"),
        ("mi bemol", "Eb"),
        ("mi", "E"),
        ("mi sustenido", "E#"),
        ("fá bemol", "Fb"),
        ("fá", "F"),
        ("fá sustenido", "F#"),
        ("sol bemol", "Gb"),
        ("sol", "G"),
        ("sol sustenido", "G#"),
        ("lá bemol", "Ab"),
        ("lá", "A"),
        ("lá sustenido", "A#"),
        ("si bemol", "Bb"),
        ("si", "B"),
        ("si sustenido", "B#"),
        ("eu falara", "I had spoken (literary)"),
        ("falaras", "you had spoken (fam. sing., literary)"),
        ("ele falara", "he had spoken (literary)"),
        ("faláramos", "we had spoken (literary)"),
        ("eu vendera", "I had sold (literary)"),
        ("venderas", "you had sold (fam. sing., literary)"),
        ("ele vendera", "he had sold (literary)"),
        ("vendêramos", "we had sold (literary)"),
        ("eu partira", "I had departed (literary)"),
        ("partiras", "you had departed (fam. sing., literary)"),
        ("ele partira", "he had departed (literary)"),
        ("partíramos", "we had departed (literary)"),
        ("eu fizera", "I had done (literary)"),
        ("fizeras", "you had done (fam. sing., literary)"),
        ("ele fizera", "he had done (literary)"),
        ("fizéramos", "we had done (literary)"),
        ("espero que eu fale", "I hope that I speak"),
        ("espero que fales", "I hope that you speak (fam. sing.)"),
        ("espero que ele fale", "I hope that he speaks"),
        ("espero que falemos", "I hope that we speak"),
        ("espero que eles falem", "I hope that they speak"),
        ("se eu falasse", "if I spoke"),
        ("se falasses", "if you spoke (fam. sing.)"),
        ("se ele falasse", "if he spoke"),
        ("se falássemos", "if we spoke"),
        ("se eles falassem", "if they spoke"),
        ("assim que eu falar", "as soon as I speak"),
        ("assim que falares", "as soon as you speak (fam. sing.)"),
        ("assim que ele falar", "as soon as he speaks"),
        ("assim que falarmos", "as soon as we speak"),
        ("assim que eles falarem", "as soon as they speak"),
        ("espero que eu venda", "I hope that I sell"),
        ("espero que vendas", "I hope that you sell (fam. sing.)"),
        ("espero que ele venda", "I hope that he sells"),
        ("espero que vendamos", "I hope that we sell"),
        ("espero que eles vendam", "I hope that they sell"),
        ("se eu vendesse", "if I sold"),
        ("se vendesses", "if you sold (fam. sing.)"),
        ("se ele vendesse", "if he sold"),
        ("se vendêssemos", "if we sold"),
        ("se eles vendessem", "if they sold"),
        ("assim que eu vender", "as soon as I sell"),
        ("assim que venderes", "as soon as you sell (fam. sing.)"),
        ("assim que ele vender", "as soon as he sells"),
        ("assim que vendermos", "as soon as we sell"),
        ("assim que eles venderem", "as soon as they sell"),
        ("espero que eu parta", "I hope that I depart"),
        ("espero que partas", "I hope that you depart (fam. sing.)"),
        ("espero que ele parta", "I hope that he departs"),
        ("espero que partamos", "I hope that we depart"),
        ("espero que eles partam", "I hope that they depart"),
        ("se eu partisse", "if I departed"),
        ("se partisses", "if you departed (fam. sing.)"),
        ("se ele partisse", "if he departed"),
        ("se partíssemos", "if we departed"),
        ("se eles partissem", "if they departed"),
        ("assim que eu partir", "as soon as I depart"),
        ("assim que partires", "as soon as you depart (fam. sing.)"),
        ("assim que ele partir", "as soon as he departs"),
        ("assim que partirmos", "as soon as we depart"),
        ("assim que eles partirem", "as soon as they depart"),
        ("espero que eu vá", "I hope that I go"),
        ("espero que vás", "I hope that you go (fam. sing.)"),
        ("espero que ele vá", "I hope that he goes"),
        ("espero que vamos", "I hope that we go"),
        ("espero que eles vão", "I hope that they go"),
        ("se eu fosse", "if I went, if I was (ser)"),
        ("se fosses", "if you went (fam. sing.), if you were (fam. sing., ser)"),
        ("se ele fosse", "if he went, if he was (ser)"),
        ("se fôssemos", "if we went, if we were (ser)"),
        ("se eles fossem", "if they went, if they were (ser)"),
        ("assim que eu for", "as soon as I go, as soon as I am (ser)"),
        ("assim que fores", "as soon as you go (fam. sing.), as soon as you are (fam. sing., ser)"),
        ("assim que ele for", "as soon as he goes, as soon as he is (ser)"),
        ("assim que formos", "as soon as we go, as soon as we are (ser)"),
        ("assim que eles forem", "as soon as they go, as soon as they are (ser)"),
        ("espero que eu seja", "I hope that I am (ser)"),
        ("espero que sejas", "I hope that you are (fam. sing., ser)"),
        ("espero que ele seja", "I hope that he is (ser)"),
        ("espero que sejamos", "I hope that we are (ser)"),
        ("espero que eles sejam", "I hope that they are (ser)"),
        ("espero que eu esteja", "I hope that I am (estar)"),
        ("espero que estajas", "I hope that you are (fam. sing., estar)"),
        ("espero que ele esteja", "I hope that he is (estar)"),
        ("espero que estejamos", "I hope that we are (estar)"),
        ("espero que eles estejam", "I hope that they are (estar)"),
        ("se eu estivesse", "if I was (estar)"),
        ("se estivesses", "if you were (fam. sing., estar)"),
        ("se ele estivesse", "if he was (estar)"),
        ("se estivéssemos", "if we were (estar)"),
        ("se eles estivessem", "if they were (estar)"),
        ("assim que eu estiver", "as soon as I am (estar)"),
        ("assim que estiveres", "as soon as you are (fam. sing., estar)"),
        ("assim que ele estiver", "as soon as he is (estar)"),
        ("assim que estivermos", "as soon as we are (estar)"),
        ("assim que eles estiverem", "as soon as they are (estar)"),
        ("espero que eu tenha", "I hope that I have"),
        ("espero que tenhas", "I hope that you have (fam. sing.)"),
        ("espero que ele tenha", "I hope that he has"),
        ("espero que tenhamos", "I hope that we have"),
        ("espero que eles tenham", "I hope that they have"),
        ("se eu tivesse", "if I had"),
        ("se tivesses", "if you had (fam. sing.)"),
        ("se ele tivesse", "if he had"),
        ("se tivéssemos", "if we had"),
        ("se eles tivessem", "if they had"),
        ("assim que eu tiver", "as soon as I have"),
        ("assim que tiveres", "as soon as you have (fam. sing.)"),
        ("assim que ele tiver", "as soon as he has"),
        ("assim que tivermos", "as soon as we have"),
        ("assim que eles tiverem", "as soon as they have"),
    ]:  # fmt: on:
        data.append({"question": question, "answer": answer})
        data.append({"question": answer, "answer": question})

    data = pd.DataFrame(data)
    assert data.question.duplicated().sum() == 0
    assert data.answer.duplicated().sum() == 0

    return data


# NOTE: See `https://www.edrdg.org/kanjidic/kanjd2index_legacy.html`.
# NOTE: See `https://github.com/davidluzgouveia/kanji-data/blob/master/tools/kanjidic.py`.
def kanjidic():
    with open(os.path.join("data", "kanjidic2.xml.gz"), "rb") as file:
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

    data.sort_values(
        ["stroke_count", "freq"],
        ascending=[True, True],
        ignore_index=True,
        inplace=True,
    )

    data["question"] = data.literal
    data["answer"] = data.meaning_pt.map(lambda meaning: meaning[0])
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

    with open(os.path.join("data", "Kaishi 1.5k.txt"), "r") as file:
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
        mask[:10] = True

        memory["mask"] = mask

        memory.to_csv(path, index=False)
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
        print(f"Added {len(missing)} new questions!")


if __name__ == "__main__":
    main()
