
% InitRobotAndEnvironment.m
% Initialisation du robot suiveur de ligne avec bras manipulateur

% Paramètres physiques
L = 0.2;             % Distance entre les roues [m]
L1 = 0.15;           % Longueur du premier segment du bras [m]
L2 = 0.1;            % Longueur du second segment du bras [m]

% Paramètres du contrôleur
omega = 3;           % pulsation propre
xi = 0.8;            % amortissement
alpha = 1 / L;
ki_theta = omega^2 / alpha;
kp_theta = 2 * xi * omega / alpha;

% Position initiale
x0 = 0;
y0 = 0;
theta0 = 0;

% Orientation sommet 1, 2, 3 du triangle (en radians)
angles_triangle = [0, -2*pi/3, 2*pi/3];

% Charge les paramètres dans le workspace
assignin('base', 'L', L);
assignin('base', 'L1', L1);
assignin('base', 'L2', L2);
assignin('base', 'kp_theta', kp_theta);
assignin('base', 'ki_theta', ki_theta);
assignin('base', 'x0', x0);
assignin('base', 'y0', y0);
assignin('base', 'theta0', theta0);
assignin('base', 'angles_triangle', angles_triangle);

disp('Environnement initialisé.');
