from flask import Flask, request, render_template
import re

app = Flask(__name__)

def convertir_enteros_a_decimales(texto):
    def reemplazo(match):
        numero = match.group(0)
        # Comprobar si es un entero
        if re.match(r'^\d+$', numero):
            return f"{numero}.00"
        return numero
    
    # Buscar números enteros y flotantes
    patron = re.compile(r'\b\d+(\.\d+)?\b')
    resultado = patron.sub(reemplazo, texto)
    return resultado

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convertir', methods=['POST'])
def convertir():
    entrada = request.form.get('entrada', '')
    lineas = entrada.split('\n')
    productos = []
    
    for linea in lineas:
        partes = linea.split()
        if len(partes) >= 2:
            descripcion = ' '.join(partes[:-1])
            precio = partes[-1]
            precio_convertido = convertir_enteros_a_decimales(precio)
            precio_float = float(precio)
            iva = precio_float * 0.16
            iva_convertido = f"{iva:.2f}"
            total = precio_float + iva
            total_convertido = f"{total:.2f}"
            productos.append({
                'descripcion': descripcion,
                'precio': precio,
                'iva': f"{iva:.2f}",
                'precio_convertido': precio_convertido,
                'iva_convertido': iva_convertido,
                'total_convertido': total_convertido
            })
    
    return render_template('index.html', entrada=entrada, productos=productos)

if __name__ == '__main__':
    app.run(debug=True)
