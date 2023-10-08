import math

pi = math.pi

#Get patient's sex and height
while True:
    patient_sex = input("Enter Patient's Sex (M or F): ")
    if patient_sex != "M" and patient_sex != "F":
        print("Sorry, please use the values M or F only, please try again")
        continue
    else:
        break

while True:
    try:
        height = float(input("Enter Patient's Height (in cm): "))
    except ValueError:
        print("Sorry, the input must be a number, please try again")
        continue
    else:
        break

#Get patient's hip and waist circumeference using method 2
while True:
    try:
        waist_circumference = float(input("Enter Patient's waist circumference (in cm): "))
    except ValueError:
        print("Sorry, the input must be a number, please try again")
        continue
    else:
        break

while True:
    try:
        hip_circumference = float(input("Enter Patient's hip circumference (in cm): "))
    except ValueError:
        print("Sorry, the input must be a number, please try again")
        continue
    else:
        break

#Get patient's hip and waist radius and height to calculate weight using method 3
while True:
    try:
        waist_radius = float(input("Enter Patient's waist radius (in cm): "))
    except ValueError:
        print("Sorry, the input must be a number, please try again")
        continue
    else:
        break

while True:
    try:
        waist_height = float(input("Enter Patient's waist height (in cm): "))
    except ValueError:
        print("Sorry, the input must be a number, please try again")
        continue
    else:
        break

while True:
    try:
        hip_radius = float(input("Enter Patient's hip radius (in cm): "))
    except ValueError:
        print("Sorry, the input must be a number, please try again")
        continue
    else:
        break

while True:
    try:
        hip_height = float(input("Enter Patient's hip height (in cm): "))
    except ValueError:
        print("Sorry, the input must be a number, please try again")
        continue
    else:
        break

#Calculate waist and hip circumference for method 3
waist_circumference2 = 2*pi*math.sqrt(((waist_radius**2)+(waist_height**2))/2) 
hip_circumference2 = 2*pi*math.sqrt(((hip_radius**2)+(hip_height**2))/2)

#Check if male or female and perform corresponding calculations
if patient_sex == 'M':
    weight = (0.6*height) + (waist_circumference*0.785) + (hip_circumference*0.392) -137.432
    weight2 = (0.6*height) + (waist_circumference2*0.78) + (hip_circumference2*0.392) -137.4
elif patient_sex == 'F':
    weight = (0.4*height) + (waist_circumference*0.325) + (hip_circumference*0.836) -110.924
    weight2 = (0.4*height) + (waist_circumference2*0.325) + (hip_circumference2*0.836) -110.924

#Output results
print(f"\nPatient's weight using method 2: {weight}\n")	
print(f"\nPatient's weight using method 3: {weight2}\n")