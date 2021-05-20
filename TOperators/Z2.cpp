#include <algorithm>
#include <iostream>
#include "Z2.hpp"

/**
 * Constructor that initializes object corresponding to (a+sqrt(2)*b)/(2^c)
 * @param a integer part of numerator
 * @param b sqrt(2) part of numerator
 * @param c log_2 of the denominator
 */
Z2::Z2(int a, int b, int c){
    val[0] = a;
    val[1] = b;
    val[2] = c;
    Z2::reduce();
}

/**
 * Constructor to initialize Z2 corresponding to 0.
 */
Z2::Z2(){
    val[0] = 0;
    val[1] = 0;
    val[2] = 0;
}

/**
 * Overloads + operator for Z2
 * @param other reference to Z2 object to be added
 * @return summation the sum of other and *this
 */
Z2 Z2::operator+(Z2& other){
    int k = std::max(val[2], other[2]);
    int* scaled0 = scale(k);
    int* scaled1 = other.scale(k);
    Z2 summation = Z2(scaled0[0]+scaled1[0], scaled0[1]+scaled1[1], k);
    return summation;
}

/**
 * Overloads += operator for Z2
 * @param other reference to Z2 object to be added to *this
 * @return *this reference to this object, onto which other has been added
 */
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

/**
 * Overloads the - operator for Z2
 * @param other reference to Z2 object to be subtracted
 * @return summation the subtraction *this - other
 */
Z2 Z2::operator-(Z2& other){
    int k = std::max(val[2], other[2]);
    int* scaled0 = scale(k);
    int* scaled1 = other.scale(k);
    Z2 subtraction = Z2(scaled0[0]-scaled1[0], scaled0[1]-scaled1[1], k);
    return subtraction;
}

/**
 * Overloads the * operator for Z2
 * @param other reference to Z2 object to be multiplied
 * @return
 */
Z2 Z2::operator*(const Z2& other){
    return Z2(val[0]*other[0]+2*val[1]*other[1], val[0]*other[1]+val[1]*other[0], val[2]+other[2]);
}

/**
 * Overloads the == operator for Z2
 * @param other reference to Z2 object to be compared to
 * @return whether or not the entries of the two Z2s are equal
 */
bool Z2::operator==(const Z2& other){
    return (val[0]==other[0]&& val[1]==other[1] && val[2]==other[2]);
}

/**
 * Overloads the = operator for Z2
 * @param other reference to object make *this equal to
 * @return *this reference to this object which has been made equal to other
 */

Z2& Z2::operator=(const Z2& other){
    //assigns an operator
    val[0] = other[0];
    val[1] = other[1];
    val[2] = other[2];
    return *this;
}

/**
 * Reduces this Z2 to simplest form
 * @return *this reference to simplified object
 */
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

/**
 * Scales the Z2 to a different denominator exponent
 * @param k the exponent to scale to
 * @return reg the workspace array containing the scaled values
 */
int* Z2::scale(const int& k){
    // scales a Z2's entries to a given denominator exponent
    int expdiff = k - val[2];
    reg[0] = val[0] << expdiff;
    reg[1] = val[1] << expdiff;
    reg[2] = k;
    return reg;
}

/**
 * Gives the denominator exponent when this operator is reduced with sqrt(2) in the denominator
 * @return exponent of sqrt(2) in reduced form of the operator
 */
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

/**
 * Overloads << function for Z2
 * @param os reference to ostream object needed to implement <<
 * @param z reference to Z2 object to be displayed
 * @returns reference ostream with the Z2's display form appended
 */
std::ostream& operator<<(std::ostream& os, const Z2& z){
    os << '(' << z[0] << '+' << z[1] << "*sqrt(2))/2^" << z[2];
    return os;
}
