clear;clc;
inputfile = 'apriori_task.txt'; 
outputfile='outputFreq.txt';
minSup = 0.06; 
minConf = 0.75;
nRules = 1000000;% �����������
sortFlag = 1;% ��֧�ֶ�����
rulefile = 'outputRules.txt'; 
[transactions,code] = trans2matrix(inputfile,outputfile,','); %������ת��Ϊ0,1����
[Rules,FreqItemsets] = findRules(transactions, minSup, minConf, nRules, sortFlag, code, rulefile);
disp('Apriori�㷨�ھ��Ʒ��������������ɣ�');
