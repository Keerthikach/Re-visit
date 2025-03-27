from database import add_questions,fetch_for_rev,init_db,del_entry

def main():
    init_db()
    while True:
        print("Revision Tracker menu")
        print("1- Add questions")
        print("2- view questions due for revision")
        print("3- To delete a specific entry")
        print("4- To exit")

        choice=input("Enter a choice (1-4)")

        if choice=='1':
            question=input("Enter the question")
            description=input("Enter the description of the question (optional)")

            add_questions(question,description)

            print("Successfully added")

        elif choice=="2":
            my_ques=fetch_for_rev()

            if my_ques:
                print("The questions are")    
                for i,q,d in my_ques:
                    print(f"{i}- {q}")
                    print(f"- {d}")
            else:
                print("No questions") 

        elif choice=='3':
            print("Enter the id of the question that you want to delete")
            id=int(input())
            del_entry(id)
            print("Entry is successfully deleted")

        elif choice=='4':
            print("Exiting....")        
            break 

        else:
            print("Invalid input")

if __name__=="__main__":
    main()            


