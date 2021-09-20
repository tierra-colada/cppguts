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
