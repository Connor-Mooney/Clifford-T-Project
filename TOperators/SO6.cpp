#include <algorithm>
#include <iostream>
#include <vector>
#include "Z2.hpp"
#include "SO6.hpp"

SO6::SO6(){
    //initializes all entries as 0
    for(int i=0; i<6; i++){
        for(int j=0; j<6; j++)
            arr[i][j]=Z2();
    }
}

SO6::SO6(Z2 a[6][6]){
    //initializes SO6's entries according to a
    for(int i = 0; i<6; i++){
        for(int j = 0; j<6; j++)
            arr[i][j] = a[i][j];
    }
}

SO6 SO6::operator*(SO6& other){
    //multiplies operators
    SO6 prod;
    Z2 next;
    for(int i=0; i<6; i++){
        for(int j = 0; j<6; j++){
            for(int k = 0; k<6; k++){
                next = arr[i][k]*other(k,j);
                prod(i,j) += next;
            }
        }
    }
    return prod;
}

Z2& SO6::operator()(int i, int j){
    //returns the (i,j)th entry
    return arr[i][j];
}

const Z2& SO6::operator()(int i, int j) const{
    //returns the (i,j)th entry but for const
    return arr[i][j];
}

bool SO6::operator==(SO6& other){
    //checks for equality up to signed column permutations
    //based on Andrew's method
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


