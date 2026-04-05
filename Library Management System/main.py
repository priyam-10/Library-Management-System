import random
import string
from pathlib import Path
import json

class lib_management :

    __id = "admin"
    __pass = 1234
    
    user_data = 'data.json'
    user_book = 'book.json'

    data = []
    books = []

    try : 
        if Path(user_data).exists():
            with open(user_data) as f :
                data = json.load(f)
        else :
            print("File not exists !")


        if Path(user_book).exists():
            with open(user_book) as f :
                books = json.load(f)
        else :
            print("File not exists !")
    except Exception as err :
        print(f"Error accour due to {err}")
    


    @staticmethod
    def __update_userdata () :
        with open(lib_management.user_data, 'w') as f :
            json.dump(lib_management.data, f)



    @staticmethod
    def __update_bookdata () :
        with open(lib_management.user_book, 'w') as f :
            json.dump(lib_management.books, f)


    @staticmethod
    def random_acc () :
        alp = random.choices(string.ascii_letters, k=4)
        num = random.choices(string.digits, k = 6)
        acc_random = alp + num
        random.shuffle(acc_random)
        return "".join(acc_random)




    def admin_login (self) :
        print("\n---- Welcome to Admin Login page ----\n")

        acc_no = input("Enter admin id : ")
        acc_pin = int(input("Enter admin pin : "))

        if acc_no == lib_management._lib_management__id and acc_pin == lib_management._lib_management__pass :
            return True
        else :
            return False




    def update_books(self):
        
        print(f"\n---- Enter new book detail ----\n")
        new_book = {
            "title" : input("Enter book name : "),
            "author" : input("Enter author name : "),
            "ISBN_no" : input("Enter the ISBN number : "),
            "quantity" : int(input("Enter the quantity : "))
        }

        lib_management.books.append(new_book)
        lib_management.__update_bookdata()
                



    def update_book_quantity(self) :

        isbn = input("Enter the isbn number : ")
        book_data = [ i for i in lib_management.books if i["ISBN_no"] == isbn]

        if not book_data :
            print("No records found")
        else :
            quantity = int(input("Enter new book quantitiy : "))
            book_data[0]['quantity'] += quantity
            lib_management.__update_bookdata()
            print(f"Qunatity has been added, now total has {book_data[0]['quantity']}")





    def book_list(self):
        num = 1

        for i in lib_management.books :
            print(f"{num}. Title : {i["title"]}, and its isbn number is {i["ISBN_no"]}, and it Quantity : {i["quantity"]}")
            num += 1



    def create_account(self) : 

        while True :

            info = {
                "name" : input("Enter your name : "),
                "age" : int(input("Enter your age : ")),
                "mobile number" : int(input("Enter your mobile number : ")),
                "account" : lib_management.random_acc(),
                "pin" : int(input("Enter 4 digit pin for your account : ")),
                "issue_book" : 0,
                "book_name" : "",
                "isbn" : ""
            }


            if ( info['age'] > 14 and len(str(info['mobile number'])) == 10 and  len(str(info['pin'])) == 4 ) :
                lib_management.data.append(info)
                lib_management.__update_userdata()
                print("\nAccount has been created successfully !!")
                print(f"PLease note your account id for login again and save it : {info['account']}")
                break


            else :
                print("\nSorry, you are not able to create a account beacause - ")

                if info['age'] <= 14 :
                    print("Your age is less than 15")
                if info['mobile number'] != 10 :
                    print("Please enter correct 10 digit mobile number")
                if len(str(info['pin'])) != 4 :
                    print("Please enter only 4 digit pin")

                check = input("Enter 'y' to retry and 'n' for exit : ").lower()
                if check == "y" :
                    pass
                elif check == "n" :
                    break
                else :
                    print("wrong input")
            



    def details(self, acc , pin) :

        database = [ i for i in lib_management.data if i['account'] == acc and i["pin"] == pin]

        for i in database[0] :
            print(f"{i} : {database[0][i]}")





    def issue_book(self, acc , pin):
        print("Note : We only provide one book at a time")
        database = [ i for i in lib_management.data if i['account'] == acc and i["pin"] == pin]
        
        
        if database[0]['issue_book'] == 1 :
            print("\nSorry, you already issue one book. To issue other book please return first")
        
        else : 
            isbn = input("Enter isbn number : ")
            bookdata = [ i for i in lib_management.books if i["ISBN_no"] == isbn ]

            if not bookdata :
                print("Sorry, we dont have that book")
            
            else :
                if bookdata[0]['quantity'] <= 0 :
                    print("Book out of stock")
                else :         
                    database[0]['issue_book'] = 1
                    database[0]['book_name'] = bookdata[0]['title']
                    database[0]['isbn'] = bookdata[0]['ISBN_no']
                    bookdata[0]['quantity'] -= 1
                    lib_management.__update_bookdata()
                    lib_management.__update_userdata()

                    print("Book have been issued.")





    def return_book(self, acc , pin):
        database = [ i for i in lib_management.data if i['account'] == acc and i["pin"] == pin]
        
        
        if database[0]['issue_book'] == 0 :
            print("\nYou have not issue any book")
        
        else : 
            isbn = database[0]['isbn']
            bookdata = [ i for i in lib_management.books if i["ISBN_no"] == isbn ]

            database[0]['issue_book'] = 0
            database[0]['book_name'] = ""
            database[0]['isbn'] = ""
            bookdata[0]['quantity'] += 1
            lib_management.__update_bookdata()
            lib_management.__update_userdata()

            print("Book have been returned.")




    def update_detail(self, acc , pin):

        database = [ i for i in lib_management.data if i['account'] == acc and i["pin"] == pin]

        print("Enter 1 for update name")
        print("Enter 2 for update phone number")
        print("Enter 3 for update pin")
        check = int(input("Enter number as per query : "))

        if check == 1 :
            name = input("Enter your new name : ")
            database[0]['name'] = name
            lib_management.__update_userdata()
            print("Name has been updated\n")

        elif check == 2 :
            phone = int(input("Enter your new phone number : "))
            if len(str(phone)) == 10 :
                database[0]['mobile number'] = phone
                lib_management.__update_userdata()
                print("Phone number has been updated\n")
            else :
                print("Please enter correct phone number\n")

        elif check == 3 :
            pin = int(input("Enter your new password : "))
            if len(str(pin)) == 4 :
                database[0]['pin'] = pin
                lib_management.__update_userdata()
                print("Pin has been updated\n")
            else :
                print("Please enter only 4 digit pin\n")

        else : 
            print("Wrong input\n")








library = lib_management()


while True :           # true statement for login and new account
    # This flag is checked by the outer menu loop; keep it True only when app should fully exit.
    logout = False

    print("\n---- Welcome to Library management System ----\n")
    print("Enter 1 for creating account")
    print("Enter 2 for Login")
    print("Enter 3 for Admin login")
    print("Enter 4 for exit")
    check = int(input("Enter number as per query : "))



    if check == 1 :
        print("\n---- Create acount ----\n")
        library.create_account()


    elif check == 2 :

        logout = False
        while True :
            

            print("\n---- Welcome to Login page ----\n")
            acc_no = input("Enter you account id : ")
            acc_pin = int(input("Enter your account pin : "))

            database = [ i for i in library.data if i["account"] == acc_no and i["pin"] == acc_pin ]


    
            if not database :
                print("Please Enter correct id and password, try again")
                check = input("Enter 'y' to retry and 'n' for exit : ").lower()
                if check == "y" :
                    pass
                elif check == "n" :
                    break
                else :
                    print("wrong input")
                    break


            else :
                print(f"\n---- Welcome {database[0]['name']} to Library management system ----\n")
                while True :    #  true statement  for different operation in a library system
                    
                    print("Press 1 for see details ")
                    print("Enter 2 for see Book list")
                    print("Enter 3 for issue book")
                    print("Enter 4 for return book")
                    print("Enter 5 for update details")
                    print("Enter 6 to exit")
                    check = int(input("Enter number as per query : "))


                    if check == 1 :
                        print(f"\n---- Account Details ----\n") 
                        library.details(acc_no, acc_pin)
                        print("")
                    
                    elif check == 2 :
                        print(f"\n---- Book List ----\n") 
                        library.book_list()
                        print("")

                    elif check == 3 :
                        print(f"\n---- Issue Book ----\n")
                        library.issue_book(acc_no, acc_pin)
                        print("")

                    elif check == 4 :
                        print(f"\n---- Return Book ----\n")
                        library.return_book(acc_no, acc_pin)
                        print("")

                    elif check == 5 :
                        print(f"\n---- update ----\n")
                        library.update_detail(acc_no, acc_pin)
                        print("")


            # logout part

                    elif check == 6 :
                        print(f"\n---- Thanks {database[0]['name']} for using Library management system ----\n")
                        logout = True
                        break
                    
                    else :
                        print(f"\n---- Thanks {database[0]['name']} for using Library management system ----\n")
                        logout = True
                        break
            
            # Problem: user submenu sets logout=True when user selects 6 (logout).
            # If we break without resetting, the outer loop also sees True and ends the program.
            if logout :
                logout = False
                break

                


    elif check == 3 :
        
        if library.admin_login() :
            print(f"\n---- Welcome Admin ----\n")

            while True :
                print("Enter 1 for book list")
                print("Enter 2 for to update book quantity")
                print("Enter 3 for add new book")
                print("Enter 4 for logout")
                check = int(input("Enter number as per query : "))
                
                if check == 1 :
                    print(f"\n---- Books List ----\n") 
                    library.book_list()
                    print("")

                
                elif check == 2 :
                    print(f"\n---- Update book quantity ----\n") 
                    library.update_book_quantity()
                    print("")
            
                elif check == 3 :
                    print(f"\n---- Add new book ----\n") 
                    library.update_books()
                    print("")
                
                elif check == 4 :
                    break

                else :
                    print("Wrong Input\n")

        else :
            print("Please Enter correct id and password, try again")
            check = input("Enter 'y' to retry and 'n' for exit : ").lower()
            if check == "y" :
                pass
            elif check == "n" :
                break
            else :
                print("wrong input")
                break



    elif check == 4 :
        logout = True
        break


    else :
        print("\nPlease enter correct value as per your query.")
        
        tryagain = input("Enter 'y' to retry and 'n' for exit : ").lower()
        if tryagain == "y" :
            pass
        elif tryagain == "n" :
            print("thanks for using")
            logout = True
            break
        else :
            logout = True
            break

    if logout == True :
        break
