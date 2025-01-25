#include <iostream>
#include <algorithm>
using namespace std;

void mergeArrays(int** arrays, int* sizes, int numArrays, int* result, int& resultSize) {
    resultSize = 0;

    for (int i = 0; i < numArrays; i++) {
        for (int j = 0; j < sizes[i]; j++) {
            result[resultSize++] = arrays[i][j];
        }
    }

    sort(result, result + resultSize);
}

int main() {
    int numArrays;
    cout << "Enter the number of arrays you want to merge: ";
    cin >> numArrays;

    if (numArrays <= 0) {
        cout << "Invalid number of arrays!" << endl;
        return 1;
    }

    int* sizes = new int[numArrays];
    int** arrays = new int*[numArrays];


    for (int i = 0; i < numArrays; i++) {
        cout << "Enter the size of array " << i + 1 << ": ";
        cin >> sizes[i];

        if (sizes[i] <= 0) {
            cout << "Invalid size for array " << i + 1 << "!" << endl;
            return 1;
        }

        arrays[i] = new int[sizes[i]];

        cout << "Enter the elements of array " << i + 1 << ": ";
        for (int j = 0; j < sizes[i]; j++) {
            cin >> arrays[i][j];
        }

        sort(arrays[i], arrays[i] + sizes[i]);
    }

    int totalSize = 0;
    for (int i = 0; i < numArrays; i++) {
        totalSize += sizes[i];
    }

    int* result = new int[totalSize];
    int resultSize;


    mergeArrays(arrays, sizes, numArrays, result, resultSize);


    cout << "The merged and sorted array is: ";
    for (int i = 0; i < resultSize; i++) {
        cout << result[i] << " ";
    }
    cout << endl;


    for (int i = 0; i < numArrays; i++) {
        delete[] arrays[i];
    }
    delete[] arrays;
    delete[] sizes;
    delete[] result;

    return 0;
}
