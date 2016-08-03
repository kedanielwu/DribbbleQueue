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

    top_in = input("--- Enter the letter of the function: ")
    while top_in != 'a' and top_in != 'b' and top_in != 'c':
        print("*** Warning: Invalid Command!")
        top_in = input("--- Enter the letter of the function: ")

    # Command

    return top_in

if __name__ == '__main__':
    print("****** Program instantiate... ******")
    time.sleep(2)
    factory = Factory()
    command = make_menu()
    if command == 'a':
        factory.extracting()
        print("======== Work Done! ======")
        factory.report_top()
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
        print("====== Work Done! ======")
        factory.report_top()
    elif command == 'c':
        print("====== Note: This function might take several minutes ======")
        time.sleep(2)
        factory.download_all()
        print("====== Work Done! ======")

