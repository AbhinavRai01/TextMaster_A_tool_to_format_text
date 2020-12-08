from django.shortcuts import render
from spellchecker import SpellChecker


def removepunctuation(text):
    punctuations = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    djtext = text
    returnvalue = ""

    for char in djtext:
        if char not in punctuations:
            returnvalue = returnvalue + char

    return returnvalue


def index(request):
    return render(request, "index.html")


def edited(request):
    text = request.GET.get('text')
    italics = request.GET.get('italics', 'off')
    bold = request.GET.get('bold', 'off')
    upper = request.GET.get('upper', 'off')
    removepunc = request.GET.get('removepunc', 'off')
    spellcheck = request.GET.get('spelling', 'off')
    newlineremover = request.GET.get('removenewline', 'off')
    reluctlineremover = request.GET.get('removerelucline', 'off')
    countwords = request.GET.get('countwords', 'off')
    countchar = request.GET.get('countchar', 'off')
    countsentences = request.GET.get('countsentences', 'off')
    countparagraph = request.GET.get('countparagraph', 'off')

    analyzed = text
    wordcount = ""
    correction = {}
    spellcorrection = ""
    count = ""

    if upper == "on":
        analyzed = analyzed.upper()

    if removepunc == "on":
        analyzed = removepunctuation(analyzed)

    if spellcheck == "on":
        spelltext = removepunctuation(analyzed)
        spell = SpellChecker()

        words = spelltext.split()
        wrongwords = spell.unknown(words)

        correctiondic = {}

        for i in wrongwords:
            correct = spell.correction(i)
            correctiondic[i] = correct

        spellcorrection = "<br><h4> Spelling correction </h4> "

        for key in correctiondic:
            spellcorrection = spellcorrection + '<b align = "center" style = "color : red">' + str(
                key) + '</b>' + ' - ' '<b>' + str(correctiondic[key]) + '<b>' + '</b><br>'

    analyzed = str(analyzed)
    if italics == "on":
        analyzed = "<i>" + analyzed + "</i>"

    if bold == "on":
        analyzed = "<b>" + analyzed + "</b>"

    if reluctlineremover == 'on':
        analyzed = analyzed.replace("\r", "")

        i = 0

        while i < len(analyzed.split('\n')):
            analyzed = analyzed.replace('\n\n\n', '\n')
            analyzed = analyzed.replace('\n\n', '\n')

            i += 2

    if newlineremover == 'off':
        analyzed = analyzed.replace("\n", " <br> ")

    if countchar == 'on':
        i = 0
        for char in analyzed:
            i += 1

        count = count + "<b>Character Count : </b><b style = 'color:green'>" + str(i) + "</b><br>"

    if countwords == 'on':
        wordcount = len(text.split())
        count = count + "<b>Word Count : </b><b style = 'color:green'>" + str(wordcount) + "</b><br>"

    if countsentences == 'on':
        i = 0
        for char in analyzed:
            if char == '.':
                i += 1

        count = count + "<b>Sentence Count : </b><b style = 'color:green'>" + str(i) + "</b><br>"

    if countparagraph == 'on':
        paras = analyzed.find("<br>")
        count = count + "<b>Paragraph Count : </b><b style = 'color:green'>" + str(paras) + "</b><br>"

    analyzed = '<h6>' + analyzed + '<h6>'

    print(analyzed)
    print(text)

    params = {'analyzed': analyzed, 'spelling': spellcorrection, 'count': count}
    return render(request, 'edited.html', params)
