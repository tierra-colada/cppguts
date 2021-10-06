# cppguts
If your project depends on some external C/C++ projects and 
you want to make some changes in external functions/methods 
and then copy/paste these changes automatically - this package may help you. 

There are two tools:
1) `editcpp` used to edit source code;
2) `dumpcpp` used to print some information about C/C++ translation units

We will discuss `editcpp` as it is the objective tool.

Same tool aimed at editing `python` files is also available as [pythonguts](https://github.com/tierra-colada/pythonguts)

**`editcpp` doesn't work with templates.**

## The idea behind `editcpp` tool
`editcpp` uses `libclang` to find function/method definition start/end lines in text file (`.c`, `.h`, `.hpp`, `.cpp` or whatever C/C++ extension). `libclang` parses each `dest.cpp` and `src.cpp` and everything that is
included by `#include` preprocessor directives. Then `editcpp` tool
selects all functions and methods defined in `dest.cpp` and `src.cpp` 
(it assumes that you know where old and new function/method definition resides) and tries to find matching functions/methods. After that `editcpp` copies function/method definition from `src.cpp` and pastes it to the `dest.cpp` while deleting old funcion/method definition.

<ins>To find common function `editcpp` checks:</ins>
* are they both _definitions?_
* are they both _const?_
* are they both _static?_
* are they both _vitual?_
* are they both _functions?_
* are they both _methods?_
* do they both have the same name?
* do they both have the same return type and arg types?
* do they both have the same semantic parent (classname)? (for methods only)

## Notes

* you are free to pass any clang argument after `editcpp` otions but don't pass file without flag to clang (as we usually do when using clang)
* if you parse files that includes non standard headers then you probably need to pass `-I<include_dir>` flag to clang to include directories;
* if you parse `C++` files then it may be necessary to pass `-std=c++03` (or higher) flag to inform clang that the file is `C++`;
* if your new function/method definition uses external types then
these types must be preliminary declared (not necessary to define them);

Remember that after `editcpp` finds common functions/methods
it will simply copy selected text lines from one file to another

## Example
original function/method definition file **dest.h**:
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

new function/method definition file **src.h**:
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
Run: 

`editcpp --src-file=src.h --dest-file=dest.h --oldfile-keep -std=c++03`

The `-std=c++03` tells the clang to parse the files as C++. Also you may need to use any other clang flags like `-I` to include directories that are required by the files.

`--oldfile-keep` (default) is used to keep the original file (it will be renamed by adding `_OLD_N` suffix). Otherwise use `--oldfile-delete` to delete the original file.

Another option is to run the test (though the test deletes all the generated files so you better take a look in `/tests` dir):

`python -m unittest cppguts.tests.test_cppguts`