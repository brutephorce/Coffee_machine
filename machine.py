import test1,test2,test3


'''
Assumptions:
1. Since practically its not possible to supply different beverage from same outlet (that is going to ruin the taste all the way), so we are proceeding with the assumption that the number of outlets would be exactly same as the number of diffrent beverages available in the machine. But still we have a hypothetical solution, we will serve 'n' items at a time and would consider that other outlets are inactive at that instance.


2. As mentioned that we have to make an indication whenever any ingredient is running low, so we are moving forward with the assumption that 20% of the initial amount stored would be regarded as 'running low' for any ingredient. And would be notified if the remaining amount of that ingredient is below that.


3. Since the beverage can be served only if the all ingredients are available and are available sufficiently, so even a single omission of any ingredient or insuffient available quantity of any single ingredient would terminate the order and would not let the order complete. Therefore, we would terminate that order on the very first instance of any unavailable item or insufficient amount of any item. There might be unavailable items as well as insufficient amount of item after that but we will focus only on the first instance of either of them.

'''


########################################################### Code starts here  #############################################################



class Machine:

    # Initialization of Machine class to reset values of every component
    def __init__(self, test):
        self.machine = test["machine"]

        # Initialize no. of outlets possible to run in parallel
        self.num_outlets = self.machine["outlets"]["count_n"]

        # Storing up total quantity of each ingredient available initially before executing any order
        self.total_quantity = self.machine["total_items_quantity"]

        # Storing up the individual requirement of ingredients for each beverage in order to complete the order successfully
        self.indiv_req = self.machine["beverages"]

        # Setting up 20% refilling limit for each ingredient. This would act as indicator to which ingredient is running lower than 20% of initial refillment.
        self.limit = {}
        for ingrd in self.total_quantity:
            self.limit[ingrd] = self.total_quantity[ingrd]*0.2

    def prepare(self, beverage):

        if beverage not in self.indiv_req:
            print("Beverage not available")
            return

        # variable to store nmbr of available and sufficient ingredients. This would finally represent the number of ingredients which were completely and sufficiently present in order to fulfil the beverage requirements.
        ingrd_count = 0

        # variable to store the ingredient which was insufficient while preparing the beverage
        insuff = None

        # variable to store the ingredient which was unavailable while preparing the beverage
        unavail = None

        # Lookup dictionary for keeping a track of the quantities of respective ingredients that were used in this preparation. This would also come handy when a particular ingredient is not available or is insufficient, we would add back all the ingredients quantities to self.total_quantity so that those ingredients could be used by other orders.
        usedup = {}

        # Iterating over the respective ingredients required to prepare this beverage
        for ingrd in self.indiv_req[beverage]:



            # If a certain ingredient is not available in the machine then exit the loop and store which ingredient is unavailable as 'unavail'.
            if ingrd not in self.total_quantity:
                unavail = ingrd
                break

            # If the ingredient is present...
            else:
                # Check whether the ingredient amount present is sufficient to complete this order. If no, exit the loop and store which ingredient is insufficient as 'insuff'.
                if self.total_quantity[ingrd] < self.indiv_req[beverage][ingrd]:
                    insuff = ingrd
                    break

                else:
                    # If the amount of this ingredient is sufficient, subtract the amount of ingredient required for this particular order from the amount of ingredient available in the machine. Also store the amount of ingredient used in 'usedup' in order to traceback any further ingredient unvailability or insufficiency. Also increase 'ingrd_count' by one, which means that this particular ingredient fulfilled the requirement completely for the beverage.

                    self.total_quantity[ingrd] -= self.indiv_req[beverage][ingrd]
                    usedup[ingrd] = self.indiv_req[beverage][ingrd]
                    ingrd_count += 1
                  
        # If all ingredients required for this beverage were available and in sufficient quantity then the order would be prepared successfully
        if ingrd_count == len(self.indiv_req[beverage]):
            print(beverage, "is prepared")


        else:
            # Now some of the items quantity might have been subtracted already from the self.total_quantity, we need to traceback them and add them up back so that other further orders could use these ingredients.
            for waste in usedup:
                self.total_quantity[waste] += usedup[waste]
            
            # Here if any of the ingredients might have been unavailable then that must have been stored in 'unavail'. We would print that unvailable item.
            if unavail:
                print(beverage, "cannot be prepared because",
                      unavail, "is not available")

            # Here if any of the ingredients might have been insufficient in quantity then that must have been stored in 'insuff'. We would print that insufficient item.
            if insuff:
                print(beverage, "cannot be prepared because item",
                      insuff, "is not sufficient")

        # Now we iterate over all the ingredients present in the machine once to check if any of them have gone below 20% of their initial level. If there are any, notify them.
        running_low=[]

        for item in self.total_quantity:
          if self.total_quantity[item] < self.limit[item]:
            running_low.append(item)
        
        if running_low:
          running_low=', '.join(running_low)
          print("ALERT - REFILLING REMINDER => Ingredients running low: ",running_low)
        else:
            print("All ingredients above their 20% mark")
        print()



    

    #  In order to take orders we will need to divide the orders in chunks of size n. So that n orders could be executed at a time.
    def take_orders(self,order_list,n):
      size=len(order_list)
      rounds=[]

      i=0
      while i<size:
        curr=[]
        for order_num in range(n):
          if order_list:
            curr.append(order_list.pop(0))
        rounds.append(curr)
        i+=n
    # Now all orders from order_list are divide in chunks of size<=n. Now we will execute the orders of each chunk one by one.
      for round in rounds:
        for beverage_num in range(len(round)):
          self.prepare(round[beverage_num])





########################################################### Code ends here  #############################################################








'''
Input format:

Input would be simply a list or orders that is to be given to the machine. For example:
If there are 6 customers and there orders are as:
1 - Green_tea
2 - Hot_coffee
3 - Hot_tea
4 - Green_tea
5 - Black_tea
6 - Hot_tea

So their order would be passed as a list parameter to the Machine class method 'take_orders' as ['Green_tea', 'Hot_coffee', 'Hot_tea', 'Green_tea', Black_tea', 'Hot_tea'] and also the number of outlets active at a time is passed as second parameter to the Machine class method 'take_orders'.



Output format:

Output would consist of two lines for each order, first line would determine state of the order that whether the order is successfully executed or is terminated in between due to ingredient insufficiency or unavailability. Second line would update about all the ingredient amount present in the machine. An alert refilling reminder would be issued if any ingredient quantity is below 20%.



'''


########################################################### test case 1  #############################################################

# To run this test case comment out test case 2 and test case 3 first

tea_coffee = Machine(test1.test1)
for order in test1.orders:
    print('#####################',order,'###################')
    tea_coffee.take_orders(test1.orders[order],tea_coffee.num_outlets)


########################################################### test case 2  #############################################################

# To run this test case comment out test case 1 and test case 3 first

soda = Machine(test2.test2)
for order in test2.orders:
    print('#####################',order,'###################')
    soda.take_orders(test2.orders[order],soda.num_outlets)


########################################################### test case 3  #############################################################

# To run this test case comment out test case 1 and test case 2 first

nutritional_drinks = Machine(test3.test3)
for order in test3.orders:
    print('#####################',order,'###################')
    nutritional_drinks.take_orders(test3.orders[order],nutritional_drinks.num_outlets)


#######################################################################################################################################
