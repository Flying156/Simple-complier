void  main()
{
    int a=2;
    int b=3;
    int c=0;
    int d=1;
    scanf(a);
    c = d-a;
    b = d + a;
    c = b * a;
    d = a / b;
    if(a > b){
        d = a + b;
    }else{
        c = b + a;
    }

    printf(c);
    return 0;
}