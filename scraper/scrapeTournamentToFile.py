import scraper
import sys

def main():
    if len(sys.argv) != 3:
        print("Idiot")
        print("python3 scrapteTournamentToFile.py <url to tournament> <file.txt>")
    
    pgnList = scraper.completePgnStringFromUrl(sys.argv[1])

    outputFile = open(sys.argv[2],'w')

    outputFile.write(pgnList)
    outputFile.close()


if __name__ == "__main__":
    main()