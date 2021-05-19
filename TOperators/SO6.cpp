#include <algorithm>
#include <iostream>
#include <vector>
#include "Z2.hpp"
#include "SO6.hpp"

SO6::SO6(){
    name = "Zero Matrix";
    for(int i=0; i<6; i++){
        for(int j=0; j<6; j++)
            arr[i][j]=Z2();
    }

    genLDE();
}

SO6::SO6(std::string n){
    name = n;
    //initializes all entries as 0
    for(int i=0; i<6; i++){
        for(int j=0; j<6; j++)
            arr[i][j]=Z2();
    }
    genLDE();
}

SO6::SO6(Z2 a[6][6], std::string n){
    name = n;
    //initializes SO6's entries according to a
    for(int i = 0; i<6; i++){
        for(int j = 0; j<6; j++)
            arr[i][j] = a[i][j];
    }
    genLDE();
}

SO6 SO6::operator*(SO6& other){
    //multiplies operators
    SO6 prod(name + other.getName());
    Z2 next;
    for(int i=0; i<6; i++){
        for(int j = 0; j<6; j++){
            for(int k = 0; k<6; k++){
                next = arr[i][k]*other(k,j);
                prod(i,j) += next;
            }
        }
    }
    prod.genLDE();
    return prod;
}


bool SO6::operator==(SO6& other){
    //checks for equality up to signed column permutations
    //based on Andrew's method

    //checking LDE
    if(LDE != other.getLDE())
        return(false);
    //checking if this^dagger * other is a generalized perm matrix
    Z2 entry;
    std::vector<int> cols{0,1,2,3,4,5};
    int i = 0;
    int j = 0;
    Z2 next;
    while(i<6){
        entry = Z2();
        //entry is the (i,col(j))th element of (*this)^dagger * other
        for(int k = 0; k<6; k++){
                next = arr[i][k]*other(cols[j],k);
                entry += next;
        }
        if(!(entry==Z2()||entry==Z2(1,0,0)||entry==Z2(-1,0,0)))
            return(false);
        else if(entry==Z2()&& j<cols.size()-1)
            j++;
        else{
            i++;
            cols.erase(cols.begin()+j);
            j=0;
        }
    }
    return(true);
}

void SO6::genLDE(){
    int maximum = 0;
    for(int i = 0; i<6; i++){
        for(int j = 0; j<6; j++){
            LDE = arr[i][j].getLDE();
            maximum = std::max(LDE,maximum);
        }
    }
    LDE = maximum;
}

std::ostream& operator<<(std::ostream& os, const SO6& m){
    for(int i = 0; i<6; i++){
        os << '[';
        for(int j = 0; j<6; j++)
            os << m(i,j)<<' ';
        os << "] \n";
    }
    os << "\n";
    return os;
}


