x = 10 
y = 3.5 
z = "10" 
print(x + y) 
print("x" + "z")

print(type(10)) 
print(type(3.5)) 
print(type("hello"))
print(type(True))

nums = [1, 2, 3, 4] 
nums.append(4) 
print(nums) 
nums[0] = 99 
print(nums)

x = "123" 
y = int(x) 
print(x, y)

a = 5 
b = 10 
print(a > b) 
print(a == 5)

light = input("Light color: ")

if light == "green":
    print("Go")
elif light == "yellow":
    print("Slow down")
else:
    print("Stop")


for i in range(1, 6): 
    print(i)

count = 0 
while count < 5: 
    print(count) 
    count += 1
    
for i in range(1, 4): 
    if i % 2 == 0: 
        print(i, "is even") 
    else: 
        print(i,"is odd")

