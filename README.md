
# Convert a number to words in euro in Estonian

## Demo

### Curl

```bash
$ curl https://dnesxr2s91.execute-api.eu-west-3.amazonaws.com/num2word/est/euro?n=-110.45
miinus ükssada kümme eurot ja nelikümmend viis senti
```

### Microsoft Excel

```
=WEBSERVICE(CONCAT("https://dnesxr2s91.execute-api.eu-west-3.amazonaws.com/num2word/est/euro?n=",B10))
```

## Install Serverless tool

```bash
make deps
```

## Create serverless template

```bash
serverless create --template aws-python3 --path num2word-est --name num2word-est
```

## Deploy function

```bash
cd num2word-est && serverless deploy
```
