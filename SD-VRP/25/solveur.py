import numpy as np
import pulp
from math import ceil, floor

N = 33

for case in range(N):
    # Chemin du fichier d'entrée
    file_path = f"Instances/Case{case}.txt"

    lines = []

    # Lecture du fichier
    with open(file_path, 'r') as file:
        lines = [line for line in file.readlines() if line.strip()]

    # Extraction des informations de la première ligne
    first_line = lines[0].strip().split()
    n, Q = map(int, lines[0].split(" "))

    # Extraction des informations de la deuxième ligne
    ci = [int(x) for x in lines[1].split(" ") if x != "\n" and x != ""]  # Demandes de chaque client

    # Extraction de la matrice des coordonnées à partir de la troisième ligne
    coordinates = []
    for line in lines[2:]:
        coordinates.append([int(x) for x in line.split(" ") if x != "\n" and x != ""])

    # Conversion en tableau NumPy pour des manipulations faciles
    coordinates = np.array(coordinates)

    # Calcul de la matrice des distances
    num_nodes = len(coordinates)
    distance_matrix = np.zeros((num_nodes, num_nodes))

    for i in range(num_nodes):
        for j in range(num_nodes):
            xi, yi = coordinates[i]
            xj, yj = coordinates[j]
            distance_matrix[i, j] = floor(np.sqrt((xj - xi)**2 + (yj - yi)**2) + 0.5)

    # Impression des résultats
    print(f"Nombre de clients (n) : {n}")
    print(f"Capacité de chaque véhicule (Q) : {Q}")
    print(f"Demandes de chaque client (ci) : {ci}")
    print("\nMatrice des distances :")
    print(distance_matrix)

    # Calcul du nombre minimal de véhicules nécessaires
    M = ceil(sum(ci) / Q) # Calcul du nombre minimal de véhicules nécessaires
    print(f"Nombre minimal de véhicules nécessaires (M) : {M}")

    if sum(ci) > M * Q:
        print("Problème infaisable : la somme des demandes dépasse la capacité totale des véhicules.")
        continue

    # Créer le problème
    prob = pulp.LpProblem("SD-VRP", pulp.LpMinimize)

    # Variables de décision
    x = pulp.LpVariable.dicts("x", ((i, j, k) for i in range(n+1) for j in range(n+1) for k in range(1, M+1)), cat="Binary")
    y = pulp.LpVariable.dicts("y", ((i, k) for i in range(1, n+1) for k in range(1, M+1)), lowBound=0)
    #u = pulp.LpVariable.dicts("u", ((i, k) for i in range(1, n+1) for k in range(1, M+1)), lowBound=1, upBound=n)

    # Objectif : minimiser la somme des distances parcourues par tous les véhicules
    prob += pulp.lpSum(
        distance_matrix[i][j] * x[i, j, k]
        for k in range(1, M+1)
        for i in range(n+1)
        for j in range(n+1)
        if i != j
    )

    # Contraintes

    # 1. Satisfaction de la demande des clients
    for i in range(1, n+1):
        prob += pulp.lpSum(y[i, k] for k in range(1, M+1)) == ci[i-1]

    # 2. Capacité des véhicules
    for k in range(1, M+1):
        prob += pulp.lpSum(y[i, k] for i in range(1, n+1)) <= Q

    # 3. Flux entrant et sortant pour chaque client
    for i in range(1, n+1):
        for k in range(1, M+1):
            prob += pulp.lpSum(x[i, j, k] for j in range(n+1)) == pulp.lpSum(x[j, i, k] for j in range(n+1))

    # 4. Flux depuis et vers le dépôt (0)
    for k in range(1, M+1):
        prob += pulp.lpSum(x[0, j, k] for j in range(1, n+1)) == 1
        prob += pulp.lpSum(x[j, 0, k] for j in range(1, n+1)) == 1

    # 5. Compatibilité des trajets et livraisons
    for i in range(1, n+1):
        for k in range(1, M+1):
            prob += y[i, k] <= Q * pulp.lpSum(x[i, j, k] for j in range(n+1))

    
    # 6. Chaque client doit être visité exactement une fois
    for i in range(1, n+1):
        prob += pulp.lpSum(x[i, j, k] for j in range(n+1) for k in range(1, M+1)) == 1

    
    # 7. Interdire les boucles inutiles
    for i in range(n+1):
        for k in range(1, M+1):
            prob += x[i, i, k] == 0

    """
    # 8. Contraintes MTZ
    for i in range(1, n+1):
        for k in range(1, M+1):
            prob += pulp.lpSum(u[i, k] - u[j, k] + (n - 1) * x[i, j, k] <= n - 2 for j in range(1, n+1))
    """

    # Résoudre le problème avec une limite de temps
    time_limit = 1000
    solver = pulp.PULP_CBC_CMD(timeLimit=time_limit, msg = False)
    prob.solve(solver)

    # Validation et recalcul du coût après résolution
    # Validation et recalcul du coût après résolution
    if pulp.LpStatus[prob.status] == "Optimal":
        truck_loads = [0] * M
        deliveries = 0
        output = []

        # Affichage des segments actifs et calcul des coûts
        for k in range(1, M+1):
            route = [(0, 0)]  # Départ du dépôt
            route_cost = 0
            for i in range(n+1):
                for j in set(range(i)).union(set(range(i + 1, n + 1))):
                    if pulp.value(x[i, j, k]) > 0:
                        if j != 0 and y[j, k].varValue != 0:
                            deliveries += 1
                            route.append((j, int(y[j, k].varValue)))
                            truck_loads[k-1] += ci[j-1]
            if route[-1] != (0, 0):
                route.append((0, 0))  # Retour au dépôt si nécessaire
            output.append(f"Route {k}: {' - '.join(map(lambda X : f"{str(X[0])} ({str(X[1])})" if X[0] != 0 else "0", route))}")
        output.append(f"Total cost: {int(pulp.value(prob.objective))}")
        output.append(f"Number of deliveries: {deliveries}")
        output.append(f"Truck loads: {' '.join(map(str, truck_loads))}")
    else:
        output = ["Aucune solution realisable trouvee dans la limite de temps."]

    # Sauvegarde dans un fichier
    solution_file = f"SolutionsPulp/Solution{case}.txt"
    with open(solution_file, "w") as file:
        file.write("\n".join(output))

    print("\n".join(output))  # Affiche la solution
    print(f"La solution a été enregistrée dans '{solution_file}'.")