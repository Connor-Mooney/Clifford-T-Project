#include <algorithm>
#include <iostream>
#include <vector>
#include "Z2.hpp"
#include "SO6.hpp"

/**
 * Basic constructor. Initializes Zero matrix.
 *
 */
SO6::SO6(){
    name = "0";
    for(int i=0; i<6; i++){
        for(int j=0; j<6; j++)
            arr[i][j]=Z2();
    }

    genLDE();
}

/**
 * Constructor that initializes zero matrix with arbitrary name
 * @param n the name of the object
 */
SO6::SO6(std::string n){
    name = n;
    //initializes all entries as 0
    for(int i=0; i<6; i++){
        for(int j=0; j<6; j++)
            arr[i][j]=Z2();
    }
    genLDE();
}


/**
 * Constructor that initializes arbitrary matrix with arbitrary name
 * @param a array of Z2 that the SO6 will take as values
 * @param n the name of the object
 */
SO6::SO6(Z2 a[6][6], std::string n){
    name = n;
    //initializes SO6's entries according to a
    for(int i = 0; i<6; i++){
        for(int j = 0; j<6; j++)
            arr[i][j] = a[i][j];
    }
    genLDE();
}

/**
 * Overloads the * operator with matrix multiplication for SO6 objects
 * @param other reference to SO6 to be multiplied with (*this)
 * @return matrix multiplication of (*this) and other
 */
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

/** overloads == method to check equality up to signed column permutation
 *  @param other reference to SO6 to be checked against
 *  @return whether or not (*this) and other are equivalent up to signed column permutation
 */
bool SO6::operator==(SO6 &other) {
    // int tot;
    // bool flag;
    Z2 dot_product;
    Z2 next;
    for(int i = 0; i < 6; i++) {
        // tot = 0;
        for(int j = 0; j < 6; j++) {
            dot_product = Z2(0,0,0);
            for(int k = 0; k <6; k++) {
                next = arr[i][k]*other(j,k);
                dot_product += next;
            }
            // if(dot_product.B != 0 || dot_product.K != 0) return false;
            if(dot_product[2] != 0) return false;
            // tot += (dot_product.A)*(dot_product.A);
            // if(tot > 1) return false;
        }
        // if(tot !=1) return false;
    }
    return true;
}

/**
 * Generates LDE. Needs to be called any time the matrix is modified to make sure LDE stays current
 */
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

/**
 * Overloads << function for SO6.
 * @param os reference to ostream object needed to implement <<
 * @param m reference to SO6 object to be displayed
 * @returns reference ostream with the matrix's display form appended
 */
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


