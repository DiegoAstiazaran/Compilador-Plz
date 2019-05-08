# Compilador-Plz


### Plz Quick Reference Guide

Welcome to the Plz Tutorial.

We want to give you a quick introduction to Plz. 

As of now, Plz has a basic programming language functionality. This means learning it is not that hard.

Let us start with variables. Declaring and Initializing variables.

Our language works in the following way:

The first statements must be (in any order):
* Declarations 
* Initializations
* Classes
* Subroutines

After that, once you start with your main block, you will no longer be able to declare or initialize variables, or create classes and subroutines.

Declaration:
``` 
  int a.
```

Initialization:
```
  int a = 3.
```

Pretty easy huh? Let's go with something a little more fun. 

Plz has several data types, including some non-primitive types such as arrays, matrices and lists. 
```
  int a.
  flt b.
  str c.
  int d(10).
  flt e(10)(10).
  list int f.
  
  int a = 9.
  flt b = 9.0.
  str c = "My name".
  int d(10) = {1,2,3,4,5,6,7,8,9,10}.
  flt e(2)(2) = {{1.0,2.0},{1.0,2.0}}.
  list int f = {1,2,3,4,5}.

```

We do have some fun stuff like for, when, and repeat while loops. 

For loop:

```
  int i.
  for i from 0 by 1 while i < 5:
    print: i end
  end
```
Which would produce:
```
0
1
2
3
4
5
```

The for loop can also have other iterating operations. 
```
  for i from 0 by +1 while i < 5:
  for i from 0 by -1 while i < 5:
  for i from 0 by *1 while i < 5:
  for i from 0 by /1 while i < 5:
  for i from 0 by 1 while i < 5:  (setting no operation defaults to +1) 
```
When loop
```
int a = 5.
when a > 0 repeat:
  print: a end
end

```

repeat while loop:
```
int i_a.
repeat:
  if 1 > 0:
    i_a = 2.
  end
  i_a = 3.
  print: i_a end
while True end
    
```

You can also declare and use classes and objects!
```
int a.

class Person:
  attributes:
    private int age.
    public str name.

  methods:
    sub Person(str s_name, int i_age):
      this.age = i_age.
      this.name = s_name.
    end

    public sub str get_name():
      return name.
    end
end

class Child under Person:
  attributes:
    public int a.
    public int b.
    public int c.
  
  methods:
    sub Child(int a, int b, int c):
      this.a = a.
      this.b = b.
      this.c = c.
      this.age = 2.
      this.name = "My name".
      this.numbers[0] = 1.
    end

    public sub int get_age():
      return this.age.
    end
end
```
To call attributes of a class, you use object@attribute. 
to call a method, you use object$method.
```

Person p1("John", 20 + 2).

sub void printDate():
  print: 'Today is Sunday' end
  print: p1$get_age() end
  print: p1$get_name() end
  print: p1@name end
end

Child c1(1,2,3).

print: c1$get_age() end

```
Lists also have some methods defined by default:
```
list int f = {1,2,3,4,5}.
```
* min() : Gets the minimum element on the list.
* max() : Gets the maximum element on the list.
* size() : Gets the size of the list.
* empty() : Checks if the list is empty.
* reverse() : Reverses the list
* print() : prints all the element on the list. 

* append(element): Adds to the end of the list the given element.
* remove(element) : Removes all instances found of the given element
* index(index): Gets the value of the element in given index on the list.
* count(element): Get the amount of times the element is on the list. 
* find(element): Gets the index if the element exists, returns -1 if it does not exists.
* pop(index) : pops the element on given index. If no argument is given, it popos the last elememt

* insert(element, index): inserts the elememt on given index. If the size is lower than the given index, the element will repeatedly be appended until the index is reached. 

# Extra notes:
* Dividing an integer by an integer will return an integer! So be careful!
* Declared variables have no default value!
