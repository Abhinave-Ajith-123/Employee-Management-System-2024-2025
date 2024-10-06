import mysql.connector
import tkinter as tk
from hashlib import sha3_256 as hash
import datetime
from tkinter import messagebox, ttk
import random
from PIL import Image, ImageTk
import poplib

dark = True # flag for dark theme

def update_time(window, time, date):

    current_date = datetime.datetime.now().strftime('Date : %d - %m - %Y')
    current_time = datetime.datetime.now().strftime('Time : %H : %M : %S')

    time.config(text = current_time)
    date.config(text = current_date)

    if window.winfo_exists():
        update = window.after(1000, lambda : update_time(window, time, date))  

    else:
        pass  

def timeframe(window):

    datetime_frame = tk.Frame(window)
    datetime_frame.pack(padx = 5, pady = 1, fill = 'both')

    time = tk.Label(datetime_frame, font = ('Arial', 10, 'bold'))
    date = tk.Label(datetime_frame, font = ('Arial', 10, 'bold'))

    time.pack(padx = 5, pady = 3, side = 'right')
    date.pack(padx = 5, pady = 3, side = 'left')

    update_time(datetime_frame, time, date)

    dark_theme(datetime_frame)

# establish connection with mysql database
connection = mysql.connector.connect(
    host = 'sql.freedb.tech',
    user = 'freedb_pranav',
    password = 'x$CSpqPg8sN8*7n',
    database = 'freedb_empsys'
)

cursor = connection.cursor() # establish cursor

def on_enter(event): # hover effect 

    # dark theme

    if dark:
        event.widget.config(bg = '#003', fg = 'white')
    
    # light theme

    if not dark:
        event.widget.config(bg = 'light grey', fg = 'black')

def on_leave(event): # hover effect

    # dark theme
    
    if dark:
        event.widget.config(bg = '#112', fg = 'white')

    # light theme
        
    if not dark:
        event.widget.config(bg = 'SystemButtonFace', fg = 'black')

def on_click(event): # hover effect
    
    # dark theme

    if dark:
        event.widget.config(bg = 'grey', fg = 'white')

    # light theme
        
    if not dark:
        event.widget.config(bg = 'white', fg = 'black')

def hover(window):

    for widget in window.winfo_children():

        if isinstance(widget, tk.Button):

            widget.bind('<Enter>', on_enter)
            widget.bind('<Leave>', on_leave)
            widget.bind('<Button-1>', on_click)

def switch_theme(window, subwindows):
        
    global dark
    dark = False if dark else True
    dark_theme(window)
    for subwindow in subwindows:
        dark_theme(subwindow)

def dark_theme(window):

    global dark

    bg = '#112' if dark else 'SystemButtonFace'
    fg = 'white' if dark else 'black'

    style = ttk.Style()

    window.configure(bg=f'{bg}')

    if not style.theme_names().__contains__('dark_custom'):
        style.theme_create('dark_custom', parent='alt', settings={
            'TCombobox': {'configure': {'selectbackground': f'{bg}', 'fieldbackground': f'{bg}', 'foreground': f'{fg}'}},
            'TComboboxPopup': {'configure': {'background': f'{bg}', 'foreground': f'{fg}'}},
        })
    style.theme_use('dark_custom')

    for widget in window.winfo_children():
        if isinstance(widget, ttk.Combobox):
            widget.configure(background=f'{bg}', foreground=f'{fg}')
        elif not isinstance(widget, tk.Frame):
            widget.configure(bg=f'{bg}', fg=f'{fg}')

def title_page(exit = False,from_window = None, to_function = None, titles = 'Employee Management System'.split(' ')):
      
    if from_window is not None: # destroy the window
        from_window.destroy()

    if to_function is None: # defining default to_function
        to_function = homepage
    
    # creating the tkinter screen
    window = tk.Tk() 
    window.title('Title')

    # row and column for gridding
    title_row, title_column = 0, 0

    # creating frame
    title_frame = tk.LabelFrame(window, bd = 15, relief = 'groove')
    title_frame.pack(padx = 10, pady = 10, fill = 'both')

    #interating through words
    for title in titles:
          
        # adding label widget
        label = tk.Label(title_frame, text = title, font = ('Trebuchet MS', 24, 'bold', 'italic'))
        label.grid(row = title_row, column = title_column, padx = 5, pady = 5)

        # condition for adjusting column spacing
        if len(titles)%2 != 0 and titles[-1] == title:
            label.grid_configure(columnspan = 2)
        
        # increasing row and column variable
        title_column = title_column + 1 if title_column + 1 < 2 else 0
        title_row = title_row + 1 if title_column == 0 else title_row

    # adjusting to screen resizing
    title_frame.grid_columnconfigure('all', weight = 1)

    # function for timeout
    def timeout(event = None):

        # to cancel the after function is not used before destroying
        if event is not None:
            window.after_cancel(timeout_call)

        window.destroy() # to destroy the window
        if not exit:
            to_function() # to the next function
        
        if exit:
            #ccommiting and closing the connections
            connection.commit()
            cursor.close()
            connection.close()

    title_frame.bind('<Button-1>', timeout) # destroy on click
    timeout_call = window.after(5000, timeout) # destroy after 5s (5000ms = 5s)

    window.mainloop() # looping the main screen

def homepage(): # home screen to the app

    # creating the window
    window = tk.Tk()
    window.title('Employee Management System')

    datetime_frame = tk.Frame(window)
    datetime_frame.pack(padx = 5, pady = 1, fill = 'both')

    time = tk.Label(datetime_frame, font = ('Arial', 10, 'bold'))
    date = tk.Label(datetime_frame, font = ('Arial', 10, 'bold'))

    time.pack(padx = 5, pady = 3, side = 'right')
    date.pack(padx = 5, pady = 3, side = 'left')

    update_time(datetime_frame, time, date)

    #creating the frame
    frame = tk.LabelFrame(window, text = 'Options', bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    # labels on the buttons
    button_Label = ['Administrator Interface', 
                    'Employee Interface', 
                    'Employee Registration', 
                    'Mark Attendance', 
                    'Exit']
    
    #functions fot the button
    button_function = [lambda: entry_ticket_x_attendance(window, lower = False),
                       lambda: entry_ticket_x_attendance(window), 
                       lambda : new_x_edit_reg(window), 
                       lambda: entry_ticket_x_attendance(window, attendance = True), 
                       lambda : title_page(exit = True, from_window = window, titles = 'Thank You....'.split(' '))]

    # row and column for gridding
    row, column = 0, 0

    #iterating label and function with relation
    for label, function in zip(button_Label, button_function):

        # defining button widget and gridding
        button = tk.Button(frame, text = label, command = function, padx = 20, pady = 20)
        button.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'news')

        # adjusting the column
        if label == 'Exit':
            button.grid_configure(columnspan = 2)

        #increasing the row-column variables
        column = column + 1 if column + 1 < 2 else 0
        row = row + 1 if column == 0 else row

    #theme change button and gridding
    theme_change = tk.Button(window, text = 'Change Theme\nLight / Dark', command = lambda : switch_theme(window, (frame, datetime_frame)), padx = 10, pady = 10)
    theme_change.pack(padx = 5, pady = 5, fill = 'both')

    #adding hover effects
    hover(window)
    hover(frame)

    dark_theme(window)
    dark_theme(frame)
    dark_theme(datetime_frame)
        
    #adjusting according th resizing of the screen
    frame.grid_columnconfigure('all', weight = 1)

    window.mainloop()  #looping the screen

# combined function to mark attendance and to get data for interface access
def entry_ticket_x_attendance(from_window, lower = True, attendance = False): 

    from_window.destroy()

    def back_func(): # back function
        
        # destroy the window and goes to homepage
        window.destroy()
        homepage()

    def enter_func(): # enter function

        #retrieving the data from entry widgets
        emp_code = employee_code.get()
        first_name = f_name.get().title()
        last_name = l_name.get().title()
        passcode = password.get()

        #checking for fake data
        if emp_code == '' or first_name == '' or last_name == '' or passcode == '' or not emp_code.isdigit():
            tk.messagebox.showerror(title = 'Error', message = 'Invalid Entry')
            return
        
        emp_code = int(emp_code) # converting to integer

        if not attendance: # data verification and interface access

            table = 'Employee' if lower else 'Administrator'
            passcode = passcode if lower else hash(passcode.encode()).hexdigest()
            
            cursor.execute(f"""SELECT {table}_Code  FROM {table}
                            WHERE {table}_Code = {int(emp_code)}
                            AND First_Name = '{first_name}'
                            AND Last_Name = '{last_name}'""")
            data = cursor.fetchone()

            cursor.execute(f"""SELECT Interface FROM Login_Details
                           WHERE Login_Password = '{passcode}'""")
            Interface = cursor.fetchone()

            if Interface is None and data is None:
                tk.messagebox.showerror(title = 'Error', message = 'Incorrect Data and Password')
                return
            
            elif data is None:
                #error message if data not found
                tk.messagebox.showerror(title = 'Error', message = 'Incorrect Data')
                return

            elif Interface is None:
                tk.messagebox.showerror(title = 'Error', message = 'Incorrect Password')
                return
            
            Interface = Administrator if Interface[0] == 'Administrator' else Employee
            
            #running interface
            window.destroy()
            tk.messagebox.showinfo(title = 'Login Successful', message = 'Login Successful')

            Interface(emp_code)
        
        elif attendance and lower: # to mark attendance
            
            cursor.execute('SHOW COLUMNS FROM Attendance_Sheet')
            columns = [column[0] for column in cursor.fetchall()]

            last_date = datetime.datetime.strptime(columns[-1], '%Y-%m-%d').date() if len(columns) > 2 else datetime.date.today() - datetime.timedelta(days = 1)

            dates = []
            
            while last_date != datetime.date.today():
                last_date += datetime.timedelta(days = 1)
                dates.append(last_date)
            
            any(cursor.execute(f"""ALTER TABLE Attendance_Sheet 
                               ADD COLUMN `{date}` CHAR(1) DEFAULT 'A'""") for date in dates)
            
            cursor.execute(f"""SELECT `{last_date}` FROM Attendance_Sheet
                            WHERE Employee_Code = {int(emp_code)}
                            AND Attendance_Passcode = '{passcode}'""")
            
            status = cursor.fetchone()

            if status is None:
                tk.messagebox.showerror(title = 'Error', message = 'Incorrect Data')
                return

            if status[0] == 'P':

                window.destroy()
                tk.messagebox.showinfo(title = 'Attendance Marked Already', message = 'Attendance has been already marked for the day')
                return

            cursor.execute(f"""UPDATE Attendance_Sheet
                        SET `{last_date}` = 'P'
                        WHERE Employee_Code = {emp_code}
                        AND Attendance_Passcode = '{passcode}'""")
            
            connection.commit()
        
            window.destroy()
            tk.messagebox.showinfo(title = 'Attendance Marked', message = 'Attendance has been marked for the day')
            homepage()

    #creating the window
    window = tk.Tk()
    window.title('Data Verification')
    window.minsize(width = 400, height = 0)

    timeframe(window)

    #creating the frame
    frame = tk.LabelFrame(window, relief = 'groove', bd = 5)
    frame.pack(padx = 5, pady = 5, fill = 'both')

    # widget Labels
    Labels = ['Employee Code' if lower else 'Administrator Code', 
              'First Name', 
              'Last Name', 
              'Login Password' if not attendance else 'Attendance Passcode']
    
    for label, row in zip(Labels, range(4)):
        
        #gridding the widget label
        text = tk.Label(frame, text = label + ' : ')
        text.grid(row = row, column = 0, padx = 5, pady = 5)

    #creating widgets
    employee_code = tk.Entry(frame, width = 20)
    f_name = tk.Entry(frame, width = 20)
    l_name = tk.Entry(frame, width = 20)
    password = tk.Entry(frame, width = 20)

    widgets = [employee_code, f_name, l_name, password]
    #gridding the widgets
    for widget, row in zip(widgets, range(4)):
        widget.grid(row = row, column = 1, padx = 5, pady = 5)
    
    #creating buttons( back, enter ) and packing
    button_back = tk.Button(window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_back.pack(padx = 5, pady = 5, side = tk.LEFT, fill = 'x', expand = True)

    button_enter = tk.Button(window, text = 'Enter', command = enter_func, padx = 10, pady = 10)
    button_enter.pack(padx = 5, pady = 5, side = tk.RIGHT, fill = 'x', expand = True)

    #adding hover effect
    hover(window)

    # adjusting to resizing of window
    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(window)
    dark_theme(frame)

    window.mainloop()# looping the window

def Administrator(emp_code): # administrator interface
    
    #creating the window
    window = tk.Tk()
    window.title('Employee Interface')

    timeframe(window)

    #creeating a frame
    frame = tk.LabelFrame(window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    #button labels and functions
    Labels = ['retrieve your data', 
              'edit your data', 
              'add new administrator data', 
              'retrieve all administrator data', 
              'retrieve all employee data', 
              'retrieve all employee data\n[ emergency contacts ]', 
              'retrieve all attendance data', 
              'retrieve an employee data',
              'retrieve an employee data\n[ attendance data ]', 
              'manage position and salary\nof new registration', 
              'manage transfer details of an employee',
              'promote an employee',
              'demote an employee', 
              'provide incrementation to an employee', 
              'provide decrementation to an employee',
              'add client data',
              'retrieve all client data', 
              'retrieve all data of clients\nunder an employee', 
              'retrieve a client data',
              'delete a client data',
              'Conduct a poll', 
              'read appeals', 
              'read messages', 
              'draft a message to all employees', 
              'draft a message to an employee', 
              'draft a message to a department', 
              'draft a message to an administrator', 
              'Delete an employee data', 
              'delete all employee data', 
              'delete all client data', 
              'delete all attendance data', 
              'exit']
    functions = []

    # row-column variables for griding
    row, column = 0, 0

    for label in Labels:
        
        #creating button widget and gridding them
        button = tk.Button(frame, text = label.title(), padx = 20, pady = 20)
        button.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'news')

        #adjusting the columns
        '''if label == 'exit':
            button.grid_configure(columnspan = 4)'''

        #incrementing the row-column variables
        column = column + 1 if column + 1 < 4 else 0
        row = row + 1 if column == 0 else row

    #adding hover effects
    hover(frame)
    
    frame.grid_columnconfigure('all', weight = 1)

    window.mainloop() # looping the main screen

def Employee(emp_code): # employee interface
    
    #creating window
    window = tk.Tk()
    window.title('Employee Interface')

    timeframe(window)

    #creating frame
    frame = tk.LabelFrame(window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    #button labels
    Labels = ['retrieve your data', 
              'edit your data', 
              'retrieve your attendance data', 
              "retrieve all employee data",
              "retrieve all administrator data", 
              'add client data', 
              'retrieve cliet data', 
              'retrieve all client data', 
              'delete client data', 
              'change ownership of a client', 
              'change ownership of all clients', 
              'compose an email',
              'read messages', 
              'draft appeals', 
              'vote for exisiting pole',
              'exit']
    
    #buttone functions
    functions = []

    #row-column variables for gridding
    row, column = 0, 0

    for label in Labels:

        #creating button widgets and gridding them
        button = tk.Button(frame, text = label.title(), padx = 20, pady = 20)
        button.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'news')

        #adding hover effects
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        button.bind('<Button-1>', on_click)

        if label == 'exit':
            button.grid_configure(columnspan = 3)
            column += 2

        #incrementing the row and column values
        column = column + 1 if column + 1 < 3 else 0
        row = row + 1 if column == 0 else row
    
    #adapting to resizing
    frame.grid_columnconfigure('all', weight = 1)

    window.mainloop() #looping the window

# combined function to add new registeration or edit ones registration for both employee and admisistrator
def new_x_edit_reg(from_window, from_function = None, from_code = None, emp_code = None, lower = True, edit = False):
    
    #from_window.destroy()

    def back(): # back function
        
        window.destroy()
        
        if from_function is None:
            homepage()
            return
        
        from_function(from_code)

    def clear(datas = None): # function to clear the form

        # clear the entry widget ; add default value / existing value
        
        f_name.delete(0, tk.END) ; f_name.insert(0, 'First Name' if not edit else datas[0])
        l_name.delete(0, tk.END) ; l_name.insert(0, 'Last Name' if not edit else datas[1])
        gender.delete(0, tk.END) ; gender.insert(0, 'Gender' if not edit else datas[2])

        age.delete(0, tk.END) ; age.insert(0, 'Age' if not edit else datas[3])
        nationality.delete(0, tk.END) ; nationality.insert(0, 'Nationality' if not edit else datas[4])
        phone_no.delete(0, tk.END) ; phone_no.insert(0, '+971 ' if not edit else datas[5])

        email.delete(0, tk.END) ; email.insert(0, 'Email' if not edit else datas[6])

        dob_date.delete(0, tk.END) ; dob_date.insert(0, 'Date' if not edit else datas[7][2])
        dob_month.delete(0, tk.END) ; dob_month.insert(0, 'Month' if not edit else datas[7][1])
        dob_year.delete(0, tk.END) ; dob_year.insert(0, 'Year' if not edit else datas[7][0])

        doh_date.delete(0, tk.END) ; doh_date.insert(0, 'Date' if not edit else datas[8][2])
        doh_month.delete(0, tk.END) ; doh_month.insert(0, 'Month' if not edit else datas[8][1])
        doh_year.delete(0, tk.END) ; doh_year.insert(0, 'Year' if not edit else datas[8][0])

        name_1.delete(0, tk.END) ; name_1.insert(0, 'Name' if not edit else datas[9])
        phone_no_1.delete(0, tk.END) ; phone_no_1.insert(0, '+971 ' if not edit else datas[10])

        name_2.delete(0, tk.END) ; name_2.insert(0, 'Name' if not edit else datas[11])
        phone_no_2.delete(0, tk.END) ; phone_no_2.insert(0, '+' if not edit else f'{datas[12]} {datas[13]}')

        if lower:

            emp_type.delete(0, tk.END) ; emp_type.insert(0, 'Employement Type' if not edit else datas[14])
            branch.delete(0, tk.END) ; branch.insert(0, 'Branch' if not edit else datas[15])
            dept.delete(0, tk.END) ; dept.insert(0, 'Department' if not edit else datas[16])
        
        if not lower: # fields specific to admininstrator

            position.delete(0, tk.END) ; position.insert(0, 'Position' if not edit else datas[14])
            salary.delete(0, tk.END) ; salary.insert(0, 'Salary' if not edit else datas[15])

    def add(): # update or add new registration function
        
        first_name = f_name.get().title() if (f_name.get()).isalpha() else None
        last_name = l_name.get().title() if (l_name.get()).isalpha() else None
        _gender = gender.get().title() if (gender.get()).isalpha() else None


        _age = int(age.get()) if (age.get()).isdigit() else None
        _nationality = nationality.get().title() if (nationality.get()).isalpha() else None
        _phone_no = int(phone_no.get()[5:]) if ((phone_no.get())[5:]).isdigit() else None

        _email = email.get() if '@' in email.get() and '.com' in email.get() else None

        date_dob = int(dob_date.get()) if (dob_date.get()).isdigit() else None
        month_dob = int(dob_month.get()) if (dob_month.get()).isdigit() else None
        year_dob = int(dob_year.get()) if (dob_year.get()).isdigit() else None

        date_doh = int(doh_date.get()) if (doh_date.get()).isdigit() else None
        month_doh = int(doh_month.get()) if (doh_month.get()).isdigit() else None
        year_doh = int(doh_year.get()) if (doh_year.get()).isdigit() else None

        _name_1 = name_1.get() if (name_1.get()).isalpha() else None
        _contact_1 = (phone_no_1.get()[5:]) if ((phone_no_2.get())[5:]).isdigit() else None

        _name_2 = name_2.get() if (name_2.get()).isalpha() else None
        country_code = ((phone_no_2.get()).split())[0] if ((((phone_no_2.get()).split())[0])[1:]).isdigit() else None
        contact_2 = int(((phone_no_2.get()).split())[1]) if (((phone_no_2.get()).split())[1]).isdigit() else None

        if lower:
            _emp_type = emp_type.get() if (emp_type.get()).isalpha() else None
            _branch = branch.get() if (branch.get()).isalpha() else None
            _dept = dept.get() if (dept.get()).isalpha() else None

        if not lower:
            _position = position.get() if (position.get()).isalpha() else None
            _salary = salary.get() if (salary.get()).isdigit() else None

        datas = [('First_Name', first_name), 
                ('Last_Name', last_name),
                ('Gender', _gender), 
                ('Age', _age), 
                ('Nationality', _nationality),
                ('Phone_Number', _phone_no), 
                ('Date_Of_Birth', f'{year_dob}-{month_dob}-{date_dob}'),
                ('Date_Of_Hire', f'{year_doh}-{month_doh}-{date_doh}'),
                ('Emg_Contact_1_Name', _name_1), 
                ('Emg_Contact_1_Phone_Number', _contact_1),
                ('Emg_Contact_2_Name', _name_2), 
                ('Country_Code', country_code), 
                ('Emg_Contact_2_Phone_Number', int(contact_2)),
                ('Email', _email)]
        
        datas = datas + [('Employment_Type', _emp_type), ('Branch', _branch), ('Department', _dept)] if lower else datas + [('Salary', _salary), ('Position', _position)]

        if any(data[1] is None or data[0].replace('_', ' ') == data[1] for data in datas):

            print([data for data in datas if data[1] is None])
            tk.messagebox.showerror(title = 'Error', message = 'Invalid Entry')
            return

        table = 'Employee' if lower else 'Administrator'

        if edit:

            window.destroy()

            tk.messagebox.showinfo(title = 'Updated', message = 'Data Edited Succesfully')

            for data in datas:
                
                statement = f"""UPDATE {table} SET `{data[0]}` = {data[1]} WHERE {table}_Code = {emp_code}""" if isinstance(data[1], int) else f"""
                               
                               UPDATE {table} SET `{data[0]}` = '{data[1]}' WHERE {table}_Code = {emp_code}"""
                
                cursor.execute(statement)

            connection.commit()

        else:

            window.destroy()

            values = code_passcode_generator(lower)
            
            Values = ', '.join([f'{table}_Code'] + [data[0] for data in datas])
            data_lst = tuple([values[0]] + [value[1] for value in datas])

            cursor.execute(f"""INSERT INTO {table} ({Values})
                           VALUES {data_lst}""")
            
            if lower:
                cursor.execute(f"""INSERT INTO Attendance_Sheet (Employee_Code, Attendance_Passcode)
                               VALUES ({values[0]}, '{values[1]}')""")
                
            connection.commit()

            if lower:
                generated_data(values)

            else:
                tk.messagebox.showinfo(title = 'Registeration Complete', message = f'Data Registered.\n\nAdministrator Code : {values}')

        if from_function is None:
            homepage()
            return
        
        from_function(from_code)

    current_year = datetime.datetime.now().year # variable to mark current year

    # combobox values for nationalities
    nationality_contry_code = [
    ("Afghan", "+93"),
    ("Albanian", "+355"),
    ("Algerian", "+213"),
    ("American", "+1"),
    ("Andorran", "+376"),
    ("Angolan", "+244"),
    ("Antiguan", "+1-268"),
    ("Argentine", "+54"),
    ("Armenian", "+374"),
    ("Australian", "+61"),
    ("Austrian", "+43"),
    ("Azerbaijani", "+994"),
    ("Bahamian", "+1-242"),
    ("Bahraini", "+973"),
    ("Bangladeshi", "+880"),
    ("Barbadian", "+1-246"),
    ("Barbudan", "+1-268"),
    ("Batswana", "+267"),
    ("Belarusian", "+375"),
    ("Belgian", "+32"),
    ("Belizean", "+501"),
    ("Beninese", "+229"),
    ("Bhutanese", "+975"),
    ("Bolivian", "+591"),
    ("Bosnian", "+387"),
    ("Brazilian", "+55"),
    ("Bruneian", "+673"),
    ("Bulgarian", "+359"),
    ("Burkinabe", "+226"),
    ("Burmese", "+95"),
    ("Burundian", "+257"),
    ("Cambodian", "+855"),
    ("Cameroonian", "+237"),
    ("Canadian", "+1"),
    ("Cape Verdean", "+238"),
    ("Central African", "+236"),
    ("Chadian", "+235"),
    ("Chilean", "+56"),
    ("Chinese", "+86"),
    ("Colombian", "+57"),
    ("Comoran", "+269"),
    ("Congolese", "+242"),
    ("Costa Rican", "+506"),
    ("Croatian", "+385"),
    ("Cuban", "+53"),
    ("Cypriot", "+357"),
    ("Czech", "+420"),
    ("Danish", "+45"),
    ("Djiboutian", "+253"),
    ("Dominican", "+1-767"),
    ("Dutch", "+31"),
    ("East Timorese", "+670"),
    ("Ecuadorean", "+593"),
    ("Egyptian", "+20"),
    ("Emirati", "+971"),
    ("Equatorial Guinean", "+240"),
    ("Eritrean", "+291"),
    ("Estonian", "+372"),
    ("Ethiopian", "+251"),
    ("Fijian", "+679"),
    ("Filipino", "+63"),
    ("Finnish", "+358"),
    ("French", "+33"),
    ("Gabonese", "+241"),
    ("Gambian", "+220"),
    ("Georgian", "+995"),
    ("German", "+49"),
    ("Ghanaian", "+233"),
    ("Greek", "+30"),
    ("Grenadian", "+1-473"),
    ("Guatemalan", "+502"),
    ("Guinea-Bissauan", "+245"),
    ("Guinean", "+224"),
    ("Guyanese", "+592"),
    ("Haitian", "+509"),
    ("Herzegovinian", "+387"),
    ("Honduran", "+504"),
    ("Hungarian", "+36"),
    ("Icelander", "+354"),
    ("Indian", "+91"),
    ("Indonesian", "+62"),
    ("Iranian", "+98"),
    ("Iraqi", "+964"),
    ("Irish", "+353"),
    ("Israeli", "+972"),
    ("Italian", "+39"),
    ("Ivorian", "+225"),
    ("Jamaican", "+1-876"),
    ("Japanese", "+81"),
    ("Jordanian", "+962"),
    ("Kazakhstani", "+7"),
    ("Kenyan", "+254"),
    ("Kiribati", "+686"),
    ("Kuwaiti", "+965"),
    ("Kyrgyz", "+996"),
    ("Laotian", "+856"),
    ("Latvian", "+371"),
    ("Lebanese", "+961"),
    ("Liberian", "+231"),
    ("Libyan", "+218"),
    ("Liechtensteiner", "+423"),
    ("Lithuanian", "+370"),
    ("Luxembourger", "+352"),
    ("Macedonian", "+389"),
    ("Malagasy", "+261"),
    ("Malawian", "+265"),
    ("Malaysian", "+60"),
    ("Maldivian", "+960"),
    ("Malian", "+223"),
    ("Maltese", "+356"),
    ("Marshallese", "+692"),
    ("Mauritanian", "+222"),
    ("Mauritian", "+230"),
    ("Mexican", "+52"),
    ("Micronesian", "+691"),
    ("Moldovan", "+373"),
    ("Monacan", "+377"),
    ("Mongolian", "+976"),
    ("Montenegrin", "+382"),
    ("Moroccan", "+212"),
    ("Mozambican", "+258"),
    ("Namibian", "+264"),
    ("Nauruan", "+674"),
    ("Nepalese", "+977"),
    ("New Zealander", "+64"),
    ("Nicaraguan", "+505"),
    ("Nigerien", "+227"),
    ("Nigerian", "+234"),
    ("Norwegian", "+47"),
    ("Omani", "+968"),
    ("Pakistani", "+92"),
    ("Palauan", "+680"),
    ("Panamanian", "+507"),
    ("Papua New Guinean", "+675"),
    ("Paraguayan", "+595"),
    ("Peruvian", "+51"),
    ("Polish", "+48"),
    ("Portuguese", "+351"),
    ("Qatari", "+974"),
    ("Romanian", "+40"),
    ("Russian", "+7"),
    ("Rwandan", "+250"),
    ("Saint Lucian", "+1-758"),
    ("Saint Vincentian", "+1-784"),
    ("Samoan", "+685"),
    ("San Marinese", "+378"),
    ("Sao Tomean", "+239"),
    ("Saudi", "+966"),
    ("Senegalese", "+221"),
    ("Serbian", "+381"),
    ("Seychellois", "+248"),
    ("Sierra Leonean", "+232"),
    ("Singaporean", "+65"),
    ("Slovak", "+421"),
    ("Slovenian", "+386"),
    ("Solomon Islander", "+677"),
    ("Somali", "+252"),
    ("South African", "+27"),
    ("South Korean", "+82"),
    ("South Sudanese", "+211"),
    ("Spanish", "+34"),
    ("Sri Lankan", "+94"),
    ("Sudanese", "+249"),
    ("Surinamer", "+597"),
    ("Swazi", "+268"),
    ("Swedish", "+46"),
    ("Swiss", "+41"),
    ("Syrian", "+963"),
    ("Taiwanese", "+886"),
    ("Tajik", "+992"),
    ("Tanzanian", "+255"),
    ("Thai", "+66"),
    ("Togolese", "+228"),
    ("Tongan", "+676"),
    ("Trinidadian", "+1-868"),
    ("Tunisian", "+216"),
    ("Turkish", "+90"),
    ("Tuvaluan", "+688"),
    ("Ugandan", "+256"),
    ("Ukrainian", "+380"),
    ("Uruguayan", "+598"),
    ("Uzbekistani", "+998"),
    ("Vanuatuan", "+678"),
    ("Venezuelan", "+58"),
    ("Vietnamese", "+84"),
    ("Yemeni", "+967"),
    ("Zambian", "+260"),
    ("Zimbabwean", "+263")
]
    countries = [country[0] for country in nationality_contry_code]

    #combobox values for days, month, year
    days = ['01', '02', '03', '04', '05', '06', '07', '08', '09'] + [str(day) for day in range(10, 32)]
    months = ['01','02','03','04','05','06','07','08','09','10','11','12']
    years = [str(year) for year in range(current_year - 60, current_year - 17)]

    #combobox values for employment types
    employment_types = ['Full Time', 'Part Time', 'Contract', 'Intern']
    branches = ['Branch - 1']
    departments = ['Department']
    
    #creating window
    window = tk.Tk()
    window.title('Registration Form' if not edit else 'Edit Registration')

    timeframe(window)

    #creating common frames ( for administrator and employee ) and packing them
    emp_data_frame = tk.LabelFrame(window, text = 'Employee Details', bd = 5, relief = 'groove')
    job_data_frame = tk.LabelFrame(window, text = 'Job Details', bd = 5, relief = 'groove')

    emp_data_frame.pack(padx = 5, pady = 5, fill = 'both')
    job_data_frame.pack(padx = 5, pady = 5, fill = 'both')

    #creating emergency contact data frame and packing them
    emg_data_frame = tk.LabelFrame(window, text = 'Emergency Contact Details', bd = 5, relief = 'groove')
    emg_data_frame.pack(padx = 5, pady = 5, fill = 'both')

    # list of labels in frame 3
    Label_lst_3 = ['Contact - 1 ( From UAE )', 'Name', 'Phone Number', 'Contact - 2 ( From Motherland )', 'Name', 'Phone Number']
    Label_lst_1 = ['First Name', 'Last Name', 'Gender', 'Age', 'Nationality', 'Phone Number', 'Email', 'Date of Birth']

    #row-column variable for gridding
    row, column = 0, 0

    # defining widgets for frame 1
    f_name = tk.Entry(emp_data_frame, width = 25)
    l_name = tk.Entry(emp_data_frame, width = 25)
    gender = ttk.Combobox(emp_data_frame, width = 25, 
                          values = ['Male ( Mr. )', 'Married Female ( Mrs. )', 'Unmarried Female ( Ms. )'])

    age = ttk.Combobox(emp_data_frame, width = 25, values = list(range(18, 61)))
    nationality = ttk.Combobox(emp_data_frame, width = 25, values = [country[0] for country in nationality_contry_code])
    phone_no = tk.Entry(emp_data_frame, width = 25)

    email = tk.Entry(emp_data_frame, width = 25)

    dob_date = ttk.Combobox(emp_data_frame, width = 25, values = days)
    dob_month = ttk.Combobox(emp_data_frame, width = 25, values = months)
    dob_year = ttk.Combobox(emp_data_frame, width = 25, values = years)

    #list of widgets for frame 1
    widgets = [f_name, l_name, gender, age, nationality, phone_no, email, (dob_date, dob_month, dob_year) ]

    for label, widget in zip(Label_lst_1, widgets):

        # adding labels and gridding them
        text = tk.Label(emp_data_frame, text = label, font = ('Arial', 9, 'bold', 'underline'))
        text.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'news')

        # gridding the widgets ( except date of birth )
        if not isinstance(widget, tuple):
            widget.grid(row = row + 1, column = column, columnspan = 1 if widget != email else 3, 
                        padx = 5, pady = 5, sticky = 'news')

        # gridding date of birth widgets
        if isinstance(widget, tuple):

            date, month, year = widget

            date.grid(row = row + 1, column = 0, padx = 5, pady = 5, sticky = 'news')
            month.grid(row = row + 1, column = 1, padx = 5, pady = 5, sticky = 'news')
            year.grid(row = row + 1, column = 2, padx = 5, pady = 5, sticky = 'news')

        #adjusting the column space
        if label == 'Date of Birth' or label == 'Email':
            text.grid_configure(columnspan = 3)
            column += 2

        # incrementing the row-column variable
        column = column + 1 if column + 1 < 3 else 0
        row = row + 2 if column == 0 else row
    
    #defining date of hire label
    doh_label = tk.Label(job_data_frame, text = 'Date of Hire', font = ('Arial', 9, 'underline', 'bold'))
    doh_label.grid(row = 2, column = 0, columnspan = 3 if lower else 4, padx = 5, pady = 5, sticky = 'news')

    # defining comman widgets for frame 2
    doh_date = ttk.Combobox(job_data_frame, width = 25, values = days)
    doh_month = ttk.Combobox(job_data_frame, width = 25, values = months)
    doh_year = ttk.Combobox(job_data_frame, width = 25, values = years + [str(year) for year in range(current_year - 17, current_year + 1)])

    #gridding common widgets for frame 2
    doh_date.grid(row = 3, column = 0, padx = 5, pady = 5, sticky = 'news')
    doh_month.grid(row = 3, column = 1, columnspan = 1 if lower else 2, padx = 5, pady = 5, sticky = 'news')
    doh_year.grid(row = 3, column = 2 if lower else 3, padx = 5, pady = 5, sticky = 'news')

    if lower: # specific wigets, frames and labels for employee

        # defining  widget
        emp_type = ttk.Combobox(job_data_frame,width = 25, values = employment_types)
        branch = ttk.Combobox(job_data_frame,width = 25, values = branches)
        dept = ttk.Combobox(job_data_frame,width = 25, values = departments)

        widgets = [('Employment Type', emp_type), ('Posting', branch), ('Department', dept)]

        for widget, column in zip(widgets, range(3)):

            label = tk.Label(job_data_frame, text = widget[0], font = ('Arial', 9, 'bold', 'underline'))
            label.grid(row = 0, column = column, padx = 5, pady = 5, sticky = 'ew')

            widget[1].grid(row = 1, column = column, padx = 5, pady = 5, sticky = 'ew')

    if not lower: # specific widgets, frames, labels for administrator

        #defining administrator special eidgets for frame 2
        position = tk.Entry(job_data_frame, width = 25)
        salary = tk.Entry(job_data_frame, width = 25)

        # list of labels ; list of widgets
        Labels = ['Position', 'Salary'] ; widgets = [position, salary]

        for label, widget, column in zip(Labels, widgets, range(0, 4, 2)):

            # creating labels and gridding them
            text = tk.Label(job_data_frame, text = label, font  = ('Arial', 9, 'underline', 'bold'))
            text.grid(row = 0, column = column, columnspan = 2, padx = 5, pady = 5)
            
            #gridding widgets
            widget.grid(row = 1, column = column, columnspan = 2, padx = 5, pady = 5, sticky = 'news')

    #redefining the row-column variables
    row, column = 0, 0

    # defining widgets for frame 3
    name_1 = tk.Entry(emg_data_frame, width = 25)
    phone_no_1 = tk.Entry(emg_data_frame, width = 25)

    name_2 = tk.Entry(emg_data_frame, width = 25)
    phone_no_2 = tk.Entry(emg_data_frame, width = 25)

    # widget list for frame 3
    widgets = [None, name_1, phone_no_1, None, name_2, phone_no_2]

    for label, widget in zip(Label_lst_3, widgets):
        
        # defining and gridding labels
        text = tk.Label(emg_data_frame, text = label, font = ('Arial', 9, 'bold', 'underline'))
        text.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'news')

        #adjusting the column space
        if  'Contact' in label:
            text.grid_configure(columnspan = 2)
            column += 1

        #gridding the widgets
        if widget is not None:
            widget.grid(row = row + 1, column = column, padx = 5, pady = 5, sticky = 'news')

        # incrementing row-column variable
        column = column + 1 if column + 1 < 2 else 0
        row = row + 1 if label == 'Contact - 1' or label == 'Contact - 2' else row + 2 if column == 0 else row
    
    #adapting to window resizing
    emg_data_frame.grid_columnconfigure('all', weight = 1)
    emp_data_frame.grid_columnconfigure('all', weight = 1)
    job_data_frame.grid_columnconfigure('all', weight = 1)

    if edit: # for editing data

        datas = ['First_Name', 
                 'Last_Name', 
                 'Gender', 
                 'Age', 
                 'Nationality', 
                 'Phone_Number', 
                 'Email', 
                 'Date_Of_Birth',
                 'Date_Of_Hire', 
                 'Emg_Contact_1_Name', 
                 'Emg_Contact_1_Phone_Number', 
                 'Emg_Contact_2_Name',
                 'Country_Code', 
                 'Emg_Contact_2_Phone_Number']
        
        #table variable definition
        table = 'Employee' if lower else 'Administrator'

        #excess datas to be retrieved
        datas = datas + ['Employment_Type', 'Branch', 'Department'] if lower else datas + ['Salary', 'Position']

        for data, index in zip(datas, range(len(datas))):

                #retrieveing data from database             
                cursor.execute(f"""SELECT {data} FROM {table}
                               WHERE {table}_Code = {emp_code}""")
                datas[index] = str(cursor.fetchone()[0]) if 'Date' not in data else str(cursor.fetchone()[0]).split('-')

    # function to run on double click on widgets
    def on_double_click(event):
        event.widget.delete(0, tk.END)

    #to add default data or to add exisiting data to be edited ; to add bind effect on the entry widgets
        
    f_name.insert(0, 'First Name' if not edit else datas[0]) ; f_name.bind('<Double-Button-1>', on_double_click)
    l_name.insert(0, 'Last Name' if not edit else datas[1]) ; l_name.bind('<Double-Button-1>', on_double_click)
    gender.insert(0, 'Gender' if not edit else datas[2]) ; gender.bind('<Double-Button-1>', on_double_click)

    age.insert(0, 'Age' if not edit else datas[3]) ; age.bind('<Double-Button-1>', on_double_click)
    nationality.insert(0, 'Nationality' if not edit else datas[4]) ; nationality.bind('<Double-Button-1>', on_double_click)
    phone_no.insert(0, '+971 ' if not edit else '+971 ' + datas[5])

    email.insert(0, 'Email' if not edit else datas[6]) ; email.bind('<Double-Button-1>', on_double_click)

    dob_date.insert(0, 'Date' if not edit else datas[7][2]) ; dob_date.bind('<Double-Button-1>', on_double_click)
    dob_month.insert(0, 'Month' if not edit else datas[7][1]) ; dob_month.bind('<Double-Button-1>', on_double_click)
    dob_year.insert(0, 'Year' if not edit else datas[7][0]) ; dob_year.bind('<Double-Button-1>', on_double_click) 

    doh_date.insert(0, 'Date' if not edit else datas[8][2]) ; doh_date.bind('<Double-Button-1>', on_double_click)
    doh_month.insert(0, 'Month' if not edit else datas[8][1]) ; doh_month.bind('<Double-Button-1>', on_double_click)
    doh_year.insert(0, 'Year' if not edit else datas[8][0]) ; doh_year.bind('<Double-Button-1>', on_double_click)
    
    name_1.insert(0, 'Name' if not edit else datas[9]) ; name_1.bind('<Double-Button-1>', on_double_click)
    phone_no_1.insert(0, '+971 ' if not edit else '+971 ' + datas[10])

    def get_country_code(event):

        if nationality.get() in countries:
            
            country_code = nationality_contry_code[countries.index(nationality.get())][1]
        
            event.widget.delete(0, tk.END)
            event.widget.insert(0, country_code + ' ')

    name_2.insert(0, 'Name' if not edit else datas[11]) ; name_2.bind('<Double-Button-1>', on_double_click)
    phone_no_2.insert(0, '+' if not edit else f'{datas[12]}  {datas[13]}') ; phone_no_2.bind('<Button-1>', get_country_code)

    if lower:
        emp_type.insert(0, 'Employement Type' if not edit else datas[14]) ; emp_type.bind('<Double-Button-1>', on_double_click)
        branch.insert(0, 'Branch' if not edit else datas[15]) ; branch.bind('<Double-Button-1>', on_double_click)
        dept.insert(0, 'Department' if not edit else datas[16]) ; dept.bind('<Double-Button-1>', on_double_click)

    if not lower: # fields specific to administrator
        
        position.insert(0, 'Position' if not edit else datas[14]) ; position.bind('<Double-Button-1>', on_double_click)
        salary.insert(0, 'Salary' if not edit else datas[15]) ; salary.bind('<Double-Button-1>', on_double_click)

    #defining buttons
    Back_button = tk.Button(window, text = 'Back', command = back, padx = 10, pady = 10)
    Clear_button = tk.Button(window, text = 'Clear Form', command = lambda: clear(datas = datas if edit else None), padx = 10, pady = 10)
    Next_button = tk.Button(window, text = 'Register' if not edit else 'Update', command = add, padx = 10, pady = 10)

    #packing the buttons
    Back_button.pack(padx = 5, pady = 5, fill = 'x', side = 'left', expand = True)
    Clear_button.pack(padx = 5, pady = 5, fill = 'x', side = 'left', expand = True)
    Next_button.pack(padx = 5, pady = 5, fill = 'x', side = 'right', expand = True)

    #adding hover effect on the buttons
    hover(window)

    dark_theme(window)
    for frame in window.winfo_children():
        dark_theme(frame)

    window.mainloop() # looping the screen

def new_x_edit_client():
    pass

def change_dealership():
    pass

def generated_data(Values):

    def next_func():
        
        window.destroy()
        tk.messagebox.showinfo(title = 'Registered', message = 'Employee Registered')
    
    window = tk.Tk()
    window.title('Generated Data')

    window.minsize(width = 400, height = 0)

    frame_1 = tk.LabelFrame(window, bd  = 5, relief = 'groove')
    frame_1.pack(padx = 5, pady = 5, fill = 'both')

    frame_2 = tk.LabelFrame(window, bd  = 5, relief = 'groove')
    frame_2.pack(padx = 5, pady = 5, fill = 'both')

    Labels = ['Employee Code', 'Attendance Passcode', 'Login Password']
    texts = ['Note', 'Keep these data safe. Do not Share.', 'Once lost, Contact Administrators']

    for label, value, text, row in zip(Labels, Values, texts, range(4)):

        Label = tk.Label(frame_1, text = label + ' :', font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

        Value = tk.Label(frame_1, text = value)
        Value.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

        if text is not None:
            Text = tk.Label(frame_2, text = text)
            Text.grid(row = row, column = 0, padx = 5, pady = 2, sticky = 'ew')

        if text == 'Note':
            Text.configure(font = ('Arial', 9, 'underline', 'bold'))

    button_next = tk.Button(window, text = 'Next', command = next_func, padx = 10, pady = 10)
    button_next.pack(padx = 5, pady = 5, fill = 'both', expand = True)

    hover(window)

    frame_1.grid_columnconfigure('all', weight = 1)
    frame_2.grid_columnconfigure('all', weight = 1)

    dark_theme(window)
    dark_theme(frame_1)
    dark_theme(frame_2)

    window.mainloop()

def code_passcode_generator(lower = True):
    
    strs = 'abcdefghijkmnopqrstuvwxyz0123456789'
    code = str(random.randint(10000000, 99999999))
    passcode = ''

    for i in range(8):
        passcode += random.choice(strs)

    if lower:
        cursor.execute(f"""SELECT Employee_Code FROM Attendance_Sheet
                   WHERE Employee_Code = {code} OR Attendance_Passcode = '{passcode}'""")
    
    if not lower:
        cursor.execute(f"""SELECT Employee_Code FROM Administrator
                       WHERE Administrator_Code = {code}""")
        
    existing = True if cursor.fetchone() is not None else False

    if existing:
        code_passcode_generator()
        
    return [code, passcode, '12345678'] if lower else [code, 'a1b2c3d4']

def read_datas(from_window = None, from_function = None, from_code = None, from_name = None, min = 0, 
               lower = True, client = False, emp_code = None, dept = None, indices = [0,2,3,4,5,6,7,8,1,9,10,11,12,13,14]):

    def back_func(homepage = True):
        
        window.destroy()

        if homepage:
            from_function(from_code, from_name)
        
        else:
            from_function(emp_code, lower = True)

    def next_func():
        
        window.withdraw()
        read_datas(from_window, from_function, from_code, from_name, min = min + 20, 
                        lower = lower, client = client, emp_code = emp_code, dept = dept, indices = indices)

    def prev_func():
            
        window.withdraw()
        read_datas(from_window, from_function, from_code, from_name, min = min - 20, 
                   lower = lower, client = client, emp_code = emp_code, dept = dept, indices = indices)

    #table definition
    table = 'Administrator' if not lower else 'Client_Database' if client else 'Employee'

    # header row
    cursor.execute(f'SHOW COLUMNS FROM {table}')
    header_row = [header[0] for header in cursor.fetchall()]

    # MySQL statement for retrieving data
    statement = f"""SELECT * FROM {table} WHERE Employee_Code = {emp_code}""" if emp_code is not None else f"""
    SELECT * FROM {table} WHERE Department = '{dept}'""" if dept is not None else f"""SELECT * FROM {table}"""

    # Datas
    cursor.execute(statement)
    datas = (cursor.fetchall())[min::]

    # Check weather any data exists
    if not datas or not header_row:
        tk.messagebox.showerror(title = 'Error', message = 'Data not found')
        return
    
    # destroying from function
    from_window.destroy()
    
    # Screen Definition
    window = tk.Tk()
    window.title('Data')

    timeframe(window)

    #frame definition
    frame = tk.Frame(window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    # gridding the header row and divider between data and header as per given indices
    for index, column in zip(indices, range(len(indices))):

        #gridding header
        header_label = tk.Label(frame, text = header_row[index], font = ('Arial', 9, 'bold', 'underline'))
        header_label.grid(row = 0, column = column, padx = 1, pady = 3, sticky = 'ew')

    data_count = 0

    while data_count < 20 and data_count != len(datas):

        for index, column in zip(indices, range(len(indices))):

            data_label = tk.Label(frame, text = datas[data_count][index])
            data_label.grid(row = data_count + 1, column = column, padx = 1, pady = 3, sticky = 'ew')

        data_count += 1

    button_back = tk.Button(window, text = 'Employee Data' if from_function is not None else 'Exit', 
                            command = back_func if from_function is None else lambda : back_func(False), 
                            padx = 10, pady = 10)
    
    button_next = tk.Button(window, text = 'Next Page',  command = next_func, padx = 10, pady = 10)
    button_previous = tk.Button(window, text = 'Previous Page',  command = prev_func, padx = 10, pady = 10)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)

    if (min == 0 or min + 20 < min + len(datas)) and len(datas) > 20:
        button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)
    
    if min >= 20:
        button_previous.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)

    if from_function == read_data and min + 20 > min + len(datas):

        button_exit = tk.Button(window, text = 'Exit', command = back_func, padx = 10, pady = 10)
        button_exit.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(window)
    dark_theme(frame)

    window.mainloop()

def read_data(emp_code, from_function = None, from_code = None, from_name = None, lower = True):

    def back_func():
        
        window.destroy()
        from_function(from_code, from_name)
    
    def next_func():
        read_datas(from_window = window, from_function = read_data, client = True, emp_code = emp_code)
    
    table = 'Administrator' if not lower else 'Employee'

    datas = ['Employee_Code', 'First_Name', 'Last_Name', 'Gender', 'Age', 'Nationality', 'Date_Of_Birth',
             'Phone_Number', 'Email', 'Position', 'Salary', 'Date_Of_Hire', 'Emg_Contact_1_Name',
             'Emg_Contact_1_Phone_Number', 'Emg_Contact_2_Name', 'Country_Code', 'Emg_Contact_2_Phone_Number']
    
    datas = datas + ['Employment_Type', 'Branch', 'Department'] if lower else datas

    for data, index in zip(datas, range(len(datas))):

        cursor.execute(f'SELECT {data} FROM {table} WHERE Employee_Code = {emp_code}')
        _data = cursor.fetchone()
        
        if _data is not None:
            datas[index] = (data.replace('_', ' '), _data[0])

        else:
            tk.messagebox.showerror(title = 'Error', message = 'Data Not Found')
            back_func()

    window = tk.Tk()
    window.title('Data')

    timeframe(window)

    emp_data_frame = tk.LabelFrame(window, bd = 5, relief = 'groove', text = 'Employee Data')
    job_data_frame = tk.LabelFrame(window, bd = 5, relief = 'groove', text = 'Job Details')
    emg_data_frame = tk.LabelFrame(window, bd = 5, relief = 'groove', text = 'Emergency Contact Details')

    emp_data_frame.pack(padx = 5, pady = 5, fill = 'both')
    job_data_frame.pack(padx = 5, pady = 5, fill = 'both')
    emg_data_frame.pack(padx = 5, pady = 5, fill = 'both')

    emp_data = datas[0:9]
    job_data = datas[9:12] if not lower else datas[9:12] + datas[17:20]

    emp_data[1] = ('Name', f'{emp_data[1][1]} {emp_data[2][1]}')
    emp_data.pop(2)

    row, column = 0, 0

    for data in emp_data:
        
        label = tk.Label(emp_data_frame, text = f'{data[0]} :', font = ('Arial', 9, 'bold'))
        label.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'e')

        value = tk.Label(emp_data_frame, text = data[1])
        value.grid(row = row, column = column + 1, padx = 5, pady = 5, sticky = 'w')

        if column + 2 < 5:
            seperator = tk.Label(emp_data_frame, text = '|', font = 'bold')
            seperator.grid(row = row, column = column + 2, padx = 5, pady = 5, sticky = 'ew')

        column = column + 3 if column + 3 < 6 else 0
        row = row + 1 if column == 0 else row

    row, column = 0, 0

    for data in job_data:
        
        label = tk.Label(job_data_frame, text = f'{data[0]} :', font = ('Arial', 9, 'bold'))
        label.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'e')

        value = tk.Label(job_data_frame, text = data[1])
        value.grid(row = row, column = column + 1, padx = 5, pady = 5, sticky = 'w')

        if column + 2 < 7:
            seperator = tk.Label(job_data_frame, text = '|', font = 'bold')
            seperator.grid(row = row, column = column + 2, padx = 5, pady = 5, sticky = 'ew')

        column = column + 3 if column + 3 < 9 else 0
        row = row + 1 if column == 0 else row

    emg_data = ['Contact-1', ('Name : ', datas[12][1]), ('Phone Number : ', datas[13][1]),
                'Contact-2', ('Name : ', datas[14][1]), ('Phone Number : ', f'{datas[15][1]} {datas[16][1]}')]
    
    row, column = 0, 0

    for data in emg_data:

        if not isinstance(data, tuple):

            label = tk.Label(emg_data_frame, text = data, font = ('Arial', 9, 'bold', 'underline'))
            label.grid(row = row, column = 0, columnspan = 5, padx = 5, pady = 5, sticky = 'ew')

            column = 0
            row += 1
        
        if isinstance(data, tuple):

            label = tk.Label(emg_data_frame, text = f'{data[0]} :', font = ('Arial', 9, 'bold'))
            label.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'e')

            value = tk.Label(emg_data_frame, text = data[1])
            value.grid(row = row, column = column + 1, padx = 5, pady = 5, sticky = 'w')

            if column + 2 < 5:
                seperator = tk.Label(emg_data_frame, text = '|', font = 'bold')
                seperator.grid(row = row, column = column + 2, padx = 5, pady = 5, sticky = 'ew')

            column = column + 3 if column + 3 < 6 else 0
            row = row + 1 if column == 0 else row


    button_back = tk.Button(window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)

    if lower:
        button_next = tk.Button(window, text = 'Client Details', command = next_func, padx = 10, pady = 10)
        button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    emp_data_frame.grid_columnconfigure('all', weight = 1)
    job_data_frame.grid_columnconfigure('all', weight = 1)
    emg_data_frame.grid_columnconfigure('all', weight = 1)

    dark_theme(window)
    dark_theme(emp_data_frame)
    dark_theme(job_data_frame)
    dark_theme(emg_data_frame)
    

    window.mainloop()

def read_client_data():
    pass

def read_att_datas():
    pass

def read_att_data():
    pass

def read_messages_appeals():
    pass

def draft_message():
    pass

def draft_appeals(emp_code):

    def back_func():
        
        window.destroy()
        Employee(emp_code, from_data[1])

    def next_func():
        
        _position = position.get()
        _Appeal_reason = Appeal_reason.get()
        _letter = letter.get('1.0', tk.END)
        
        cursor.execute(f"""INSERT INTO Appeals (To_Position, From_Employee_Code, From_Name,
                       From_Position, Appeal_Reason, Letter)
                       VALUES ('{_position}', {from_data[0]}, '{from_data[1]} {from_data[2]}',
                       '{from_data[3]}', '{_Appeal_reason}', '{_letter}')""")
        
        connection.commit()
        
        tk.messagebox.showinfo(message = 'Appeal Registered', title = 'Info')
        back_func()

    cursor.execute('SELECT DISTINCT(Position) FROM Administrator')
    positions = [position[0] for position in cursor.fetchall()]

    reasons = ['Promotion', 'Incrementation', 'Leave', 'Resignation']

    cursor.execute(f"""SELECT Employee_Code, First_Name, Last_Name, Position
                   FROM Employee
                   WHERE Employee_Code = {emp_code}""")
    
    from_data = cursor.fetchone()
    
    window = tk.Tk()
    window.title('Draft Appeals')

    timeframe(window)

    frame = tk.Frame(window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    position = ttk.Combobox(frame, width = 50, values = positions)
    Appeal_reason = ttk.Combobox(frame, width = 50, values = reasons)
    letter = tk.Text(frame, width = 39, height = 10)

    Labels = [('Position :', position), ('Appeal Reason :', Appeal_reason), ('Letter : ', letter)]

    for label, row in zip(Labels, range(3)):

        Label = tk.Label(frame, text = label[0], font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

        label[1].grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

    button_back = tk.Button(window, text = 'Back', command = back_func, padx = 20, pady = 20)
    button_next = tk.Button(window, text = 'Compose', command = next_func, padx = 20, pady = 20)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)
    button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    frame.grid_columnconfigure('all', weight = 1)

    hover(window)

    dark_theme(window)
    dark_theme(frame)

    window.mainloop()

def sal_position(from_window, ad_emp_code):

    cursor.execute("""SELECT Employee_Code, First_Name, Last_Name FROM Employee
                   WHERE Position OR Salary IS NULL""")
    
    datas = cursor.fetchall()

    if not any(tuple(datas)):
        
        tk.messagebox.showinfo(title = 'No Data Found', message = 'No new registration has been found')
        return
    
    #from_window.destroy()
    
    for data in datas:

        def next_func():

            salary = Salary.get()
            position = Position.get()

            if not salary.isdigit() or position == '':
                tk.messagebox.showerror(title = 'Error', message = 'Invalid Entry')
                return

            cursor.execute(f"""UPDATE Employee
                           SET Salary = {int(salary)}, Position = '{position}'
                           WHERE Employee_Code = {data[0]}""")

            connection.commit()
            
            if data != datas[-1]:
                window.destroy()
                return

            else:
                window.destroy()
                tk.messagebox.showinfo(title = 'All Done', message = 'All Data Has Been Added')
                Administrator(ad_emp_code)
                return

        def back_func():
            window.destroy()
            Administrator(ad_emp_code)
            return

        window = tk.Tk()
        window.title('Manage Salary and Position')

        timeframe(window)
        
        window.minsize(width = 400, height = 100)

        details = tk.LabelFrame(window, relief = 'groove', bd = 5, text = 'Existing Basic Details')
        details.pack(padx = 5, pady = 5, fill = 'both')

        Labels = 'Employee Code :', 'Name :'
        Values = data[0], f'{data[1]} {data[2]}'

        for Label, Value, row in zip(Labels, Values, range(2)):

            label = tk.Label(details, text = Label, font = ('Arial', 9, 'bold'))
            label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

            value = tk.Label(details, text = Value)
            value.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

        new_data = tk.LabelFrame(window, relief = 'groove', bd = 5, text = 'New Data')
        new_data.pack(padx = 5, pady = 5, fill = 'both')

        Position = tk.Entry(new_data, width = 30)
        Salary = tk.Entry(new_data, width = 30)

        labels = ['Position : ', 'Salary : ']
        widgets = [Position, Salary]

        for label, widget, row in zip(labels, widgets, range(2)):

            Label = tk.Label(new_data, text = label, font = ('Arial', 9, 'bold'))
            Label.grid(row = row, column = 0, padx = 10, pady = 10, sticky = 'e')

            widget.grid(row = row, column = 1, padx = 15, pady = 10, sticky = 'w')

        details.grid_columnconfigure('all', weight = 1)
        new_data.grid_columnconfigure('all', weight = 1)

        next_button = tk.Button(window, text = 'Next', command = next_func, padx = 10, pady = 10)
        next_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

        back_button = tk.Button(window, text = 'Back', command = back_func, padx = 10, pady = 10)
        back_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')

        hover(window)

        details.grid_columnconfigure('all', weight = 1)
        new_data.grid_columnconfigure('all', weight = 1)

        dark_theme(window)
        dark_theme(details)
        dark_theme(new_data)

        window.mainloop()

def new_position_or_salary(_position = False, increment = True):
    
    def next_func():
        pass

    def back_func():
        pass

    title = 'Promotion' if _position and increment else 'Demotion' if _position and not increment else 'Incrementation' if not _position and increment else 'Decrementation'

    window = tk.Tk()
    window.title(title)

    timeframe(window)

    frame = tk.Frame(window, bd = 5, relief = 'groove', height = 50)
    frame.pack(padx = 5, pady = 5, fill = 'both')

    sal_lab = 'New Salary : ' if _position else 'Increment [ in % ] : ' if increment else 'Decrement [ in % ]'
    labels = ['Employee Code : ', sal_lab, 'New Position : ']

    row = 0
    for label in labels:

        if not _position and label == 'New Position : ':
            continue

        Label = tk.Label(frame, text = label, font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')
        row += 1

    emp_code = tk.Entry(frame, width = 50)
    position = tk.Entry(frame, width = 50)
    salary = tk.Entry(frame, width = 50)

    widgets = [emp_code, position, salary]

    row = 0
    for widget in widgets:
        
        if not _position and widget == position:
            continue

        widget.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')
        row += 1

    frame.grid_columnconfigure('all', weight = 1)

    button_back = tk.Button(window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_next = tk.Button(window, text = 'Update', command = next_func, padx = 10, pady = 10)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)
    button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    hover(window)

    dark_theme(window)
    dark_theme(frame)

    window.mainloop()

def compose_email():

    def next_func():
        pass

    def back_func():
        pass

    def attachment():
        pass
    
    window = tk.Tk()
    window.title('Compose Email')

    # real time date and time packing
    
    timeframe(window)

    # function code

    from_details = tk.Frame(window, bd = 5, relief = 'groove')
    from_details.pack(padx = 5, pady = 5, fill = 'both')

    to_details = tk.Frame(window, bd = 5, relief = 'groove')
    to_details.pack(padx = 5, pady = 5, fill = 'both')

    label = ['From', 'Password']

    for Label, row in zip(label, range(2)):

        text = tk.Label(from_details, text = f'{Label} : ', font = ('Arial', 9, 'bold'))
        text.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

    _from = tk.Entry(from_details, width = 50)
    _from.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'w')

    passwd = tk.Entry(from_details, width = 50, show = '•')
    passwd.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'w')

    label = ['To', 'Cc', 'Bcc', 'Subject', 'Matter']

    for Label, row in zip(label, range(5)):

        text = tk.Label(to_details, text = f'{Label} : ', font = ('Arial', 9, 'bold'))
        text.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')
    
    to = tk.Entry(to_details, width = 50)
    to.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'ew')

    cc = tk.Entry(to_details, width = 50)
    cc.grid(row = 1, column = 1, padx = 5, pady = 5, sticky = 'ew')

    bcc = tk.Entry(to_details, width = 50)
    bcc.grid(row = 2, column = 1, padx = 5, pady = 5, sticky = 'ew')

    sub = tk.Entry(to_details, width = 50)
    sub.grid(row = 3, column = 1, padx = 5, pady = 5, sticky = 'ew')

    con = tk.Text(to_details, width = 50, height = 10)
    con.grid(row = 4, column = 1, padx = 5, pady = 5, sticky = 'ew')

    image = Image.open('attachment_b.png' if not dark else 'attachment_w.png')
    image = image.resize((30, 30))

    icon = ImageTk.PhotoImage(image)

    attach = tk.Button(to_details, image = icon, compound = 'left', text = 'Add Attachments', command = attachment, padx = 10, pady = 10)
    attach.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'news')

    next_button = tk.Button(window, text = 'Next', command = next_func, padx = 10, pady = 10)
    next_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

    back_button = tk.Button(window, text = 'Back', command = back_func, padx = 10, pady = 10)
    back_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')

    from_details.grid_columnconfigure('all', weight = 1)
    to_details.grid_columnconfigure('all', weight = 1)

    hover(to_details)
    hover(window)

    dark_theme(window)
    dark_theme(to_details)
    dark_theme(from_details)

    window.mainloop()

def conduct_poll():

    def next_func():
        pass

    def back_func():
        pass
    
    window = tk.Tk()
    window.title('Conduct Poll')

    timeframe(window)

    frame = tk.Frame(window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    labels = ['Matter', 'Option 1', ' Option 2', 'Option 3', 'Option 4', 'Option 5']

    matter = tk.Text(frame, width = 50, height = 10)
    option_1 = tk.Entry(frame, width = 50)
    option_2 = tk.Entry(frame, width = 50)
    option_3 = tk.Entry(frame, width = 50)
    option_4 = tk.Entry(frame, width = 50)
    option_5 = tk.Entry(frame, width = 50)

    widgets = [matter, option_1, option_2, option_3, option_4, option_5]

    for label, widget, row in zip(labels, widgets, range(6)):

        Label = tk.Label(frame, text = label + ' : ', font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'ew')

        widget.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'ew')

    button_back = tk.Button(window, text = 'Back', command = back_func, padx = 20, pady = 20)
    button_next = tk.Button(window, text = 'Add Poll', command = next_func, padx = 20, pady = 20)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)
    button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    frame.grid_columnconfigure('all', weight = 1)

    hover(window)

    dark_theme(window)
    dark_theme(frame)

    window.mainloop()

def attend_poll():
    
    def next_func():
        pass

    def back_func():
        pass

    def option_click(n):
        pass

    window = tk.Tk()
    window.title('Conduct Poll')

    timeframe(window)

    frame = tk.Frame(window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    labels = ['Matter', 'Option 1', ' Option 2', 'Option 3', 'Option 4', 'Option 5', 'Skip Vote']
    
    for label, index in zip(labels, range(len(labels))):

        cursor.execute(f"""SELECT {label.replace(' ', '_')} FROM Poll WHERE Status = 'Ongoing'""")
        labels[index] = (label, cursor.fetchall()[-1][0])

    matter_frame = tk.Frame(frame)
    matter_frame.grid(row = 0, column = 0, columnspan = 2, sticky = 'ew')

    matter_lab = tk.Label(matter_frame, text = 'Topic : ', font = ('Arial', 9, 'bold'))
    matter_lab.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')

    matter_lab = tk.Label(matter_frame, text = labels[0][1])
    matter_lab.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'w')

    

    button_back = tk.Button(window, text = 'Back', command = back_func, padx = 20, pady = 20)
    button_next = tk.Button(window, text = 'Add Poll', command = next_func, padx = 20, pady = 20)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)
    button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    frame.grid_columnconfigure('all', weight = 1)

    hover(window)

    dark_theme(window)
    dark_theme(frame)

    window.mainloop()
