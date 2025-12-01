import pandas as pd
import matplotlib.pyplot as plt
import glob
import os

def plot_results():
    results_dir = 'results'
    plots_dir = 'plots'
    
    # Crear carpeta de plots si no existe
    if not os.path.exists(plots_dir):
        os.makedirs(plots_dir)

    # Buscar todos los archivos CSV en la carpeta results
    files = glob.glob(os.path.join(results_dir, '*.csv'))
    
    if not files:
        print("No se encontraron archivos .csv en la carpeta 'results/'.")
        return

    print(f"Encontrados {len(files)} archivos de resultados.")

    for file in files:
        try:
            df = pd.read_csv(file)
            
            df.columns = [c.strip() for c in df.columns]
            
            type_col = 'TipoTest' if 'TipoTest' in df.columns else 'TipoExperimento'
            
            base_name = os.path.basename(file).replace('.csv', '')
            
            rank_data = df[df[type_col] == 'Rank']
            N = df['N'].iloc[0]            
            fig, axes = plt.subplots(1, 2, figsize=(16, 6))
            fig.suptitle(f'Análisis Experimental: {base_name} (N estimado $\\approx$ {N})', fontsize=16)            
            epsilons = sorted(df['Epsilon'].unique(), reverse=True)

            # Grafico de error en Rank 
            ax_rank = axes[0]
            for eps in epsilons:
                subset = rank_data[rank_data['Epsilon'] == eps].sort_values('Parametro')
                
                # Línea de Error Real
                ax_rank.plot(subset['Parametro'], subset['ErrorAbs'], marker='o', label=f'$\\epsilon={eps}$')
                
                # Línea de Límite Teórico: eps * N
                limit = eps * N
                ax_rank.axhline(y=limit, linestyle='--', alpha=0.6, color=ax_rank.get_lines()[-1].get_color(), label=f'Límite Teórico ($\\epsilon={eps}$)')

            ax_rank.set_title('Error en Consultas de Rank')
            ax_rank.set_xlabel('Valor del Dato')
            ax_rank.set_ylabel('Error Absoluto (Diferencia de Rango)')
            ax_rank.legend()
            ax_rank.grid(True, alpha=0.3)

            # Grafico de error en Quantile
            ax_quant = axes[1]
            quant_data = df[df[type_col] == 'Quantile']
            
            for eps in epsilons:
                subset = quant_data[quant_data['Epsilon'] == eps].sort_values('Parametro')
                ax_quant.plot(subset['Parametro'], subset['ErrorAbs'], marker='s', label=f'$\\epsilon={eps}$')
                        
            ax_quant.set_title('Error en Consultas de Quantile')
            ax_quant.set_xlabel('Phi (Quantil solicitado)')
            ax_quant.set_ylabel('Error Absoluto (Diferencia de Valor)')
            ax_quant.legend()
            ax_quant.grid(True, alpha=0.3)

            output_path = os.path.join(plots_dir, f'grafico_{base_name}.png')
            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()

            print(f"Gráfico guardado en: {output_path}")
        except Exception as e:
            print(f"Error procesando {file}: {e}")

if __name__ == "__main__":
    plot_results()