/******************************************************************************

                            Online C Compiler.
                Code, Compile, Run and Debug C program online.
Write your code in this editor and press "Run" button to compile and execute it.

*******************************************************************************/

#include <stdio.h>
#include <stdlib.h>
typedef struct element{
    int valor;
    void *proximo;
}element;
typedef struct front{
    element* head;
    void *proximo;
}front;
void imprime(element *s){
    element *aux = s;
    while(aux!=NULL){
        printf("%d ->", aux->valor);
        aux = aux ->proximo;
    }
    printf("\n");
}
front* add_front(front* inicial, element* front_head){
    front* aux = inicial;
    front* novo = (front*) malloc(sizeof(front));
    novo->head= front_head;
    novo->proximo = NULL;
    if(aux == NULL){
        s = novo;
    }else{
        while(aux->proximo!=NULL){
            aux = aux->proximo;
        }
        aux->proximo = novo;
    }
    return inicial;
}
element* add_element(element* s, int val_el){
    element* aux = s;
    element* el = (element*) malloc(sizeof(element));
    el->valor = val_el;
    el->proximo = NULL;
    if(aux == NULL){
        s = el;
    }else{
        while(aux->proximo!=NULL){
            aux = aux->proximo;
        }
        aux->proximo = el;
    }
    return s;
}


front* fnds(float[][] y, int n,int m){
    element* S[n];
    int np[n];
    int i,j,dom;
    front* inicial = (front*)malloc(sizeof(front))
    inicial->head = NULL;
    inicial->proximo = NULL;
    for(i=0; i<n; i++){
        S[i] = NULL;
        np[i] = 0; 
    }
    for(i=0; i<n-1;i++){
        for(j=i+1; i<n; j++){
            dom = domina(y[i], y[j]);
            if(dom == 1){
                S[i] = add_element(S[i],j);
                np[j] = np[j] + 1;
            }else if(dom == -1){
                S[j] = add_element(S[j],i);
                np[i] = np[i] + 1;
            }
        }
        if(np[i]==0){
            inicial->head = add_element(inicial->head,i);
        }
        front* aux = inicial;
        while aux->head != NULL{
            element* novo = NULL;
            
        }
    }
    S[0] = add_element(S[0], 10);
    imprime(S[0]);
    S[0] = add_element(S[0], 2);
    imprime(S[0]);
    return 1;
}
int domina(int a[], int b[], int n){
    int i = 0;
    int best_is_one = 0;
    int best_is_two = 0;
    for(i = 0; i < n; i++){
        if(a[i] < b[i]){
            best_is_one = 1;
        }else if(a[i] > b[i]){
            best_is_two = 1;
        }
        
    }
    if(best_is_one > best_is_two){
        return 1;
    }
    if(best_is_one < best_is_two){
        return -1;
    }
    return 0;
}
int main()
{
    printf("Hello World");
    int a[3] = {0,0,1};
    int b[3] = {0,1,2};
    fnds(5,6);
    return 0;
}

