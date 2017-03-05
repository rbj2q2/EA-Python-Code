#include <iostream>
#include <stdlib.h>

using namespace std;

int main(int argc, char* argv[])
{
  if (argc < 2)
  {
    cout << "Usage:\n";
    cout << "\tHelloEC <configFile>" << endl;
    exit(EXIT_FAILURE);
  }

  cout << "Hello, EC!" << endl;
  cout << "I'm using the configuration file: " << argv[1] << endl;
  return 0;
}
