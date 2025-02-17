#include<stdio.h>
#include <iostream>
using namespace std;
int n;
int cost[21][21];
int path[21];
bool visited[21];
int curcost = 0;
int mincost = __INT_MAX__;
int minpath = __INT_MAX__;
void backtrack(int k){
   
        for(int i=0; i<n;i++){
            if(!visited[i]){
                path[k] = i;
                visited[i] = true;
                curcost += cost[path[k-1]][path[k]];

                if(k==n-1){
                    mincost = min(mincost, curcost + cost[path[n-1]][path[0]]);
                }
                else if (curcost + (n-k-1)*minpath < mincost){
                     backtrack(k+1);
                }
                
                visited[i]= false;
                curcost -= cost[path[k-1]][path[k]];
            }
        }
    
    
}
int main(){
    std::ios::sync_with_stdio(false);
    cin>>n;
    for(int i=0; i<n; i++){
        for(int j=0; j<n; j++){
            cin>>cost[i][j];
            minpath = min(minpath, cost[i][j]);
        }
    }
    for(int i=0; i<n; i++){
        visited[i]=false;
    }
    backtrack(0);
    cout<<mincost;
    return 0;
}
   