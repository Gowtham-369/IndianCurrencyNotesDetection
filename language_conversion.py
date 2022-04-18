# from gtts import gTTS 

convert_word_to_hindi = {
    "and" : "aur ",
    "one" : "ek",
    "two" : "do",
    "three": "teen",
    "four": "chaar", 
    "five" : "paanch", 
    "six" : "chhah",
    "seven" : "saat",
    "eight": "aath", 
    "nine" : "nau",
    "10Rupees": "das rupaye ",
    "20Rupees": "bees rupaye ",
    "50Rupees": "pachaas rupaye ",
    "100Rupees": "ek sau rupaye ",
    "200Rupees": "do sau rupaye ",
    "500Rupees": "paanch sau rupaye ",
    "Notes": "ke not ",
    "Note" : "ka not ",
}

def convert_lang(text):
    res = ""
    if(text == "Reload the page and try with another better image"):
        res = "Page ko punah lod karo aur ek aur behatar chhavi ke saath prayaas karo"
    else:
        wordArr = list(text.split(' '))
        res = "is chhavi mein "
        for word in wordArr:
            if(word in convert_word_to_hindi):
                res += convert_word_to_hindi[word]

        res += "hai"
        
    return res
