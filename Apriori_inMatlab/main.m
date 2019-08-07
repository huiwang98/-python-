clear;clc;
inputfile = 'apriori_task.txt'; 
outputfile='outputFreq.txt';
minSup = 0.06; 
minConf = 0.75;
nRules = 1000000;% 输出最大规则数
sortFlag = 1;% 按支持度排序
rulefile = 'outputRules.txt'; 
[transactions,code] = trans2matrix(inputfile,outputfile,','); %把数据转换为0,1矩阵
[Rules,FreqItemsets] = findRules(transactions, minSup, minConf, nRules, sortFlag, code, rulefile);
disp('Apriori算法挖掘菜品订单关联规则完成！');
