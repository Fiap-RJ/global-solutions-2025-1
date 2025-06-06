# app/main.py
from fastapi import FastAPI
from app.api import routes as api_routes # Importa o módulo de rotas

# --- Inicialização da Aplicação FastAPI ---
app = FastAPI(
    title="API de Análise de Risco Climático Modular",
    description="Uma API modular que utiliza um modelo de Machine Learning para prever o risco climático instantâneo com base na temperatura e umidade.",
    version="1.1.0",
    # Adicione outras configurações globais da app aqui se necessário
    # openapi_tags=[ # Exemplo de como definir tags globais para a documentação
    #     {
    #         "name": "Predictions",
    #         "description": "Endpoints relacionados à predição de risco climático.",
    #     },
    #     {
    #         "name": "Utilities",
    #         "description": "Endpoints de utilidade, como verificação de saúde.",
    #     },
    # ]
)

# --- Inclusão dos Roteadores ---
# Inclui todas as rotas definidas em app.api.routes
# Você pode adicionar um prefixo comum para todas essas rotas, se desejar
# Ex: app.include_router(api_routes.router, prefix="/api/v1")
app.include_router(api_routes.router)


# --- Endpoint Raiz (Opcional, pode estar em routes.py também) ---
@app.get("/", summary="Endpoint Raiz", include_in_schema=False) # include_in_schema=False para não poluir /docs
async def read_root():
    return {"message": "Bem-vindo à API de Análise de Risco Climático Modular. Acesse /docs para a documentação interativa."}

# Para rodar esta aplicação (a partir da pasta raiz 'climate_risk_api/'):
# 1. Certifique-se de que o modelo 'climate_risk_classifier_model.pkl' está em 'climate_risk_api/ml_models/'.
# 2. No terminal, execute:
#    uvicorn app.main:app --reload
#
#    Isso informa ao uvicorn para procurar o objeto 'app' dentro do arquivo 'main.py' que está no pacote 'app'.