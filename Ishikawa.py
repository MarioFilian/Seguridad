from flask import Flask, request, render_template
import openai
import os
from dotenv import load_dotenv
#cambio

def crear_app():
    
    load_dotenv()

    app = Flask(__name__)

    openai.api_key = os.getenv("openai.api_key")

    def generar_causas(problema):
        categorias = ["Gente", "Procesos", "Tecnología", "Ambiente"]
        causas = {}
        
        for categoria in categorias:
            prompt = (f"Identifica las posibles causas relacionadas con '{categoria}' "
                    f"para el siguiente problema de ciberseguridad: '{problema}'.")
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en ciberseguridad y realizas un análisis basado en el método Ishikawa."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0
            )
            causas[categoria] = response.choices[0].message.content
        return causas

    def generar_recomendaciones(causas):
        recomendaciones = {}
        
        for categoria, causa in causas.items():
            prompt = (f"Ofrece recomendaciones para abordar las causas de '{categoria}' "
                    f"en el siguiente problema de ciberseguridad: '{causa}'.")
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Eres un experto en ciberseguridad y realizas un análisis basado en el método Ishikawa."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=0.5,
                presence_penalty=0
            )
            recomendaciones[categoria] = response.choices[0].message.content
        return recomendaciones

    @app.route('/', methods=['GET', 'POST'])

    def index():
        if request.method == 'POST':
         problema = request.form['problema']
         causas = generar_causas(problema)
         recomendaciones = generar_recomendaciones(causas)
         return render_template('index.html', causas=causas, recomendaciones=recomendaciones, problema=problema)
        return render_template('index.html')
    return app

if __name__ == '__main__':
    app= crear_app()
    app.run(debug=True)
