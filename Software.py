import mysql.connector
import tkinter as tk
from hashlib import sha3_256 as hash
from tkinter import messagebox, ttk
import random
import smtplib
from Variables import *

dark = True # flag for dark theme

def update_time(window, time, date):

    current_date = datetime.datetime.now().strftime('Date : %d - %m - %Y')
    current_time = datetime.datetime.now().strftime('Time : %H : %M : %S')

    time.config(text=current_time)
    date.config(text=current_date)

    if window.winfo_exists():
        # Store the after() ID to manage it later if needed
        window.update_id = window.after(1000, lambda: update_time(window, time, date))
        
    if not hasattr(window, 'update_id'):
        window.after_cancel(window.update_id)

def timeframe(window):

    datetime_frame = tk.Frame(window)
    datetime_frame.pack(padx=5, pady=1, fill='both')

    time = tk.Label(datetime_frame, font=('Arial', 10, 'bold'))
    date = tk.Label(datetime_frame, font=('Arial', 10, 'bold'))

    time.pack(padx=5, pady=3, side='right')
    date.pack(padx=5, pady=3, side='left')

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

def title_page(exit = False,from_window = None, to_function = None, titles = 'Pantheon Co'.split(' ')):
      
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

    update_pf()

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
        
        # destroy the entry_window and goes to homepage
        entry_window.destroy()
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
            entry_window.destroy()
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

                entry_window.destroy()
                tk.messagebox.showinfo(title = 'Attendance Marked Already', message = 'Attendance has been already marked for the day')
                return

            cursor.execute(f"""UPDATE Attendance_Sheet
                        SET `{last_date}` = 'P'
                        WHERE Employee_Code = {emp_code}
                        AND Attendance_Passcode = '{passcode}'""")
            
            connection.commit()
        
            entry_window.destroy()
            tk.messagebox.showinfo(title = 'Attendance Marked', message = 'Attendance has been marked for the day')
            homepage()

    #creating the entry_window
    entry_window = tk.Tk()
    entry_window.title('Data Verification')
    entry_window.minsize(width = 400, height = 0)

    timeframe(entry_window)

    #creating the frame
    frame = tk.LabelFrame(entry_window, relief = 'groove', bd = 5)
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
    button_back = tk.Button(entry_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_back.pack(padx = 5, pady = 5, side = tk.LEFT, fill = 'x', expand = True)

    button_enter = tk.Button(entry_window, text = 'Enter', command = enter_func, padx = 10, pady = 10)
    button_enter.pack(padx = 5, pady = 5, side = tk.RIGHT, fill = 'x', expand = True)

    #adding hover effect
    hover(entry_window)

    # adjusting to resizing of entry_window
    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(entry_window)
    dark_theme(frame)

    entry_window.mainloop()# looping the entry_window

def Administrator(ad_code): # administrator interface

    def exit():

        admin_window.destroy()
        homepage()
    
    #creating the admin_window
    admin_window = tk.Tk()
    admin_window.title('Employee Interface')

    timeframe(admin_window)

    #creeating a frame
    frame = tk.LabelFrame(admin_window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    #button labels and functions
    Labels = ['retrieve your data', 
              'edit your data', 
              'add new administrator data', 
              'retrieve all administrator data', 
              'retrieve all employee data\n[ emergency contacts ]',
              'retrieve all employee data', 
              'retrieve all employee data\n[ emergency contacts ]', 
              'retrieve all attendance data', 
              'retrieve an employee data',
              'retrieve an employee data\n[ attendance data ]', 
              'manage position and salary\nof new registration', 
              'promote an employee',
              'demote an employee', 
              'provide incrementation to an employee', 
              'provide decrementation to an employee',
              'add client data',
              'retrieve all client data', 
              'retrieve all data of clients\nunder an employee', 
              'retrieve a client data',
              'delete a client data',
              'read appeals', 
              'read messages', 
              'draft a message to all employees', 
              'draft a message to an employee', 
              'draft a message to a department', 
              'draft a message to an administrator',
              'Compose Email' ,
              'Delete an employee data', 
              'delete all employee data', 
              'delete all client data', 
              'delete all attendance data', 
              'exit']
    
    functions = [lambda : read_data(admin_window, ad_code, Administrator, ad_code, lower = False),
                 lambda : new_x_edit_reg(admin_window, Administrator, ad_code, lower = False, edit = True, emp_code = ad_code),
                 lambda : new_x_edit_reg(admin_window, Administrator, ad_code, lower = False),
                 lambda : read_datas(admin_window, Administrator, ad_code, lower = False, indices = list(range(14))),
                 lambda : read_datas(admin_window, Administrator, ad_code, lower = False, indices = [14, 15, 16]),
                 lambda : read_datas(admin_window, Administrator, ad_code, lower = True, indices = list(range(15))),
                 lambda : read_datas(admin_window, Administrator, ad_code, lower = True, indices = [14, 15, 16]),
                 lambda : get_month(admin_window, Administrator, ad_code, all = True),
                 lambda : get_code(admin_window, Administrator, ad_code, lower = False),
                 lambda : get_month(admin_window, Administrator, ad_code),
                 lambda : sal_position(admin_window, ad_code),
                 lambda : new_position_or_salary(admin_window, Administrator, ad_code, True),
                 lambda : new_position_or_salary(admin_window, Administrator, ad_code, True, False),
                 lambda : new_position_or_salary(admin_window, Administrator, ad_code),
                 lambda : new_position_or_salary(admin_window, Administrator, increment = False),
                 lambda : new_x_edit_client(admin_window, Administrator, ad_code),
                 lambda : read_datas(admin_window, Administrator, ad_code, lower = False, client = True, indices = []),
                 lambda : get_code(admin_window, Administrator, ad_code, lower = False, client = True, all = True),
                 lambda : get_code(admin_window, Administrator, ad_code, False, True, False),
                 lambda : delete(admin_window, Administrator, ad_code, client = True, Emp = False),
                 lambda : read_appeals(admin_window, Administrator, ad_code),
                 lambda : read_messages(admin_window, Administrator, ad_code, lower = False),
                 lambda : draft_message(admin_window, Administrator, ad_code, all = True),
                 lambda : draft_message(admin_window, Administrator, ad_code),
                 lambda : draft_message(admin_window, Administrator, ad_code, dept = True, all = True),
                 lambda : draft_message(admin_window, Administrator, ad_code, lower = False, all = True),
                 lambda : compose_email(admin_window, Administrator, ad_code),
                 lambda : delete(admin_window, Administrator, ad_code),
                 lambda : delete(admin_window, Administrator, ad_code, all = True),
                 lambda : delete(admin_window, Administrator, ad_code, all = True, client = True, Emp = False),
                 lambda : delete(admin_window, Administrator, ad_code, all = True, Att = True, Emp = False),
                 exit]

    # row-column variables for griding
    row, column = 0, 0

    for label, function in zip(Labels, functions):
        
        #creating button widget and gridding them
        button = tk.Button(frame, text = label.title(), command = function, padx = 20, pady = 20)
        button.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'news')

        #incrementing the row-column variables
        column = column + 1 if column + 1 < 4 else 0
        row = row + 1 if column == 0 else row

    #adding hover effects
    hover(frame)
    
    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(admin_window)
    dark_theme(frame)

    admin_window.mainloop() # looping the main screen

def Employee(emp_code): # employee interface

    def exit():

        emp_window.destroy()
        homepage()
    
    #creating emp_window
    emp_window = tk.Tk()
    emp_window.title('Employee Interface')

    timeframe(emp_window)

    #creating frame
    frame = tk.LabelFrame(emp_window, bd = 5, relief = 'groove')
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
              'exit']
    
    #buttone functions
    functions = [lambda : read_data(emp_window, emp_code, Employee, emp_code),
                 lambda : new_x_edit_reg(emp_window, Employee, emp_code, emp_code ,edit = True),
                 lambda : get_month(emp_window, Employee, emp_code, default_code = emp_code),
                 lambda : read_datas(emp_window, Employee, emp_code, indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 14]),
                 lambda : read_datas(emp_window, Employee, emp_code, lower = False, indices = [1, 2, 3, 4, 5, 6, 7, 8, 9, 12, 13]),
                 lambda : new_x_edit_client(emp_window, Employee, emp_code),
                 lambda : get_code(emp_window, Employee, emp_code, lower = True, client = True),
                 lambda : read_datas(emp_window, Employee, emp_code, client = True, emp_code = emp_code, indices = list(range(20))),
                 lambda : delete(emp_window, Employee, emp_code, client = True, Emp = False),
                 lambda : change_dealership(emp_window, Employee, emp_code),
                 lambda : change_dealership(emp_window, Employee, emp_code, True),
                 lambda : compose_email(emp_window, Employee, emp_code),
                 lambda : read_messages(emp_window, Employee, emp_code, lower = True),
                 lambda : draft_appeals(emp_window, emp_code),
                 exit]

    #row-column variables for gridding
    row, column = 0, 0

    for label, function in zip(Labels, functions):

        #creating button widgets and gridding them
        button = tk.Button(frame, text = label.title(), command = function, padx = 20, pady = 20)
        button.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'news')

        #adding hover effects
        button.bind('<Enter>', on_enter)
        button.bind('<Leave>', on_leave)
        button.bind('<Button-1>', on_click)

        #incrementing the row and column values
        column = column + 1 if column + 1 < 3 else 0
        row = row + 1 if column == 0 else row
    
    #adapting to resizing
    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(emp_window)
    dark_theme(frame)

    emp_window.mainloop() #looping the emp_window

# combined function to add new registeration or edit ones registration for both employee and admisistrator
def new_x_edit_reg(from_window, from_function = None, from_code = None, emp_code = None, lower = True, edit = False):
    
    from_window.destroy()

    def back(): # back function
        
        add_emp_window.destroy()
        
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
        
        first_name = f_name.get().title() if (f_name.get()).strip() and f_name.get() != 'First Name' else None
        last_name = l_name.get().title() if (l_name.get()).strip() and l_name.get() != 'Last Name'  else None
        _gender = (gender.get()[:4].strip()).title() if (gender.get()[:4]).strip() and gender.get() != 'Gender'  else None

        _age = int(age.get()) if (age.get()).isdigit() else None
        _nationality = nationality.get().title() if (nationality.get()).strip() and nationality.get() != 'Nationality'  else None
        _phone_no = int(phone_no.get()[5:]) if ((phone_no.get())[5:]).isdigit() else None

        _email = email.get() if '@' in email.get() and '.com' in email.get() else None

        date_dob = int(dob_date.get()) if (dob_date.get()).isdigit() else None
        month_dob = int(dob_month.get()) if (dob_month.get()).isdigit() else None
        year_dob = int(dob_year.get()) if (dob_year.get()).isdigit() else None

        date_doh = int(doh_date.get()) if (doh_date.get()).isdigit() else None
        month_doh = int(doh_month.get()) if (doh_month.get()).isdigit() else None
        year_doh = int(doh_year.get()) if (doh_year.get()).isdigit() else None

        _name_1 = name_1.get() if (name_1.get()).strip() and name_1.get() != 'Name'  else None
        _contact_1 = (phone_no_1.get()[5:]) if ((phone_no_2.get())[5:]).isdigit() else None

        _name_2 = name_2.get() if (name_2.get()).strip() and name_2.get() != 'Name'  else None
        country_code = ((phone_no_2.get()).split())[0] if ((((phone_no_2.get()).split())[0])[1:]).isdigit() else None
        contact_2 = int(((phone_no_2.get()).split())[1]) if (((phone_no_2.get()).split())[1]).isdigit() else None

        if lower:
            _emp_type = emp_type.get() if (emp_type.get()).strip() and emp_type.get() != 'Emloyment Type'  else None
            _branch = branch.get() if (branch.get()).strip() and branch.get() != 'Branch'  else None
            _dept = dept.get() if (dept.get()).strip() and dept.get() != 'Department'  else None

        if not lower:
            _position = position.get() if (position.get()).strip() and position.get() != 'Position'  else None
            _salary = salary.get() if (salary.get()).strip() and salary.get() != 'Salary'  else None

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

        if any(data[1] is None for data in datas):

            tk.messagebox.showerror(title = 'Error', message = 'Invalid Entry')
            return

        table = 'Employee' if lower else 'Administrator'

        if edit:

            add_emp_window.destroy()

            tk.messagebox.showinfo(title = 'Updated', message = 'Data Edited Succesfully')

            for data in datas:
                
                statement = f"""UPDATE {table} SET `{data[0]}` = {data[1]} WHERE {table}_Code = {emp_code}""" if isinstance(data[1], int) else f"""
                               
                               UPDATE {table} SET `{data[0]}` = '{data[1]}' WHERE {table}_Code = {emp_code}"""
                
                cursor.execute(statement)

            connection.commit()

        else:

            add_emp_window.destroy()

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

    #combobox values for employment types
    employment_types = ['Full Time', 'Part Time', 'Contract', 'Intern']
    branches = ['Branch - 1']
    departments = ['Department']
    
    #creating add_emp_window
    add_emp_window = tk.Tk()
    add_emp_window.title('Registration Form' if not edit else 'Edit Registration')

    timeframe(add_emp_window)

    #creating common frames ( for administrator and employee ) and packing them
    emp_data_frame = tk.LabelFrame(add_emp_window, text = 'Employee Details', bd = 5, relief = 'groove')
    job_data_frame = tk.LabelFrame(add_emp_window, text = 'Job Details', bd = 5, relief = 'groove')

    emp_data_frame.pack(padx = 5, pady = 5, fill = 'both')
    job_data_frame.pack(padx = 5, pady = 5, fill = 'both')

    #creating emergency contact data frame and packing them
    emg_data_frame = tk.LabelFrame(add_emp_window, text = 'Emergency Contact Details', bd = 5, relief = 'groove')
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
    nationality = ttk.Combobox(emp_data_frame, width = 25, values = countries)
    phone_no = tk.Entry(emp_data_frame, width = 25)

    email = tk.Entry(emp_data_frame, width = 25)

    dob_date = ttk.Combobox(emp_data_frame, width = 25, values = days)
    dob_month = ttk.Combobox(emp_data_frame, width = 25, values = months)
    dob_year = ttk.Combobox(emp_data_frame, width = 25, values = emp_years)

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
    doh_year = ttk.Combobox(job_data_frame, width = 25, values = emp_years + [str(year) for year in range(current_year - 17, current_year + 1)])

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
    
    #adapting to add_emp_window resizing
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
    Back_button = tk.Button(add_emp_window, text = 'Back', command = back, padx = 10, pady = 10)
    Clear_button = tk.Button(add_emp_window, text = 'Clear Form', command = lambda: clear(datas = datas if edit else None), padx = 10, pady = 10)
    Next_button = tk.Button(add_emp_window, text = 'Register' if not edit else 'Update', command = add, padx = 10, pady = 10)

    #packing the buttons
    Back_button.pack(padx = 5, pady = 5, fill = 'x', side = 'left', expand = True)
    Clear_button.pack(padx = 5, pady = 5, fill = 'x', side = 'left', expand = True)
    Next_button.pack(padx = 5, pady = 5, fill = 'x', side = 'right', expand = True)

    #adding hover effect on the buttons
    hover(add_emp_window)

    dark_theme(add_emp_window)
    for frame in add_emp_window.winfo_children():
        dark_theme(frame)

    add_emp_window.mainloop() # looping the screen

def get_code(from_window, from_function, from_code, lower = True, client = False, all = False):

    from_window.destroy()

    def back():

        get_code_window.destroy()
        from_function(from_code)

    def next():

        _code = int(code.get()) if code.get().isdigit() else None

        if _code is None:
            tk.messagebox.showerror(message = 'Incorrect data entered', title = 'Error')
            return

        statement = f"""
SELECT Client_Code, Employee_Code FROM Client
WHERE Client_Code = {_code}
AND Employee_Code = {from_code}""" if client and lower and not all else f"""

SELECT Client_Code FROM Client
WHERE Client_Code = {_code}""" if client  and not all else f"""

SELECT Employee_Code FROM Employee
WHERE Employee_Code = {_code}"""
        
        cursor.execute(statement)
        existing = True if cursor.fetchone() else False

        if not existing:
            tk.messagebox.showerror(message = 'Entered code does not exist', title = 'Error')
            return

        if client and not all:
            read_client_data(get_code_window, _code, from_function, from_code, lower = False)
        
        if all and client and not lower:
            read_datas(get_code_window, from_function, from_code, lower = True, client = True, emp_code = _code, indices = list(range(15)))
        
        if not client:
            read_data(get_code_window, _code, from_function, from_code, lower = True)
    
    get_code_window = tk.Tk()
    get_code_window.title('Code')

    timeframe(get_code_window)

    frame = tk.Frame(get_code_window, relief = 'groove', bd = 5, height = 20)
    frame.pack(padx = 5, pady = 5, fill = 'both')

    code_lab = tk.Label(frame, text = 'Client Code : ' if client and not all else 'Employee Code : ')
    code_lab.grid(row = 0, column = 0, padx = 5, pady = 5, sticky = 'e')

    code = tk.Entry(frame, width = 25)
    code.grid(row = 0, column = 1, padx = 5, pady = 5, sticky = 'w')

    button_back = tk.Button(get_code_window, text = 'Next', padx = 10, pady = 10, command = back)
    button_back.pack(padx  =5, pady = 5, side = 'left', fill = 'both', expand = True)
    
    button_next = tk.Button(get_code_window, text = 'Next', padx = 10, pady = 10, command = next)
    button_next.pack(padx  =5, pady = 5, side = 'right', fill = 'both', expand = True)

    frame.grid_columnconfigure('all', weight = 1)

    hover(get_code_window)

    dark_theme(get_code_window)
    dark_theme(frame)

    get_code_window.mainloop()

def new_x_edit_client(from_window, from_function, from_code, client_code = None, edit = False):
    
    from_window.destroy()

    def back_func():
        add_client_window.destroy()
        from_function(from_code)

    def clear_func(data = None):
        
        company_name.delete(0, tk.END) ; company_name.insert(0, 'Company Name' if not edit else data[3])
        location.delete(0, tk.END) ; location.insert(0, 'Location' if not edit else data[4])
        tele_no.delete(0, tk.END) ; tele_no.insert(0, 'Telephone Number' if not edit else data[5])

        email.delete(0, tk.END) ; email.insert(0, 'Email' if not edit else data[6])

        client_name.delete(0, tk.END) ; client_name.insert(0, 'Client Name' if not edit else data[7])
        phone_no.delete(0, tk.END) ; phone_no.insert(0, 'Phone Number' if not edit else f'{data[8]} {data[9]}')
        contract_period.delete(0, tk.END) ; contract_period.insert(0, 'Contract Period ( In Months )' if not edit else data[10])

        from_date.delete(0, tk.END) ; from_date.insert(0, 'Date' if not edit else data[11][2])
        from_month.delete(0, tk.END) ; from_month.insert(0, 'Month' if not edit else data[11][1])
        from_year.delete(0, tk.END) ; from_year.insert(0, 'Year' if not edit else data[11][0])

        to_date.delete(0, tk.END) ; to_date.insert(0, 'Date' if not edit else data[12][2])
        to_month.delete(0, tk.END) ; to_month.insert(0, 'Month' if not edit else data[12][1])
        to_year.delete(0, tk.END) ; to_year.insert(0, 'Year' if not edit else data[12][0])

        avg_sales.delete(0, tk.END) ; avg_sales.insert(0, 'Average Sales Per Month' if not edit else data[13])
        total_sales.delete(0, tk.END) ; total_sales.insert(0, 'Sales This Month' if not edit else data[14])

        prod_1.delete(0, tk.END) ; prod_1.insert(0, 'Product 1' if not edit else data[15])
        prod_2.delete(0, tk.END) ; prod_2.insert(0, 'Product 2' if not edit else data[16] if data[16] is not None else 'Nil')
        prod_3.delete(0, tk.END) ; prod_3.insert(0, 'Product 3' if not edit else data[17] if data[17] is not None else 'Nil')
        prod_4.delete(0, tk.END) ; prod_4.insert(0, 'Product 4' if not edit else data[18] if data[18] is not None else 'Nil')
        prod_5.delete(0, tk.END) ; prod_5.insert(0, 'Product 5' if not edit else data[19] if data[19] is not None else 'Nil')

        tk.messagebox.showinfo(title = 'Successfully Cleared', message = 'Form has been cleared')

    def add_func():
        
        _company_name = company_name.get().title() if company_name.get().strip() and company_name.get() != 'Company Name' else None
        _location = location.get().title() if location.get().strip() and location.get() != 'Location' else None
        _tele_no = int(tele_no.get()) if tele_no.get().isdigit() else 'Nil'

        _email = email.get().title() if '@' and '.com' in email.get() else None

        _client_name = client_name.get().title() if client_name.get().strip() and client_name.get() != 'Client Name' else None
        _country_code = phone_no.get().split()[0] if phone_no.get().split()[0][1:].isdigit() else 'Nil'
        _phone_no = int(phone_no.get().split()[1]) if phone_no.get().split()[1].isdigit() else 'Nil'
        _contract_period = int(contract_period.get()) if contract_period.get().isdigit() else None

        _from_date = from_date.get() if from_date.get().isdigit() else None
        _from_month = from_month.get() if from_month.get().isdigit() else None
        _from_year = from_year.get() if from_year.get().isdigit() else None

        _to_date = to_date.get() if to_date.get().isdigit() else None
        _to_month = to_month.get() if to_month.get().isdigit() else None
        _to_year = to_year.get() if to_year.get().isdigit() else None

        _avg_sales = int(avg_sales.get()) if avg_sales.get().isdigit() else None
        _total_sales = int(total_sales.get()) if total_sales.get().isdigit() else None

        _prod_1 = prod_1.get().title() if prod_1.get().strip() and prod_1.get() != 'Product 1' else None
        _prod_2 = prod_2.get().title() if prod_2.get().strip() and prod_2.get() != 'Product 2' else 'Nil'
        _prod_3 = prod_3.get().title() if prod_3.get().strip() and prod_3.get() != 'Product 3' else 'Nil'
        _prod_4 = prod_4.get().title() if prod_4.get().strip() and prod_4.get() != 'Product 4' else 'Nil'
        _prod_5 = prod_5.get().title() if prod_5.get().strip() and prod_5.get() != 'Product 5' else 'Nil'

        datas = [('Company_Name', _company_name),
                 ('Location', _location),
                 ('Company_Telephone_Number', _tele_no) if _tele_no != 'Nil' else 'NULL',
                 ('Email', _email), 
                 ('Client_Name', _client_name),
                 ('Country_Code', _country_code) if _country_code != 'Nil' else 'NULL',
                 ('Client_Phone_Number', _phone_no) if _phone_no != 'Nil' else 'NULL',
                 ('Contract_Period', _contract_period),
                 ('Contract_From', f'{_from_year}-{_from_month}-{_from_date}'),
                 ('Contract_To', f'{_to_year}-{_to_month}-{_to_date}'),
                 ('Avg_Sales_Per_Month', _avg_sales),
                 ('Total_Sales', _total_sales),
                 ('Product_1', _prod_1),
                 ('Product_2', _prod_2) if _prod_2 != 'Nil' else 'NULL',
                 ('Product_3', _prod_3) if _prod_3 != 'Nil' else 'NULL',
                 ('Product_4', _prod_4) if _prod_4 != 'Nil' else 'NULL',
                 ('Product_5', _prod_5) if _prod_5 != 'Nil' else 'NULL']
        
        if any(data[1] is None for data in datas):
            tk.messagebox.showerror(message = 'Incorrect Data Entered', title = 'Error')
            return
        
        add_client_window.destroy()

        if edit:

            tk.messagebox.showinfo(message = 'Data Updated', title = 'Updated')

            for data in datas:

                if data != 'NULL':
                    cursor.execute(f"""UPDATE Client
                                   SET `{data[0]}` = {data[1]}
                                   WHERE Client_Code = {client_code}""" if isinstance(data[1], int) else f"""
                                   UPDATE Client
                                   SET `{data[0]}` = '{data[1]}'
                                   WHERE Client_Code = {client_code}""")
                    connection.commit()
            
            from_function(from_code)

        else:

            existing = True

            while existing:

                client_code = random.randint(1, 10001)
                
                cursor.execute(f'''SELECT Client_Code FROM Client
                               WHERE Client_Code = {client_code}''')
                code = cursor.fetchone()

                existing = False if code is None else True
            
            table = 'Employee' if from_function == Employee else 'Administrator'

            cursor.execute(f"""SELECT First_Name, Last_Name FROM {table}
                           WHERE {table}_Code = {from_code}""")
            name = [f'{name[0]} {name[1]}' for name in cursor.fetchall()][0]

            tk.messagebox.showinfo(message = f'Data Registered\n Client Code : {client_code}', title = 'Registered')
        
            headers = ', '.join(['Employee_Code, Employee_Name', 'Client_Code'] + [data[0] for data in datas if data != 'NULL'])
            values = tuple([from_code, name, client_code] + [data[1] for data in datas if data != 'NULL'])
            
            cursor.execute(f"""INSERT INTO Client ({headers})
                           VALUES {values}""")
            
            connection.commit()
            
        from_function(from_code)

    add_client_window = tk.Tk()
    add_client_window.title('Add Client' if not edit else 'Edit Client Data')

    timeframe(add_client_window)

    client_frame = tk.LabelFrame(add_client_window, text = 'Client Data', relief = 'groove', bd = 5)
    product_frame = tk.LabelFrame(add_client_window, text = 'Product Data', relief = 'groove', bd = 5)

    client_frame.pack(padx = 5, pady = 5, fill = 'both')
    product_frame.pack(padx = 5, pady = 5, fill = 'both')

    company_name = tk.Entry(client_frame, width = 25)
    location = ttk.Combobox(client_frame, width = 25, values = countries)
    tele_no = tk.Entry(client_frame, width = 25)

    email = tk.Entry(client_frame, width = 25)

    client_name = tk.Entry(client_frame, width = 25)
    phone_no = tk.Entry(client_frame, width = 25)
    contract_period = ttk.Combobox(client_frame, width = 25, values = list(range(6, 61, 6)))

    from_date = ttk.Combobox(client_frame, width = 25, values = days)
    from_month = ttk.Combobox(client_frame, width = 25, values = months)
    from_year = ttk.Combobox(client_frame, width = 25, values = client_years)

    to_date = ttk.Combobox(client_frame, width = 25, values = days)
    to_month = ttk.Combobox(client_frame, width = 25, values = months)
    to_year = ttk.Combobox(client_frame, width = 25, values = client_years + list(range(current_year, current_year + 6)))

    avg_sales = tk.Entry(client_frame, width = 25)
    total_sales = tk.Entry(client_frame, width = 25)

    widgets = [company_name, location, tele_no, email, client_name, phone_no, contract_period,
               (from_date, from_month, from_year), (to_date, to_month, to_year), avg_sales, total_sales]

    prod_1 = tk.Entry(product_frame, width = 25)
    prod_2 = tk.Entry(product_frame, width = 25)
    prod_3 = tk.Entry(product_frame, width = 25)
    prod_4 = tk.Entry(product_frame, width = 25)
    prod_5 = tk.Entry(product_frame, width = 25)

    client_Labels = ['Company Name *', 'Location *', 'Telephone Number', 'Email *',
                     'Client Name *', 'Phone Number', 'Contract Period ( In Months ) *', 
                     'Contract Valid From *', 'Contract Valid Until *',
                     'Average Sales Per Month *', 'Sales This Month *']
    
    row, column = 0, 0

    for label, widget in zip(client_Labels, widgets):

        Label = tk.Label(client_frame, text = label, font = ('Arial', 9, 'bold', 'underline'))
        Label.grid(row = row, column = column, columnspan = 2, padx = 5, pady = 5, sticky = 's')

        if not isinstance(widget, tuple):
            widget.grid(row = row+1, column = column, columnspan = 2, padx = 5, pady = 5, sticky = 'news')

        if 'Valid' in label:
            Label.grid_configure(columnspan = 6)
            for Widget, i in zip(widget, range(0, 6, 2)):
                Widget.grid(row = row+1, column = column + i, padx = 5, pady = 5, columnspan = 2, sticky = 'news')
            column += 4
        
        if label == 'Email *':
            Label.grid_configure(columnspan = 6)
            widget.grid_configure(columnspan = 6)
            column += 4
        
        if 'Sales' in label:
            Label.grid_configure(columnspan = 3)
            widget.grid_configure(columnspan = 3)
            column += 1

        column = column + 2 if column + 2 < 6 else 0
        row = row + 2 if column == 0 else row  

    prod_widgets = [prod_1, prod_2, prod_3, prod_4, prod_5] 

    row, column = 0, 0

    for widget, num in zip(prod_widgets, range(1, 6)):
        
        Label = tk.Label(product_frame, text = f'Product {num}' if num != 1 else f'Product {num} *', 
                         font = ('Arial', 9, 'bold', 'underline'))
        Label.grid(row = row, column = column, padx = 5, pady = 5, sticky = 's')

        widget.grid(row = row+1, column = column, padx = 5, pady = 5, sticky = 'news')

        if num == 5:
            Label.grid_configure(columnspan = 2)
            widget.grid_configure(columnspan = 2)
        
        column = column + 1 if column + 1 < 2 else 0
        row = row + 2 if column == 0 else row

    back_button = tk.Button(add_client_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    clear_button = tk.Button(add_client_window, text = 'Clear Form', command = clear_func if not edit else lambda : clear_func(data)
                             , padx = 10, pady = 10)
    add_button = tk.Button(add_client_window, text = 'Add Client' if not edit else 'Edit Data', command = add_func, padx = 10, pady = 10)

    back_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')
    clear_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')
    add_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

    if edit:
        
        cursor.execute(f"""SELECT * FROM Client
                       WHERE Client_Code = {client_code}
                       AND Employee_Code = {from_code}""")
        data = list(cursor.fetchone())

        
        data[11], data[12] = str(data[11]).split('-'), str(data[12]).split('-')

    def on_double_click(event):
        event.widget.delete(0, tk.END)
    
    def get_country_code(event):

        if location.get() in countries:
            
            country_code = nationality_contry_code[countries.index(location.get())][1]
        
            event.widget.delete(0, tk.END)
            event.widget.insert(0, country_code + ' ')

    company_name.insert(0, 'Company Name' if not edit else data[3]) ; company_name.bind('<Double-Button-1>', on_double_click)
    location.insert(0, 'Location' if not edit else data[4]) ; location.bind('<Double-Button-1>', on_double_click)
    tele_no.insert(0, 'Telephone Number' if not edit else data[5]) ; tele_no.bind('<Double-Button-1>', on_double_click)

    email.insert(0, 'Email' if not edit else data[6]) ; email.bind('<Double-Button-1>', on_double_click)

    client_name.insert(0, 'Client Name' if not edit else data[7]) ; client_name.bind('<Double-Button-1>', on_double_click)
    phone_no.insert(0, 'Phone Number' if not edit else f'{data[8]} {data[9]}') ; phone_no.bind('<Button-1>', get_country_code)
    contract_period.insert(0, 'Contract Period ( In Months )' if not edit else data[10]) ; contract_period.bind('<Double-Button-1>', on_double_click)

    from_date.insert(0, 'Date' if not edit else data[11][2]) ; from_date.bind('<Double-Button-1>', on_double_click)
    from_month.insert(0, 'Month' if not edit else data[11][1]) ; from_month.bind('<Double-Button-1>', on_double_click)
    from_year.insert(0, 'Year' if not edit else data[11][0]) ; from_year.bind('<Double-Button-1>', on_double_click)

    to_date.insert(0, 'Date' if not edit else data[12][2]) ; to_date.bind('<Double-Button-1>', on_double_click)
    to_month.insert(0, 'Month' if not edit else data[12][1]) ; to_month.bind('<Double-Button-1>', on_double_click)
    to_year.insert(0, 'Year' if not edit else data[12][0]) ; to_year.bind('<Double-Button-1>', on_double_click)

    avg_sales.insert(0, 'Average Sales Per Month' if not edit else data[13]) ; avg_sales.bind('<Double-Button-1>', on_double_click)
    total_sales.insert(0, 'Sales This Month' if not edit else data[14]) ; total_sales.bind('<Double-Button-1>', on_double_click)

    prod_1.insert(0, 'Product 1' if not edit else data[15]) ; prod_1.bind('<Double-Button-1>', on_double_click)
    prod_2.insert(0, 'Product 2' if not edit else data[16] if data[16] is not None else 'Nil') ; prod_2.bind('<Double-Button-1>', on_double_click)
    prod_3.insert(0, 'Product 3' if not edit else data[17] if data[17] is not None else 'Nil') ; prod_3.bind('<Double-Button-1>', on_double_click)
    prod_4.insert(0, 'Product 4' if not edit else data[18] if data[18] is not None else 'Nil') ; prod_4.bind('<Double-Button-1>', on_double_click)
    prod_5.insert(0, 'Product 5' if not edit else data[19] if data[19] is not None else 'Nil') ; prod_5.bind('<Double-Button-1>', on_double_click)

    client_frame.grid_columnconfigure('all', weight = 1)
    product_frame.grid_columnconfigure('all', weight = 1)

    dark_theme(add_client_window)
    dark_theme(client_frame)
    dark_theme(product_frame)

    hover(add_client_window)

    add_client_window.mainloop()

def change_dealership(from_window, from_function, from_code, all = False):

    from_window.destroy()

    def back_func():
        
        change_window.destroy()
        from_function(from_code)

    def next_func():
        
        new_name = name.get().title() if any(name.get()) else None
        
        if not all:
            client_code = int(c_code.get()) if c_code.get().isdigit() else None
            client_name = c_name.get() if any(c_name.get()) else None

        cursor.execute(f"""SELECT Employee_Code FROM Employee
                       WHERE First_Name = '{new_name.split()[0]}'
                       AND Last_Name = '{new_name.split()[1]}'""")
        new_code = cursor.fetchone()[0]

        if None in [new_name, new_code, client_code if not all else 'None', client_name if not all else 'None']:
            tk.messagebox.showerror(title = 'Error', message = 'Incorrect Data Entered')
            return
        
        statement = f"""UPDATE Client
                       SET Employee_Name = '{new_name}',
                       Employee_Code = {new_code}
                       WHERE Client_Code = {client_code} 
                       AND Client_Name = '{client_name}'""" if not all else f"""
                       
                       UPDATE Client
                       SET Employee_Name = '{new_name}',
                       Employee_Code = {new_code} 
                       WHERE Employee_Code = {from_code}"""
        
        cursor.execute(statement)
        connection.commit()

        change_window.destroy()
        tk.messagebox.showinfo(title = 'Success', message = 'Client Successfully Transferred')
        from_function(from_code)
        
    change_window = tk.Tk()
    change_window.title('Change Ownership of Client')

    change_window.minsize(width = 400, height = 100)
    
    timeframe(change_window)

    frame = tk.Frame(change_window, relief = 'groove', bd = 5)
    frame.pack(padx = 5, pady = 5, fill = 'both')

    Labels = ['New Employee Name', 'Client Code', 'Client Name']

    cursor.execute("""SELECT First_Name, Last_Name FROM Employee
                   WHERE Position = 'Sales Executive'""")
    names = [f'{name[0]} {name[1]}' for name in cursor.fetchall()]
    

    name = ttk.Combobox(frame, width = 25, values = names)
    
    if not all:
        c_code = tk.Entry(frame, width = 27)
        c_name = tk.Entry(frame, width = 27)

    widgets = [name, c_code, c_name] if not all else [name]

    for label, widget, row in zip(Labels, widgets, range(3)):

        Label = tk.Label(frame, text = f'{label} :', font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 8, sticky = 'e')

        widget.grid(row = row, column = 1, padx = 5, pady = 8, sticky = 'w')
    
    button_back = tk.Button(change_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_back.pack(padx = 5, pady = 5, fill = 'both', side = 'left', expand = True)

    button_next = tk.Button(change_window, text = 'Next', command = next_func, padx = 10, pady = 10)
    button_next.pack(padx = 5, pady = 5, fill = 'both', side = 'right', expand = True)

    dark_theme(change_window)
    dark_theme(frame)

    hover(change_window)

    frame.grid_columnconfigure('all', weight = 1)

    change_window.mainloop()

def generated_data(Values):

    def next_func():
        
        generated_data_window.destroy()
        tk.messagebox.showinfo(title = 'Registered', message = 'Employee Registered')
    
    generated_data_window = tk.Tk()
    generated_data_window.title('Generated Data')

    timeframe(generated_data_window)

    generated_data_window.minsize(width = 400, height = 0)

    frame_1 = tk.LabelFrame(generated_data_window, bd  = 5, relief = 'groove')
    frame_1.pack(padx = 5, pady = 5, fill = 'both')

    frame_2 = tk.LabelFrame(generated_data_window, bd  = 5, relief = 'groove')
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

    button_next = tk.Button(generated_data_window, text = 'Next', command = next_func, padx = 10, pady = 10)
    button_next.pack(padx = 5, pady = 5, fill = 'both', expand = True)

    hover(generated_data_window)

    frame_1.grid_columnconfigure('all', weight = 1)
    frame_2.grid_columnconfigure('all', weight = 1)

    dark_theme(generated_data_window)
    dark_theme(frame_1)
    dark_theme(frame_2)

    generated_data_window.mainloop()

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

def read_datas(from_window = None, from_function = None, from_code = None, min = 0, 
               lower = True, client = False, emp_code = None, dept = None, indices = [0,2,3,4,5,6,7,8,1,9,10,11,12,13,14]):

    def back_func():
        
        if from_function not in (Administrator, Employee):
            read_data(read_datas_window, emp_code, from_function, from_code, lower = True)

        else:
            read_datas_window.destroy()
            from_function(from_code)

    def next_func():
        
        read_datas(read_datas_window, from_function, from_code, min = min + 20, 
                        lower = lower, client = client, emp_code = emp_code, dept = dept, indices = indices)

    def prev_func():
        
        read_datas(read_datas_window, from_function, from_code, min = min - 20, 
                   lower = lower, client = client, emp_code = emp_code, dept = dept, indices = indices)

    #table definition
    table = 'Administrator' if not lower else 'Client' if client else 'Employee'

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
    read_datas_window = tk.Tk()
    read_datas_window.title('Data')

    timeframe(read_datas_window)

    #frame definition
    frame = tk.Frame(read_datas_window, bd = 5, relief = 'groove')
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

    button_back = tk.Button(read_datas_window, text = 'Employee Data' if from_function not in (Administrator, Employee) else 'Exit', 
                            command = back_func, padx = 10, pady = 10)
    
    button_next = tk.Button(read_datas_window, text = 'Next Page',  command = next_func, padx = 10, pady = 10)
    button_previous = tk.Button(read_datas_window, text = 'Previous Page',  command = prev_func, padx = 10, pady = 10)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)

    if (min == 0 or min + 20 < min + len(datas)) and len(datas) > 20:
        button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)
    
    if min >= 20:
        button_previous.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)

    if from_function == read_data and min + 20 > min + len(datas):

        button_exit = tk.Button(read_datas_window, text = 'Exit', command = back_func, padx = 10, pady = 10)
        button_exit.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(read_datas_window)
    dark_theme(frame)

    read_datas_window.mainloop()

def read_data(from_window, emp_code, from_function = None, from_code = None, lower = True):

    def back_func():
        
        read_data_window.destroy()
        from_function(from_code)
    
    def next_func():
        read_datas(from_window = read_data_window, from_function = from_function, from_code = from_code, client = True, emp_code = emp_code)

    from_window.destroy()
    
    table = 'Administrator' if not lower else 'Employee'

    datas = ['First_Name', f'{table}_Code', 'Last_Name', 'Gender', 'Age', 'Nationality', 'Date_Of_Birth',
             'Phone_Number', 'Email', 'Position', 'Salary', 'Provident_Fund', 'Date_Of_Hire', 'Emg_Contact_1_Name',
             'Emg_Contact_1_Phone_Number', 'Emg_Contact_2_Name', 'Country_Code', 'Emg_Contact_2_Phone_Number']
    
    datas = datas + ['Employment_Type', 'Branch', 'Department'] if lower else datas

    for data, index in zip(datas, range(len(datas))):

        cursor.execute(f'SELECT `{data}` FROM {table} WHERE {table}_Code = {emp_code}')
        _data = cursor.fetchone()
        
        if _data is not None:
            datas[index] = (data.replace('_', ' '), _data[0])

        else:
            tk.messagebox.showerror(title = 'Error', message = 'Data Not Found')
            back_func()

    read_data_window = tk.Tk()
    read_data_window.title('Data')

    timeframe(read_data_window)

    emp_data_frame = tk.LabelFrame(read_data_window, bd = 5, relief = 'groove', text = 'Employee Data')
    job_data_frame = tk.LabelFrame(read_data_window, bd = 5, relief = 'groove', text = 'Job Details')
    emg_data_frame = tk.LabelFrame(read_data_window, bd = 5, relief = 'groove', text = 'Emergency Contact Details')

    emp_data_frame.pack(padx = 5, pady = 5, fill = 'both')
    job_data_frame.pack(padx = 5, pady = 5, fill = 'both')
    emg_data_frame.pack(padx = 5, pady = 5, fill = 'both')

    emp_data = datas[0:9]
    job_data = datas[9:13] if not lower else datas[9:13] + datas[18:21]

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

    emg_data = ['Contact-1', ('Name : ', datas[13][1]), ('Phone Number : ', datas[14][1]),
                'Contact-2', ('Name : ', datas[15][1]), ('Phone Number : ', f'{datas[16][1]} {datas[17][1]}')]
    
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


    button_back = tk.Button(read_data_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)

    if lower:
        button_next = tk.Button(read_data_window, text = 'Client Details', command = next_func, padx = 10, pady = 10)
        button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    emp_data_frame.grid_columnconfigure('all', weight = 1)
    job_data_frame.grid_columnconfigure('all', weight = 1)
    emg_data_frame.grid_columnconfigure('all', weight = 1)

    dark_theme(read_data_window)
    dark_theme(emp_data_frame)
    dark_theme(job_data_frame)
    dark_theme(emg_data_frame)
    

    read_data_window.mainloop()

def read_client_data(from_window, client_code, from_function, from_code, lower = False):
    
    statement = f"""SELECT * FROM Client
        WHERE Client_Code = {client_code}
        AND Employee_Code = {from_code}""" if lower else f"""SELECT * FROM Client
        WHERE Client_Code = {client_code}"""
    
    cursor.execute(statement)
    data = cursor.fetchone()

    emp_labels = ['Employee Code', 'Employee Name']
    client_labels = ['Client Code', 'Company Name', 'Location',
                   'Telephone Number', 'Email', 'Client Name', 'Phone Number',
                   'Contract From', 'Contract To', 'Contract Period',
                   'Total Sales', 'Average Sales Per Month']
    
    if data is None:
        tk.messagebox.showerror(title = 'Error', message = 'Data Not Found')
        return

    from_window.destroy()

    def back_func():

        read_client_data_window.destroy()
        from_function(from_code)

    read_client_data_window = tk.Tk()
    read_client_data_window.title('Client Data')

    emp_frame = tk.LabelFrame(read_client_data_window, text = 'Employee Details', relief = 'groove', bd = 5)
    client_frame = tk.LabelFrame(read_client_data_window, text = 'Client Details', relief = 'groove', bd = 5)
    product_frame = tk.LabelFrame(read_client_data_window, text = 'Product List', relief = 'groove', bd = 5)

    emp_frame.pack(padx = 5, pady = 5, fill = 'both')
    client_frame.pack(padx = 5, pady = 5, fill = 'both')
    product_frame.pack(padx = 5, pady = 5, fill = 'both')

    emp_data = data[0:2]
    client_data = list(data[2:15])
    product_data = data[15:]

    client_data[6] = f'{client_data[6]} {client_data[7]}'
    client_data.pop(7)

    row, column = 0, 0

    for label, datum in zip(emp_labels, emp_data):

        Label = tk.Label(emp_frame, text = f'{label} :', font = ('Arial', 9, 'bold'))
        Label.grid(row = 0, column = column, padx = 5, pady = 5, sticky = 'e')

        Datum = tk.Label(emp_frame, text = datum)
        Datum.grid(row = 0, column = column + 1, padx = 5, pady = 5, sticky = 'w')

        if column < 3:
            sep = tk.Label(emp_frame, text = '|', font = ('Arial', 9, 'bold'))
            sep.grid(row = 0, column = column + 2, padx = 5, pady = 5, sticky = 'ew')
        
        column = column + 3 if column < 6 else 0

    row, column = 0, 0

    for label, datum in zip(client_labels, client_data):

        Label = tk.Label(client_frame, text = f'{label} :', font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'e')

        Datum = tk.Label(client_frame, text = datum if datum is not None else 'NA')
        Datum.grid(row = row, column = column + 1, padx = 5, pady = 5, sticky = 'w')

        if column + 3 < 6:
            sep = tk.Label(client_frame, text = '|', font = ('Arial', 9, 'bold'))
            sep.grid(row = row, column = column + 2, padx = 5, pady = 5, sticky = 'ew')

        column = column + 3 if column + 3 < 6 else 0
        row = row + 1 if column == 0 else row

    row, column = 0, 0

    for datum, num in zip(product_data, range(1, 6)):

        Label = tk.Label(product_frame, text = f'Product {num} :', font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'e')

        Datum = tk.Label(product_frame, text = datum if datum is not None else 'NA')
        Datum.grid(row = row, column = column + 1, padx = 5, pady = 5, sticky = 'w')

        if column < 3 and product_data[-1] != datum:
            sep = tk.Label(product_frame, text = '|', font = ('Arial', 9, 'bold'))
            sep.grid(row = row, column = column + 2, padx = 5, pady = 5, sticky = 'ew')

        column = column + 3 if column + 3 < 6 else 0
        row = row + 1 if column == 0 else row

    button_back = tk.Button(read_client_data_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_back.pack(padx = 5, pady = 5, fill = 'both', expand = True)

    dark_theme(read_client_data_window)
    dark_theme(emp_frame)
    dark_theme(client_frame)
    dark_theme(product_frame)

    emp_frame.grid_columnconfigure('all', weight = 1)
    client_frame.grid_columnconfigure('all', weight = 1)
    product_frame.grid_columnconfigure('all', weight = 1)

    hover(read_client_data_window)

    read_client_data_window.mainloop()

def get_month(from_window, from_function, from_code, all = False, default_code = None):

    from_window.destroy()

    def back_func():
        
        get_month_window.destroy()
        from_function(from_code)

    def next_func():
        
        if not all and from_function == Employee:
            code = int(default_code)
        
        elif not all:
            code = int(emp_code.get()) if (emp_code.get()).isdigit() else None

        _year = year.get() if (year.get()).isdigit() else None
        _month = month.get() if (month.get()).isdigit() else None

        datas = [code, _year, _month] if not all else [_year, _month]

        if any(data is None for data in datas):
            tk.messagebox.showerror(title = 'Error', message = 'Incorrect datatype entered')
            return
        
        cursor.execute(f"""SHOW COLUMNS FROM Attendance_Sheet
                       WHERE Field LIKE '{_year}-{_month}-%'
                       OR Field = 'Employee_Code'""")
    
        headers = [header[0] for header in cursor.fetchall()]

        if len(headers) < 2:
            tk.messagebox.showerror(message = 'Data with corresponding Date format\nwas not found', title = 'Error')
            return
        
        if all:

            headers.insert(1, 'First_Name')
            headers.insert(2, 'Last_Name')

            cursor.execute(f"""SELECT E.`{'`, `'.join(headers)}` FROM Attendance_Sheet A
                           JOIN Employee E
                           WHERE A.Employee_Code = E.Employee_Code""")
            datas = cursor.fetchall()

            if not any(datas):
                tk.messagebox.showerror(title = 'Error', message = 'No existing data was found')
                return
            
            headers[1] = 'Name'
            headers.pop(2)

            for data, index in zip(datas, range(len(datas))):

                data = list(data)
                data[1] = f'{data[1]} {data[2]}'
                data.pop(2)

                datas[index] = data

            read_att_datas(get_month_window, from_function, from_code, headers, datas)
        
        else:
            
            cursor.execute(f"""SELECT {', '.join(headers)} FROM Attendance_Sheet
                           WHERE Employee_Code = {code}""")
            datas = cursor.fetchone()

            if datas is None:
                tk.messagebox.showerror(title = 'Error', message = 'Data with corresponding Employee Code\nwas not found')
                return

            read_att_data(get_month_window, from_function, from_code, headers, datas)
    
    get_month_window = tk.Tk()
    get_month_window.title('Attendance Data')

    timeframe(get_month_window)

    frame = tk.Frame(get_month_window, relief = 'groove', bd = 5)
    frame.pack(padx = 5, pady = 5, fill = 'both')

    if not all and from_function != Employee:
        emp_code = tk.Entry(frame, width = 25)

    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    month = ttk.Combobox(frame, width = 25, values = months)
    year = ttk.Combobox(frame, width = 25, values = list(range(2020, datetime.datetime.now().year + 1)))

    labels = ['Employee Code', 'Month', 'Year'] if not all and from_function != Employee else ['Month', 'Year']
    widgets = [emp_code, month, year] if not all and from_function != Employee else [month, year]

    row, column = 0, 0

    for label, widget in zip(labels, widgets):
        
        Label = tk.Label(frame, text = f'{label} :', font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = column, padx = 5, pady = 5, sticky = 'ew')

        widget.grid(row = row + 1, column = column, padx = 5, pady = 5, sticky = 'ew')

        if label == 'Employee Code':
            Label.grid_configure(columnspan = 2)
            widget.grid_configure(columnspan = 2)
            column += 1

        column = column + 1 if column + 1 < 2 else 0
        row = row + 2 if column == 0 else row

    back_button = tk.Button(get_month_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    next_button = tk.Button(get_month_window, text = 'Proceed', command = next_func, padx = 10, pady = 10)

    back_button.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)
    next_button.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    hover(get_month_window)

    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(get_month_window)
    dark_theme(frame)

    get_month_window.mainloop()

def read_att_datas(from_window, from_function, from_code, headers, datas, page_count = 0):

    from_window.destroy()

    def back_func():
        read_att_datas_window.destroy()
        from_function(from_code)

    def next_func():
        read_att_datas(read_att_datas_window, from_function, from_code, headers, datas, page_count = page_count+1)

    def prev_func():
        read_att_datas(read_att_datas_window, from_function, from_code, headers, datas, page_count = page_count-1)

    read_att_datas_window = tk.Tk()
    read_att_datas_window.title('Attendance Datas')

    frame = tk.Frame(read_att_datas_window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    dark_theme(frame)

    for header, column in zip(headers, range(len(headers))):
        
        header_lab = tk.Label(frame, text = header[-2:] if header[-2:].isdigit() else header, 
                              font = ('Arial', 9, 'bold', 'underline'))
        header_lab.grid(row = 0, column = column, padx = 5, pady = 5, sticky = 'news') 

        if dark:
                header_lab.config(bg = '#112', fg = 'white')

    _datas = datas[page_count * 20::]

    data_count = 0

    while data_count < 20 and data_count < len(_datas):

        data = _datas[data_count]

        for column in range(len(data)):

            data_lab = tk.Label(frame, text = data[column])
            data_lab.grid(row = data_count + 1, column = column, padx = 2, pady = 3, sticky = 'news') 

            if dark:
                data_lab.config(bg = '#112', fg = 'white')

            if data[column] == 'A' or data[column] == 'P':

                data_lab.config(font = ('Arial', 9, 'bold'))
                data_lab.config(fg = '#3CB371' if data[column] == 'P' else '#CD5C5C')

        data_count += 1

    frame.grid_columnconfigure('all', weight = 1) 

    button_back = tk.Button(read_att_datas_window, text = 'Exit', command = back_func, padx = 10, pady = 10)
    
    button_next = tk.Button(read_att_datas_window, text = 'Next Page',  command = next_func, padx = 10, pady = 10)
    button_previous = tk.Button(read_att_datas_window, text = 'Previous Page',  command = prev_func, padx = 10, pady = 10)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)

    if page_count > 0:
        button_previous.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')

    if (page_count + 1) * 20 < len(datas) and len(_datas) > 20:
        button_next.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

    dark_theme(read_att_datas_window)

    read_att_datas_window.mainloop()

def read_att_data(from_window, to_function, to_code, headers, datas):

    from_window.destroy()
    
    def back_func():

        read_att_data_window.destroy()
        to_function(to_code)
    
    read_att_data_window = tk.Tk()
    read_att_data_window.title('Attendance Data')

    timeframe(read_att_data_window)

    cursor.execute(f'''SELECT First_Name, Last_Name FROM Employee
                   WHERE Employee_Code = {datas[0]}''')
    name = ' '.join(list(cursor.fetchone()))

    emp_frame = tk.LabelFrame(read_att_data_window, text = 'Employee Details', bd = 5, relief = 'groove')
    emp_frame.pack(padx = 5, pady = 5, fill = 'both')
    
    emp_details = ['Employee Code : ', datas[0], '|', 'Name : ', name]
    
    for data, column in zip(emp_details, range(5)):

        label = tk.Label(emp_frame, text = data)
        label.grid(row = 0, column = column, padx = 5, pady = 5, sticky = 'w')

        if ':' in str(data) or data == '|':
            label.config(font = ('Arial', 9, 'bold'))
            label.grid_configure(sticky = 'e' if data != '|' else 'ew')

    att_frame = tk.LabelFrame(read_att_data_window, text = 'Attendance Data', relief = 'groove', bd = 5)
    att_frame.pack(padx = 5, pady = 5, fill = 'both')

    row, column = 0, 0

    total_columns = (((len(headers[1:]) + 9 ) // 10) * 3 ) - 1
    
    for header, data in zip(headers[1:], datas[1:]):
        
        date = tk.Label(att_frame, text=f'{header} :', font=('Arial', 9, 'bold'))
        date.grid(row=row, column=column, padx=5, pady=5, sticky='e')

        stat = 'Present' if data == 'P' else 'Absent'
        
        status = tk.Label(att_frame, text=stat)
        status.grid(row=row, column=column + 1, padx=5, pady=5, sticky='w')

        if column + 3 < total_columns:
            sep = tk.Label(att_frame, text='|', font=('Arial', 9, 'bold'))
            sep.grid(row=row, column=column + 2, padx=5, pady=5, sticky='ew')

        row = row + 1 if row + 1 < 10 else 0
        column = column + 3 if row == 0 else column

    back_button = tk.Button(read_att_data_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    back_button.pack(padx = 5, pady = 5, fill = 'both', expand = True)

    emp_frame.grid_columnconfigure('all', weight = 1)
    att_frame.grid_columnconfigure('all', weight = 1)

    hover(read_att_data_window)

    dark_theme(read_att_data_window)
    dark_theme(emp_frame)
    dark_theme(att_frame)

    read_att_data_window.mainloop()

def read_messages(from_window, from_function, from_code, lower = True): 
    
    level = 'Admin' if not lower else 'Employee'

    cursor.execute(f"""SELECT Name, Position, Message_Reason, Message, To_Code, Message_Number
                   FROM Messages
                   WHERE To_Level = '{level}'""")
    message_datas = [data for data in cursor.fetchall() if from_code in eval(data[-2]) or from_code == eval(data[-2])]

    if not message_datas:
        tk.messagebox.showinfo(message = 'No New Messages', title = 'Inbox Empty')
        return
    
    from_window.destroy()

    terminate = False

    for data in message_datas:

        if terminate:
            
            from_function(from_code)
            break

        def back_func():

            nonlocal terminate

            terminate = True
            read_message_window.destroy()

        def next_func():

            data_lst = eval(data[-2])

            data_lst.remove(from_code)

            if data_lst:
                cursor.execute(f"""UPDATE Messages
                            SET To_Code = '{data_lst}'
                            WHERE Message_Number = {data[-1]}""")
                
            if not data_lst:
                cursor.execute(f"""DELETE FROM Messages
                            WHERE Message_Number = {data[-1]}""")
                
            connection.commit()
            
            read_message_window.destroy()
            
            if message_datas[-1] == data:
                tk.messagebox.showinfo(message = 'All Messages Have Been Read', title = 'All Messages Read')
                from_function(from_code)
            
            else:
                pass

        read_message_window = tk.Tk()
        read_message_window.title('Message')

        timeframe(read_message_window)

        from_frame = tk.LabelFrame(read_message_window, text = 'Message From', bd = 5, relief = 'groove')
        message_frame = tk.LabelFrame(read_message_window, text = 'Message', bd = 5, relief = 'groove')

        from_frame.pack(padx = 5, pady = 5, fill = 'both')
        message_frame.pack(padx = 5, pady = 5, fill = 'both')

        from_labels = ['Admin Name : ','Position : ', 'Message Reason : ', 'Message : ']

        for label, datum, row in zip(from_labels, data, range(4)):

            frame = from_frame if row < 2 else message_frame
            row = row - 2 if row > 1 else row

            Label = tk.Label(frame, text = label, font = ('Arial', 9, 'bold'))
            Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

            Data = tk.Label(frame, text = datum)
            Data.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

        button_back = tk.Button(read_message_window, text = 'Back', command = back_func, padx = 10, pady = 10)
        button_next = tk.Button(read_message_window, text = 'Draft', command = next_func, padx = 10, pady = 10)

        button_back.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')
        button_next.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

        dark_theme(read_message_window)
        dark_theme(from_frame)
        dark_theme(message_frame)

        from_frame.grid_columnconfigure('all', weight = 1)
        message_frame.grid_columnconfigure('all', weight = 1)

        hover(read_message_window)

        read_message_window.mainloop()

def read_appeals(from_window, from_function, from_code):

    cursor.execute(f"""SELECT First_Name, Last_Name, Position FROM Administrator
                   WHERE Administrator_Code = {from_code}""")
    ad_data = [(f'{data[0]} {data[1]}', data[2]) for data in cursor.fetchall()][0]

    cursor.execute(f"""SELECT From_Employee_Code, From_Name, From_Position, Appeal_Reason, Letter, Appeal_Number
                   FROM Appeals
                   WHERE To_Position = '{ad_data[1]}'""")
    
    appeals = cursor.fetchall()

    if not appeals:
        tk.messagebox.showinfo(title = 'Inbox Empty', message = 'No New Appeals')
        return
    
    from_window.destroy()

    terminate = False

    for appeal in appeals :

        if terminate:
            
            from_function(from_code)
            break

        def back_func():
             
             nonlocal terminate

             terminate = True
             read_appeal_window.destroy()

        def rej_acc_func(accept = True):

            var = 'Accept' if accept else 'Reject'
            msg = f'Your Appeal on {appeal[3]} has been rejected. Contact Administrators for Re-Consideration' if not accept else f'''
            Your Appeal on {appeal[3]} has been accepted'''
            
            cursor.execute(f"""DELETE FROM Appeals
                           WHERE Appeal_Number = {appeal[-1]}""")
            
            cursor.execute(f"""INSERT INTO Messages
                           (To_Code, To_Level, Administrator_Code, Name, Position, Message_Reason, Message)
                           VALUES
                           ({appeal[0]}, 'Employee', {from_code}, '{ad_data[0]}', '{ad_data[1]}', 'Appeal {var}ed',
                           '{msg}')""")
            
            connection.commit()

            read_appeal_window.destroy()

            if appeal == appeals[-1]:
                tk.messagebox.showinfo(message = 'All Appeals have been marked', title = 'Inbox Cleared')
                from_function(from_code)            

        def skip_func():
            read_appeal_window.destroy()

            if appeal == appeals[-1]:
                tk.messagebox.showinfo(message = 'All Appeals have been marked', title = 'Inbox Cleared')
                from_function(from_code)

        read_appeal_window = tk.Tk()
        read_appeal_window.title('Appeals')

        timeframe(read_appeal_window)

        from_frame = tk.LabelFrame(read_appeal_window, bd = 5, relief = 'groove', text = 'Appeal From')
        appeal_frame = tk.LabelFrame(read_appeal_window, bd = 5, relief = 'groove', text = 'Appeal')

        from_frame.pack(padx = 5, pady = 5, fill = 'both')
        appeal_frame.pack(padx = 5, pady = 5, fill = 'both')

        labels = ['Employee Code', 'Name', 'Position', 'Appeal Reason', 'Appeal']

        for label, data, row in zip(labels, appeal, range(5)):

            frame = from_frame if row < 3 else appeal_frame
            row = row - 3 if row > 2 else row

            Label = tk.Label(frame, text = f'{label} : ', font = ('Arial', 9, 'bold'))
            Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

            Data = tk.Label(frame, text = data)
            Data.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

        button_back = tk.Button(read_appeal_window, text = 'Back', command = back_func, padx = 10, pady = 10)
        button_rej = tk.Button(read_appeal_window, text = 'Reject', command = lambda : rej_acc_func(False), padx = 10, pady = 10)
        button_skip = tk.Button(read_appeal_window, text = 'Skip', command = skip_func, padx = 10, pady = 10)
        button_acc = tk.Button(read_appeal_window, text = 'Accept', command = rej_acc_func, padx = 10, pady = 10)

        button_back.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')
        button_rej.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')
        button_acc.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')
        button_skip.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

        dark_theme(read_appeal_window)
        dark_theme(from_frame)

        dark_theme(appeal_frame)

        from_frame.grid_columnconfigure('all', weight = 1)
        appeal_frame.grid_columnconfigure('all', weight = 1)

        hover(read_appeal_window)

        read_appeal_window.mainloop()

def draft_message(from_window, from_function, from_code, dept = False, lower = True, all = False):

    from_window.destroy()

    def back_func():
        draft_message_window.destroy()
        from_function(from_code)

    def next_func():
        
        if dept:
            _dept = department.get().title() if (department.get()).strip() else None
        
        elif lower and not all:
            _code = int(code_.get()) if (code_.get()).isdigit() else None

        _reason = reason.get() if (reason.get()).strip() else None
        _message = message.get('1.0', tk.END)

        datas = [_reason, _message]

        if dept or (not all and lower):
            datas.insert(0, _dept if dept else _code)

        if any(data is None for data in datas):
            tk.messagebox.showerror(title = 'Error', message = 'Incorrect Data Entered')
            return
        
        if dept:
            cursor.execute(f"""SELECT Employee_Code FROM Employee
                           WHERE Department = '{_dept}'""")    
            codes = [data[0] for data in cursor.fetchall()]
        
        if all and not dept:
            cursor.execute("SELECT Employee_Code FROM Employee" if lower else f"""
                           SELECT Administrator_Code FROM Administrator
                           WHERE Administrator_Code != {from_code}""")
            codes = [data[0] for data in cursor.fetchall()]

        cursor.execute(f"""SELECT First_Name, Last_Name, Position FROM Administrator
                       WHERE Administrator_Code = {from_code}""")
        datas = cursor.fetchone()

        name, position = f'{datas[0]} {datas[1]}', datas[2]

        if lower and not all:
            cursor.execute(f"""INSERT INTO Messages (To_Code, To_Level, Administrator_Code, Name, Position, Message_Reason, Message)
                            VALUES
                            ('{_code}', 'Employee', {from_code}, '{name}', '{position}', '{_reason}', '{_message}')""")
            connection.commit()
        
        elif dept or all:
            level = 'Admin' if not lower and not dept else 'Employee'
            cursor.execute(f"""INSERT INTO Messages (To_Code, To_Level, Administrator_Code, Name, Position, Message_Reason, Message)
                            VALUES
                            ('{codes}', '{level}', {from_code}, '{name}', '{position}', '{_reason}', '{_message}')""")
            connection.commit()

        tk.messagebox.showinfo(title = 'Success', message = 'Message Sent')

        draft_message_window.destroy()
        from_function(from_code)

    draft_message_window = tk.Tk()
    draft_message_window.title('Draft Message')

    timeframe(draft_message_window)

    frame = tk.Frame(draft_message_window, relief = 'groove', bd = 5)
    frame.pack(padx = 5,  pady = 5, fill = 'both')

    labels = ['Message Reason', 'Message']

    reason = tk.Entry(frame, width = 40)
    message = tk.Text(frame, width = 37, height = 10)

    widgets = [reason, message]

    if dept or (not all and lower):

        labels.insert(0, 'Department' if dept else 'Employee Code')

        if dept:

            cursor.execute(f'SELECT DISTINCT(Department) FROM Employee')
            depts = [dept[0] for dept in cursor.fetchall()]
            department = ttk.Combobox(frame, width = 40, values = depts)
            widgets.insert(0, department)
        
        elif lower and not all:
            code_ = tk.Entry(frame, width = 40)
            widgets.insert(0, code_)
    
    for label, widget, row in zip(labels, widgets, range(len(labels))):

        Label = tk.Label(frame, text = f'{label} :', font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx  =5, pady = 5, sticky = 'e')

        widget.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

    button_back = tk.Button(draft_message_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_next = tk.Button(draft_message_window, text = 'Draft', command = next_func, padx = 10, pady = 10)

    button_back.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')
    button_next.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

    frame.grid_columnconfigure('all', weight = 1)

    dark_theme(draft_message_window)
    dark_theme(frame)

    hover(draft_message_window)

    draft_message_window.mainloop()

def draft_appeals(from_window, emp_code):

    from_window.destroy()
    
    def back_func():
        
        draft_appeal_window.destroy()
        Employee(emp_code)

    def next_func():
        
        _position = position.get()
        _Appeal_reason = Appeal_reason.get()
        _letter = letter.get('1.0', tk.END)
        
        cursor.execute(f"""INSERT INTO Appeals (To_Position, From_Employee_Code, From_Name, From_Position, Appeal_Reason, Letter)
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
    
    draft_appeal_window = tk.Tk()
    draft_appeal_window.title('Draft Appeals')

    timeframe(draft_appeal_window)

    frame = tk.Frame(draft_appeal_window, bd = 5, relief = 'groove')
    frame.pack(padx = 5, pady = 5, fill = 'both')

    position = ttk.Combobox(frame, width = 50, values = positions)
    Appeal_reason = ttk.Combobox(frame, width = 50, values = reasons)
    letter = tk.Text(frame, width = 39, height = 10)

    Labels = [('Position :', position), ('Appeal Reason :', Appeal_reason), ('Letter : ', letter)]

    for label, row in zip(Labels, range(3)):

        Label = tk.Label(frame, text = label[0], font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

        label[1].grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

    button_back = tk.Button(draft_appeal_window, text = 'Back', command = back_func, padx = 20, pady = 20)
    button_next = tk.Button(draft_appeal_window, text = 'Compose', command = next_func, padx = 20, pady = 20)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)
    button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    frame.grid_columnconfigure('all', weight = 1)

    hover(draft_appeal_window)

    dark_theme(draft_appeal_window)
    dark_theme(frame)

    draft_appeal_window.mainloop()

def sal_position(from_window, ad_emp_code):

    cursor.execute("""SELECT Employee_Code, First_Name, Last_Name FROM Employee
                   WHERE Position OR Salary IS NULL""")
    
    datas = cursor.fetchall()

    if not any(tuple(datas)):
        
        tk.messagebox.showinfo(title = 'No Data Found', message = 'No new registration has been found')
        return
    
    from_window.destroy()
    
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
                new_sal_pos_window.destroy()
                return

            else:
                new_sal_pos_window.destroy()
                tk.messagebox.showinfo(title = 'All Done', message = 'All Data Has Been Added')
                Administrator(ad_emp_code)
                return

        def back_func():
            new_sal_pos_window.destroy()
            Administrator(ad_emp_code)
            return

        new_sal_pos_window = tk.Tk()
        new_sal_pos_window.title('Manage Salary and Position')

        timeframe(new_sal_pos_window)
        
        new_sal_pos_window.minsize(width = 400, height = 100)

        details = tk.LabelFrame(new_sal_pos_window, relief = 'groove', bd = 5, text = 'Existing Basic Details')
        details.pack(padx = 5, pady = 5, fill = 'both')

        Labels = 'Employee Code :', 'Name :'
        Values = data[0], f'{data[1]} {data[2]}'

        for Label, Value, row in zip(Labels, Values, range(2)):

            label = tk.Label(details, text = Label, font = ('Arial', 9, 'bold'))
            label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

            value = tk.Label(details, text = Value)
            value.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

        new_data = tk.LabelFrame(new_sal_pos_window, relief = 'groove', bd = 5, text = 'New Data')
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

        next_button = tk.Button(new_sal_pos_window, text = 'Next', command = next_func, padx = 10, pady = 10)
        next_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

        back_button = tk.Button(new_sal_pos_window, text = 'Back', command = back_func, padx = 10, pady = 10)
        back_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')

        hover(new_sal_pos_window)

        details.grid_columnconfigure('all', weight = 1)
        new_data.grid_columnconfigure('all', weight = 1)

        dark_theme(new_sal_pos_window)
        dark_theme(details)
        dark_theme(new_data)

        new_sal_pos_window.mainloop()

def new_position_or_salary(from_window, from_function, from_code, _position = False, increment = True):

    from_window.destroy()
    
    def next_func():
        
        _code = int(emp_code.get()) if emp_code.get().isdigit() else None
        if _position:
            position_ = position.get() if position.get().strip() else None
        _sal = int(salary.get()) if salary.get().isdigit() else None

        datas = [_code, _sal, position_] if _position else [_code, _sal]

        if any(data is None for data in datas):
            tk.messagebox.showerror(message = 'Incorrect data entered')
            return
        
        _sal = 1 + (_sal)/100 if not _position and increment else 1 - (_sal)/100 if not _position and not increment else _sal

        statement = f"""UPDATE Employee
                       SET Salary = Salary * {_sal}
                       WHERE Employee_Code = {_code}""" if not _position else f"""
                       UPDATE Employee
                       SET Salary = {_sal},
                       Position = '{position_}'
                       WHERE Employee_Code = {_code}"""

        cursor.execute(statement)

        connection.commit()

        tk.messagebox.showinfo(message = 'Data Updated Succesfully', title = 'Completed')
        
        update_sal_pos_window.destroy()
        from_function(from_code)

    def back_func():
        update_sal_pos_window.destroy()
        from_function(from_code)

    title = 'Promotion' if _position and increment else 'Demotion' if _position and not increment else 'Incrementation' if not _position and increment else 'Decrementation'

    update_sal_pos_window = tk.Tk()
    update_sal_pos_window.title(title)

    timeframe(update_sal_pos_window)

    frame = tk.Frame(update_sal_pos_window, bd = 5, relief = 'groove', height = 50)
    frame.pack(padx = 5, pady = 5, fill = 'both')

    sal_lab = 'New Salary : ' if _position else 'Increment [ in % ] : ' if increment else 'Decrement [ in % ]'
    labels = ['Employee Code : ', sal_lab, 'New Position : ']

    emp_code = tk.Entry(frame, width = 50)
    if _position:
        position = tk.Entry(frame, width = 50)
    salary = tk.Entry(frame, width = 50)

    widgets = [emp_code, salary, position] if _position else [emp_code, salary]

    for label, widget, row in zip(labels, widgets, range(len(widgets))):

        if not _position and label == 'New Position : ':
            continue

        Label = tk.Label(frame, text = label, font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

        widget.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

    frame.grid_columnconfigure('all', weight = 1)

    button_back = tk.Button(update_sal_pos_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_next = tk.Button(update_sal_pos_window, text = 'Update', command = next_func, padx = 10, pady = 10)

    button_back.pack(padx = 5, pady = 5, side = 'left', fill = 'both', expand = True)
    button_next.pack(padx = 5, pady = 5, side = 'right', fill = 'both', expand = True)

    hover(update_sal_pos_window)

    dark_theme(update_sal_pos_window)
    dark_theme(frame)

    update_sal_pos_window.mainloop()

def update_pf():

    if datetime.datetime.now().day == 1:

        cursor.execute('''UPDATE Employee
                       SET Provident_Fund = Provident_Fund + (Salary * 0.1)''')
        cursor.execute('''UPDATE Administrator
                       SET Provident_Fund = Provident_Fund + (Salary * 0.15)''')
        connection.commit()

def compose_email(from_window, from_function, from_code):

    from_window.destroy()

    def next_func():
        pass

    def back_func():
        email_window.destroy()
        from_function(from_code)

    def attachment():
        pass
    
    email_window = tk.Tk()
    email_window.title('Compose Email')

    # real time date and time packing
    
    timeframe(email_window)

    # function code

    from_details = tk.Frame(email_window, bd = 5, relief = 'groove')
    from_details.pack(padx = 5, pady = 5, fill = 'both')

    to_details = tk.Frame(email_window, bd = 5, relief = 'groove')
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

    attach = tk.Button(to_details, compound = 'left', text = 'Add Attachments', command = attachment, padx = 10, pady = 10)
    attach.grid(row = 5, column = 0, columnspan = 2, padx = 5, pady = 5, sticky = 'news')

    next_button = tk.Button(email_window, text = 'Next', command = next_func, padx = 10, pady = 10)
    next_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

    back_button = tk.Button(email_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    back_button.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')

    from_details.grid_columnconfigure('all', weight = 1)
    to_details.grid_columnconfigure('all', weight = 1)

    hover(to_details)
    hover(email_window)

    dark_theme(email_window)
    dark_theme(to_details)
    dark_theme(from_details)

    email_window.mainloop()

def delete(from_window, from_function, from_code, all = False, client = False, Att = False, Emp = True):

    from_window.destroy()
    
    def back_func():
        delete_window.destroy()
        from_function(from_code)

    def next_func():

        ad_code_ = int(ad_code.get()) if ad_code.get().isdigit() else None
        name_ = name.get().title() if name.get().strip() else None

        if not all:
            _code = int(code.get()) if code.get().isdigit() else None

        if any(data is None for data in [ad_code_, name_, _code if not all else 'None']):
            tk.messagebox.showerror(message = 'Incorrect data entered', title = 'Error')
            return

        cursor.execute(f"""SELECT Administrator_Code, First_Name, Last_Name FROM Administrator
                       WHERE Administrator_Code = {ad_code_}
                       AND First_Name = '{name_.split()[0]}'
                       AND Last_Name = '{name_.split()[1]}'""")
        
        if cursor.fetchone() is None:
            tk.messagebox.showerror(message = 'Incorrect data entered', title = 'Error')
            return

        if Att and all:

            cursor.execute(f'SHOW COLUMNS FROM {table}')
            headers = [data[0] for data in cursor.fetchall()]

            for header in headers:
                cursor.execute(f"""ALTER TABLE {table}
                               DROP COLUMN `{header}`""")
                
        elif not all and client and Emp:

            cursor.execute(f"""SELECT * FROM Client
                           WHERE Client_Code = {_code}""")
            
            if cursor.fetchone() is None:
                tk.messagebox.showerror(message = 'Entered code does not exist', title = 'Error')
                return

            cursor.execute(f"""DELETE FROM Client
                           WHERE Client_Code = {_code}""")

        elif not all and Emp:

            cursor.execute(f"""SELECT * FROM Employee
                           WHERE Employee_Code = {_code}""")
            
            if cursor.fetchone() is None:
                tk.messagebox.showerror(message = 'Entered code does not exist', title = 'Error')
                return

            cursor.execute(f"""DELETE FROM Employee
                           WHERE Employee_Code = {_code}""")
            
            cursor.execute(f"""DELETE FROM Attendance_Sheet
                           WHERE Employee_Code = {_code}""")
            
        elif all:

            table = 'Employee' if Emp else 'Client'
            cursor.execute(f"TRUNCATE {table}")

        connection.commit()

        delete_window.destroy()

        tk.messagebox.showinfo(message = 'Data Cleared', title = 'Successful')

        from_function(from_code)
    
    delete_window = tk.Tk()
    delete_window.title('Delete Data')

    timeframe(delete_window)

    frame = tk.Frame(delete_window, relief = 'groove', bd = 5)
    frame.pack(padx = 5, pady = 5, fill = 'both')

    Labels = ['Employee Code : ' if client and Emp else 'Administrator Code :', 'Name : ']

    ad_code = tk.Entry(frame, width = 25)
    name = tk.Entry(frame, width = 25)

    widgets = [ad_code, name]

    if (client or Emp) and not all:
        Labels.append('Client Code : ' if client else 'Employee Code : ')

        code = tk.Entry(frame, width = 25)
        widgets.append(code)

    for label, widget, row in zip(Labels, widgets, range(len(Labels))):

        Label = tk.Label(frame, text = label, font = ('Arial', 9, 'bold'))
        Label.grid(row = row, column = 0, padx = 5, pady = 5, sticky = 'e')

        widget.grid(row = row, column = 1, padx = 5, pady = 5, sticky = 'w')

    button_back = tk.Button(delete_window, text = 'Back', command = back_func, padx = 10, pady = 10)
    button_next = tk.Button(delete_window, text = 'Next', command = next_func, padx = 10, pady = 10)

    button_back.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'left')
    button_next.pack(padx = 5, pady = 5, fill = 'both', expand = True, side = 'right')

    dark_theme(delete_window)
    dark_theme(frame)

    frame.grid_columnconfigure('all', weight = 1)

    hover(delete_window)

    delete_window.mainloop()

title_page()
