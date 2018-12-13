TEXT = "As you’ve just heard, punctuation is everywhere. While it can be a struggle at first to learn the rules that come along with each mark, punctuation is here to help you: these marks were invented to guide readers through passages—to let them know how and where words relate to each other. When you learn the rules of punctuation, you equip yourself with an extensive toolset so you can better craft language to communicate the exact message you want."


def findFrequencies(text):
    text = text.lower()
    nonapprovedchars = r" :\;,./()*&—–^%\#@!?~"
    tempword = ""
    d = {}
    for character in text:
        if character not in nonapprovedchars:
            tempword += character
        elif character in nonapprovedchars:
            if tempword != "": 
                if tempword in d:
                    d[tempword] += 1
                    tempword = ""
                else:
                    d[tempword] = 1
                    tempword = ""
    return d

print(findFrequencies(TEXT))