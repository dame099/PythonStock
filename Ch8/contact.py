class Contact:
    def __init__(self,name,phone_number,e_mail,addr):
        self.name = name
        self.phone_number = phone_number
        self.e_mail = e_mail
        self.addr = addr

    def print_info(self):
        print("Name : " , self.name)
        print("Phone Number : " , self.phone_number)
        print("E-mail : " , self.e_mail)
        print("Address : " , self.addr)

    def set_contact(self):
        self.name = input("Name : ")
        self.phone_number = input("Phone Number : ")
        self.e_mail = input("E-mail : ")
        self.addr = input("Address : ")

def run():
    me = Contact(0,0,0,0)
    me.set_contact()
    me.print_info()

if __name__ == "__main__":
    run()


 