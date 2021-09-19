# cppguts
If your C/C++ project depends on external C/C++ projects and 
you want to make some changes in external functions/methods 
and you would like to copy/paste these changes automatically 
then this package may help you. 

There are two tools:
1) `editcpp` used to edit source code;
2) `dumpcpp` used to print some information about C/C++ translation units

We will discuss `editcpp` as it is the objective tool.

**`editcpp` doesn't work with templates.**

##The idea behind `editcpp` tool
`editcpp` tool uses `libclang` to find function/method definitions.
`libclang` parses each `dest.cpp` and `src.cpp` and everything that is
included by `#include` preprocessor directives. Then `editcpp` tool
selects all functions and methods defined in `dest.cpp` and `src.cpp` 
(it skips any function/method defined in other file) and 
tries to find matching functions/methods. After that `editcpp` copies 
function/method definition from `src.cpp` and paste it to the `dest.cpp` 
while deleting old funcion/method definition.

<ins>To find common function `editcpp` checks:</ins>
* _are they both definitions?_
* _are they both const?_
* _are they both static?_
* _are they both vitual?_
* _are they both functions?_
* _are they both methods?_
* _do they both have the same name?_
* _do they both have the same return type and arg types?_
* _do they both have the same semantic parent (classname)? (for methods only)_

If your new function/method definition uses external types then
these types must be declared (not necessary to define them). 

**Remember that after `editcpp` finds common functions/methods
it will simply copy selected text lines from one file to another.** 

## Example
original function/method definitions file **dest.h**:
 ```cpp
#include <iostream>

// helper class that is used by the target class `Src`
class SrcPrivate {
public:
  SrcPrivate(){};

  void add(int v){
    val += v;
  }

  void substract(int v){
    val -= v;
  }

private:
  int val;
}

// target class
class Src {
  // method defined inside the class
  void add(SrcPrivate p, int v){
    p.add(v);
  }

// method defined outside the class
  void substract(SrcPrivate p, int v);

// we won't tuch this method
  void untouched_print(int v){
    std::cout << "The value is:\t" << v << std::endl;
  }
}

void Src::substract(SrcPrivate p, int v){
  p.substract(v);
}

// simple function
void foo(int &v){
  v--;
}

namespace ns {
  // function in namespace
  void bar(int &v){
    v++;
  }
}
```

new function/method definitions file **src.h**:
```cpp
class SrcPrivate;   // declare helper type

// target class
class Src {
  // NEW method definition inside class
  void add(SrcPrivate p, int v){

    p.add(v) + 10;

  }

  // NEW method definition ouside class
  void substract(SrcPrivate p, int v);
}

void Src::substract(SrcPrivate p, int v){
  p.substract(v) - 10;
}

// NEW simple function definition 
void foo(int &v){
  v -= 10;
}

// NEW function definition in namespace
namespace ns {
  void bar(int &v){
    v += 10;
  }
}
```
Run: `editcpp --source-file=src.h --dest-file=dest.h --oldfile-keep -std=c++17`

The `-std=c++17` is simply for illustration but you can pass any clang flag
for example `-I` to include directories that are required by the files.

`--oldfile-keep` is used to keep the original file (it will be renamed 
by adding `_OLD_N` suffix). Otherwise use `--oldfile-delete` to delete the 
original file.