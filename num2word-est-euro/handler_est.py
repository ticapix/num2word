#!/usr/bin/env python3

from math import trunc

places = ["", "tuhat ", "miljon ", "mijard ", "triljon "]

digit = ["null ", "üks ", "kaks ", "kolm ", "neli ", "viis ", "kuus ", "seitse ", "kaheksa ", "üheksa "]


def convertIntHundreds(number: int):
    word = ""
    if trunc(number / 100) != 0:
        word = digit[trunc(number / 100)] + "sada "
    if number % 100 == 10:
        return word + "kümme "
    if trunc((number % 100) / 10) != 0:
        word = word + digit[trunc((number % 100) / 10)] + "kümmend "
    if number % 10 != 0:
        word = word + digit[number % 10]
    return word


def convertInt(number: int):
    if number > 10**15 - 1:
        raise Exception("can't convert number bigger than |(10**15)-1|")
    if number == 0:
        return digit[0]
    word = ""
    loop = 0
    while number:
        if number % 1000:
            word = convertIntHundreds(number % 1000) + places[loop] + word # get last 3 digits on the right
        number = trunc(number / 1000)
        loop += 1
    return word


def euro(event, context=None):
    try:
        query = event['queryStringParameters']
        query = query if query is not None else {}
        number = float(query.get('n', 0))
        word = ""
        if number < 0:
            word = "miinus "
        whole = abs(trunc(number))
        decimal = trunc(abs(number - trunc(number)) * 100)
        word = word + convertInt(whole) + ("euro" if whole == 1 else "eurot") + " ja " + convertInt(decimal) +  ("sent" if decimal == 1 else "senti")
    except Exception as ex:
        word = str(ex)
    return {
        "statusCode": 200,
        "body": word
        }


def test(number, word):
    result = euro({"queryStringParameters": {"n": str(number)}})['body']
    print(number, result)
    assert result == word


if __name__ == '__main__':
    test(0, 'null eurot ja null senti')
    test(1, 'üks euro ja null senti')
    test(-1, 'miinus üks euro ja null senti')
    test(10, 'kümme eurot ja null senti')
    test(-123, 'miinus üks sada kaks kümmend kolm eurot ja null senti')
    test(456, 'neli sada viis kümmend kuus eurot ja null senti')
    test(1001, 'üks tuhat üks eurot ja null senti')
    test(9090, 'üheksa tuhat üheksa kümmend eurot ja null senti')
    test(10**9 + 1, 'üks mijard üks eurot ja null senti')
    test(0.10, 'null eurot ja kümme senti')
    test(1.789, 'üks euro ja seitse kümmend kaheksa senti')
    test(-110.45, 'miinus üks sada kümme eurot ja neli kümmend viis senti')
