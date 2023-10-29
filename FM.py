# File-Manager (FM)
import os

# global variables
DIR_NAME = "data"
DIR_NAME += "/"

if not os.path.exists(DIR_NAME):
    os.makedirs(DIR_NAME)

class FileManager:
    def __init__(self, filename="File-Manager.txt"):
        self.__filepath = DIR_NAME + filename
        with open(self.__filepath, "a") as f:
            pass

    def _get_filepath(self):
        return self.__filepath

    def add(self, first_value, second_value):
        with open(self.__filepath, "a") as f:
            f.write(f"{first_value}\t{second_value}\n")
    
    def search(self, first_value):
        with open(self.__filepath, "r") as f:
            for line in f:
                line = line.strip()
                fields = line.split("\t")
                if len(fields) == 2 and fields[0] == first_value:
                    return fields
        return False
    
    def delete(self, first_value):
        assert self.search(first_value)
        with open(self.__filepath, "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if first_value in line:
                del lines[i]
                break
        with open(self.__filepath, "w") as f:
            f.writelines(lines)
    
    def view_all(self):
        data = {}
        with open(self.__filepath, "r") as f:
            for line in f:
                line = line.strip()
                fields = line.split("\t")
                data[fields[0]] = fields[1]
        return data

class WebuserFM(FileManager):
    def __init__(self, filename="Webuser.txt"):
        super().__init__(filename)

    def register(self, username, password):
        if not super().search(username):
            return super().add(username, password)
        return False

    def login(self, username, password):
        data = super().view_all()
        try:
            if data[username].split(",")[0] == password:
                return True
        except:
            return False
    
    def search(self, username):
        fields = super().search(username)
        if len(fields) == 2:
            return fields[0]
        return False

class RecordsFM(FileManager):
    def __init__(self, filename="Records.txt"):
        super().__init__(filename)

    def add(self, membership_id, username, password, first_name, last_name, emirate, telephone, email, card_id, account_id, user_type, reward_points=0):
        combine = f"{username},{password},{first_name},{last_name},{emirate},{telephone},{email},{card_id},{account_id},{reward_points},{user_type}"
        super().add(membership_id, combine)

    def search(self, username):
        records = super().view_all()
        for key, value in records.items():
            values = value.split(",")
            if username == values[0]:
                return [key] + values
        return False

class MembershipAndRewardsFM(FileManager):
    def __init__(self, filename="Membership&Rewards.txt"):
        super().__init__(filename)

    def update_reward_points(self, reward_points):
        super().delete()

class ProductPurchasedFM(FileManager):
    def __init__(self, filename="Product-Purchased.txt"):
        super().__init__(filename)

    def activate_account(self, account_id):
        with open(super()._get_filepath(), "r") as f:
            lines = f.readlines()
        for line in lines:
            if account_id in line:
                return
        with open(super()._get_filepath(), "a") as f:
            f.write(account_id + "\t" + "zero,0,0\n")

    def add(self, account_id, product):
        with open(super()._get_filepath(), "r") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            if account_id in line:
                line = line.split("\t")
                lines[i] = account_id + "\t" + product + ";" + line[1]
                break
        with open(super()._get_filepath(), "w") as f:
            f.writelines(lines)

    def send_to(self, account_id, amount):
        account_details = self.search(account_id)
        if account_details:
            amount = int(amount)
            try:
                account_balance = float(account_details[0][2])
            except:
                print("FM line 129 error")
                return False
            product = f"Funds Transfer,{amount},{account_balance+amount}"
            self.add(account_id, product)
            return True
        return False

    def search(self, account_id):
        purchases = []
        with open(super()._get_filepath(), "r") as f:
            lines = f.readlines()
        for line in lines:
            line = line.split("\t")
            if account_id == line[0]:
                purchase = line[1].split(";")
                for field in purchase:
                    fields = field.split(",")
                    purchases.append(fields)
        return purchases
    
    def view_all(self):
        all_purchases = {}
        with open(super()._get_filepath(), "r") as f:
            lines = f.readlines()
        for line in lines:
            field = line.split("\t")
            all_purchases[field[0]] = self.search(field[0])
        return all_purchases