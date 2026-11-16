// Least-cost search on two copper layers. A via is permitted only if its full
// annulus, drill and solder-land exclusion are all clear on both layers.
#include <cstdint>
#include <cstdio>
#include <limits>
#include <queue>
#include <utility>
#include <vector>
extern "C" int trace_grid(int nx,int ny,const unsigned char* pass,
                          const unsigned char* via,const unsigned char* starts,
                          const unsigned char* goals,int* path,int capacity) {
    const int plane=nx*ny, n=2*plane;
    using Step=std::pair<int,int>;
    std::priority_queue<Step,std::vector<Step>,std::greater<Step>> open;
    std::vector<int> cost(n, std::numeric_limits<int>::max()), previous(n,-1);
    for(int i=0;i<n;i++) if(starts[i] && pass[i]) {cost[i]=0;open.push({0,i});}
    constexpr int dx[8]={1,-1,0,0,1,1,-1,-1};
    constexpr int dy[8]={0,0,1,-1,1,-1,1,-1};
    while(!open.empty()) {
        const auto current=open.top();open.pop();
        int c=current.first, p=current.second;
        if(cost[p]!=c) continue;
        if(goals[p]) {
            int len=0;
            for(int t=p;t>=0;t=previous[t]) {
                if(len==capacity)return -2;
                path[len++]=t;
            }
            return len;
        }
        int layer=p/plane, y=(p%plane)/nx, x=p%nx;
        auto relax=[&](int q,int step) {
            if(!pass[q] || cost[q]<=c+step)return;
            cost[q]=c+step;previous[q]=p;open.push({c+step,q});
        };
        for(int k=0;k<8;k++) {
            int xx=x+dx[k],yy=y+dy[k];
            if(xx<0||xx>=nx||yy<0||yy>=ny)continue;
            if(k>=4 && (!pass[layer*plane+y*nx+xx]||!pass[layer*plane+yy*nx+x]))continue;
            relax(layer*plane+yy*nx+xx,(k<4?10:14)+(layer?3:0));
        }
        if(via[p%plane])relax((1-layer)*plane + p%plane,850);
    }
    return 0;
}
