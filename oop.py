
from helper import *
from FM import *

global limit
# labda to dhabe the 
ID_LENGTH = 5

class Account:
    def __init__(self):
        self._productPurchasedFM = ProductPurchasedFM()
        self.__id = generate_random_string(ID_LENGTH)
        while self._productPurchasedFM.search(self.__id):
            self.__id = generate_random_string(ID_LENGTH)

    def get_account_id(self):
        return self.__id

    def set_account_id(self, account_id):
        self.__id = account_id
    
class SharableAccount(Account):
    def __init__(self, parent_id):
        super().__init__()
        self.__parent_id = parent_id

    def get_parent_id(self):
        return self.__parent_id
    
    def set_parent_id(self, parent_id):
        self.__parent_id = parent_id
    
    def withdraw(self, amount):
        pass

    def deposit(self, amount):
        pass

    def transfer(self, amount):
        pass

class Balance:
    def __init__(self, balance=0):
        self.__id = generate_random_string()
        self.__balance = balance

    def get_balance(self):
        return float(self.__balance)
    
    def set_balance(self, balance):
        assert balance >= 0
        self.__balance = balance
    
    def add_money(self, amount):
        assert amount > 0
        self.__balance += amount
        return self.__balance
    
    def deduct_money(self, amount):
        assert amount > 0
        self.__balance -= amount
        return self.__balance
    
class FamilyAccount(Account):
    def __init__(self):
        super().__init__()
        self.__balance = Balance()
        self.__sub_accounts = []

    def withdraw(self, amount, selected_item="Purchased"):
        assert amount > 0
        self.__balance.deduct_money(amount)
        product = f"{selected_item},-{amount},{self.__balance.get_balance()}"
        self._productPurchasedFM.add(super().get_account_id(), product)
        return self.__balance.get_balance()
    
    def deposit(self, amount, source="Top-Up"):
        assert amount > 0
        self.__balance.add_money(amount)
        product = f"{source},{amount},{self.__balance.get_balance()}"
        self._productPurchasedFM.add(super().get_account_id(), product)
        return self.__balance.get_balance()
    
    def get_balance(self):
        return self.__balance.get_balance()
    
    def set_balance(self, balance):
        assert balance >= 0
        self.__balance.set_balance(balance)
    
    def transfer(self, amount, receiver_id):
        assert float(amount) > 0
        if self._productPurchasedFM.send_to(receiver_id, amount) == False:
            return False
        self.withdraw(amount, "Funds Transfer")
        return self.__balance
    
class SmilesCard:
    def __init__(self, account=FamilyAccount()):
        self.__membershipAndRewardsFM = MembershipAndRewardsFM()
        self.__id = generate_random_string()
        while self.__membershipAndRewardsFM.search(self.__id):
            self.__id = generate_random_string()
        self.__account = account

    def get_id(self):
        return self.__id

    def set_id(self, id):
        self.__id = id
    
    def get_account_id(self):
        return self.__account.get_account_id()
    
    def set_account_id(self, account_id):
        self.__account.set_account_id(account_id)
    
    def get_account_balance(self):
        return self.__account.get_balance()
    
    def set_account_balance(self, balance):
        assert balance >= 0
        self.__account.set_balance(balance)

    def top_up(self, amount):
        assert amount > 0
        self.__account.deposit(amount)
        return self.get_account_balance()

    def pay(self, amount, selected_item="Purchased"):
        assert int(amount) > 0
        self.__account.withdraw(amount, selected_item)
        return self.get_account_balance()
    
    def money_transfer(self, amount, receiver_id):
        assert int(amount) > 0
        if self.__account.transfer(amount, receiver_id):
            return self.get_account_balance()
        return False

class User:
    def __init__(self, username="user", password="user", first_name="Reem", last_name="Alkatheeri", emirate="", telephone="", email=""):
        self.__username = username if username else "user"
        self.__password = password if password else "user"
        self.__first_name = first_name if first_name else "Reem"
        self.__last_name = last_name if last_name else "Alkatheeri"
        self.__emirate = emirate if emirate else "default"
        self.__telephone = telephone if telephone else "+971 ****"
        self.__email = email if email else "abc@zu.uae"
        self.__membership_id = generate_random_string(ID_LENGTH)
        self.__card = SmilesCard()
        self._webuserFM = WebuserFM()
        self._recordsFM = RecordsFM()
        self._membershipAndRewardsFM = MembershipAndRewardsFM()
        self._productPurchasedFM = ProductPurchasedFM()
    
    def update_record(self, username):
        self._webuserFM.delete(self.__username)
        self._recordsFM.delete(self.__username)
        self._webuserFM.add(username, self.__password)
        self._recordsFM.add(self.__membership_id, username, self.__password, self.__first_name, self.__last_name, self.__emirate, self.__telephone, self.__email, self.__card.get_id(), self.__card.get_account_id(), type(self).__name__)

    def get_membership_id(self):
        return self.__membership_id
    
    def set_membership_id(self, membership_id):
        self.__membership_id = membership_id
        self.update_record(self.__username)

    def get_username(self):
        return self.__username
    
    def set_username(self, username):
        if username:
            self.update_record(username)
            self.__username = username

    def get_password(self):
        return self.__password
    
    def set_password(self, password):
        if password:
            self.__password = password
            self.update_record(self.__username)

    def check_password(self, password):
        return password == self.__password

    def get_fullname(self):
        return self.__first_name + " " + self.__last_name
    
    def get_first_name(self):
        return self.__first_name
    
    def get_last_name(self):
        return self.__last_name
    
    def set_fullname(self, first_name, last_name):
        if first_name:
            self.__first_name = first_name
            self.update_record(self.__username)
        if last_name:
            self.__last_name = last_name
            self.update_record(self.__username)

    def get_emirate(self):
        return self.__emirate
    
    def set_emirate(self, emirate):
        if emirate:
            self.__emirate = emirate
            self.update_record(self.__username)

    def get_telephone(self):
        return self.__telephone
    
    def set_telephone(self, telephone):
        if telephone:
            self.__telephone = telephone
            self.update_record(self.__username)

    def get_email(self):
        return self.__email
    
    def set_email(self, email):
        if email:
            self.__email = email
            self.update_record(self.__username)

    def search(self, username):
        return self._recordsFM.search(username)
    
    def all_transactions(self):
        data = self._productPurchasedFM.view_all()
        return data[self.__card.get_account_id()]

    def get_card(self):
        return self.__card

    def login(self, username, password):
        if self._webuserFM.login(username, password):
            user = self.search(username)
            self.__membership_id = user[0]
            self.__username = user[1]
            self.__password = user[2]
            self.__first_name = user[3]
            self.__last_name = user[4]
            self.__emirate = user[5]
            self.__telephone = user[6]
            self.__email = user[7]
            self.__card.set_id(user[8])
            self.__card.set_account_id(user[9])
            balance = self._productPurchasedFM.search(self.__card.get_account_id())[0][2]
            self.__card.set_account_balance(float(balance))
            return True
        return False
    
    def register(self, username, password, first_name, last_name, emirate, telephone, email, reward_points=0):
        if self.search(username):
            return
        while self._recordsFM.search(self.__membership_id):
            self.__membership_id = generate_random_string(ID_LENGTH)
        self.__username = username
        self.__password = password
        self.__first_name = first_name
        self.__last_name = last_name
        self.__emirate = emirate
        self.__telephone = telephone
        self.__email = email
        account_id = self.__card.get_account_id()
        self._productPurchasedFM.activate_account(account_id)
        self._recordsFM.add(self.__membership_id, self.__username, self.__password, self.__first_name, self.__last_name, self.__emirate, self.__telephone, self.__email, self.__card.get_id(), account_id, type(self).__name__, reward_points)
        self._webuserFM.register(self.__username, self.__password)

class Customer(User):
    def __init__(self, username="user", password="user", first_name="Reem", last_name="Alkatheeri", emirate="", telephone="", email=""):
        super().__init__(username, password, first_name, last_name, emirate, telephone, email)
        self.__membershipAndRewardsFM = MembershipAndRewardsFM()
        self.__reward_points = 0
    
    def get_reward_points(self):
        return self.__reward_points
    
    def set_reward_points(self, points):
        assert points > 0
        self.__reward_points = points
    
    def add_reward_points(self, points):
        if points > 0:
            self.__reward_points += points
        return self.__reward_points
    
    def deduct_reward_points(self, points):
        if points > 0 and points < self.__reward_points:
            self.__reward_points -= points
        return self.__reward_points
    
    def place_order(self, selected_item, amount):
        amount = int(amount) - self.cal_discount(amount)
        super().get_card().pay(amount, selected_item)
        self.add_reward_points(amount)
        self._membershipAndRewardsFM.delete(super().get_membership_id())
        self._membershipAndRewardsFM.add(super().get_membership_id(), self.__reward_points)
    
    def login(self, username, password):
        assert super().login(username, password)
        # user = super().search(username)
        data = self.__membershipAndRewardsFM.search(super().get_membership_id())
        self.__reward_points = float(data[1])

    def register(self, username, password, first_name, last_name, emirate, telephone, email):
        self.__membershipAndRewardsFM.add(super().get_membership_id(), self.__reward_points)
        return super().register(username, password, first_name, last_name, emirate, telephone, email, self.__reward_points)

    def cal_discount(self, amount):
        amount = int(amount)
        assert amount > 0
        discount_percentage = 0
        if self.__reward_points >= 1000:
            discount_percentage = 20
        elif self.__reward_points >= 500:
            discount_percentage = 10
        elif self.__reward_points >= 300:
            discount_percentage = 5
        return amount * discount_percentage / 100
    
    def __str__(self):
        return "Customer"
    
class Employee(User):
    def __init__(self, job_title="waiter", username="user", password="user", first_name="Reem", last_name="Alkatheeri", emirate="", telephone="", email=""):
        super().__init__(username, password, first_name, last_name, emirate, telephone, email)
        self.__employee_id = generate_random_string(ID_LENGTH)
        self.__job_title = job_title
        self.__discount = 15
        self.__customers = []

    def get_employee_id(self):
        return self.__employee_id
    
    def get_job_title(self):
        return self.__job_title
    
    def set_job_title(self, job_title):
        if job_title:
            self.__job_title = job_title

    def login(self, username, password):
        assert super().login(username, password)
        user = super().search(username)
        self.__employee_id = user[8]
        self.set_job_title(user[9])

    def get_discount(self, amount):
        discount_amount = 0
        if amount > 0:
            discount_amount = amount * self.__discount
        return discount_amount
    
    def set_discount(self, discount):
        assert discount >= 0
        self.__discount = discount
    
    def get_customers(self):
        return self.__customers
    
    def search_customer(self, customer_id):
        for customer in self.__customers:
            if customer.id == customer_id:
                return customer
    
    def modify_customer(self, customer_id):
        customer = self.search_customer(customer_id)
        return customer
    
    def get_all_customers(self):
        data = [i.split(",") for i in self._recordsFM.view_all().values()]
        customers = []
        for customer in data:
            if customer[-1] == "Customer":
                customers.append(customer)
        return customers
    
    def delete_all_customers(self):
        users = self.get_all_customers()
        for user in users:
            self._recordsFM.delete(user[0])
    
    def place_order(self, selected_item, amount):
        amount = int(amount) - int(amount) * self.__discount / 100
        super().get_card().pay(amount, selected_item)
    
class Staff(Employee):
    def __init__(self, employee_id="324", job_title="cook", username="user", password="user", first_name="Reem", last_name="Alkatheeri", emirate="", telephone="", email=""):
        super().__init__("Staff", username, password, first_name, last_name, emirate, telephone, email)
    
    def __str__(self):
        return "Staff"

class Manager(Employee):
    def __init__(self, employee_id="324", job_title="sales manager", username="user", password="user", first_name="Reem", last_name="Alkatheeri", emirate="", telephone="", email=""):
        super().__init__("Manager", username, password, first_name, last_name, emirate, telephone, email)
        super().set_discount(25)
        self.__staff_members = []

    def get_staff_members(self):
        return self.__staff_members
    
    def search_staff(self, staff_id):
        for staff in self.__staff_members:
            if staff.id == staff_id:
                return staff
    
    def modify_staff(self, staff_id, new_staff):
        old_staff = self.search_customer(staff_id)
        if old_staff:
            self.__staff_members.remove(old_staff)
            self.__staff_members.append(new_staff)
        return new_staff
    
    def delete_a_customer(self, customer_id):
        customer = self.search_customer(customer_id)
        if customer:
            self.__customers.remove(customer)
        return customer

    def delete_a_staff(self, staff_id):
        staff = self.search_customer(staff_id)
        self.__staff_members.remove(staff)
        return staff

    def delete_all_staff(self):
        users = self.get_all_staff()
        for user in users:
            self._recordsFM.delete(user[0])

    def delete_all(self):
        super().delete_all_customers()
        self.delete_all_staff()
    
    def get_all_staff(self):
        data = [i.split(",") for i in self._recordsFM.view_all().values()]
        customers = []
        for customer in data:
            if customer[-1] == "Staff":
                customers.append(customer)
        return customers
    
    def __str__(self):
        return "Manager"