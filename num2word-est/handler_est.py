#!/usr/bin/env python3

from math import trunc
from typing import List

places = [None,
lambda n: "tuhat",
lambda n: "miljon" if n == 1 else "miljonit",
lambda n: "mijard" if n == 1 else "mijardit",
lambda n: "triljon" if n == 1 else "triljonit"
]

digit = ["null", "üks", "kaks", "kolm", "neli", "viis", "kuus", "seitse", "kaheksa", "üheksa"]


def convertIntHundreds(number: int) -> List[str]:
    word = []
    if trunc(number / 100) != 0:
        word = [digit[trunc(number / 100)] + "sada"]
    if number % 100 == 10:
        return word + ["kümme"]
    print(trunc(number % 100))
    if 10 < trunc(number % 100) and trunc(number % 100) < 20:
        return word + [digit[number % 10] + "teist"]
    if trunc((number % 100) / 10) != 0:
        word = word + [digit[trunc((number % 100) / 10)] + "kümmend"]
    if number % 10 != 0:
        word = word + [digit[number % 10]]
    return word


def convertInt(number: int) -> List[str]:
    if number > 10**15 - 1:
        raise Exception("can't convert number bigger than |(10**15)-1|")
    if number == 0:
        return [digit[0]]
    word = []
    loop = 0
    while number:
        if number % 1000:
            word = convertIntHundreds(number % 1000) + ([places[loop](number % 1000)] if loop > 0 else []) + word # get last 3 digits on the right
            print(word)
        number = trunc(number / 1000)
        loop += 1
    return word


def euro(event, context=None):
    if 'queryStringParameters' not in event:
        return {
            "statusCode": 400,
            "body": "missing query parameter 'n'"
        }
    try:
        query = event['queryStringParameters']
        query = query if query is not None else {}
        number = float(query.get('n', 0).replace(",", "."))
        word = []
        if number < 0:
            word = ["miinus"]
        whole = abs(trunc(number))
        decimal = trunc(abs(number - trunc(number)) * 100)
        word = word + convertInt(whole) + [("euro" if whole == 1 else "eurot"), "ja"] + convertInt(decimal) + [("sent" if decimal == 1 else "senti")]
        word = " ".join(word)
    except Exception as ex:
        word = "Error: " + str(ex)
    return {
        "statusCode": 200,
        "body": word
        }


def test(number, word):
    result = euro({"queryStringParameters": {"n": str(number)}})['body']
    print(number, result)
    assert result == word, f"{result} != {word}"


if __name__ == '__main__':
    test(0, 'null eurot ja null senti')
    test(1, 'üks euro ja null senti')
    test(-1, 'miinus üks euro ja null senti')
    test(10, 'kümme eurot ja null senti')
    test(-123, 'miinus ükssada kakskümmend kolm eurot ja null senti')
    test(456, 'nelisada viiskümmend kuus eurot ja null senti')
    test(1001, 'üks tuhat üks eurot ja null senti')
    test(9090, 'üheksa tuhat üheksakümmend eurot ja null senti')
    test(10**9 + 1, 'üks mijard üks eurot ja null senti')
    test(0.10, 'null eurot ja kümme senti')
    test(1.789, 'üks euro ja seitsekümmend kaheksa senti')
    test(-110.45, 'miinus ükssada kümme eurot ja nelikümmend viis senti')
    test(15, 'viisteist eurot ja null senti')
    test(22, 'kakskümmend kaks eurot ja null senti')
    test(456, 'nelisada viiskümmend kuus eurot ja null senti')
    test(1000000, 'üks miljon eurot ja null senti')
    test(2345678, 'kaks miljonit kolmsada nelikümmend viis tuhat kuussada seitsekümmend kaheksa eurot ja null senti')

