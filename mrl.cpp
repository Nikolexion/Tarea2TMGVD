#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
#include <cmath>
#include <utility>

class MRL {
    private:
        int n, k;
        float e, L;
        std::vector<std::vector<int>> A;

    public:
        MRL(int n, float e) : n(n), e(e) {
            k = (std::ceil(std::log((e*n))/ e)) + 1;
            if (k % 2 == 1) {
                k = k + 1;
            }
            L = std::ceil(std::log((n / k)));

            A.resize(L+1);
        }

        void insertar(int i) {
            A[0].push_back(i);
            int j = 0;
            while(A[j].size() == k  && j < L) {
                std::sort(A[j].begin(), A[j].end());
                for (int m = 0; m < k - 1; m += 2) {
                    A[j+1].push_back(A[j][m]);
                }
                A[j].clear();
                j++;                
            }
        }

        int rank(int x) {
            int ans = 0;
            for (int j = 0; j <= L; ++j) {
                for (const auto& z : A[j]) {
                    if (z < x) {
                        ans = ans + (1 << j);
                    }
                }
            }
            return ans;
        }

        int select(int r) {
            std::vector<std::pair<int, int>> B;
            for (int j = 0; j <= L; ++j) {
                for (const auto& z : A[j]) {
                    B.push_back(std::make_pair(z, (1 << j)));
                }
            }
            std::sort(B.begin(), B.end());

            int suma = 0;
            for (int j = 0; j < B.size(); ++j) {
                suma = suma + B[j].second;
                if (suma >= r) {
                    return B[j].first;
                }
            }
            return 0;
        }

        int quantil(float phi) {
            //quantil(phi) = select(floor(phi * n))
            int r = std::floor(phi * n);
            return select(r);
        }
        
};