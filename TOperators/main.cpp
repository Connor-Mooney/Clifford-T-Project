#include <algorithm>
#include <iostream>
#include <vector>
#include "Z2.hpp"
#include "SO6.hpp"

SO6 tMatrix(int i, int j){
    SO6 t;
    int sign;
    if((i+1==j&&i<=4&&i>=0)||(j+1==i&&j<=4&&j>=0))
        sign = 1;
    else
        sign = -1;
    for(int k=0; k<6; k++){
        t(k,k) = Z2(1,0,0);
    }
    t(i,i) = Z2(0,1,1);
    t(i,j) = Z2(0,-sign, 1);
    t(j,i) = Z2(0, sign, 1);
    t(j,j) = Z2(0,1,1);
    return(t);
}

bool containedIn(SO6 (&arr)[15], SO6& entry){
    for(SO6 item : arr){
        if(entry == item){
            return(true);
        }
    }
    return(false);
}

bool containedIn(std::vector<SO6>& v, SO6& entry){
    for(SO6 item: v){
        if(entry == item){
            return(true);
        }
    }
    return(false);
}

int main(){
    //generating list of T matrices
    SO6 ts[15];
    for(int i = 0; i<15; i++){
        if(i<5)
            ts[i] = tMatrix(0,i+1);
        else if(i<9)
            ts[i] = tMatrix(1, i-3);
        else if(i<12)
            ts[i] = tMatrix(2, i-6);
        else if(i<14)
            ts[i] = tMatrix(3, i-8);
        else
            ts[i] = tMatrix(4,5);
    }
    std::vector<SO6> t2;
    SO6 prod;
    for(int i = 0; i<15; i++){
        for(int j = 0; j<15; j++){
            prod = ts[i]*ts[j];
            if((!containedIn(ts, prod))&&(!containedIn(t2,prod))){
                t2.push_back(prod);
            }
        }
    }
    //FOR SOME REASON THIS CODE IS FINDING ONE EXTRA T=2 OPERATOR
    //ONE PERMUTATION IS NOT GETTING RECOGNIZED AS SUCH
    std::cout<<t2.size();

    return 0;
}

