# Predicción del Riesgo Crediticio

Al pedir un préstamo a una entidad financiera nos enfrentamos a dos problemas:
1. <strong>Disposición a pagar.</strong>
2. <strong>Capacidad económica de afrontar el pago.</strong>
#
En general hay 2 tipos de modelos de riesgo.
1. <strong>Riesgo de nuevo negocio. </strong>Se utiliza para evaluar el riesgo de las solicitudes asociadas con el primer préstamo que solicita.
2. <strong>Modelo de riesgo de repetición o comportamiento.</strong> El cliente ya contrató un préstamo y solicita uno nuevo. En este caso, tendremos información adicional sobre cómo pagó sus otros préstamos.
#
Objetivos:
1. <strong>Clustering </strong> para ver qué tipos de cliente tiene el banco.
2. <strong>Clasificador</strong> que indique si el préstamo es bueno o no.
#
<p align =center><strong>DATASETS</p></strong>

1. <strong>Datos demográficos (*train_datos_demograficos.csv*).</strong>Información sobre el cliente como edad, empleo, estudios, etc.,
2. <strong>Performance Data (*train_performance.csv*).</strong> Este conjunto de datos incluye los préstamos de los clientes que hay que predecir. Básicamente, necesitamos predecir si este préstamo pasaría el modelo dado el histórico de préstamos anteriores y los datos demográficos de un cliente.
3. <strong>Datos de préstamos anteriores (*train_previous_loan.csv*).</strong> Este dataset incluye todos los préstamos anteriores que el cliente tenía antes del préstamo anterior para el cual queremos predecir el rendimiento. Cada préstamo tendrá un systemloanid diferente, pero el mismo customerid para cada cliente.

```mermaid
flowchart LR
A[(DATASETS)] ==oB[TRAIN]
A[(DATASETS)] ==oC[TEST]
subgraph train
B[TRAIN] -.->D(performance.csv)
B[TRAIN] -.->E(demograficos.csv)
B[TRAIN] -.->F(previous_loan.csv)
end
subgraph test
C[TEST] -.->G(performance.csv)
C[TEST] -.->H(demograficos.csv)
C[TEST] -.->I(previous_loan.csv)
end
D(performance.csv) ---J[merged_files.py]
E(demograficos.csv) ---J[merged_files.py]
F(previous_loan.csv) ---J[merged_files.py]
G(performance.csv) ---J[merged_files.py]
H(demograficos.csv) ---J[merged_files.py]
I(previous_loan.csv) ---J[merged_files.py]
J[merged_files] ==oK[NOTEBOOKS]
J[merged_files] ==oL(merged_train.csv)
subgraph NOTEBOOK
K{{NB}} -->M(clustering)
K{{NB}} -->N(Feature Importance)
K{{NB}} -->O(PCA)
end
M(clustering) -->P(modelo_cluster)
N(Feature Importance) -->Q(modelo_feature_importance)
O(PCA) -->R(modelo_PCA)
L(merged_train.csv) -->S(modelo_gs)
L(merged_train.csv) -->T(modelo_base)
J[merged_files.py] ==oU(merged_test.csv)
P(modelo_cluster) -->V{compare_models.py}
Q(modelo_feature_importance) -->V{compare_models.py}
R(modelo_PCA) -->V{compare_models.py}
S(modelo_gs) -->V{compare_models.py}
T(modelo_base) -->V{compare_models.py}
U(merged_test.csv) -->V{compare_models.py}
V{compare_models.py} ==> W(((final_model)))
```