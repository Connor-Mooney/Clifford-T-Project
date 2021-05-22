
class SO6{
public:
    SO6();
    SO6(std::string); //initializes zero matrix
    SO6(Z2[6][6], std::string); //initializes matrix according to a 6x6 array of Z2
    SO6 operator*(SO6&); //mutliplication
    inline Z2& operator()(int i, int j){return arr[i][j];} //returns the (i,j)th entry
    inline const Z2& operator()(int i, int j) const{return arr[i][j];} //returns the (i,j)th entry but for const
    bool operator==(SO6&); //checking equality up to signed permutation
    inline std::string getName(){return(name);} //getter for Name
    inline void setName(std::string newName){name = newName;}
    inline int getLDE(){return(LDE);} //getter for LDE
    void genLDE(); //generates LDE, called after multiplication and constructor
    friend std::ostream& operator<<(std::ostream&,const SO6&); //display
private:
    Z2 arr[6][6];
    std::string name;
    int LDE;
};
