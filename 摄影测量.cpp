#include<stdio.h>
#include<math.h>
double X[6]={0,0,0,0,0,0};    //����ȫ�ֱ���XΪ����������
double *temp;   //����ȫ��ָ�룬��Ÿ��������м���
#define m 4
void ShuChu (double a[],int hang ,int lie) //���� A ����ʼ��ַ���������������Ӷ�����þ���
{

    int i;
    for(i=0;i<hang*lie;i++) //���� for ѭ���������
    {

        if(i%lie==0)  printf("\n"); //ÿ��Ԫ�ط����������
        printf("%.6f ",a[i]); //������������е�ֵ��С�����ȣ�С���������λС���� }
        printf("\n");
}
}
void XiangCheng(double A[],double a1[],double a2[],int hang,int lie,int lie2 ) //����˷� hang*lie lie*lie2��hang��lie �ֱ�Ϊ���� a1 ���к��У�lie��lie2 �ֱ�Ϊ���� a2 ���к��У����� A �������� a1*a2 �Ľ��
{

    int i,j,k;
    for(i=0;i<hang;i++) 
        for(k=0;k<lie2;k++)
            for(j=0;j<lie;j++)
                A[i*lie2+k]+=a1[i*lie+j]*a2[j*lie2+k];
}
void QiuNi(double result[][m],double a1[][m]) //����պ��� QiuNi��ֻ�ʺ� lie*lie,����
{
    int k,i,j;
    double A[m][2*m]={0}; //������󣬶�˫���ȸ��������� A ���ʼֵ
    for(i=0;i<m;i++)
        for(j=0;j<2*m;j++)
{
    if(j<m) A[i][j]=a1[i][j];
    else
        if((j-m)==i) A[i][j]=1;
		else A[i][j]=0;
} //�����������
for(k=0;k<m;k++)
for(i=k+1;i<m;i++)
for(j=2*m-1;j>=k;j--) {
A[i][j]-=A[i][k]*A[k][j]/A[k][k];
} //���ϻ�Ϊ����������
for(k=0;k<m;k++)
for(j=2*m-1;j>=k;j--)
A[k][j]=A[k][j]/A[k][k];//���Խ���ȫ����Ϊ�� 1
for(k=1;k<m;k++) 
for(i=0;i<k;i++)
for(j=2*m-1;j>=k;j--) {
A[i][j]-=A[i][k]*A[k][j];
}
for(i=0;i<m;i++)
for(j=0;j<2*m;j++)
if(j>m-1)
result[i-1][j]=A[i][j];//��ȡ��������е������
}
void zhuanzhi(double *A,double *B,int hang,int lie){
	double *C=A;
	for(int i=0;i<hang;i++)
}
void getA(int n,double a[][6],double f,double xy[][2],double XYZ[][3],double R[3][3],double XYZs[][3]) //��ȡϵ������A
{
	for(int i=1;i<=n;i=i+2){
		a[i-1][0]=
	}
}
void getL()//��ȡ��������L
{

}
void result()  //��������
{

}
void dataput(float a[][n]){

}