# Context Manager for a  Connection
"""
Concept Covered
Context Managers
enter()
exit()
"""
class Open_File():
    def __init__(self , filename , mode):
        self.filename = filename
        self.mode = mode
    def __enter__(self):
        print("opening file ")
        self.file = open(self.filename , self.mode)
        return self.file
    def __exit__(self, exc_type, exc, tb):
        print("closing file ")
        self.file.close()

filename = input("enter filename : ")
with Open_File(filename , "w+") as f:
    f.write("Context manager ")
    f.seek(0)
    print(f.read())
