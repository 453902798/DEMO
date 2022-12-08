function [y_RBF,error,net] = RBF(x,y)
    goal = 10e-20;
    spread = 1.0;
    MN = 100;
    DF = 2;
    net = newrb(x,y,goal,spread,MN,DF);
    y_RBF = sim(net,x);
    error = abs(y_RBF - y);
end

