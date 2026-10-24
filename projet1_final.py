import os
from time import sleep

def load_records():
     global roll
     try:
          with open('record.txt') as f:
             
               records = f.read().splitlines()

               if records:
                    roll = max(int(record.split(',')[0]) for record in records) + 1

               for record in records:
                    data=record.split(',')
                    std_rec.append({
                         'roll' : int(data[0]),
                         'name' : data[1],
                         'marks': int(data[2])
                    })
               
     except FileNotFoundError:
          with open('record.txt','w'):
               return

def update_records():
     with open("record.txt",'w') as f:
          for records in std_rec:
               f.write(f"{records['roll']},{records['name']},{records['marks']}\n")
          print('Saving Records...')
          sleep(3)

def add_stu():
     os.system('cls')
     global roll
     print("="*10+"Add Student"+"="*10)
     print()
     print(f"Student Roll No :{roll}")
     try:
          name = input("Enter Your Name :")
          marks = int(input("Enter Your Marks (1-100): "))
          if marks not in range(1,101):
               print("Invalid Marks")
               sleep(1)
               return 
          else:
               std_rec.append({
                    "roll":roll,
                    "name":name,
                    "marks":marks
               })
                
               roll+=1
               print("Student Added Successfully")
               sleep(1)
               return
     except ValueError:
          print("Marks Should Be Digits")
          sleep(1)

def update_stu():
    os.system("cls")
   
    print("=" * 10 + " Update Student " + "=" * 10)
    print()
    try:
        roll_s = int(input("Enter Roll No To Update: "))
        mark = int(input("Enter Updated Marks: "))
        if mark not in range(1,101):
            print("Invalid Marks")
            sleep(1)
            return
        for student in std_rec:
            if  student["roll"] == roll_s:
                student["marks"] = mark
                print("Marks Updated Successfully")
                sleep(1)
                return

        print("Student Not Found")
        sleep(1)
        return

    except ValueError:
        print("Invalid Input")
        sleep(1)

def del_stu():
    os.system('cls')
    
    print("="*10+"Delete Student"+"="*10)
    print()
    try:
        roll_s=int(input("Enter Student Rollno: "))
        for std in std_rec:
            if std['roll']==roll_s:
                 std_rec.remove(std)
                 print("Deleted Succesfully")
                 sleep(1)
                 return
        print("Student Not Found")
        sleep(1)
        return
    
    except ValueError:
         print("Invalid Format")
         sleep(1)

def search():
     os.system('cls')
     
     print("="*10+"Search Student"+"="*10)
     print()
     try:
          roll_s=int(input("Enter Rollno To Search :"))
          for std in std_rec:
               if std['roll']==roll_s:
                    print(f"Rollno : {std['roll']}")
                    print(f"Name : {std['name']}")
                    print(f"Marks : {std['marks']}")
                    input("Press any key...")
                    return
          print("Student Not Found")
          sleep(1)
          return    
         
     except ValueError:
          print("Invalid Format")
          sleep(1)

def display():
     os.system('cls')
    
     if std_rec==[]:
          print("No Record Found")
          input("Press any key...")
          return
     else:
          print(f" {'Rollno':<10}{'Name':<15}{'Marks'}")
          for std in std_rec:
               print(f"  {std['roll']:<10}{std['name']:<15}{std['marks']}")
          input('Press any key...')
          return

def show_topper():

    os.system('cls')
    
    
    if not std_rec:
        print("No Record Found")
        input('Press any key...')
        return

    roll=[]
    name=[]
    marks=[]
    
    max_m=0

    for std in std_rec:
        if max_m<std['marks']:
            max_m=std['marks']

    for std in std_rec:
        if std['marks']==max_m:
            roll.append(std['roll'])
            name.append(std['name'])
            marks.append(std['marks'])    

    print("-------Topper-------")
    print()         
    print(f"{'Rollno':<10}{'Name':<15}{'Marks'}")

    for i in range(len(roll)):
        print(f"{roll[i]:<10}{name[i]:<15}{marks[i]}") 

    input('Press any key...')
    return

def avg_mark():
     os.system('cls')
     
     if not std_rec:
          print("No Record Found")
          sleep(1)
          return
     
     print(f"Total Students :{len(std_rec)}")
     count=0
     for std in std_rec:
          count+=std['marks']
     avg = count/len(std_rec)
     print(f"Average Marks :{avg}")
     input("Press any key...")
     return

def choice(ch):
     if ch == 1:
          add_stu()
          return True
     elif ch == 2:
          update_stu()
          return True
     elif ch == 3:
          del_stu()
          return True
     elif ch == 4:
          search()
          return True
     elif ch == 5:
          display()
          return True
     elif ch == 6:
          show_topper()
          return True
     elif ch == 7:
          avg_mark()
          return True
     elif ch == 8:
          os.system('cls')
          update_records()
          return False
          
def menu():
    os.system('cls')
    print("="*10+"Student Management System"+"="*10)
    print("1.Add Student")
    print("2.Update Student")
    print("3.Delete Student")
    print("4.Search Student")
    print("5.Display Records")
    print("6.Show Topper")
    print("7.Show Average Marks")
    print("8.Exit")
    print()
    try :
        ch=int(input("Enter Your Choice : "))
        if ch not in range(1,9):
                return "Invalid"
        else:
                return choice(ch)
    except ValueError:
        return "Invalid"

def main():
    load_records()
    while True:
        state = menu()
        if state == "Invalid":
            print("Invalid Choice")
            sleep(1)
            continue
        elif not state:
            break

roll = 1
std_rec=[]
main()