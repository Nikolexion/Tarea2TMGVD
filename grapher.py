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
            
            # Limpiar nombres de columnas por si hay espacios
            df.columns = [c.strip() for c in df.columns]
            
            type_col = 'TipoTest' if 'TipoTest' in df.columns else 'TipoExperimento'
            
            base_name = os.path.basename(file).replace('.csv', '')
            
            # Datos filtrados
            rank_data = df[df[type_col] == 'Rank']
            quant_data = df[df[type_col] == 'Quantile']
            
            N = df['N'].iloc[0]            
            
            # --- MODIFICACIÓN: Creamos una grilla de 2 filas x 2 columnas ---
            fig, axes = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle(f'Análisis Experimental: {base_name} (N={N})', fontsize=16)            
            
            epsilons = sorted(df['Epsilon'].unique(), reverse=True)

            # ==========================================
            # FILA 1: ERROR ABSOLUTO (Original)
            # ==========================================
            
            # --- 1. Rank Error Absoluto ---
            ax_rank_abs = axes[0, 0]
            for eps in epsilons:
                subset = rank_data[rank_data['Epsilon'] == eps].sort_values('Parametro')
                
                # Línea de Error
                ax_rank_abs.plot(subset['Parametro'], subset['ErrorAbs'], marker='o', label=f'$\\epsilon={eps}$')
                
                # Línea de Límite Teórico: eps * N
                limit = eps * N
                ax_rank_abs.axhline(y=limit, linestyle='--', alpha=0.6, color=ax_rank_abs.get_lines()[-1].get_color(), label=f'Límite ($\\epsilon={eps}$)')

            ax_rank_abs.set_title('Error Absoluto en Consultas de Rank')
            ax_rank_abs.set_xlabel('Valor del Dato')
            ax_rank_abs.set_ylabel('Error Absoluto')
            ax_rank_abs.legend()
            ax_rank_abs.grid(True, alpha=0.3)

            # --- 2. Quantile Error Absoluto ---
            ax_quant_abs = axes[0, 1]
            for eps in epsilons:
                subset = quant_data[quant_data['Epsilon'] == eps].sort_values('Parametro')
                ax_quant_abs.plot(subset['Parametro'], subset['ErrorAbs'], marker='s', label=f'$\\epsilon={eps}$')
                        
            ax_quant_abs.set_title('Error Absoluto en Consultas de Quantile')
            ax_quant_abs.set_xlabel('Phi (Quantil solicitado)')
            ax_quant_abs.set_ylabel('Error Absoluto')
            ax_quant_abs.legend()
            ax_quant_abs.grid(True, alpha=0.3)

            # ==========================================
            # FILA 2: ERROR RELATIVO (Nuevo)
            # ==========================================

            # --- 3. Rank Error Relativo ---
            ax_rank_rel = axes[1, 0]
            for eps in epsilons:
                subset = rank_data[rank_data['Epsilon'] == eps].sort_values('Parametro')
                # Usamos ErrorRel en lugar de ErrorAbs
                ax_rank_rel.plot(subset['Parametro'], subset['ErrorRel'], marker='o', linestyle='--', label=f'$\\epsilon={eps}$')
                
            ax_rank_rel.set_title('Error Relativo en Consultas de Rank')
            ax_rank_rel.set_xlabel('Valor del Dato')
            ax_rank_rel.set_ylabel('Error Relativo')
            ax_rank_rel.legend()
            ax_rank_rel.grid(True, alpha=0.3)

            # --- 4. Quantile Error Relativo ---
            ax_quant_rel = axes[1, 1]
            for eps in epsilons:
                subset = quant_data[quant_data['Epsilon'] == eps].sort_values('Parametro')
                # Usamos ErrorRel en lugar de ErrorAbs
                ax_quant_rel.plot(subset['Parametro'], subset['ErrorRel'], marker='s', linestyle='--', label=f'$\\epsilon={eps}$')
                        
            ax_quant_rel.set_title('Error Relativo en Consultas de Quantile')
            ax_quant_rel.set_xlabel('Phi (Quantil solicitado)')
            ax_quant_rel.set_ylabel('Error Relativo')
            ax_quant_rel.legend()
            ax_quant_rel.grid(True, alpha=0.3)

            # Guardar
            output_path = os.path.join(plots_dir, f'grafico_{base_name}.png')
            plt.tight_layout()
            plt.savefig(output_path)
            plt.close()

            print(f"Gráfico guardado en: {output_path}")
        except Exception as e:
            print(f"Error procesando {file}: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    plot_results()