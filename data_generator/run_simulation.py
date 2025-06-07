# /data_generator/run_simulation.py

from src.simulation import generate_simulation_data, save_data_to_csv
from src.config import NUM_SAMPLES, OUTPUT_PATH, OUTPUT_FILENAME


def main():
    """Função principal para orquestrar a geração de dados."""
    print("Iniciando a simulação para geração de dados...")

    simulated_df = generate_simulation_data(num_samples=NUM_SAMPLES)

    # 2. Mostra um resumo dos dados gerados
    print(simulated_df.head())
    print(
        "\nDistribuição dos Rótulos:\n%s",
        simulated_df["risk_label"].value_counts(normalize=True).sort_index(),
    )
    save_data_to_csv(df=simulated_df, path=OUTPUT_PATH, filename=OUTPUT_FILENAME)


if __name__ == "__main__":
    main()
