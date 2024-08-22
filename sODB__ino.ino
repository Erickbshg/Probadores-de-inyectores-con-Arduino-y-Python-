//definimos los pines para los inyectores 
const int inyector1 = 2; 
const int inyector2 = 3;
const int inyector3 = 4;
const int inyector4 = 5;

//Variables para contor de orden y velocidad 
int orden [4] = {0, 1, 2, 3}; //orden por defecto 
int velocidad = 500; //Tiempo por milesegundos de inicio 

//Funcion para activar el inyector 
void activarInyector(int inyector) {
  digitalWrite(inyector, HIGH);
  delay(10); //Duracion en milese.
  digitalWrite(inyector, LOW);
}

void setup() {
    // Configurar los pines como salida
    pinMode(inyector1, OUTPUT);
    pinMode(inyector2, OUTPUT);
    pinMode(inyector3, OUTPUT);
    pinMode(inyector4, OUTPUT);

    Serial.begin(9600);
}
void loop() {
    // Leer la entrada serial para cambiar el orden o la velocidad
    if (Serial.available() > 0) {
        char command = Serial.read();
        if (command == 'v') { // Cambiar velocidad
            velocidad = Serial.parseInt();
        } else if (command == 'o') { // Cambiar orden
            for (int i = 0; i < 4; i++) {
                orden[i] = Serial.parseInt();
            }
        }
    }

    // Activar los inyectores en el orden especificado
    for (int i = 0; i < 4; i++) {
        int inyector = orden[i];
        switch (inyector) {
            case 0:
                activarInyector(inyector1);
                break;
            case 1:
                activarInyector(inyector2);
                break;
            case 2:
                activarInyector(inyector3);
                break;
            case 3:
                activarInyector(inyector4);
                break;
        }
        delay(velocidad); // Esperar antes de activar el siguiente inyector
    }
}
