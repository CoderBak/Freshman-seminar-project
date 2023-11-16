#include<bits/stdc++.h>

#define maxEdge 2001000
#define maxNode 4100
#define inf 2147483647
using namespace std;
struct Node {
    int to, value, next;
} edge[maxEdge];
int dep[maxNode], head[maxNode], cnt;
int s, t;

void add_edge(int x, int y, int z) {
    edge[++cnt] = {y, z, head[x]};
    head[x] = cnt;
}

int bfs() {
    memset(dep, 0, sizeof(dep));
    queue<int> q;
    q.push(s);
    dep[s] = 1;
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        for (int i = head[u]; i; i = edge[i].next)
            if (!dep[edge[i].to] && edge[i].value > 0) {
                dep[edge[i].to] = dep[u] + 1;
                q.push(edge[i].to);
            }
    }
    return dep[t];
}

int dfs(int u, int cur) {
    if (u == t) return cur;
    for (int i = head[u]; i; i = edge[i].next)
        if (dep[edge[i].to] == dep[u] + 1 && edge[i].value > 0) {
            int flow = dfs(edge[i].to, min(cur, edge[i].value));
            if (flow) {
                edge[i].value -= flow;
                edge[i + ((i & 1) ? 1 : -1)].value += flow;
                return flow;
            }
        }
    return 0;
}

int n, m, tmp, x, y, ans;

int main() {
    freopen("output.txt", "r", stdin);
    scanf("%d%d", &n, &m);
    t = n + m + 1;
    for (int i = 1; i <= n; i++) {
        add_edge(0, i, 1);
        add_edge(i, 0, 0);
    }
    for (int i = n + 1; i <= n + m; i++) {
        add_edge(i, t, 1);
        add_edge(t, i, 0);
    }
    while (~scanf("%d%d", &x, &y)) {
        add_edge(x, y + n, 1);
        add_edge(y + n, x, 0);
    }
    while (bfs())
        while (tmp = dfs(s, inf))
            ans += tmp;
    printf("%d", ans);
    return 0;
}