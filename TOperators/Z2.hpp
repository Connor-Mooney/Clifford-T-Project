
class Z2{
// elements of Z[1/sqrt(2)] are stored in the form (val[0] + val[1]*sqrt(2))/2^val[2]
public:
    Z2(int, int, int); // the ints paseed form the entries of val
    Z2();// the entries of val are all 0
    int& operator[](int); //index accessor for non-constant Z2s
    const int& operator[](int) const; //index accessor function for constant Z2s
    Z2 operator+(Z2&); //handles addition
    Z2& operator+=(Z2&); //handles +=
    Z2 operator-(Z2&); //handles subtraction
    Z2 operator*(const Z2&); //function that handles multiplication
    bool operator==(const Z2&); //function that checks equality between two Z2
    Z2& operator=(const Z2&); //function that makes the operator have equal entries to parameter
    Z2& reduce(); //auxiliary function to make sure every triad is in a consistent most reduced form
    int* scale(const int&); //auxiliary function to make sure that when addition is performed the exponents in the denominators are equal
    friend std::ostream& operator<<(std::ostream&,const Z2&); //display
private:
    int val[3]; //values of the Z2
    int reg[3]; //workspace array
};
