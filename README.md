# cvActualice.py

¿Estás mejorando tu CV y al mínimo cambio que le haces tenés que volver a actualizarlo en todos lados?  
  
**cvActualice** es una herramienta automatizada que funciona en Linux, desarrollada en Python con Selenium para actualizar el Currículum Vitae en los principales portales de empleo de Argentina.

## Instalación de requerimientos

```bash
# Creación y activación de entorno virtual
python -m venv venv 
source venv/bin/activate
# Instalación de requerimientos
pip install -r requirements.txt
```

## Ejecución

```bash
python3 cvActualice.py
```

## Demostración

![Demo](assets/cvActualice.gif)

## Notas

- El AdBlock únicamente se instala si el usuario selecciona el portal Trabajos Diarios por razones obvias.  
- La herramienta utiliza ChromeDriver que cada vez que se ejecuta, trabaja en una sesión limpia e independiente, la cuál desaparece una vez finaliza el script.
