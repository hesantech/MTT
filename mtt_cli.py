import csv
import time
import os

'''
Date 2023-09-20	
Time 0.5	
Project	<Different projects>
Task  <KT, Mentoring, On-call, US, Meeting, Writing, Automation>
Division <NonBAU, BAU, Mentorship, Break/Fix, Learning, Training, Documentation>
Details <Details about the task>
'''

class Item():
    def __init__(self):
        self.date = ""
        self.time = ""
        self.project = ""
        self.task = ""
        self.division = ""
        self.details = ""
        self.start = "00:00"
        self.end = "00:00"

    def prompt_date(self, prompt):
        t = input(prompt)
        if t == '' :
            now = time.localtime()
            t = str(now.tm_year)+"-"+str(now.tm_mon)+"-"+str(now.tm_mday)
        elif len(t) != 10 or t.count('-') != 2:
            print(t)
            print("Please enter date in format e.g. 2023-12-30")
            self.prompt_end(prompt)
            return False
        try: # check for valid date
            time.strptime(t, "%Y-%m-%d")
        except ValueError:
            print("Unrecognized time. Please enter date in format e.g. 2023-12-30")
            self.prompt_end(prompt)
            return False
        self.date = t

    def prompt_project(self, prompt):
        t = input(prompt)
        if t == '':
            print("Please enter a Project:")
            self.prompt_project(prompt)
        self.project = t

    def prompt_task(self, prompt):
        t = input(prompt)
        if t == '':
            print("Please enter task:")
            self.prompt_task(prompt)
        self.task = t

    def prompt_division(self, prompt):
        t = input(prompt)
        if t == '':
            print("Please enter division:")
            self.prompt_division(prompt)
        self.division = t

    def prompt_details(self, prompt):
        t = input(prompt)
        if t == '':
            print("Please enter details:")
            self.prompt_details(prompt)
        self.details = t


    def prompt_time(self):
        # t = input(prompt)
        # if t == '':
        #     i = input("Enter number of hours: ")
        #     try:
        #         t = float(i) # Convert the input to a float
        #         if i.count('.') == 1 and i[-1] != '.': # Check if the input has exactly one decimal place
        #             print("Unrecognized no of hrs. Please enter correctly")
        #             self.prompt_time(prompt)
        #             return False
        #     except ValueError:
        #         print("Invalid input. Please enter a valid number of hrs.")
        # self.time = t
        # convert string to time.struct_time
        t1 = time.strptime(self.start, "%H:%M")
        t2 = time.strptime(self.end, "%H:%M")
        dif = time.mktime(t2)-time.mktime(t1)
        if dif < 0:
            dif+=60*60*24
        min = str(round(dif/60/60,1))
        self.time = min
    
    def prompt_start(self, prompt):
        t = input(prompt)
        if t == '':
            now = time.localtime()
            t = tostr(now.tm_hour)+":"+tostr(now.tm_min)
        elif len(t) != 5: # check for format
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_start(prompt)
            return False # To end the current branch, otherwise becomes a tail-call
        try: # check for valid time
            time.strptime(t, "%H:%M")
        except ValueError:
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_start(prompt)
            return False # To end the current branch, otherwise becomes a tail-call

        self.start = t

    def prompt_end(self, prompt):
        t = input(prompt)
        if t == '':
            i = input("Type in 'end' to stop timer... ")
            while i == '' or i: # essentialy while True
                if i == "end":
                    now = time.localtime()
                    t = tostr(now.tm_hour)+":"+tostr(now.tm_min)
                    break
                else:
                    i = input("Type in 'end' to stop timer... ")
        elif len(t) != 5:
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_end(prompt)
            return False
        try: # check for valid time
            time.strptime(t, "%H:%M")
        except ValueError:
            print("Unrecognized time. Please enter time in 24h format e.g. 00:00")
            self.prompt_end(prompt)
            return False

        self.end = t

    def display(self):
        print(" Date: " + self.date + " Project: " + self.project + " Hours: " + self.time + " Task: "+ self.task + " Division: " + self.division + " Details: " + self.details + " was started at " + self.start + " and ended at " + self.end)


def export_to_csv(*items):
    now = time.localtime()
    filename = "time_tracker_"+str(now.tm_year)+'.csv'
    present = os.path.exists(filename)
    with open(filename, 'a', newline='') as f:
        fieldnames = ['Date', 'Time' , 'Project', 'Task', 'Division', 'Details', 'Start_time', 'End_time']
        iw = csv.DictWriter(f, fieldnames=fieldnames, dialect='excel')
        if not present:
            iw.writeheader()
        for i in items:
            iw.writerow({'Date': i.date,
                         'Time': i.time,
                         'Project': i.project,
                         'Task': i.task,
                         'Division': i.division,
                         'Details': i.details,
                         'Start_time': i.start,
                         'End_time': i.end})

def view_history():
    try:
        now = time.localtime()
        file_path = "time_tracker_"+str(now.tm_year)+'.csv'
        with open(file_path, 'r') as file:
            # Read all lines from the file
            lines = file.readlines()
            # Extract the last five lines
            last_five_lines = lines[-5:]
            # Display the last five lines
            for line in last_five_lines:
                print(line.strip())  # Remove leading/trailing whitespace
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def delete_last_record():
    try:
        now = time.localtime()
        file_path = "time_tracker_"+str(now.tm_year)+'.csv'
        # Read all lines from the CSV file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Check if there is at least one line after title
        if len(lines) > 1:
            # Display the last line for confirmation
            print("Last record to be deleted:")
            print(lines[-1].strip())  # Remove leading/trailing whitespace

            # Ask for confirmation
            confirmation = input("Are you sure you want to delete the last record? (yes/no): ").lower()

            if confirmation == 'yes':
                # Remove the last line
                lines.pop()
                # Write the updated content back to the file
                with open(file_path, 'w', newline='') as file:
                    file.writelines(lines)

                print("Last record deleted successfully.")
            else:
                print("Deletion canceled. The file remains unchanged.")
        else:
            print("File is empty. Nothing to delete.")

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

def handle_option(option):
    if option.lower() == 'v':
        view_history()     
    elif option.lower() == 'u':
        i = Item()
        i.prompt_date("Enter the date: (blank for today) ")
        i.prompt_project("Name of the Project: ")
        i.prompt_task("Name of the Task: ")
        i.prompt_division("Name of the Division: ")
        i.prompt_details("Name of the Details: ")
        i.prompt_start("Enter start time: (blank for current) ")
        i.prompt_end("Enter end time: (blank for timer) ")
        i.prompt_time()
        i.display()
        export_to_csv(i)
    
        while input("Do you want to enter another item?(yY): ").lower() == 'y':
            i.prompt_date("Enter the date: (blank for today) ")
            i.prompt_project("Name of the Project: ")
            i.prompt_task("Name of the Task: ")
            i.prompt_division("Name of the Division: ")
            i.prompt_details("Name of the Details: ")
            i.prompt_start("Enter start time: (blank for current) ")
            i.prompt_end("Enter end time: (blank for timer) ")
            i.prompt_time()
            i.display()
            export_to_csv(i)
    elif option.lower() == 'd':
        delete_last_record()
    else:
        print("Invalid option. Please enter valid option")

if __name__ == "__main__":
    user_option = input(" 'v' to view, 'u' to udpate, 'd' to delete, or 'q' to quit: ")
    if user_option.lower() == 'q' or user_option == "":
        print("Exiting the program. Goodbye!")
    else:
       handle_option(user_option)

