
class SO6{
public:
    SO6();
    SO6(Z2[6][6]);
    SO6 operator*(SO6&);
    Z2& operator()(int, int);
    const Z2& operator()(int, int) const;
    bool operator==(SO6&);
    friend std::ostream& operator<<(std::ostream&,const SO6&);
private:
    Z2 arr[6][6];
};
