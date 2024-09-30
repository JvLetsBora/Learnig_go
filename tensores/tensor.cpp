#include <iostream>
#include <vector>
#include <string>
#include <algorithm>


using namespace std;

class tensor
{
private:
    /* data */
public:
    tensor(/* args */);
    ~tensor();
};

tensor::tensor(/* args */)
{
}

tensor::~tensor()
{
}



int main()
{

    vector<int> v = {(1, 2), 3, 4, 5};
    vector<int> v2 = {(3, 4), 5, 6, 7};

    // sum vectors
    vector<int> v3;
    for (int i = 0; i < v.size(); i++)
    {
        v3.push_back(v[i] + v2[i]);
    }

    for (int i = 0; i < v3.size(); i++)
    {
        cout << v3[i] << endl;
    }

    // print result

    for (int i = 0; i < v.size(); i++)
    {
        cout << v[i] << endl;
    }

    

    return 0;
}
