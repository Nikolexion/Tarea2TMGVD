#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include "mrl.h"      

using namespace std;

// Retorna el nombre base del archivo 
string getNombreBase(const string& path) {
    size_t ultimoSlash = path.find_last_of("/\\");
    if (ultimoSlash == string::npos) return path;
    return path.substr(ultimoSlash + 1);
}

// Lee los datos del archivo de texto y los carga en un vector
vector<int> cargarData(const string& filename) {
    vector<int> data;
    ifstream file(filename);
    if (!file.is_open()) {
        cerr << "Error: No se pudo abrir el archivo " << filename << endl;
        exit(1);
    }
    int val;
    while (file >> val) {
        data.push_back(val);
    }
    file.close();
    return data;
}

// Calcula el rank exacto de un valor en un dataset ordenado
int calcularRankExacto(const vector<int>& sortedData, int value) {
    // lower_bound encuentra el primer elemento >= value.
    auto it = lower_bound(sortedData.begin(), sortedData.end(), value);
    return distance(sortedData.begin(), it);
}

// Ejecuta la experimentación para un epsilon específico
void runExperiment(const vector<int>& data, const vector<int>& sortedData, float epsilon, const string& fileLabel, ofstream& csvFile) {
    int n = data.size();
    
    // Crear el sketch 
    MRL mrl(n, epsilon);
    for (int x : data) {
        mrl.insertar(x);
    }

    // Experimento de Quantiles 
    vector<float> phis = {0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 0.95}; 
    
    for (float phi : phis) {
        int estimated = mrl.quantil(phi);
        
        
        int idx = floor(phi * n);
        if (idx >= n) idx = n - 1; 
        int exact = sortedData[idx];

        int error = abs(estimated - exact);

        // Archivo, N, Epsilon, TipoExperimento, Parametro(phi), Estimado, Exacto, ErrorAbsoluto
        csvFile << fileLabel << "," << n << "," << epsilon << ",Quantile," << phi << "," << estimated << "," << exact << "," << error << endl;
    }

    // Experimento de Rank 
    // Usamos los mismos valores que obtuvimos de los quantiles reales como queries para probar el rank
    for (float phi : phis) {
        int idx = floor(phi * n);
        if (idx >= n) idx = n - 1;
        int queryValue = sortedData[idx]; 

        int estimatedRank = mrl.rank(queryValue);
        int exactRank = calcularRankExacto(sortedData, queryValue);
        
        int error = abs(estimatedRank - exactRank);

        // Guardar: Archivo, N, Epsilon, TipoExperimento, Parametro(valor), Estimado, Exacto, ErrorAbsoluto
        csvFile << fileLabel << "," << n << "," << epsilon << ",Rank," << queryValue << "," << estimatedRank << "," << exactRank << "," << error << endl;
    }
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "Uso: " << argv[0] << " <archivo_de_datos.txt>" << endl;
        return 1;
    }

    string inputPath = argv[1];
    string baseName = getNombreBase(inputPath);
    
    string outputPath = "results/resultado_" + baseName + ".csv";
    
    ofstream csvFile(outputPath);
    // Header del CSV
    csvFile << "Archivo,N,Epsilon,TipoExperimento,Parametro,Estimado,Exacto,ErrorAbs" << endl;

    cout << "Experimento para: " << baseName << endl;

    // Cargar y preparar datos
    cout << "Cargando datos" << endl;
    vector<int> data = cargarData(inputPath);
    vector<int> sortedData = data;
    cout << "Ordenando datos para Ground Truth" << endl;
    sort(sortedData.begin(), sortedData.end());

    // Ejecutar experimentos
    cout << "Ejecutando con epsilon = 0.1" << endl;
    runExperiment(data, sortedData, 0.1f, baseName, csvFile);

    cout << "Ejecutando con epsilon = 0.05" << endl;
    runExperiment(data, sortedData, 0.05f, baseName, csvFile);

    csvFile.close();
    cout << "Resultados guardados en: " << outputPath << endl;

    return 0;
}