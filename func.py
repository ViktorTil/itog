from classes import Name, Phone, Record, Birthday, Email, Note
import re
from functools import wraps


def error_with_func(arg1,arg2):
    
    def input_error(func):
        @wraps(func)
        def proc_error(phone_book, *args):
            try:
               return func(phone_book, *args)
            except IndexError :
                return f'Добавьте все данные корректно в команду \033[34m{arg1}\033[0m по шаблону: \033[34m<{arg2}>\033[0m'
            except ValueError as e:
                return e
            except AttributeError as e:
                return e
            except KeyError:
                return f'Нет контакта: \033[34m{args[0]}\033[0m в вашей книге'
        return proc_error
    return input_error

@error_with_func('email', 'email [name] [email: vasya.pupkin@posta.com]') 
def add_email(phone_book, *args):
    name = args[0].capitalize()
    rec = phone_book[name]
    email = Email(args[1])
    message_email = f"Не могу добавить строку : \033[34m{args[1]}\033[0m к контакту {name}"
    if email.value:
        rec.email = email
        message_email = f"{email} добавлен к контакту {name}"
        
    return message_email

@error_with_func('add note', 'add note [name] [note]')
def add_note(phone_book, *args):
    name = args[0].capitalize()
    phone_book[name].add_note(Note(" ".join(args[1:])))
    return f"Заметка \033[34m{' '.join(args[1:])}\033[0m к контакту \033[34m{name}\033[0m успешно добавлена"
    
    

@error_with_func('add', 'add [name] [phone]')  
def add_phone(phone_book, *args):

    name = args[0].capitalize()
    contact_phone = "".join(args[1:])


    if len(args) >= 2:
        if not name in phone_book.keys():
            phone = Phone(contact_phone)
            rec = Record(Name(name), phone)
            phone_book.add_record(rec)
            if phone.value:
                message_add = f"Новый контакт \033[34m{name}\033[0m с номером \033[34m{phone}\033[0m создан"
            else:
                message_add = f"Новый контакт \033[34m{name}\033[0m без номера создан"
        else: 
            rec = phone_book.get(name)
            phone = Phone(contact_phone)
            if phone.value:
                rec.add_phone(phone)
                message_add = f"Номер \033[34m{phone}\033[0m добавлен к контакту \033[34m{name}\033[0m"
            else:
                message_add = f"Не могу добавить номер \033[34m{contact_phone}\033[0m к контакту \033[34m{name}\033[0m"
                
                
    else:
        message_add =  "Добавьте в команду \033[34madd\033[0m номер телефона"
        if not name in phone_book.keys():
            rec = Record(Name(name))
            phone_book.add_record(rec)
            message_add = f"Контакт \033[34m{name}\033[0m без номера добавлен"
        
    return message_add
        
@error_with_func('birthdate', 'birthdate [name] dd-mm-yy')
def get_birthdate(phone_book, *args):
    name = args[0].capitalize()
    rec = phone_book[name]
    birth_list = re.findall(r'\d{2}', "".join(args[1:]))
    birth_date = ",".join([birth_list[0],birth_list[1],"".join(birth_list[2:])])
    birth = Birthday(birth_date)
    message_birthday = f"Контакту \033[34m{name}\033[0m не могу записать эту дату рождения "
    if birth.value:
        rec.birthday = birth
        message_birthday= f"Контакту \033[34m{name}\033[0m добавили дату рождения: \033[34m{birth.value}\033[0m"
    return message_birthday

    
@error_with_func('birthday', 'birthday [name]')
def when_birthday(phone_book, *args):
    name = args[0].capitalize()
    rec = phone_book[name]
    return rec.days_to_birthday()


@error_with_func('change', 'change [name] [old_phone], [new_phone]')
def change(phone_book, *args):
    name = args[0].capitalize()
    args = [x for x in ''.join(args[1:]).split(',') if x ]
    old_phone = args[0]
    new_phone = args[1]
    rec = phone_book[name]
    return rec.change_phone(Phone(old_phone), Phone(new_phone))

@error_with_func('correct email', 'correct email [name] [old_email], [new_email]')
def correct_email(phone_book, *args):
    name = args[0].capitalize()
    rec = phone_book[name]
    args = [x for x in ''.join(args[1:]).split(',') if x ]
    old_email = args[0]
    new_email = args[1]
    return rec.change_email(Email(old_email), Email(new_email))


def future_congratulation(phone_book, *args):
    message_congratulate = f"\033[31mНа следующей неделе не забудьте поздравить:\033[0m \n\n"
    for day, rec in phone_book.congratulate().items():
        if rec:
            message_congratulate += f"\033[31m{day}\033[0m: {', '.join(map(str,rec))} \n"
            
    return message_congratulate

@error_with_func('del', 'del [name]')
def delete(phone_book, *args):
    name=args[0].capitalize()
    rec = phone_book[name]
    return phone_book.del_record(rec)
 
        
@error_with_func('del phones', 'del phones [name]')
def delete_phones(phone_book, *args):
    name = args[0].capitalize()
    rec = phone_book[name]
    return rec.del_phone()




@error_with_func('find', 'find [str]')
def find_contact(phone_book, *args):
    str_find = args[0]
    if not str_find:
        raise ValueError
    itog_find = ""
    for rec in phone_book.values():
        united_value = rec.name.value.lower() + ''.join(list(phone.value for phone in rec.phones))
        find_str = united_value.find(str_find)
        
        if find_str != -1:
            itog_find = itog_find + f"{rec}\n"

    if not itog_find:
        itog_find = f'По вашему поиску в книге ничего не найдено'
         
    return itog_find

@error_with_func('find note', 'find note [str]')
def find_note(phone_book, *args):
    str_find = "".join(args)
    itog_find = ""
    print(str_find)
    for rec in phone_book.values():
        find_str = rec.note.value.find(str_find)
        if find_str != -1:
            itog_find = itog_find + f"{rec}\n"
            
    if not itog_find:
        itog_find = f'По вашему поиску в книге ничего не найдено'
        
    return itog_find

def hello(*args):
    return f'Hello! How can I help you?/ Привет! Чем могу помочь?'

def help_me(*args):
    with open("help.txt", "r") as fh:
        lines = fh.readlines()[1:]
        help_info = "".join(lines)
        """
        for line in lines:
            try:
                print(line.replace("\n",""))
            except AttributeError:
                print(line)
        """
    return help_info

@error_with_func('phone', 'phone [name]')
def phone(phone_book, *args):
    name = args[0].capitalize()
    return f'Данные {phone_book[name]}'


def show_all(phone_book, *args):
    page_len = 3

    if args:
        try:
            page_len = int(args[0])
        except ValueError:
            pass
    num_rec = len(phone_book) 

    for i in phone_book.iterator(page_len):
        num_rec -= page_len
        for rec in i:
            print(rec)
        if  num_rec > 0:
            input(f"Вывод по \033[34m{page_len}\033[0m контактов из книги, для продолжения нажмите \033[34m[ENTER]\033[0m")
    return f"\r"
  
def unknow_command(*args):
    
    with open("help.txt", "r") as fh:
        line_0 = fh.readline()
        
    return f"Для работы с чат-ботом используйте команды из списка: \033[34m{line_0}\033[0m"

@error_with_func('whom birthday', 'whom birthday [number days->int]')
def whom_to_congratulate(phone_book, *args):
    return phone_book.congratulate_period(int(args[0]))
    