# importing the dependencies
import tkinter as tk
from FM import *
from oop import *
from helper import *

# creating new object of User class
user = User()

############################ HELPER FUNCTION START #########################

def get_products_list():
    return [
        {"name": "Latte", "price": 39.99, "image": "latte.png"},
        {"name": "Cappuccino", "price": 99.99, "image": "cappuccino.png"},
        {"name": "Iced", "price": 41.99, "image": "iced.png"}
    ]

def get_other_products_list():
    return [
        {"name": "Biscuits", "price": 39.99, "image": "biscuits.png"},
        {"name": "Cream", "price": 44.99, "image": "cream.png"}
    ]

# Function to register new users
def show_error_message(message):
    # resetting the success label text
    success_label.config(text="")
    # Show an error message and clear the entries\
    error_label.config(text=message)
    username_entry.delete(0, tk.END)
    password_entry.delete(0, tk.END)

# changing the user object dynamically when the user_type changes
def set_user_type(user_type):
    global user
    if user_type == "Customer":
        user = Customer()
    elif user_type == "Staff":
        user = Staff()
    elif user_type == "Manager":
        user = Manager()

# function to set the logo for the window
def set_logo(window):
    window.iconbitmap("images/starbucks_logo.ico")

# Function to validate the login credentials
def validate_login_event(event):
    validate_login()

# function to validate the login information
def validate_login():
    # specifying there that the user is global user
    global user
    user = User()
    # getting the username and password values
    username = username_entry.get()
    password = password_entry.get()

    # if username and password are black
    if username == "" or password == "":
        show_error_message("Both fields are required!")
        username_entry.focus_set()
        return

    # search in the user file, if not found, show error message
    if not user.search(username):
        show_error_message("Invalid username or password")
        username_entry.focus_set()
        return

    data = user.search(username)
    if username == data[1] and password == data[2]:
        # getting the user type
        user_type = data[-1]
        set_user_type(user_type)
        user.login(username, password)
        # If the credentials match, close the login window and open the main window
        login_window.destroy()
        open_main_window()
        return
    # If no matching credentials are found, show an error message and clear the password entry
    show_error_message("Invalid username or password")
    username_entry.focus_set()

def update_record(first_name, last_name, username, emirate, telephone, email):
    user.set_fullname(first_name, last_name)
    user.set_username(username)
    user.set_emirate(emirate)
    user.set_telephone(telephone)
    user.set_email(email)

############################ HELPER FUNCTION END #########################

############################ MAIN WINDOW START #########################
# handling the topup button clicked
def handle_topup(amount, topup_error_label, topup, root):
    try:
        amount = int(amount)
        user.get_card().top_up(amount)
        topup.destroy()
        root.destroy()
        open_main_window()
    except:
        topup_error_label.config(text="Invalid amount")

# handling the change password button clicked
def handle_change_password_window(old_password, new_password, password_window_error_label, password_window, root):
    if user.check_password(old_password):
        user.set_password(new_password)
        password_window.destroy()
        root.destroy()
        open_main_window()
    else:
        password_window_error_label.config(text="Wrong password")

# handling the buy now button clicked
def handle_buy_now(selected_item, error_label, membership_window, root):
    price = None
    # dictionary that stores the price of the item
    for item in get_products_list():
        if selected_item == item["name"]:
            price = item["price"]
    if price == None:
        for other_item in get_other_products_list():
            if selected_item == other_item["name"]:
                price = other_item["price"]
    if float(price) > user.get_card().get_account_balance():
        error_label.config(text="Insufficient balance")
        return
    # placing the order
    user.place_order(selected_item, price)
    membership_window.destroy()
    root.destroy()
    open_main_window()

# handling the money transfer button clicked
def handle_transfer_money(account_id, username, amount, error_label, window, root):
    try:
        # trying to type cast the amount to float
        amount = float(amount)
    except:
        # if error occurs, show error message
        error_label.config(text="Invalid account")
    if user.search(username)[9] == account_id and user.get_card().money_transfer(amount, account_id) != False:
        window.destroy()
        root.destroy()
        open_main_window()
        return
    error_label.config(text="Invalid account")

# function to show topup window
def topup(root):
    # user.get_card().top_up()
    topup = tk.Toplevel(root)
    topup.title("Top-Up")
    topup.geometry("200x100")
    topup.resizable(0, 0)
    set_logo(topup)
    topup.grab_set()
    center(topup)
    tk.Label(topup, text="Enter amount").pack()
    # getting the amount
    topup_entry = tk.Entry(topup, bg="white")
    topup_entry.pack()
    topup_entry.focus_set()
    topup_error_label = tk.Label(topup, text="", fg="red")
    topup_error_label.pack()
    # button to confirm the topup
    tk.Button(topup, fg="black", text="Confirm", command=lambda:handle_topup(topup_entry.get(), topup_error_label, topup, root)).pack()
    topup.mainloop()

# handling the membership purchase
def membership_purchase(root):
    membership_window = tk.Toplevel()
    membership_window.title("Membership")
    membership_window.geometry("720x480")
    membership_window.resizable(0, 0)
    set_logo(membership_window)
    membership_window.grab_set()
    center(membership_window)

    tk.Label(membership_window, text="Coffee").grid(row=0, column=0, columnspan=3)

    from tkinter import PhotoImage

    # Create a list of products with names, prices, and image file paths
    products = get_products_list()
    items_to_buy = []

    # Iterate through the products and create a PhotoImage object for each image
    for product in products:
        product["image_obj"] = PhotoImage(file=f"./images/{product['image']}", width=120, height=150)

    # Combine the product information and the PhotoImage object
    for i, product in enumerate(products):
        img_label = tk.Label(membership_window, image=product["image_obj"])
        price_label = tk.Label(membership_window, text=f"Price: {product['price']}")
        caption_label = tk.Label(membership_window, text=product["name"])
        items_to_buy.append(product["name"])

        # use grid layout to place each image and its caption in a row
        img_label.grid(row=1, column=i, padx=5, pady=5)
        price_label.grid(row=3, column=i)
        caption_label.grid(row=4, column=i)


    tk.Label(membership_window, text="Also offerring").grid(row=5, column=0, columnspan=3)

    # create labels for each image with its caption
    other_products = get_other_products_list()

    # Iterate through the other_products and create a PhotoImage object for each image
    for other_product in other_products:
        other_product["image_obj"] = PhotoImage(file=f"./images/{other_product['image']}", width=120, height=150)

    # Combine the product information and the PhotoImage object
    for i, other_product in enumerate(other_products):
        img_label = tk.Label(membership_window, image=other_product["image_obj"])
        price_label = tk.Label(membership_window, text=f"Price: {other_product['price']}")
        caption_label = tk.Label(membership_window, text=other_product["name"])
        items_to_buy.append(other_product["name"])

        # use grid layout to place each image and its caption in a row
        img_label.grid(row=6, column=i, padx=5, pady=5)
        price_label.grid(row=7, column=i)
        caption_label.grid(row=8, column=i)

    buy_now_x = 550
    buy_now_y = 40
    tk.Label(membership_window, text=f"Your balance: {user.get_card().get_account_balance()}").place(x=buy_now_x, y=buy_now_y-20)
    tk.Label(membership_window, text="Buy Now").place(x=buy_now_x, y=buy_now_y)
    # user type drop down input
    user_type_label = tk.Label(membership_window, text="User Type")
    selected_item = tk.StringVar()
    selected_item.set("No item selected")
    tk.OptionMenu(membership_window, selected_item, *items_to_buy).place(x=buy_now_x, y=buy_now_y+30)
    error_label = tk.Label(membership_window, text="", fg="red")
    error_label.place(x=buy_now_x, y=buy_now_y+70)
    tk.Button(membership_window, fg="black", text="Place order", command=lambda:error_label.config(text="No item selected") if selected_item.get() == "No item selected" else handle_buy_now(selected_item.get(), error_label, membership_window, root)).place(x=buy_now_x, y=buy_now_y+100)

    membership_window.mainloop()

# managing the customers
def manage_customers(root, main_error_label):
    try:
        # trying to get all of the users
        data = user.get_all_customers()
    except:
        # show error if some exception occurs
        main_error_label.config(text=f"{user} can't manage Customer")
        return
    customers_window = tk.Toplevel()
    customers_window.geometry("720x480")
    customers_window.title("Customers")
    set_logo(customers_window)
    customers_window.grab_set()
    center(customers_window)

    # showing the heading of the customers
    tk.Label(customers_window, text="Username").grid(row=0, column=0)
    tk.Label(customers_window, text="First Name").grid(row=0, column=2)
    tk.Label(customers_window, text="Last Name").grid(row=0, column=3)
    tk.Label(customers_window, text="Emirate").grid(row=0, column=4)
    tk.Label(customers_window, text="Telephone").grid(row=0, column=5)
    tk.Label(customers_window, text="Email").grid(row=0, column=6)
    tk.Label(customers_window, text="Card ID").grid(row=0, column=7)
    tk.Label(customers_window, text="Account ID").grid(row=0, column=8)
    tk.Label(customers_window, text="Reward Points").grid(row=0, column=9)
    tk.Label(customers_window, text="User Type").grid(row=0, column=10)

    # nested for loop
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j == 1:
                continue
            label = tk.Label(customers_window, text=str(data[i][j]))
            label.grid(row=i+1, column=j)
    # delete all customers
    tk.Button(customers_window, fg="black", text="Delete all", font=("Arial", 16), bg="red", command=lambda:(user.delete_all_customers(), customers_window.destroy())).place(x=600, y=410)
    customers_window.mainloop()

# shared account functinalaties are not there
def add_shared_account(root):
    add_shared_account_window = tk.Toplevel()
    add_shared_account_window.geometry("300x200")
    add_shared_account_window.title("Add a Shared/Sub Account")
    set_logo(add_shared_account_window)
    add_shared_account_window.grab_set()
    center(add_shared_account_window)

    # getting the username and password of user
    tk.Label(add_shared_account_window, text="Username").pack()
    username = tk.Entry(add_shared_account_window, bg="white")
    username.pack()
    username.focus_set()
    tk.Label(add_shared_account_window, text="Password").pack()
    password = tk.Entry(add_shared_account_window, bg="white", show="*")
    password.pack()
    error_label = tk.Label(add_shared_account_window, fg="red").pack()
    # button to validate and check the user
    tk.Button(add_shared_account_window, fg="black", text="Add account", bg="black", command=lambda:(SharableAccount(user.get_card().get_account_id()), add_shared_account_window.destroy()) if username.get() and password.get() and not user.search(username.get()) else error_label.config(text="Invalid")).pack()

    add_shared_account_window.mainloop()

def transfer_money(root):
    tranfer_money_window = tk.Toplevel()
    tranfer_money_window.geometry("360x240")
    tranfer_money_window.title("Transfer Money")
    set_logo(tranfer_money_window)
    tranfer_money_window.grab_set()
    center(tranfer_money_window)

    # getting the funds receiver info
    tk.Label(tranfer_money_window, text="Account ID").pack()
    account_id_entry = tk.Entry(tranfer_money_window, bg="white")
    account_id_entry.pack()
    account_id_entry.focus_set()
    tk.Label(tranfer_money_window, text="Username").pack()
    username_entry = tk.Entry(tranfer_money_window, bg="white")
    username_entry.pack()
    tk.Label(tranfer_money_window, text="Amount").pack()
    amount_entry = tk.Entry(tranfer_money_window, bg="white")
    amount_entry.pack()
    error_label = tk.Label(tranfer_money_window, text="", fg="red")
    error_label.pack()
    tk.Button(tranfer_money_window, fg="black", text="Transfer Funds", command=lambda:handle_transfer_money(account_id_entry.get(), username_entry.get(), amount_entry.get(), error_label, tranfer_money_window, root) if account_id_entry.get() and username_entry.get() and amount_entry.get() and user.search(username_entry.get()) and user.get_card().get_account_balance() >= int(amount_entry.get()) else error_label.config(text="Invalid info")).pack()
    tranfer_money_window.mainloop()

def manage_staff(root, main_error_label):
    try:
        data = user.get_all_staff()
    except:
        main_error_label.config(text=f"{user} cannot manage Staff")
        return
    staff_window = tk.Toplevel()
    staff_window.geometry("720x480")
    staff_window.title("Staff")
    set_logo(staff_window)
    staff_window.grab_set()
    center(staff_window)

    tk.Label(staff_window, text="Username").grid(row=0, column=0)
    tk.Label(staff_window, text="First Name").grid(row=0, column=2)
    tk.Label(staff_window, text="Last Name").grid(row=0, column=3)
    tk.Label(staff_window, text="Emirate").grid(row=0, column=4)
    tk.Label(staff_window, text="Telephone").grid(row=0, column=5)
    tk.Label(staff_window, text="Email").grid(row=0, column=6)
    tk.Label(staff_window, text="Card ID").grid(row=0, column=7)
    tk.Label(staff_window, text="Account ID").grid(row=0, column=8)
    tk.Label(staff_window, text="Reward Points").grid(row=0, column=9)
    tk.Label(staff_window, text="User Type").grid(row=0, column=10)
    for i in range(len(data)):
        for j in range(len(data[i])):
            if j == 1:
                continue
            label = tk.Label(staff_window, text=str(data[i][j]))
            label.grid(row=i+1, column=j)
    tk.Button(staff_window, fg="black", text="Delete all", font=("Arial", 16), bg="red", command=lambda:(user.delete_all_staff(), staff_window.destroy())).place(x=600, y=410)
    staff_window.mainloop()

def change_password_window(root):
    password_window = tk.Toplevel()
    password_window.title("Change Password")
    password_window.geometry("200x200")
    password_window.resizable(0, 0)
    set_logo(password_window)
    password_window.grab_set()
    center(password_window)
    tk.Label(password_window, text="Old Password").pack()
    old_password_entry = tk.Entry(password_window, bg="white")
    old_password_entry.pack()
    old_password_entry.focus_set()
    tk.Label(password_window, text="New Password").pack()
    new_password_entry = tk.Entry(password_window, bg="white")
    new_password_entry.pack()
    password_window_error_label = tk.Label(password_window, text="", fg="red")
    password_window_error_label.pack()
    tk.Button(password_window, fg="black", text="Change", command=lambda:handle_change_password_window(old_password_entry.get(), new_password_entry.get(), password_window_error_label, password_window, root)).pack()
    password_window.mainloop()

# Function to open the main window after successful login
def open_main_window():
    # Create the main window and add widgets
    # Create the main window
    root = tk.Tk()
    root.title("Starbucks Account")

    # Set the window size and background image
    root.geometry("720x480")
    root.resizable(0, 0)
    set_logo(root)
    center(root)
    bg_image = tk.PhotoImage(file="./images/starbucks_bg.png")
    tk.Label(root, image=bg_image).place(x=0, y=0, relwidth=1, relheight=1)

    # Create labels for account info and records
    tk.Label(root, text="Transaction Records", font=("Arial", 16, "bold"), bg="#f7d09e").place(x=20, y=20)
    transactions = user.all_transactions()
    tk.Label(root, text="Product Name").place(x=20, y=55)
    tk.Label(root, text="Amount").place(x=120, y=55)
    tk.Label(root, text="Balance Left").place(x=220, y=55)
    for i in range(len(transactions)):
        if i == 5:
            break
        try:
            balance = int(transactions[i][1])
            if balance == 0:
                break
        except:
            pass
        for j in range(len(transactions[0])):
            if float(transactions[i][1]) < 0:
                tk.Label(root, text=str(transactions[i][j]), fg="red").place(x=20+j*100, y=80+i*30)
            else:
                tk.Label(root, text=str(transactions[i][j]), fg="green").place(x=20+j*100, y=80+i*30)

    # setting the x, y coordinates for account records section
    account_records_x = 20
    account_records_x2 = 130
    account_records_y = 230
    # main heading
    account_records_label = tk.Label(root, text="Account Records", font=("Arial", 16, "bold"), bg="#f7d09e")
    account_records_label.place(x=account_records_x, y=account_records_y)

    first_name = tk.StringVar(root, value=user.get_first_name())
    tk.Entry(root, bg="white", textvariable=first_name, width=12, font="Arial 12 bold").place(x=account_records_x, y=account_records_y+10+25)
    last_name = tk.StringVar(root, value=user.get_last_name())
    tk.Entry(root, bg="white", textvariable=last_name, width=12, font="Arial 12 bold").place(x=account_records_x+account_records_x2, y=account_records_y+10+25)

    tk.Label(root, text="Account ID:", font=("Arial", 10)).place(x=account_records_x, y=account_records_y+10+50)
    id = tk.StringVar(root, value=user.get_card().get_account_id())
    tk.Entry(root, bg="white", textvariable=id, font="Arial 10 bold", width=10).place(x=account_records_x+account_records_x2, y=account_records_y+10+50)
    tk.Label(root, text=str(user), font="Arial 10 bold").place(x=account_records_x+account_records_x2+76, y=account_records_y+10+50)

    tk.Label(root, text="Username:", font=("Arial", 10)).place(x=account_records_x, y=account_records_y+10+70)
    username = tk.StringVar(root, value=user.get_username())
    tk.Entry(root, bg="white", textvariable=username, font="Arial 10 bold").place(x=account_records_x+account_records_x2, y=account_records_y+10+70)
    tk.Label(root, text="Emirate:", font=("Arial", 10)).place(x=account_records_x, y=account_records_y+10+90)
    emirate = tk.StringVar(root, value=user.get_emirate())
    tk.Entry(root, bg="white", textvariable=emirate, font="Arial 10 bold").place(x=account_records_x+account_records_x2, y=account_records_y+10+90)
    tk.Label(root, text="Telephone:", font=("Arial", 10)).place(x=account_records_x, y=account_records_y+10+110)
    telephone = tk.StringVar(root, value=user.get_telephone())
    tk.Entry(root, bg="white", textvariable=telephone, font="Arial 10 bold").place(x=account_records_x+account_records_x2, y=account_records_y+10+110)
    tk.Label(root, text="Email:", font=("Arial", 10)).place(x=account_records_x, y=account_records_y+10+130)
    email = tk.StringVar(root, value=user.get_email())
    tk.Entry(root, bg="white", textvariable=email, font="Arial 10 bold").place(x=account_records_x+account_records_x2, y=account_records_y+10+130)

    # displaying the buttons
    tk.Button(root, fg="black", text="Change Password", bg="gray", command=lambda:change_password_window(root)).place(x=account_records_x, y=account_records_y+10+150)
    tk.Button(root, fg="black", text="Update Record", bg="green", command=lambda:update_record(first_name.get(), last_name.get(), username.get(), emirate.get(), telephone.get(), email.get())).place(x=account_records_x+account_records_x2, y=account_records_y+10+150)

    # trying to get the account information related to account balance
    try:
        balance = user.get_card().get_account_balance()
    except:
        balance = 0
    tk.Label(root, text=f"Balance: {balance}", font=("Arial", 18, "bold"), bg="#f7d09e").place(x=450, y=20)

    # trying to get the account information related to reward points
    try:
        reward_points = user.get_reward_points()
    except:
        # print("reward points error", user.__class__.__name__)
        reward_points = 0
    tk.Label(root, text=f"Reward Points: {reward_points}", font=("Arial", 10, "bold"), bg="#f7d09e").place(x=450, y=56)

    tk.Button(root, fg="black", text="Top-up Starbucks Account", font=("Arial", 14), bg="#2c3e50", command=lambda:topup(root),
                            padx=10, pady=5).place(x=450, y=100)

    # Create buttons for membership purchases and top-up
    tk.Button(root, fg="black", text="Membership Purchases", font=("Arial", 14), bg="#2c3e50", command=lambda:membership_purchase(root) if user.get_card().get_account_balance() >= 10 else main_error_label.config(text="Insufficient funds."),
                                padx=10, pady=5).place(x=450, y=150)

    tk.Button(root, fg="black", text="Add a Shared Account", font=("Arial", 14), bg="green", command=lambda:add_shared_account(root),
                            padx=10, pady=5).place(x=450, y=210)

    tk.Button(root, fg="black", text="Manage Customers", font=("Arial", 10), bg="#2c3e50", command=lambda:manage_customers(root, main_error_label),
                            padx=10, pady=5).place(x=450, y=270)

    tk.Button(root, fg="black", text="Manage Staff", font=("Arial", 10), bg="#2c3e50", command=lambda:manage_staff(root, main_error_label),
                            padx=10, pady=5).place(x=595, y=270)

    tk.Button(root, fg="black", text="Transfer Money", font=("Arial", 14), bg="#23238b", command=lambda:transfer_money(root),
                            padx=10, pady=5).place(x=450, y=320)

    # Create labels for error
    main_error_label = tk.Label(root, font=("Arial", 16, "bold"), bg="red")
    main_error_label.place(x=360, y=430)

    # exit button
    exit_button = tk.Button(root, fg="black", text="< Exit", font=("Arial", 10), bg="#ee3650", command=lambda:root.destroy(),
                            padx=5, pady=3)
    exit_button.place(x=20, y=430)

    # Run the main loop
    root.mainloop()
    # Add your main window widgets here

############################ MAIN WINDOW END #########################
# function to register a function
def register_user():
    global user
    username = registration_username_entry.get()
    password = registration_password_entry.get()
    first_name = first_name_entry.get()
    last_name = last_name_entry.get()
    emirate = emirate_entry.get()
    telephone = telephone_entry.get()
    email = email_entry.get()
    user_type = selected_user_type.get()

    if user_type == "No user type":
        show_error_message("No user type selected")
    elif username == "" or password == "" or first_name == "" or last_name == "" or emirate == "" or telephone == "" or email == "":
        show_error_message("Fill all fields")
    elif user.search(username):
        show_error_message("User already exists!")
    else:
        set_user_type(user_type)
        user.register(username, password, first_name, last_name, emirate, telephone, email)
        error_label.config(text="")
        success_label.config(text="User registered successfully!")
        username_entry.focus_set()
        registration_password_entry.delete(0, tk.END)
        registration_username_entry.delete(0, tk.END)
        first_name_entry.delete(0, tk.END)
        last_name_entry.delete(0, tk.END)
        emirate_entry.delete(0, tk.END)
        telephone_entry.delete(0, tk.END)
        email_entry.delete(0, tk.END)

# Create the login window and add widgets
login_window = tk.Tk()
login_wind_width = 480
login_wind_height = 360
login_window.title("Login")
login_window.geometry(f"{login_wind_width}x{login_wind_height}")
login_window.resizable(0, 0)
login_window.config(padx=10, pady=10)
center(login_window)
set_logo(login_window)
bg_image = tk.PhotoImage(file="./images/starbucks_login.png")
bg_label = tk.Label(login_window, image=bg_image)
bg_label.place(x=-8, y=-120, relwidth=2, relheight=2)

username_label = tk.Label(login_window, text="Username:")
username_entry = tk.Entry(login_window, bg="white")
username_entry.focus_set()
password_label = tk.Label(login_window, text="Password:")
password_entry = tk.Entry(login_window, bg="white", show="*")
login_button = tk.Button(login_window, fg="black", text="Login", command=validate_login)
success_label = tk.Label(login_window, fg="green", font="Arial 10 bold")
error_label = tk.Label(login_window, fg="red", font="Arial 10 bold")

# Bind the Enter Key to the window
login_window.bind('<Return>', validate_login_event)

registration_username_label = tk.Label(login_window, text="Username:")
registration_username_entry = tk.Entry(login_window, bg="white")
registration_password_label = tk.Label(login_window, text="Password:")
registration_password_entry = tk.Entry(login_window, bg="white", show="*")

# country drop down input
user_type_label = tk.Label(login_window, text="User Type")
user_type_list = ["Customer", "Staff", "Manager"]
selected_user_type = tk.StringVar()
selected_user_type.set("No user type")
user_type_dropdown = tk.OptionMenu(login_window, selected_user_type, *user_type_list)

first_name_label = tk.Label(login_window, text="First name:")
first_name_entry = tk.Entry(login_window, bg="white")
last_name_label = tk.Label(login_window, text="Last name:")
last_name_entry = tk.Entry(login_window, bg="white")
emirate_label = tk.Label(login_window, text="Emirate:")
emirate_entry = tk.Entry(login_window, bg="white")
telephone_label = tk.Label(login_window, text="Telephone:")
telephone_entry = tk.Entry(login_window, bg="white")
email_label = tk.Label(login_window, text="Email:")
email_entry = tk.Entry(login_window, bg="white")
registration_button = tk.Button(login_window, fg="black", text="Register", command=register_user)

# Grid the widgets on the login window
username_label.grid(row=0, column=0)
username_entry.grid(row=0, column=1)
password_label.grid(row=1, column=0)
password_entry.grid(row=1, column=1)
login_button.grid(row=2, column=1, sticky="E")

error_label.grid(row=3, column=0, columnspan=2)
success_label.grid(row=3, column=0, columnspan=2)

registration_username_label.grid(row=5, column=0)
registration_username_entry.grid(row=5, column=1)
registration_password_label.grid(row=6, column=0)
registration_password_entry.grid(row=6, column=1)
user_type_label.grid(row=7, column=0)
user_type_dropdown.grid(row=7, column=1, sticky="E")
first_name_label.grid(row=8, column=0)
first_name_entry.grid(row=8, column=1)
last_name_label.grid(row=9, column=0)
last_name_entry.grid(row=9, column=1)
emirate_label.grid(row=10, column=0)
emirate_entry.grid(row=10, column=1)
telephone_label.grid(row=11, column=0)
telephone_entry.grid(row=11, column=1)
email_label.grid(row=12, column=0)
email_entry.grid(row=12, column=1)
registration_button.grid(row=13, column=1, sticky="E")

# Start the tkinter event loop
login_window.mainloop()