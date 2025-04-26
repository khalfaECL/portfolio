
function robot_anim(x, y, theta, L1, L2, theta1, theta2)
% Visualisation du robot avec bras manipulateur à 2 DOF

clf;
hold on;
axis equal;
axis([-1 1 -1 1]);
grid on;

% Base du robot
rectangle('Position', [x-0.1, y-0.05, 0.2, 0.1], 'Curvature', 0.2, 'FaceColor', [0.5 0.5 0.5]);

% Affichage de la direction
quiver(x, y, cos(theta)*0.2, sin(theta)*0.2, 'r', 'LineWidth', 2);

% Position de l'épaule du bras
x1 = x + 0.1 * cos(theta);
y1 = y + 0.1 * sin(theta);

% Calcul de la position du coude
x2 = x1 + L1 * cos(theta + theta1);
y2 = y1 + L1 * sin(theta + theta1);

% Calcul de la position de l'effecteur final
x3 = x2 + L2 * cos(theta + theta1 + theta2);
y3 = y2 + L2 * sin(theta + theta1 + theta2);

% Tracé du bras
plot([x1 x2 x3], [y1 y2 y3], 'g-o', 'LineWidth', 2, 'MarkerSize', 6, 'MarkerFaceColor', 'g');

% Point de l'effecteur
plot(x3, y3, 'ko', 'MarkerSize', 8, 'MarkerFaceColor', 'k');

drawnow;
end
