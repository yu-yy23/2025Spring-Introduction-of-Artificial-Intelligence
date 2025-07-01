#include <vector>
#include <cstdlib>
#include <ctime>
#include <cmath>
#include "Point.h"
#include "Node.h"

const double TIME_LIMIT = 2 * CLOCKS_PER_SEC;
const int MAX_DEPTH = 7;

class SearchTree {
private:
    int M;
    int N;
    Point prohibitedMove;
    UCTNode* root;
public:
    SearchTree(const int m, const int n, int** _board,
        const int* _top, const Point& lastP, const Point& proP);
    Point Search();
    UCTNode* Select(UCTNode* node);
    int Simulate(UCTNode* node);
    UCTNode* BestChild(UCTNode* node, double c);
    void Backup(UCTNode* node, int result);
    UCTNode* updateRoot(const Point& lastP);
    ~SearchTree();
};