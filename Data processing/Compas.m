clear all
close all

%% Déclaration des variables
nfig=0;
% importation des datas
% [time, acc_x, acc_y, acc_z, mag_x, mag_y, mag_z] = importfile("D:\PFE\Test\Test0721\Compas.csv", [2, Inf]);
path="D:\PFE\Test\Test0724\Recording 10-39-25 24.7.2020\"
[time, acc_x, acc_y, acc_z, mag_x, mag_y, mag_z] = importCompas("D:\PFE\Test\Test0724\Recording 10-39-25 24.7.2020\Compas.csv", [2, Inf]);
% Changement de signe pour inverser x et y par rapport au compas
acc_x=-acc_x; 
acc_y=-acc_y; 
acc_z=acc_z;
mag_x=-mag_x;
mag_y=-mag_y; 
mag_z=mag_z;

%% Interpolation par un cercle sur le plan XY
[xc yx R a]=fitCircle(mag_x,mag_y);
% Tracé magy=f(magx) et interpolation


% Retirer les coordonnées du centre du cercle (Offset) et normaliser le
% vecteur magnitude
mag_x_calib=(mag_x-xc)/R;
mag_y_calib=(mag_y-yx)/R;
mag_z_calib=mag_z/R;

nfig=nfig+1;
figure(nfig);
hold on
daspect([1 1 1])
viscircles([xc,yx],R)
plot(mag_x,mag_y)
plot(mag_x_calib,mag_y_calib)

%% Filtrage Passe-bas (Savitzky-Golay)
order=2;
framelen=9;
mag_X=sgolayfilt(mag_x_calib,order,framelen);
mag_Y=sgolayfilt(mag_y_calib,order,framelen);
mag_Z=sgolayfilt(mag_z_calib,order,framelen);

nfig=nfig+1;
figure(nfig);
daspect([1 1 1])
hold on
plot(mag_x_calib,mag_y_calib);
plot(mag_X,mag_Y);
legend('Données calibrées', 'Données calibrées et filtrées')
%% Détermination des angles Roll (Roulis) et Pitch (Tangage)
% Dans le cas du robot : Roll (autour de X)   Pitch (autour de Y)  Yaw (autour de Z)
Pitch = sgolayfilt(atan(acc_x./sqrt(acc_z.^2+acc_y.^2)),order,framelen);
Roll =  sgolayfilt(atan(acc_y./sqrt(acc_z.^2+acc_x.^2)),order,framelen); 

%% Tilt Compensation 
mag_X_comp = mag_X.*cos(Pitch) + mag_Y.*sin(Roll).*sin(Pitch);% + mag_Z.*cos(Roll).*sin(Pitch);
mag_Y_comp = mag_Y.*cos(Roll);% - mag_Z.*sin(Roll);

nfig=nfig+1;
figure(nfig);
compass(mag_X_comp,mag_Y_comp)

%% Calcul du cap en radians
heading = atan2(mag_Y_comp,mag_X_comp);
nfig=nfig+1;
figure(nfig);
daspect([1 1 1])
plot(time-time(1),heading*180/pi)
title('Heading (deg) en fonction du temps (s)')
grid on


% Import des données des codeurs
CodeurA = importCodeur(path + "CodeurA.csv",2);
CodeurB = importCodeur(path + "CodeurB.csv",2);
% Filtrage des donées des codeurs
order=2;
framelen=3;
CodeurA.dist = sgolayfilt(CodeurA.dist,order,framelen);
CodeurB.dist = sgolayfilt(CodeurB.dist,order,framelen);

% Rééchantillonnage de CodeurB et Compas pour avoir le même vecteur de
% temps pour les 3 sets de donnes
timeA=CodeurA.time;
CodeurA=CodeurA.dist;
heading=interp1(time,heading,timeA);
CodeurB=interp1(CodeurB.time,CodeurB.dist,timeA);
%CodeurB(1)=0;
PosX=0;
PosY=0;

% Calcule de la distance moyenne
dist=(CodeurA+CodeurB)/2;
dist(1)=0
% Calcul des positions du robot grâce à l'intégration du chemin
for i=2:size(timeA,1)
    PosX=[PosX ; PosX(i-1)+dist(i-1)*cos(heading(i-1))];
    PosY=[PosY ;PosY(i-1)+dist(i-1)*sin(heading(i-1))];
end

nfig=nfig+1;
figure(nfig);
daspect([1 1 1])
plot(PosX,PosY)
title('Déplacements du robot dans le plan XY')