menu={"pizza":100,"pasta":250,"biriyani":350}
print("Here is our menu-")
for i in menu:
    print(i," : rs "+str(menu[i]))
bill=0    
while True:
  
    order=input("what would you like to have:")
    
    if order=='stop':
        break
    elif order in menu:
        quantity=int(input(f"How many {order}'s you want:"))
        bill=bill+menu[order]
    else:
        print("sorry we dont serve that")        
