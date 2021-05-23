/**
 * T Operator Product Generation Main File
 * @file main.cpp
 * @author Connor Mooney
 * @author Michael Jarret
 * @author Andrew Glaudell
 * @author Jacob Weston
 * @author Mingzhen Tian
 * @version 5/20/21
 */

#include <algorithm>
#include <iostream>
#include <vector>
#include <thread>
#include <future>
#include <fstream>
#include <chrono>
#include "Z2.hpp"
#include "SO6.hpp"


using namespace std;
/**
 * Returns the SO6 object corresponding to T[i+1, j+1]
 * @param i the first index to determine the T matrix
 * @param j the second index to determine the T matrix
 * @return T[i+1,j+1]
 */

SO6 tMatrix(int i, int j){
    // Generates the T Matrix T[i+1, j+1]
    SO6 t("T("+to_string(i)+","+to_string(j)+")");
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

/**
 * Returns the itemwise union of two vectors of vectors of SO6
 * @param a a vector of vectors of SO6
 * @param a another vector of vectors of SO6
 * @return m, where m[i] = a[i] union b[i]
 */
vector<vector<SO6>> mergedVect(vector<vector<SO6>>& a, vector<vector<SO6>>& b){
    //Takes two vectors of vectors of equal length a and b
    //and gives back the vector m where m[i] = a[i] union b[i]
    vector<vector<SO6>> m;
    vector<SO6> u;
    for(int i = 0; i<a.size(); i++){
        u = vector<SO6>();
        for(int j = 0; j<a[i].size(); j++)
            u.push_back(a[i][j]);
        for(int j = 0; j<b[i].size(); j++)
            u.push_back(b[i][j]);
        m.push_back(u);
    }
    return(m);
}

// Divides a vect of vects evenly over every LDE into numThreads vectors of vectors
vector<vector<vector<SO6>>> divideVect(vector<vector<SO6>>& toDivide, int numThreads){
    vector<vector<vector<SO6>>> toReturn(numThreads, vector<vector<SO6>>(toDivide.size()));
    int numPerThread;
    int remaining;
    for(int i = 0; i<toDivide.size(); i++){
        numPerThread = toDivide[i].size()/numThreads;
        for(int j = 0; j<numThreads; j++){
            for(int k = j*numPerThread; k<(j+1)*numPerThread; k++){
                toReturn[j][i].push_back(toDivide[i][k]);
            }
        }
        remaining = toDivide[i].size()-numPerThread*numThreads;
        for(int j = 0; j<remaining; j++){
            toReturn[j][i].push_back(toDivide[i][numPerThread*numThreads+j]);
        }
    }
    return toReturn;
}

/**
 * multiplies every entry of a vector of SO6 with every entry of another vector, and returns it sorted by LDE
 * @param batch small batch of various LDEs
 * @param tmats a vector of SO6 to multiply, we will always pass it the vector of the 15 T-Count 1 matrices though
 * @return a vector of vectors of SO6, containing the products of elements of tCounts and oneLDE, sorted by LDE
 */
vector<vector<SO6>> prodHelper(vector<vector<SO6>>& batch, vector<SO6>& tmats){
    // Takes one strata of LDEs from T count tCount, and multiplies by all T-count 1 matrices
    // Does NOT check for permutation
    int numLDES = batch.size()+1;
    SO6 prod;
    vector<vector<SO6>> toReturn(numLDES);
    for(int i = 0; i<15; i++){
        for(int j = 0; j<batch.size(); j++){
            for(SO6 m : batch[j]){
                prod = tmats[i]*m;
                toReturn[prod.getLDE()].push_back(prod);
            }
        }
    }
    return(toReturn);
}


/**
 * Takes a vector of vectors of SO6, all with the same T-Count, broken out by LDE, and multiplies each element
 * by those of another vector of SO6 and returns them sorted by LDE as well
 * @param TminusOne the vector of vectors of SO6, sorted by LDE, to be multiplied
 * @param tcount the T-Count of TminusOne
 * @param tmats the vector of SO6 whose elements will be multiplying those of TminusOne
 * @return the product of all elements of TminusOne and tmats, sorted by LDE
 */
vector<vector<SO6>> genAllProds(vector<vector<SO6>>& TminusOne, vector<SO6>& tmats, int numThreads){
    vector<vector<vector<SO6>>> threadinput = divideVect(TminusOne, numThreads);
    future<vector<vector<SO6>>> threads[numThreads];
    vector<vector<SO6>> prod[numThreads];
    for(int i = 0; i<numThreads; i++)
        threads[i] = async(launch::async, prodHelper, ref(threadinput[i]), ref(tmats));
    for(int i = 0; i<numThreads; i++){
        prod[i] = threads[i].get();
    }
    vector<vector<SO6>> toReturn(prod[0].size());
    for(int i = 0; i<numThreads; i++)
        toReturn = mergedVect(toReturn, prod[i]);
    return(toReturn);
}



//int getLength(vector<vector<SO6>>& input){
//    int l = 0;
//    for(int i = 0; i<input.size(); i++){
//        l+= input[i].size();
//    }
//    return l;
//}


//Helper methods for pruneAllPerms

//Prunes a vector of SO6 of matrices equivalent to check in indices between a and b
void selfCheckHelper(vector<SO6>& vec, SO6& check, int a, int b){
    for(int i = a; i<b; i++){
        if(check==vec[i])
            vec[i].setName("None"); //Marks for deletion
    }
}

/**
 * Returns whether or not an SO6 is contained in a vector of SO6
 * @param v the vector of SO6 to be checked for v
 * @param entry the SO6 to be compared to elements of v
 * @return whether or not v is contained in entry
 */
bool containedIn(vector<SO6>& v, SO6& entry){
    for(SO6 item: v){
        if(entry == item){
            return(true);
        }
    }
    return(false);
}

//Prunes a vector of SO6 of matrices equivalent to those in past in indices from a to b
void pastCheckHelper(vector<SO6>& vec, vector<SO6>& past, int a, int b){
    // Takes one strata of LDEs with LDE LDE, and then compares with relevant prior sets in lowerTs
    for(int i = a; i < b; i++){
        if(containedIn(past, vec[i]))
            vec[i].setName("None"); //Marks for deletion
    }
}

bool isNone(SO6& toCheck){
    return(toCheck.getName()=="None");
}

/**
 * Takes the unpruned LDE distribution of a T-Count, and removes all permutations
 * @param unReduced the vector of vectors of SO6, sorted by LDE, to be checked
 * @param tMinusTwo the vector the distribution of T-count N-2
 * @param numThreads the number of parallel processes to be ran
 */

void pruneAllPerms(vector<vector<SO6>>& unReduced, vector<vector<SO6>>& tMinusTwo, int numThreads){
    /*
     * General Structure: examines each LDE separately, finds redundant matrices,
     * marks them for deletion by changing their name to "None,"
     * and then at the end of the method deletes them.
     * Does this in two stages: First by comparing to the T-count 2 down,
     * and then by comparing all of the matrices in the same T-count
     */

    //initializing relevant varaibles
    std::thread threads[numThreads];
    int numPerThread;

    // Past-Checking
    //iterating over every relevant LDE
    for(int i = 0; i<tMinusTwo.size(); i++){
        if(unReduced[i].size()== 0) continue;
        numPerThread = unReduced[i].size()/numThreads;

        //distributing elements evenly to the threads and pruning
        for(int j = 0; j<numThreads-1; j++){
            threads[j] = thread(pastCheckHelper, ref(unReduced[i]), ref(tMinusTwo[i]), j*numPerThread, (j+1)*numPerThread);
        }
        threads[numThreads-1] = thread(pastCheckHelper, ref(unReduced[i]), ref(tMinusTwo[i]), numThreads*numPerThread, unReduced[i].size());

        //waiting for all threads to complete
        for(int j = 0; j<numThreads; j++)
            threads[j].join();
    }

    //Self-Checking
    //iterating over all LDEs
    for(int i = 0; i<unReduced.size(); i++){
        //iterating over all entries, and then marking all entries equivalent to them to their right for deletion
        for(int j = 0; j<unReduced[i].size(); j++){

            //skipping past entries marked as "None"
            while(unReduced[i][j].getName() == "None" && (j<unReduced.size()-1)) ++j;
            //Finding the number per thread. Notice this is integer division, so numPerThread*numThreads<= (toReturn[i].size()-j-1)
            numPerThread = (unReduced[i].size()-j-1)/numThreads;

            //allocating to threads
            //will turn equivalent matrices to "None" name
            for(int k = 0; k<numThreads-1; k++){
                //looking through toReturn[i] in parallel
                threads[k] = thread(selfCheckHelper, ref(unReduced[i]), ref(unReduced[i][j]), j+1+k*numPerThread, j+1+(k+1)*numPerThread);
            }
            threads[numThreads-1] = thread(selfCheckHelper, ref(unReduced[i]), ref(unReduced[i][j]), j+1+(numThreads-1)*numPerThread, unReduced[i].size());

            //waiting for all to be performed
            for(int k = 0; k<numThreads; k++){
                threads[k].join();
            }
        }
        //Removing all elements marked for deletion ("None" name)
        unReduced[i].erase(std::remove_if(unReduced[i].begin(), unReduced[i].end(), isNone), unReduced[i].end());
    }
}

//vector<int> findRedundantIndices(SO6 unReducedOneLDE[], vector<SO6>& tMinusTwo, int numThreads){
//    int indices[unReduced.size()];
//    int numPerThread = unReduced.size()/numThreads;
//    thread threads[numThreads];
//    for(int i =0; i < numThreads -1; i++){
//        threads[i] = thread(checkPerm)
//    }
//}


int main(){

    //Asking for number of threads and tCount to generate to
    // Seems to slow things down, so may remove this and just hardcode it in.
    int numThreads;
    int tCount;
    cout<<"How many threads would you like to utilize? Please enter here: ";
    cin>>numThreads;
    cout<<"\nTo what T-Count do you want to generate? Please enter here: ";
    cin>>tCount;
    cout<<"\n";
    ofstream write;
    string fileName;

    //timing
    auto tbefore = chrono::high_resolution_clock::now();
    //generating list of T matrices
    //in the order Andrew wanted
    vector<SO6> ts; //t count 1 matrices
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
    cout<<"Generated T count 1 \n";

    write = ofstream("T1.txt");
    for(int i = 0; i<15; i++){
        write<<ts[i].getName()<<"\n";
        write<<ts[i];
    }
    cout<<"Wrote T-Count 1 to 'T1.txt' \n\n";


    //Generating Higher T-Counts
    vector<vector<SO6>> prior;
    vector<vector<SO6>> current = vector<vector<SO6>>{vector<SO6>(), ts};
    vector<vector<SO6>> next;
    for(int i = 0; i<tCount-1; i++){
        fileName = "T" + to_string(i+2) + ".txt";
        write = ofstream(fileName);
        next = genAllProds(current, ts, numThreads);
        pruneAllPerms(next, prior, numThreads);
        cout<<"Generated T-count "<<(i+2)<<"\n";
        for(int j = 0; j<next.size(); j++){
            cout<<"LDE"<<j<<": "<<next[j].size()<< "\n";
        }
        for(int j = 0; j<next.size(); j++){
            for(int k = 0; k<next[j].size(); k++){
                write<<next[j][k].getName()<<"\n";
                write<<next[j][k];
            }
        }
        cout<<"Wrote T-Count "<<(i+2)<<" to 'T"<<(i+2)<<".txt' \n\n";
        write.close();
        prior = current;
        current = next;
    }
    chrono::duration<double> timeelapsed = chrono::high_resolution_clock::now() - tbefore;
    cout<< "Time elapsed: "<<timeelapsed.count()<<"\n";
    cout<< "Press any character and then Enter to continue...";
    string i;
    cin>> i;
    return 0;
}



