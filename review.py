import threading

# Review 1

def add_to_list(value, my_list=[]):

    my_list.append(value)

    return my_list
'''
 Issue: In Python, default arguments are evaluated only once when the function
 is defined, not each time the function is called. In this case, using [] as 
 default argument, it will retain changes to its subsequent calls to the function.
'''
# Code to reproduce the issue for Review 1:
# Call the function multiple times
result1 = add_to_list(1)
result2 = add_to_list(2)
result3 = add_to_list(3)

print(result1)  # [1, 2, 3]
print(result2)  # [1, 2, 3]
print(result3)  # [1, 2, 3]

# Fix for Review1:
def add_to_list(value, my_list=None):
    if my_list is None:
        my_list = []
    my_list.append(value)

    return my_list
# Show the same piece of code without the issue of Review 1:
result1 = add_to_list(1)
result2 = add_to_list(2)
result3 = add_to_list(3)

print(result1)  # [1]
print(result2)  # [2]
print(result3)  # [2]


# Review 2

def format_greeting(name, age):

    return "Hello, my name is {name} and I am {age} years old."

'''
 Issue: The usage of f-string is wrong. The correct way to use it is to put "f" 
 before the double quotation mark
'''
# Code to reproduce the issue for Review 2:
res = format_greeting("Jason", 18)
# Can not pass the variable into string
print(res) # Hello, my name is {name} and I am {age} years old.

# Fix for Review2:
def format_greeting(name, age):

    return f"Hello, my name is {name} and I am {age} years old."

# Show the same piece of code without the issue of Review 2:
res = format_greeting("Jason", 18) 
print(res) # Hello, my name is Jason and I am 18 years old.

# Review 3

class Counter:

    count = 0

 

    def __init__(self):

        self.count += 1

 

    def get_count(self):

        return self.count
'''
 Issue: The count variable is a class attribute, shared among all
 instances of the class. In the constructor (__init__), 
 the self.count += 1 statement is trying to modify it,
 but it only creates a shadowed instance variable for each object,
 rather than incrementing the shared class attribute. This raised the 
 issue that the shared count is not being updated as intended
'''
# Code to reproduce the issue for Review 3:
c1 = Counter()
c2 = Counter()
print(c1.get_count())  # Outputs 1
print(c2.get_count())  # Outputs 1
print(Counter.count)   # Outputs 0 (shared class attribute is not being updated)

# Fix for Review3:
class Counter:
    count = 0  # Shared among all instances

    def __init__(self):
        Counter.count += 1  # Increment shared class attribute

    @classmethod
    def get_count(cls):
        return cls.count

# Show the same piece of code without the issue of Review 3:
c1 = Counter()
c2 = Counter()
print(c1.get_count())  # Outputs 2
print(c2.get_count())  # Outputs 2
print(Counter.count)   # Outputs 2 (shared class attribute is being updated)


# Review 4

import threading

 

class SafeCounter:

    def __init__(self):

        self.count = 0

 

    def increment(self):

        self.count += 1

 

def worker(counter):

    for _ in range(1000):

        counter.increment()

 

counter = SafeCounter()

threads = []

for _ in range(10):

    t = threading.Thread(target=worker, args=(counter,))

    t.start()

    threads.append(t)

 

for t in threads:

    t.join()

'''
 Issue: The increment method is not thread-safe. Without proper
 synchronization, multiple threads can access and modify the count
 attribute simultaneously. This can lead to a race condition and 
 incur incorrect count
'''
# Code to reproduce the issue for Review 4:
def worker(counter):
    for _ in range(10000000):  # Increment loop the increase the rate of issue
        counter.increment()


for test in range(5):  # Use multiple test
    counter = SafeCounter()
    threads = []

    for _ in range(10):  
        t = threading.Thread(target=worker, args=(counter,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # print final res
    expected = 10000000 * 10  # Expected res
    print(f"Test {test + 1}: Final count = {counter.count}, Expected = {expected}")
    # This is possible to occur
    if counter.count != expected:
        print("Error detected: Race condition occurred!")

# Fix for Review4:

class SafeCounter:
    def __init__(self):
        self.count = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:  # Ensures atomic operation
            self.count += 1


def worker(counter):
    for _ in range(1000):
        counter.increment()

# Show the same piece of code without the issue of Review 4:
def worker(counter):
    for _ in range(100000):  # Increment loop the increase the rate of issue
        counter.increment()


for test in range(5):  # Use multiple test
    counter = SafeCounter()
    threads = []

    for _ in range(10):  
        t = threading.Thread(target=worker, args=(counter,))
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

    # print final res
    expected = 100000 * 10  # Expected res
    print(f"Test {test + 1}: Final count = {counter.count}, Expected = {expected}")
    # Impossible to occur after fixing
    if counter.count != expected:
        print("Error detected: Race condition occurred!")

# Review 5

def count_occurrences(lst):

    counts = {}

    for item in lst:

        if item in counts:

            counts[item] =+ 1

        else:

            counts[item] = 1

    return counts

'''
 Issue: The =+ is a typo and should be +=. The typo 
 causes the program to incorrectly set counts[item] to +1
 every time, rather than incrementing it.
'''

# Code to reproduce the issue for Review 5:

l = [1,2,1,3,1,2]
print(count_occurrences(l)) # Expected {1: 3, 2: 2, 3: 1}, but outputs {1: 1, 2: 1, 3: 1}


# Fix for Review5:
def count_occurrences(lst):
    counts = {}
    for item in lst:
        if item in counts:
            counts[item] += 1  # Fix the typo
        else:
            counts[item] = 1
    return counts


# Show the same piece of code without the issue of Review 5:
l = [1,2,1,3,1,2]
print(count_occurrences(l)) # Outputs {1: 3, 2: 2, 3: 1} as expected