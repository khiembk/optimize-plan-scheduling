#include<iostream>
using namespace std;
int node, truck, cap;
int path[21];
int truck_assigned[21];
int demand[21];
int cost[21][21];
int currentcost= 0;
int minCost = __INT_MAX__;
int curcap[21];
bool visted[21];
int minDistance = __INT_MAX__;
int truck_location[21];

bool checkValid(int step,int cur_node, int cur_truck){
    return (curcap[cur_truck] + demand[cur_node] <= cap)&&(!visted[cur_node]); 
}
void print_result(){
    cout<<"Mincost:"<<minCost<<endl;
    cout<<"path: ";
    for(int i=1;i<=node-1;i++){
        cout<<path[i]<<" ";
    }
    cout<<endl;
    cout<<"truck assigned: ";
    for(int i=1;i<=node-1;i++){
        cout<<truck_assigned[i]<<" ";
    }
    cout<<endl;
}
int comput_rest_cost(){
    int rest_cost = 0;
    for(int i= 1; i<=truck;i++){
        rest_cost+= cost[truck_location[i]][0];
    }
    return rest_cost;
}

void backtrack(int k){
    
    for (int i=1; i<node; i++){
        if(!visted[i]){
            for(int j=1; j<=truck; j++){
               if(checkValid(k,i,j)){
                   path[k] = i;
                   visted[i] = true;
                   curcap[j]+= demand[i];
                   int cur_truck_location = truck_location[j];
                   int newcost = cost[cur_truck_location][i];
                   currentcost += newcost;
                   truck_assigned[k] = j;
                   truck_location[j] = i;
                   if(k==node-1){
                        int rest_cost = comput_rest_cost();
                        //cout<<"mincost: "<<minCost;
                        
                        if (minCost > currentcost + rest_cost){
                            minCost = currentcost + rest_cost;
                            print_result();
                        }
                        //print_result();
                        
                   }else{
                       if(currentcost + (node - 1 - k)*minDistance <= minCost){
                           backtrack(k+1);
                       }
                   }
                   truck_location[j] = cur_truck_location;
                   truck_assigned[k] = 0;
                   currentcost-= newcost;
                   path[k]=0;
                   visted[i]= false;
                   curcap[j]-= demand[i];
               }
            }
        }
    }
}
int main(){
    cin>>node>>truck>>cap;
    for (int i=0; i<node; i++){
        cin>>demand[i];
    }
    for (int i=0; i< node; i++){
        for(int j=0; j< node; j++){
            cin>>cost[i][j];
            minDistance= min(minDistance, cost[i][j]);
        }
    }
    for(int i=0; i<node;i++){
        visted[i] = false;
    }
    for(int j=1;j<=truck; j++){
        curcap[j] = 0;
        truck_location[j] = 0;
    }
    backtrack(1);
    return 0;
}