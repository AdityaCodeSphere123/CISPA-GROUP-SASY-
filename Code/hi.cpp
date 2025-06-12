/**
 *    author: aditya_anand03
**/
 
#include <bits/stdc++.h>
#pragma GCC optimize("Ofast")
#pragma GCC optimize("unroll-loops")
 
using namespace std;
 
#ifdef LOCAL
#include "algo/debug.h"
#else
#define debug(...) 42
#endif
 
/* TYPES  */
#define ll long long
#define pii pair<int, int>
#define pll pair<long long, long long>
#define vi vector<int>
#define vll vector<long long>
#define mii map<int, int>
#define si set<int>
#define sc set<char>
 
/* FUNCTIONS */
#define pb push_back
#define eb emplace_back
 
/* PRINTS */
template <class T>
void print_v(vector<T> &v) { cout << "{"; for (auto x : v) cout << x << ","; cout << "\b}"; }
 
/* UTILS */
#define MOD 1000000007
#define PI 3.1415926535897932384626433832795
#define read(type) readInt<type>()
ll min(ll a,int b) { if (a<b) return a; return b; }
ll min(int a,ll b) { if (a<b) return a; return b; }
ll max(ll a,int b) { if (a>b) return a; return b; }
ll max(int a,ll b) { if (a>b) return a; return b; }
ll gcd(ll a,ll b) { if (b==0) return a; return gcd(b, a%b); }
ll lcm(ll a,ll b) { return a/gcd(a,b)*b; }
string to_upper(string a) { for (int i=0;i<(int)a.size();++i) if (a[i]>='a' && a[i]<='z') a[i]-='a'-'A'; return a; }
string to_lower(string a) { for (int i=0;i<(int)a.size();++i) if (a[i]>='A' && a[i]<='Z') a[i]+='a'-'A'; return a; }
bool prime(ll a) { if (a==1) return 0; for (int i=2;i<=round(sqrt(a));++i) if (a%i==0) return 0; return 1; }
 
void yesno(bool a) {if (a) cout << "YES\n"; else cout << "NO\n";}
 
#define get(n) int n; cin>>n;
#define getll(n) ll n; cin>>n;
#define getv(v,n) vector<int> v(n); forr(i,0,n) cin >> v[i];
#define gets(s) string s; cin >> s;
#define sortt(v) sort(v.begin(),v.end())
#define reversee(v) reverse(v.begin(),v.end())
#define revsort(v) sortt(v); reversee(v);
#define see(v) for(auto x:v) cout << x << " "; cout << endl;
#define seemap(m) for (auto x:m) cout << x.first << ":" << x.second << " " ; cout << endl;
 
 
/*  All Required define Pre-Processors and typedef Constants */
typedef long int int32;
typedef unsigned long int uint32;
typedef long long int int64;
typedef unsigned long long int  uint64;
 
 
void solve() {
    int n;
    cin >> n;

    int a[n];

    for (int i = 0 ; i < n ; i++){
        cin >> a[i];
    }
    int ans = 0;
    set<int> cur, seen;
    for(int i=0; i<n; i++){
        cur.insert(a[i]);
        seen.insert(a[i]);
        if(cur.size() == seen.size()){
            ans++;
            seen.clear();
        }
    }
    cout << ans << '\n';

}
 
int main() {
    ios::sync_with_stdio(0);
    cin.tie(0);
    cout.tie(0);
    
    ll adi;
    cin >> adi;
    
    while (adi--) {
        solve();
    }
 
    return 0;
}
