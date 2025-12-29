<<<<<<< HEAD
#include <stdio.h>

void spirital(int matrix[6][6], int top, int bottom, int left, int right){
    int i;
    while(top<=bottom && left<=right){
        for(i=left; i<=right; i++){
            printf("%d ", matrix[top][i]);
        }
        top++;

        for(i=top; i<=bottom; i++){
            printf("%d ", matrix[i][right]);
        }
        right--;

        if(top<=bottom){
            for(i=right; i>=left; i--){
                printf("%d ", matrix[bottom][i]);
            }
            bottom--;
        }

        if(left<=right){
            for(i=bottom; i>=top; i--){
                printf("%d ", matrix[i][left]);
            }
            left++;
        }
    }
}

int main(){
    int matrix[6][6] = {
        {1, 2, 3, 4, 5, 6},
        {7, 8, 9, 10, 11, 12},
        {13, 14, 15, 16, 17, 18},
        {19, 20, 21, 22, 23, 24},
        {25, 26, 27, 28, 29, 30},
        {31, 32, 33, 34, 35, 36}
    };

    spirital(matrix, 0, 5, 0, 5);
    printf("\n");

    return 0;
}
=======
#include <stdio.h>

void spirital(int matrix[6][6], int top, int bottom, int left, int right){
    int i;
    while(top<=bottom && left<=right){
        for(i=left; i<=right; i++){
            printf("%d ", matrix[top][i]);
        }
        top++;

        for(i=top; i<=bottom; i++){
            printf("%d ", matrix[i][right]);
        }
        right--;

        if(top<=bottom){
            for(i=right; i>=left; i--){
                printf("%d ", matrix[bottom][i]);
            }
            bottom--;
        }

        if(left<=right){
            for(i=bottom; i>=top; i--){
                printf("%d ", matrix[i][left]);
            }
            left++;
        }
    }
}

int main(){
    int matrix[6][6] = {
        {1, 2, 3, 4, 5, 6},
        {7, 8, 9, 10, 11, 12},
        {13, 14, 15, 16, 17, 18},
        {19, 20, 21, 22, 23, 24},
        {25, 26, 27, 28, 29, 30},
        {31, 32, 33, 34, 35, 36}
    };

    spirital(matrix, 0, 5, 0, 5);
    printf("\n");

    return 0;
}
>>>>>>> 02297afcddcad879a453ccb4c6175697dc0edd72
