from time import sleep
import win32com.client as win32
 
RANGE = range(3, 8)
 
def word():
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc = word.Documents.Add()
    word.Visible = True
    sleep(1)
 
    rng = doc.Range(0,0)
    rng.InsertAfter('Hacking Word with Python\r\n\r\n')
    sleep(1)
    for i in RANGE:
        rng.InsertAfter('Line %d\r\n' % i)
        sleep(1)
    rng.InsertAfter("\r\nPython rules!\r\n")
 
    doc.Close(False)
    word.Application.Quit()
 
if __name__ == '__main__':
    word()