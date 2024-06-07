import img2pdf

class pdfCreate:
    def __init__(self, pathToSave , pathToLoad , imagesList):
        with open(f"{pathToSave}AllCard.pdf" , "wb") as f:
            f.write(img2pdf.convert([f"{pathToLoad}{i}" for i in imagesList]))
    
        print("\n"*20, "DONE PRESS ENTER TO CONTINUE !! ")
        input()