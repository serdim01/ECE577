clear all
close all
clc
cities = ["New Haven","NYC","DC","Atlanta","New Orleans"];
BFS_time = [0.011 0.045 .154 .358 .510];
UCS_time = [0.02 0.12 .44 1.29 1.75];
BS_time = [0.007 0.028 .085 0.2 0.26];

BFS_cost = [190.6 175 380 952 1399];
UCS_cost = [107 171 373 921 1350];
BS_cost = [107 171 373 921 1350];

figure
plot(BFS_time,'-ob','Linewidth',1.5)
hold on 
plot(UCS_time,'-or','Linewidth',1.5)
hold on 
plot(BS_time,'-ok','Linewidth',1.5)

set(gca, 'XTick', 1:length(cities), 'XTickLabel', cities);
xlabel('Destinations','fontweight','bold','fontsize',10)
ylabel('Execution Time (sec)','fontweight','bold','fontsize',10)
legend("BFS","UCS","BD",'Location','Northwest')
grid on

figure
plot(BFS_cost,'-ob','Linewidth',1.5)
hold on 
plot(UCS_cost,'-or','Linewidth',1.5)
hold on 
plot(BS_cost,'-ok','Linewidth',1.5)
set(gca, 'XTick', 1:length(cities), 'XTickLabel', cities);
xlabel('Destinations','fontweight','bold','fontsize',10)
ylabel('Cumulative Cost (total mileage)','fontweight','bold','fontsize',10)
legend("BFS","UCS","BD",'Location','Northwest')
grid on
