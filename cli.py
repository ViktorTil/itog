from classes import AddressBook
from func import add_phone, get_birthdate, change, delete, delete_phones, find_contact, help_me, phone, show_all, when_birthday, unknow_command, add_email, hello, future_congratulation, whom_to_congratulate, correct_email, add_note, find_note

commands = ["hello", ["good bye", "close", "exit", "bye", "esc", "q"], "add", "birthdate", "change", "del", "del phones", "find", "help",  "phone", "show all", "birthday"]
answers = ["How can I help you?", "Good bye!", add_phone, get_birthdate, change, delete, delete_phones, find_contact, help_me, phone, show_all, when_birthday]

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
     
'''
def parser(text:str):
    comm = ""
    command = None
    for cmd, kwds in COMMANDS.items():

        for kwd in kwds:
            if text.lower().startswith(kwd):
                if len(kwd) > len(comm):
                    comm = kwd
                    command = cmd
                    data = text.lower().removeprefix(comm).strip()

    return command, data.split(" ")'''

def reply(command, phone_book):
    bot=True
    operator=command.split(" ")
    if command in commands[1]:
        print(answers[1])
        
        bot = False
    elif operator[0] in commands or (" ".join(command.split(" ")[:2])) in commands:
        try:
            index_comm = commands.index(" ".join(command.split(" ")[:2]))
        except ValueError:
            index_comm = commands.index(operator[0])
        

        try:

            print(answers[index_comm](phone_book, *command.removeprefix(
                commands[index_comm]).lstrip().split(" ")))

        except:
            print(answers[index_comm])
    else:
        print(f'Введите правильную команду :\033[34m{commands[0]}, {", ".join(commands[2:])}\033[0m или \033[34m{", ".join(commands[1])}\033[0m для выхода')

    return bot


if __name__ == '__main__':
    main()