#include <algorithm>
#include <iostream>
#include <vector>
#include "Z2.hpp"
#include "SO6.hpp"

SO6 tMatrix(int i, int j){
    // Generates the T Matrix T[i+1, j+1]
    SO6 t("T("+std::to_string(i)+","+std::to_string(j)+")");
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
    t.genLDE();
    return(t);
}

bool containedIn(SO6 (&arr)[15], SO6& entry){
    // Checks if entry is contained in our one array
    for(SO6 item : arr){
        if(entry == item){
            return(true);
        }
    }
    return(false);
}

bool containedIn(std::vector<SO6>& v, SO6& entry){
    // Checks if entry is contained in a vector of SO6
    for(SO6 item: v){
        if(entry == item){
            return(true);
        }
    }
    return(false);
}

std::vector<std::vector<SO6>> genProds(std::vector<SO6>& oneLDE, int tCount, std::vector<SO6>& tmats){
    // Takes one strata of LDEs from T count tCount, and multiplies by all T-count 1 matrices
    // Does NOT check for permutation
    int numLDES = tCount+2;
    SO6 prod;
    std::vector<std::vector<SO6>> toReturn(numLDES);
    for(int i = 0; i<15; i++){
        for(SO6 m : oneLDE){
            prod = tmats[i]*m;
            toReturn[prod.getLDE()].push_back(prod);
        }
    }
    return(toReturn);
}

std::vector<SO6> genPerms(std::vector<SO6>& oneLDE, int LDE, std::vector<std::vector<std::vector<SO6>>>& lowerTs){
    // Takes one strata of LDEs with LDE LDE, and then compares with relevant prior sets in lowerTs
    std::vector<SO6> toReturn;
    bool isPerm;
    for(SO6 m : oneLDE){
        isPerm = false;
        for(std::vector<std::vector<SO6>> matDist : lowerTs){
            if(LDE<matDist.size())
                isPerm = isPerm || containedIn(matDist[LDE],m);
        }
        isPerm = isPerm || containedIn(toReturn, m);
        if(!isPerm)
            toReturn.push_back(m);
    }
    return(toReturn);
}

int main(){
    //generating list of T matrices
    //in the order Andrew wanted
    std::vector<SO6> ts;
    for(int i = 0; i<15; i++){
        if(i<5)
            ts.push_back(tMatrix(0,i+1));
        else if(i<9)
            ts.push_back(tMatrix(1, i-3));
        else if(i<12)
            ts.push_back(tMatrix(2, i-6));
        else if(i<14)
            ts.push_back(tMatrix(3, i-8));
        else
            ts.push_back(tMatrix(4,5));
    }
    std::cout<<"Generated T count 1 \n";
    std::vector<std::vector<std::vector<SO6>>> odds = std::vector<std::vector<std::vector<SO6>>>{std::vector<std::vector<SO6>>{std::vector<SO6>(), ts}};
    std::vector<std::vector<std::vector<SO6>>> evens(0);
    //generating t count 2
    //for some reason this generates 166 as opposed to 165
    //the weird thing is that the higher t counts all agree perfectly with Andrew
    //The reason is that it doesn't catch the first operator which is just a Clifford operator
    std::vector<std::vector<SO6>> t2;
    t2 = genProds(ts, 1, ts);
    t2[0] = genPerms(t2[0], 0, evens);
    t2[1] = genPerms(t2[1], 1, evens);
    t2[2] = genPerms(t2[2], 2, evens);
    std::cout<<"Generated T count 2 \n";
    std::cout<<"LDE 0:"<<t2[0].size()<<"\n";
    std::cout<<"LDE 1:"<<t2[1].size()<<"\n";
    std::cout<<"LDE 2:"<<t2[2].size()<<"\n";
    evens.push_back(t2);
//    //generating t count 3
//    std::vector<SO6> t3[4];
//    for(int j = 0; j<3; j++){
//        for(int i = 0; i<15; i++){
//            for(SO6 m : t2[j]){
//                prod = ts[i]*m;
//                int LDEIndex = prod.getLDE();
//                if((!containedIn(ts, prod))&&(!containedIn(t3[LDEIndex],prod)))
//                    t3[LDEIndex].push_back(prod);
//            }
//        }
//    }
//    std::cout<<"Generated T Count 3 \n";
//    std::cout<<"LDE 0:"<<t3[0].size()<<"\n";
//    std::cout<<"LDE 1:"<<t3[1].size()<<"\n";
//    std::cout<<"LDE 2:"<<t3[2].size()<<"\n";
//    std::cout<<"LDE 3:"<<t3[3].size()<<"\n";
//
//
//    //generating t count 4
//    //this step takes something in the order of 100 times longer,
//    //Reduced runtime including this to ~3 minutes, but it goes from 3 seconds to get to T-Count 3
//    //to that for 4... not a good growth rate
//    std::vector<SO6> t4[5];
//    for(int j = 0; j<4; j++){
//        for(int i = 0; i<15; i++){
//            std::cout<<i<<"\n";
//            for(SO6 m : t3[j]){
//                prod = ts[i]*m;
//                int LDEIndex = prod.getLDE();
//                if((!containedIn(t2[LDEIndex],prod))&&(!containedIn(t4[LDEIndex],prod)))
//                    t4[LDEIndex].push_back(prod);
//            }
//        }
//    }
//    std::cout<<"Generated T Count 4 \n";
//    std::cout<<"LDE 0:"<<t4[0].size()<<"\n";
//    std::cout<<"LDE 1:"<<t4[1].size()<<"\n";
//    std::cout<<"LDE 2:"<<t4[2].size()<<"\n";
//    std::cout<<"LDE 3:"<<t4[3].size()<<"\n";
//    std::cout<<"LDE 3:"<<t4[4].size()<<"\n";



    return 0;
}


