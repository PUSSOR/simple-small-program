#include<stdio.h>
#include<math.h>
double X[6]={0,0,0,0,0,0};    //定义全局变量X为改正数数组
double *temp;   //定义全局指针，存放各种运算中间结果
#define m 4
void ShuChu (double a[],int hang ,int lie) //输入 A 的起始地址、行数、列数，从而输出该矩阵
{

    int i;
    for(i=0;i<hang*lie;i++) //利用 for 循环输出数组
    {

        if(i%lie==0)  printf("\n"); //每行元素放满换行输出
        printf("%.6f ",a[i]); //设置输出数组中的值的小数精度（小数点后保留五位小数） }
        printf("\n");
}
}
void XiangCheng(double A[],double a1[],double a2[],int hang,int lie,int lie2 ) //矩阵乘法 hang*lie lie*lie2，hang、lie 分别为矩阵 a1 的行和列，lie、lie2 分别为矩阵 a2 的行和列，矩阵 A 用来保存 a1*a2 的结果
{

    int i,j,k;
    for(i=0;i<hang;i++) 
        for(k=0;k<lie2;k++)
            for(j=0;j<lie;j++)
                A[i*lie2+k]+=a1[i*lie+j]*a2[j*lie2+k];
}
void QiuNi(double result[][m],double a1[][m]) //定义空函数 QiuNi（只适合 lie*lie,矩阵）
{
    int k,i,j;
    double A[m][2*m]={0}; //增广矩阵，对双精度浮点型数组 A 设初始值
    for(i=0;i<m;i++)
        for(j=0;j<2*m;j++)
{
    if(j<m) A[i][j]=a1[i][j];
    else
        if((j-m)==i) A[i][j]=1;
		else A[i][j]=0;
} //定义增广矩阵
for(k=0;k<m;k++)
for(i=k+1;i<m;i++)
for(j=2*m-1;j>=k;j--) {
A[i][j]-=A[i][k]*A[k][j]/A[k][k];
} //以上化为了上三角阵
for(k=0;k<m;k++)
for(j=2*m-1;j>=k;j--)
A[k][j]=A[k][j]/A[k][k];//主对角线全部化为了 1
for(k=1;k<m;k++) 
for(i=0;i<k;i++)
for(j=2*m-1;j>=k;j--) {
A[i][j]-=A[i][k]*A[k][j];
}
for(i=0;i<m;i++)
for(j=0;j<2*m;j++)
if(j>m-1)
result[i-1][j]=A[i][j];//提取增广矩阵中的逆矩阵
}
void zhuanzhi(double *A,double *B,int hang,int lie){
	double *C=A;
	for(int i=0;i<hang;i++)
}
void getA(int n,double a[][6],double f,double xy[][2],double XYZ[][3],double R[3][3],double XYZs[][3]) //获取系数矩阵A
{
	for(int i=1;i<=n;i=i+2){
		a[i-1][0]=
	}
}
void getL()//获取常数矩阵L
{

}
void result()  //求解改正数
{

}
void dataput(float a[][n]){

}