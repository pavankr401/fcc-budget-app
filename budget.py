import re
import math


class Category:

    def __init__(self, title):
        self.ledger = []
        self.title = title

    def __repr__(self):
        # heading will be 30 characters long
        heading = self.createHeading() + '\n'
        transactions = self.showTransactions()
        
        return heading + transactions
                

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        # we store negative amount in ledger
        # this method return true if withdraw happend otherwise false

        if (self.check_funds(amount)):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        else:
            return False

    def get_balance(self):
        # show the remaining balance
        funds = 0
        for transaction in self.ledger:
            funds += transaction["amount"]

        return funds

    def transfer(self, amount, category):
        # when transfer have enough funds
        # then withdraw happen in out category amount and description should be "Transfer to [Destination Budget Category]"
        # then deposit happen in other category with amount and description should be "Transfer from [Source Budget Category]"
        # if there are not enough funds, nothing should be added to either ledgers
        # this method return True if transfer took place and False otherwise
        if (self.check_funds(amount)):
            self.withdraw(amount, "Transfer to {}".format(category.title))
            category.deposit(amount, "Transfer from {}".format(self.title))

            return True
        else:
            return False

    def check_funds(self, amount):
        # it return False if the amount is greater than the balance of the budget category
        # return True otherwise
        # this method should be used by withdraw and transfer method
        funds = self.get_balance()

        if (funds < amount):
            return False
        else:
            return True
        
    def createHeading(self):
        heading = ""

        if (len(self.title) > 30):
            reg = re.search('.{30}', self.title)
            heading = reg.group()
            
        else:
            rem_title_len = 30 - len(self.title)
            left_side_stars = 0

            if (rem_title_len < 30):
                left_side_stars = rem_title_len // 2

            right_side_stars = 0

            if (left_side_stars < rem_title_len):
                right_side_stars = rem_title_len - left_side_stars

            heading = "{}{}{}".format(left_side_stars * '*', self.title, right_side_stars * '*')
            
        return heading
    
    def showTransactions(self):
        
        totalFunds = 0
        summary = ""
        
        for transaction in self.ledger:
            totalFunds += transaction["amount"]
            
            des = transaction["description"]
            chopped_des = ""
            if(len(des) > 23):
                chopped_des = re.search('.{0,23}', des).group()
            else:
                chopped_des = des + ' ' * (23 - len(des))
                
            amount = "{0:.2f}".format(transaction["amount"])
            if(len(amount) < 7):
                amount = ' ' * (7 - len(amount)) + amount
            
            summary += chopped_des + amount + '\n'
            
        summary += 'Total: ' + "{0:.2f}".format(totalFunds)
        
        return summary
            
            
            
            


def create_spend_chart(categories):

    # creating y axis    
    lines = ["Percentage spent by category"]
    for i in range(100, -10, -10):
        if(i == 0):
            lines.append("  " + str(i) + "|")
        elif(i != 100):
            lines.append(" " + str(i) + "|")
        else:
            lines.append(str(i) + "|")
            
    # plotting
    total_spent = 0
    total_spent_by_individually = []
    titles = []
    for category in categories:
        titles.append(category.title)
        # individually
        spent = 0
        for transaction in category.ledger:
            if(transaction["amount"] < 0):
                # converting negative amount to positive
                total_spent -= transaction["amount"]
                spent -= transaction["amount"]
        
        total_spent_by_individually.append(spent)
                
    # total spent by individually is converting to percentages according to total spent
    for i in range(len(total_spent_by_individually)):
        total_spent_by_individually[i] = math.floor((total_spent_by_individually[i] / total_spent) * 10 ) 
        
        
    # add zeros in graph
    for i in total_spent_by_individually:
        for j in range(11):
            if( i >= j):
                lines[len(lines) - j -1] += ' o '
            else:
                lines[len(lines) - j -1] += ' ' * 3
    
    result = ""
    for line in lines:
        if(line == lines[0]):
            result += line + '\n'
        else:
            result += line + ' \n'

        
    # creating x axis
    # add names in x axis
    result += "{}{}\n".format(" " * 4, "-" * ( len(lines[-1]) - 4 + 1 ))  
    
    # we found biggest title length and created that many empyth string
    # to achieve the vertical titles
    xaxis_titles = []
    max = None
    for i in titles:
        if(max is None or max < len(i)):
            max = len(i)
    
    for i in range(max):
        xaxis_titles.append(" "*4)
        
    for title in titles:
        for i in range(max):
            if(len(title) > i):
                xaxis_titles[i] += " {} ".format(title[i])
            else:
                xaxis_titles[i] += " "*3
   
    for line in xaxis_titles:
        if(xaxis_titles[-1] == line):
            result += line + " "
        else:
            result += line + ' \n'
    
    return result


# food = Category('Food')
# entertainment =  Category('Entertainment')
# business = Category("Buiseness")

# food.deposit(900, "deposit")
# entertainment.deposit(900, "deposit")
# business.deposit(900, "deposit")
# food.withdraw(105.55)
# entertainment.withdraw(33.40)
# business.withdraw(10.99)

# print(create_spend_chart([business, food, entertainment]))