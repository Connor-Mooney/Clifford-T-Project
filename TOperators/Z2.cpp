#include <algorithm>
#include <iostream>
#include "Z2.hpp"

Z2::Z2(int a, int b, int c){
    val[0] = a;
    val[1] = b;
    val[2] = c;
    Z2::reduce();
}

Z2::Z2(){
    val[0] = 0;
    val[1] = 0;
    val[2] = 0;
}

Z2 Z2::operator+(Z2& other){
    int k = std::max(val[2], other[2]);
    int* scaled0 = scale(k);
    int* scaled1 = other.scale(k);
    Z2 summation = Z2(scaled0[0]+scaled1[0], scaled0[1]+scaled1[1], k);
    return summation;
}

Z2& Z2::operator+=(Z2& other){
    int k = std::max(val[2], other[2]);
    int* scaled0 = scale(k);
    int* scaled1 = other.scale(k);
    val[0] = scaled0[0] + scaled1[0];
    val[1] = scaled0[1] + scaled1[1];
    val[2] = k;
    reduce();
    return *this;
}

Z2 Z2::operator-(Z2& other){
    int k = std::max(val[2], other[2]);
    int* scaled0 = scale(k);
    int* scaled1 = other.scale(k);
    Z2 subtraction = Z2(scaled0[0]-scaled1[0], scaled0[1]-scaled1[1], k);
    return subtraction;
}

Z2 Z2::operator*(const Z2& other){
    return Z2(val[0]*other[0]+2*val[1]*other[1], val[0]*other[1]+val[1]*other[0], val[2]+other[2]);
}
bool Z2::operator==(const Z2& other){
    return (val[0]==other[0]&& val[1]==other[1] && val[2]==other[2]);
}

Z2& Z2::operator=(const Z2& other){
    //assigns an operator
    val[0] = other[0];
    val[1] = other[1];
    val[2] = other[2];
    return *this;
}

Z2& Z2::reduce(){
    // reduces a Z2 to its lowest denominator exponent expression
    while(val[0]%2 == 0 && val[1]%2 == 0 && val[2]>0){
        val[0] >>= 1;
        val[1] >>= 1;
        val[2]--;
    }
    if(val[2]<0){
        val[0] <<= -val[2];
        val[1] <<= -val[2];
        val[2] = 0;
    }
    return *this;
}

int* Z2::scale(const int& k){
    // scales a Z2's entries to a given denominator exponent
    int expdiff = k - val[2];
    reg[0] = val[0] << expdiff;
    reg[1] = val[1] << expdiff;
    reg[2] = k;
    return reg;
}

int Z2::getLDE(){
    reg[0] = val[0];
    reg[1] = val[1];
    reg[2] = 2*val[2];
    while(reg[0]%2 == 0 && reg[2]>0){
        reg[0] = reg[1];
        reg[1] = reg[0] >>= 1;
        --reg[2];
    }
    return(reg[2]);
}

std::ostream& operator<<(std::ostream& os, const Z2& z){
    os << '(' << z[0] << '+' << z[1] << "*sqrt(2))/2^" << z[2];
    return os;
}
