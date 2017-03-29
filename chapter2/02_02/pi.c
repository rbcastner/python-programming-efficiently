
#include <math.h>
#include <stdio.h>

int main(int argc, char **argv) {
    int k;
    double acc = 0.0;
    
    for(k=0; k<10000; k++) {
        acc = acc + pow(-1,k)/(2*k+1);
    }
    
    acc = 4 * acc;
    
    printf("pi: %.15f\n",acc);
    
    return 0;
}