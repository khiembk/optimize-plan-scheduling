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


bool check_truck_cap(int truck_id){
    for(int i =1 ;i <=node; i++){
     if(!visted[i] && curcap[truck_id] + demand[i] <= cap){
          return true;
     }}
     return false;
}
bool check_rest_node(){
    for (int i=1; i<=node;i++){
      if (!visted[i]){
        return true;
      }
    }
    return false;
}
int Num_rest_node(){
    int num_node = 0;
    for (int i=1; i<=node;i++){
      if (!visted[i]){
        num_node++;
      }
    }
    return num_node;
}
void back_track(int truck_id, int cur_node){
    if(truck_id < truck && cur_node!=0){
        currentcost += cost[cur_node][0];
        if (!check_rest_node()){
            minCost = min(minCost, currentcost);
        }else{
           if(currentcost + minDistance*(1 + Num_rest_node()) <= minCost){
            back_track(truck_id+1,0);
           } 
        }
        currentcost -= cost[cur_node][0];
    } 
    for(int i =1 ;i <=node; i++){
     if(!visted[i] && curcap[truck_id] + demand[i] <= cap){
        visted[i] = true;
        curcap[truck_id] = curcap[truck_id] + demand[i];
        currentcost += cost[cur_node][i];
        if (!check_rest_node()){
            minCost = min(minCost, currentcost + cost[i][0]);
        }else{
           if(currentcost + minDistance*(1 + Num_rest_node()) <= minCost){
            back_track(truck_id,i);
           } 
        }
       visted[i] = false;
       curcap[truck_id] = curcap[truck_id] - demand[i];
       currentcost -= cost[cur_node][i];
     }
   }
}

int main(){
    ios_base::sync_with_stdio(false);cin.tie(NULL);
    cin>>node>>truck>>cap;
    for (int i=1; i<=node; i++){
        cin>>demand[i];
    }
    for (int i=0; i<=node; i++){
        for(int j=0; j<= node; j++){
            cin>>cost[i][j];
            minDistance= min(minDistance, cost[i][j]);
        }
    }
    for(int i=1; i<=node;i++){
        visted[i] = false;
    }
    for(int j=1;j<=truck; j++){
        curcap[j] = 0;
    }
    back_track(1,0);
    cout<<minCost;
    return 0;
}
