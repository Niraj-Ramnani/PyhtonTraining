#Reverse Iterator
class ReverseIterator:
    def __init__(self, text):
        self.text = text
        self.index = len(text) - 1

    def __iter__(self):
        return self

    def __next__(self):
        if self.index < 0:
            raise StopIteration
        ch = self.text[self.index]
        self.index -= 1
        return ch


string = input("Enter a string: ")

reverse = ReverseIterator(string)

print("Reversed String: ", end="")
for ch in reverse:
    print(ch, end="")