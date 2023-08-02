from classes import AddressBook
from func import add_phone, get_birthdate, change, delete, delete_phones, find_contact, help_me, phone, show_all, when_birthday, unknow_command, add_email, hello, future_congratulation, whom_to_congratulate, correct_email, add_note, find_note

COMMANDS = {
    add_phone: ("add", "+"),
    change: ("change", "зміни"),
    exit: ("bye", "exit", "end", "q", "close", "esc", "good bye", "quit"),
    show_all: ("show all", "all", "view"),
    delete:("del","delete", "-", "kill"),
    delete_phones:("del phones", "delete phones"),
    find_contact:("find", "поиск", "ищи"),
    get_birthdate:("birthdate", "дата"),
    when_birthday:("birthday", "др"),
    phone:("phone", "тел", "телефон"),
    hello:("hello", "hi", "привет"),
    help_me:("help",),
    add_email:("email", "mail", "мыло", "почта"),
    future_congratulation:("congratulate", "поздравить", "др?"),
    whom_to_congratulate:("whom birthday", "period birthday"),
    correct_email:("change email", "change mail", "correct email", "correct mail"),
    add_note:("note", "заметки", "add note"),
    find_note:("find note",)
}

def main():
    working_bot= True
    phone_book = AddressBook()
    phone_book.load_book()
    phone_book.log("Open address_book")

        
    while working_bot:
        text = input("->")
        
        command, data = parser(text.lower())


        if command == exit:
            print("bye")
            working_bot= False
        else:
            print(command(phone_book, *data))
            phone_book.log(" ".join([command.__name__, *data]))

    phone_book.save_book()
    phone_book.log("Close address_book")
    
def parser(text:str):
    comm = ""
    result = [""]
    command = unknow_command
      
    for cmd, kwds in COMMANDS.items():

        for kwd in kwds:
  
            if text.startswith(kwd):
                
                if len(kwd) > len(comm):

                    comm = kwd
                    command = cmd

                    result = text.removeprefix(comm).strip().split(" ")
            elif text.lower().startswith("help"):
                return help_me, text.removeprefix("help").split(" ")
    return command, result      
     

if __name__ == '__main__':
    main()