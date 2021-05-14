
class SO6{
public:
    SO6(); //initializes zero matrix
    SO6(Z2[6][6]); //initializes matrix according to a 6x6 array of Z2
    SO6 operator*(SO6&); //mutliplication
    Z2& operator()(int, int); //indexing
    const Z2& operator()(int, int) const; //indexing for constant SO6
    bool operator==(SO6&); //checking equality up to signed permutation
    friend std::ostream& operator<<(std::ostream&,const SO6&); //display
private:
    Z2 arr[6][6];
};
