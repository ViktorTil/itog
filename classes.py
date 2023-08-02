from collections import UserDict
from datetime import datetime, timedelta
import pickle
import json
import re

class Field:
    def __init__(self, value):
        self.value = value
        
    def __str__(self) -> str:
        if self.value:
            return self.value
        else:
            return f"Вводите корректно номера телефонов, например, в формате: \033[34m0XX-XXX-XX-XX\033[0m"
                                                            
    
    def __repr__(self) -> str:
        return str(self)
        


class Birthday(Field):
    def __init__(self, value : str = None):
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, value):
        try:
            birth_date = re.findall('\d+', value)
            if birth_date[2] and len(birth_date[2])==4:
                birth_date[2] = birth_date[2][2:]
            birth ="/".join(birth_date)
            self.__value = datetime.strptime(birth, '%d/%m/%y').date()
        except ValueError:
            print(f"Введите корректную дату в формате \033[34mmm-dd-yyyy\033[0m")
    
    def __str__(self) -> str:
        try:
            return f"дата рождения: \033[34m{self.value.strftime('%d-%m-%y')}\033[0m"

    
        except AttributeError:
            return ""

class Email(Field):
    def __init__(self, email):
        self.__value = None
        self.value = email
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, email):
        try:
            pattern = r"[a-zA-Z]{1}[\w\.\-]+@[a-zA-z]+\.[a-zA-Z]{2,3}"
            result = (re.search(pattern, email)).group()
            self.__value = result.lower()
            
        except AttributeError:
            print(f"Введите корректно email в формате \033[34msomebody@example.com\033[0m")

        
    def __str__(self) -> str:
        return f"Email: \033[34m{self.value}\033[0m"

class Name(Field):
    def __str__(self):
        return f"контакт(а): \033[34m{self.value}\033[0m :"

class Note(Field):
    def __init__(self, value):
        self.value = value
        
    def __add__(self, other):
        self.value = ", ".join([self.value, other.value])
        return self
    
    def __str__(self):
        return f"Заметка: \033[34m{self.value}\033[0m"
        
        

class Phone(Field):
    def __init__(self, phone):
        self.__value = None
        self.value = phone
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, phone):
        try:
            pattern = r"\+?3?8?[- (]?0\d{2}[- )]?\d{3}[- ]?\d{2}[- ]?\d{2}$"
            add_cod = "+380"
            result = (re.search(pattern, phone)).group()
            res_phone=re.sub(r"(\D)","",result)
            form_phone = add_cod[0:13-len(res_phone)] + res_phone
            self.__value = form_phone
        
        except AttributeError:
            print(f"Вводите корректно номера телефонов, например, в формате: \033[34m0XX-XXX-XX-XX\033[0m")   




    

class Record:
    def __init__(self, name: Name, phone: Phone = None, birthday : Birthday = None, email : Email = None, note : Note = None):
        self.phones = []
        self.name = name
        if phone and phone.value:
            self.phones.append(phone)

        self.birthday = birthday
        self.email = email
        self.note = note

    def add_note(self, note: Note):
        try:
            self.note = self.note + note
        except AttributeError:
            self.note = note

    def add_phone(self, phone: Phone):
        if phone.value:
            self.phones.append(phone)

    def change_phone(self, old_phone: Phone, new_phone: Phone):
        if new_phone.value:
            for index, phone in enumerate(self.phones):
                if phone.value == old_phone.value:
                    self.phones.pop(index)
                    self.add_phone(new_phone)
                    return f"У \033[34m{self.name}\033[0m телефон \033[34m{old_phone}\033[0m изменён на \033[34m{new_phone}\033[0m"
            return f"Нет номера \033[34m{old_phone}\033[0m для изменения у \033[34m{self.name}\033[0m"
        return new_phone
    
    def change_email(self, old_email: Email, new_email: Email):
        if new_email.value and old_email.value:
            if  self.email.value == old_email.value:
                    self.email = new_email
                    return f"У \033[34m{self.name}\033[0m эл.почта \033[34m{old_email}\033[0m изменена на \033[34m{new_email}\033[0m"
            return f"Нет эл.почты \033[34m{old_email}\033[0m для изменения у \033[34m{self.name}\033[0m"
        return new_email
    
    def __calc_birthday(self):
            cd = datetime.now().date()
            nd = self.birthday.value
            if nd.month == 2 and nd.day == 29:
                new_bd = datetime(year = cd.year, month = 2, day = nd.day - int(bool(cd.year%4))).date()
            
                if new_bd < cd: 
                    new_bd = datetime(year = cd.year + 1, month = 2, day = nd.day - int(bool((cd.year+1)%4))).date()
            
            else:
                new_bd = new_bd = datetime(year = cd.year, month = nd.month, day = nd.day).date()
                if new_bd < cd:
                    new_bd = new_bd.replace(year = cd.year + 1)
            return (new_bd - cd).days      

              
    def days_to_birthday(self):
        cd = datetime.now().date()
        if hasattr(self, "birthday") and self.birthday:
            if self.__calc_birthday() > 0:
                return f"До Дня рождения {self.name} осталось \033[34m{self.__calc_birthday()}\033[0m дня(ей)"
            else:
                return f"У {self.name} сегодня День рождения! Поздравьте его 🥳"
                
                 
            '''
            nd = self.birthday.value
            if nd.month == 2 and nd.day == 29:
                new_bd = datetime(year = cd.year, month = 2, day = nd.day - int(bool(cd.year%4))).date()
            
                if new_bd < cd: 
                    new_bd = datetime(year = cd.year + 1, month = 2, day = nd.day - int(bool((cd.year+1)%4))).date()
            
            else:
                new_bd = new_bd = datetime(year = cd.year, month = nd.month, day = nd.day).date()
                if new_bd < cd:
                    new_bd = new_bd.replace(year = cd.year + 1)
            if  new_bd != cd:
                return f"До Дня рождения \033[34m{self.name}\033[0m осталось \033[34m{(new_bd - cd).days}\033[0m дня(ей)"
            return f"У контакта \033[34m{self.name}\033[0m сегодня День рождения! Поздравьте его 🥳"'''
        else:
            return f"У {self.name} нет в книге даты рождения "
    
    def del_phone(self):    
        self.phones.clear()
        return f"Номера \033[34m{self.name}\033[0m удалены из книги"
        
    def __str__(self) -> str:
       # try:
        return f"{self.name} \033[34m{', '.join(str(p) for p in self.phones)}\033[0m {self.birthday if self.birthday else ''} {self.email if self.email else ''} {self.note if self.note else ''}"
       # except AttributeError:
       #     return f"{self.name} \033[34m{', '.join(str(p) for p in self.phones)}\033[0m {self.birthday if self.birthday else ''} {self.email if self.email else ''}"
            

class AddressBook(UserDict):

    filename = "data.bin"
    
    def add_record(self, record : Record):
        self.data[record.name.value] = record
    
    def congratulate(self):
        future_week={"Monday" : [], "Tuesday" : [], "Wednesday" : [],"Thursday" : [], "Friday" : [] }
        cd = datetime.now()

        start = max(5 - cd.weekday(), 0)
        finish = 12 - cd.weekday()

        for record in self.data.values():
            if record.birthday:
                if start <= record._Record__calc_birthday() <= finish:
                    day = (cd + timedelta(record._Record__calc_birthday())).strftime("%A")
                    try:
                        future_week[day].append(record)
                    except KeyError:
                        future_week["Monday"].append(record)
                        
                    
                    

            
        return future_week
    
    def congratulate_period(self, number_days):
        start_period = datetime.now().date()
        end_period = start_period + timedelta(number_days)
        list_congratulate = []
        for record in self.data.values():
            if record.birthday:
                if record._Record__calc_birthday() <= number_days:
                    list_congratulate.append(record)
        if list_congratulate:
            return f"За период с {start_period} по {end_period} в вашей книге будут следующие именинники: {', '.join(str(p) for p in list_congratulate)}"
        else:
            return f"За период с {start_period} по {end_period} в вашей книге нет именинников"
    


    def del_record(self, record):
        self.data.pop(record.name.value)
        return f"\033[34m{record.name}\033[0m удалён из Вашей книги"
        
    def iterator(self, page_len = 3):
        page = []

        for record in self.data.values():

            page.append(record)

            if len(page) == page_len:
                yield page
                page = []

        if page:
            yield page
    
    def load_book(self):

        try:
            with open(self.filename, "rb") as fh:
                self.data = pickle.load(fh)
        except FileNotFoundError:
            pass
    
    def save_book(self):
        with open(self.filename, "wb") as fh:
            pickle.dump(self.data, fh)   
            
    def log(self, action):
       # cd = datetime.now().date()
        current_time = datetime.strftime(datetime.now(), '%d-%m-%y::%H:%M:%S')
        message = f'[{current_time}] {action}'
        with open('logs.txt', 'a') as file:
            file.write(f'{message}\n')
    
    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())
    
    def __repr__(self) -> str:
        return str(self)
