from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

datos_tabla = []

@app.route('/')
def index():
    return render_template('index.html', hours=range(1, 25))


@app.route('/generar_json', methods=['POST'])
def generar_json():
    data = request.json

    json_data = {
        'horas': data['horas'],
        'pagos': data['pagos'],
        'cobros': data['cobros']
    }

    # Verificar si hay valores nulos
    for hora, pago, cobro in zip(json_data['horas'], json_data['pagos'], json_data['cobros']):
        if pago is None or cobro is None:
            enviar_alerta_telegram(hora)
            break

    return jsonify(json_data)


@app.route('/actualizar_datos', methods=['POST'])
def actualizar_datos():
    data = request.json

    # Actualizar los datos de la tabla
    for item in datos_tabla:
        if item['hora'] == data['hora']:
            item['pago'] = data['pago']
            item['cobro'] = data['cobro']
            break

    return jsonify({'success': True})


@app.route('/eliminar_datos', methods=['POST'])
def eliminar_datos():
    hora = request.json['hora']

    # Eliminar los datos de la tabla
    for item in datos_tabla:
        if item['hora'] == hora:
            datos_tabla.remove(item)
            break

    return jsonify({'success': True})


def enviar_alerta_telegram(hora):
    telegram_token = '7175960946:AAF6cB8h8JWE3JgYeEeSySxqU_BWCgT3bo8'
    chat_id = '5774884694'

    mensaje = f"No se generó pago y/o cobro a las {hora}:00 horas."

    try:
        requests.post('https://api.telegram.org/bot'+telegram_token+'/sendMessage', data={'chat_id': chat_id, 'text': mensaje})
        print("Alerta enviada a Telegram con éxito.")
    except Exception as e:
        print(f"Error al enviar la alerta a Telegram: {str(e)}")

if __name__ == '__main__':
    app.run(debug=True)