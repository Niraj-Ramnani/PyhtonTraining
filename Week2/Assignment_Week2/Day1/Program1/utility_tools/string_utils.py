def reverse_words(text):
    words = text.split()
    reverselist = words[::-1]
    return " ".join(reverselist)

def count_vowel(text):
    vowels = "aeiouAEIOU"
    cnt = 0
    for ch in text:
        if ch in vowels:
            cnt +=1
    return cnt

