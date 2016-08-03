from Download import *
from queue import Queue
from Sorting import *
from DribbbleStorage import *
import time


def make_menu():
    # Greeting
    print("====== Dribbble  Queue ======")
    print("*****************************")
    print("*         Home Page         *")
    print("*****************************")

    # Directory Info
    print("*** Note: Image will be saved in directory named by current date.")

    # Top Menu
    print("--- a: Daily Top 10")
    print("--- b: Daily Top 10 by tags")
    print("--- c: Download all images")
    print("--- q: Exit")

    top_in = input("--- Enter the letter of the function: ")
    while top_in != 'a' and top_in != 'b' and top_in != 'c' and top_in != 'q':
        print("*** Warning: Invalid Command!")
        top_in = input("--- Enter the letter of the function: ")

    # Command

    return top_in


if __name__ == '__main__':
    print("****** Program instantiate... ******")
    time.sleep(2)
    factory = Factory()
    hidden = os.system('clear')
    print(' ______   _______ _________ ______   ______   ______   _        _______ \n'
          '(  __  \ (  ____ )\__   __/(  ___ \ (  ___ \ (  ___ \ ( \      (  ____ \ \n'
          '| (  \  )| (    )|   ) (   | (   ) )| (   ) )| (   ) )| (      | (    \/\n'
          '| |   ) || (____)|   | |   | (__/ / | (__/ / | (__/ / | |      | (__    \n'
          '| |   | ||     __)   | |   |  __ (  |  __ (  |  __ (  | |      |  __)   \n'
          '| |   ) || (\ (      | |   | (  \ \ | (  \ \ | (  \ \ | |      | (      \n'
          '| (__/  )| ) \ \_____) (___| )___) )| )___) )| )___) )| (____/\| (____/\ \n'
          '(______/ |/   \__/\_______/|/ \___/ |/ \___/ |/ \___/ (_______/(_______/\n')
    command = make_menu()
    while command != 'q':
        if command == 'a':
            factory.extracting()
            hidden = os.system('clear')
            print("======== Work Done! ======")
            factory.report_top()
            os.chdir('..')
            command = make_menu()
        elif command == 'b':
            raw_in = input("--- Enter something you are interested in, separate by comma: ")
            raw_tags = raw_in.split(',')
            tags = []
            for tag in raw_tags:
                tags.append(tag.strip())
            print("====== Tags Received ======")
            time.sleep(2)
            factory.add_tag_set(tags)
            factory.extracting()
            hidden = os.system('clear')
            print("====== Work Done! ======")
            factory.report_top()
            os.chdir('..')
            command = make_menu()
        elif command == 'c':
            print("====== Note: This function might take several minutes ======")
            time.sleep(2)
            factory.download_all()
            hidden = os.system('clear')
            print("====== Work Done! ======")
            os.chdir('..')
            command = make_menu()
    print("******* Now Exit! Thanks for using!")
    time.sleep(2)
    hidden = os.system('clear')
    exit(0)
