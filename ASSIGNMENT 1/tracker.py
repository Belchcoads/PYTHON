


#--------------------------------------------#

             # TASK 1 #

#--------------------------------------------#

print("=============================")
print("*****************************")
print("Welcome to Calorie Tracker")
print("*****************************")
print("=============================\n")

# functions of this code #

print("Tracks your daily calorie intakr")
print("You can know your total and avarage calorie intake")
print("We can use this code to meet our daily calorie intake goal\n")

#--------------------------------------------#

              # TASK 2 #
     # INPUT AND DATA COLLECTING #
 
#--------------------------------------------#


meal_names = []
calorie_values = []

conf = input("Would you like to add meals? (yes/no): ").lower()

if conf == "yes":
    meal_count = int(input("How many meals do you want to enter today? "))

    for i in range(meal_count):
        print("\nMeal", i + 1)
        meal = input("Enter meal name: ")
        calories = float(input("Enter calories for this meal: "))

        meal_names.append(meal)
        calorie_values.append(calories)

    print("\nYour meals and calories are saved")

else:
    print("\nOkay! Remember to add your meals later.")



#--------------------------------------------#

              # TASK 3 & 4 #
    # callorie calculation and warning #
 
#--------------------------------------------#


total_calories = sum(calorie_values)
average_calories = total_calories / len(calorie_values)

daily_limit = float(input("\nEnter your daily calorie limit: "))

print("\n----- Calorie Summary -----")
print("Total calories:", total_calories)
print("Average per meal:", average_calories)

if total_calories <= daily_limit:
    print("You are within your total calorie limit")
else:
    print("You have exceeded your daily calorie limit")

#--------------------------------------------#

              # TASK 5 #
     # PRINTING A FORMATTED OUTPUT #
 
#--------------------------------------------#

print("\nCalorie Report")
print("-----------------------------")

for i in range(len(meal_names)):
    print(meal_names[i], "=", calorie_values[i], "calories")

print("-----------------------------")
print("Total calories:", total_calories)
print("Average calories:", average_calories)


