filename = "C:\Users\CJ\Documents\Grad_2022-23\ECE577\Project1\BFS_NewEngland_Results.txt";
BFS_results = readtable(filename);
filename = "C:\Users\CJ\Documents\Grad_2022-23\ECE577\Project1\BD_NewEngland_Results.txt";
BD_results = readtable(filename);

%%
close all

figure
scatter((BFS_results{:,4}), BFS_results{:,5}, 'filled')
hold on
scatter((BD_results{:,4}), BD_results{:,5}, 'filled')
ylabel("Execution time (sec)"); xlabel("Depth");
legend(["Breadth First Search", "Bidirectional BFS"])
title("Execution Time vs Depth for All NE Towns");

figure
scatter((BFS_results{:,4}), BFS_results{:,7}, 'filled')
hold on
scatter((BD_results{:,4}), BD_results{:,7}, 'filled')
ylabel("Nodes Expanded"); xlabel("Depth");
legend(["Breadth First Search", "Bidirectional BFS"])
title("Nodes Expanded vs Depth for All NE Towns");

%%
close all
clc
cities = ["New Haven","NYC","DC","Atlanta","New Orleans"];
BFS_time = [0.011 0.045 .154 .358 .510];
UCS_time = [0.02 0.12 .44 1.29 1.75];
BS_time = [0.007 0.028 .085 0.2 0.26];

BFS_cost = [190.6 175 380 952 1399];
UCS_cost = [107 171 373 921 1350];
BS_cost = [109.0689625693378 177.31783130724142 379.4200205131183 949.8028452724762 1403.3787378594343];

BFS_Nodes = [316 720 3410 10356 18555];
UCS_Nodes = [435 1150 3772 10834 18720];
BS_Nodes = [317 1188 3191 9934 13766];
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
title("Runtime vs Cities")
grid on

figure
plot(BFS_cost,'-ob','Linewidth',1.5)
hold on 
plot(UCS_cost,'-or','Linewidth',1.5)
hold on 
plot(BS_cost,'-ok','Linewidth',1.5)
set(gca, 'XTick', 1:length(cities), 'XTickLabel', cities);
xlabel('Destinations','fontweight','bold','fontsize',10)
ylabel('Total Path Cost (total mileage)','fontweight','bold','fontsize',10)
legend("BFS","UCS","BD",'Location','Northwest')
title("Path Cost vs Cities")
grid on

figure
plot(BFS_Nodes,'-ob','Linewidth',1.5)
hold on 
plot(UCS_Nodes,'-or','Linewidth',1.5)
hold on 
plot(BS_Nodes,'-ok','Linewidth',1.5)
set(gca, 'XTick', 1:length(cities), 'XTickLabel', cities);
xlabel('Destinations','fontweight','bold','fontsize',10)
ylabel('Nodes Explored','fontweight','bold','fontsize',10)
legend("BFS","UCS","BD",'Location','Northwest')
title("Nodes vs Cities")
grid on