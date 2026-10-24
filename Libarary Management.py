from os import system
from time import sleep

def load_data():
    global book_id
    try:
        with open('books.txt') as f:
            content=f.read()
            if not content:
                return
            records=content.splitlines()
            for record in records:
                data=record.split(",")
                book_list.append({
                    'id':int(data[0]),
                    'name':data[1],
                    'auth':data[2],
                    'quantity':int(data[3])
                })
                book_id=int(data[0])
            book_id+=1
            return 
    except FileNotFoundError:
        with open('books.txt','w') as f:
            return

def update_data():
    with open('books.txt','w') as f:
        for book in book_list:
            f.write(f"{book['id']},{book['name']},{book['auth']},{book['quantity']}\n")
        print("Updating Database...")
        sleep(3)
        return

def add_book():
    system('cls')
    global book_id
    print("---------ADD BOOK------------")
    print()
    try:
        b_id=book_id
        print(f"Book Id : {b_id}")
        book_name=input("Enter Book Name :")
        auth_name=input("Enter Author's Name :")
        quantity=abs(int(input("Enter Quantity :")))

        if not book_name or not auth_name:
            print("Invalid Name for Book or Auhtor")
            return True

        book_list.append({
            'id':b_id,
            'name':book_name,
            'auth':auth_name,
            'quantity':quantity
        })
        book_id+=1
        print("Successfully Added")
        sleep(1)
        return True
    
    except ValueError:
        print("Invlid Quantity")
        sleep(1)
        return True

def delete_book():
    system('cls')
    print("------Delete Book-------")
    print()
    try:
        b_id=int(input("Enter Book Id : "))
        for book in book_list:
            if b_id==book['id']:
                print()
                print("Deleted Book")
                print(f"Name :{book['name']}")
                print(f"Author : {book['auth']}")
                print(f"Quantity : {book['quantity']}")

                book_list.remove(book)
                print("Succesfully Deleted")
                sleep(1)
                return True
        print("Book Not Found")
        sleep(1)
        return True
    
    except ValueError:
        print("Invalid Book Id")
        sleep(1)
        return True

def search_book():
    system('cls')
    print("Search Book")
    print()
    try:
        b_id=int(input("Enter Book Id :"))
        for book in book_list:
            if b_id==book['id']:
                print()
                print(f"Name :{book['name']}")
                print(f"Author : {book['auth']}")
                print(f"Quantity : {book['quantity']}")
                input("Press any key...")
                return True
        print("Book Not Found")
        sleep(1)
        return True
    except ValueError:
        print("invlaid Book Id")
        sleep(1)
        return True

def update_quantity():
    system('cls')
    print("Update Quantity")
    print()
    try:
        b_id=int(input("Enter Book Id :"))
        quantity=abs(int(input("Enter new Quantity : ")))

        for book in book_list :
            if b_id==book['id']:
                book['quantity']=quantity
                print("Successfully Updated")
                input("press any key..")
                return True
        print("Book Not Found")
        sleep(1)
        return True
    
    except ValueError:
        print("Invalid Book Id")
        sleep(1)
        return True

def display():
    system('cls')
    if not book_list:
        print("Not Found")
        input("Press any key...")
        return True
    print(f"{'Id':<10}{'Name':<30}{'Author':<30}{'Quantity'}")
    for book in book_list:
        print(f"{book['id']:<10}{book['name']:<30}{book['auth']:<30}{book['quantity']}")
    input('Press any key...')
    return True

def issue_book():
    system('cls')
    print("Issue Your Book")
    print()
    try:
        b_id=int(input("Enter Book id : "))
        for book in book_list:
            if b_id==book['id']:
                if book['quantity']==0:
                    print("Book is Out of Stock")
                    sleep(1)
                    return True
                else:
                    book['quantity']-=1
                    print(f"Book has been Isuued.Quantity Remaining : {book['quantity']}")
                    sleep(1)
                    return True

        print("Book Not Found")
        sleep(1)
        return True
    except ValueError:
        print("Invlid Book Id")
        sleep(1)
        return True

def return_book():
    system('cls')
    print("Return Your Book")
    print()
    try:
        b_id=int(input("Enter Book id : "))
        for book in book_list:
            if b_id==book['id']:
                book['quantity']+=1
                print("Book has been Submitted")
                sleep(1)
                return True
        print("Book Bot Found");
        sleep(1)
        return True
    except ValueError:
        print("Invlalid Book id")
        sleep(1)
        return True

def _exit_():
    return False

def menu():
    system('cls')
    print("="*10+"Library Mangement System"+"="*10)
    print()
    print("1.Add Book")
    print("2.Delete Book")
    print("3.Search Book")
    print("4.Update Quantity")
    print("5.Display Books")
    print("6.Issue Book")
    print("7.Return Book")
    print("8.Exit")
    print()
    choice={
        1:add_book,
        2:delete_book,
        3:search_book,
        4:update_quantity,
        5:display,
        6:issue_book,
        7:return_book,
        8:_exit_
    }
    try:
        ch=int(input("Enter Your Choice : "))
        if ch not in range(1,9):
            return "Invalid"
        else:
            func = choice[ch]
            return func()
       
    except ValueError:
        return "invalid"

def main():
    while True:
        state=menu()
        if not state:
            break
        elif state=="invalid":
            print("Invalid Option")
            sleep(1)
            continue
       
book_id=1
book_list=[]
load_data()
main()
update_data()
