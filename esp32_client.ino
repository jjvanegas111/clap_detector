#include <WiFi.h>
#include <WiFiClient.h>

// Configuración Wi-Fi
const char* ssid = "TU_RED_WIFI";  // Cambia esto por tu Wi-Fi
const char* password = "TU_CONTRASEÑA"; 

// Configuración del servidor
const char* serverIP = "192.168.1.100";  // Cambia esto por la IP de tu MacBook
const int serverPort = 5000;             // Puerto donde escucha el servidor

WiFiClient client;

// Configuración del micrófono
#define MIC_PIN 34   // Entrada analógica del micrófono
#define LED_PIN 2    // LED del ESP32

void setup() {
    Serial.begin(115200);
    pinMode(LED_PIN, OUTPUT);
    digitalWrite(LED_PIN, LOW); // Apagar LED al inicio

    // Conectar a Wi-Fi
    Serial.print("Conectando a Wi-Fi...");
    WiFi.begin(ssid, password);
    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.print(".");
    }
    Serial.println("\n✅ Conectado a Wi-Fi");
}

void loop() {
    Serial.println("\n🎤 Capturando audio...");

    // Capturar audio simulando una lectura de micrófono (esto debe mejorarse con un ADC)
    int sample = analogRead(MIC_PIN);

    // Enviar datos al servidor
    if (client.connect(serverIP, serverPort)) {
        Serial.println("📡 Enviando datos...");
        client.println(sample);
        client.flush();

        // Esperar respuesta
        String response = client.readStringUntil('\n');
        Serial.println("🔍 Respuesta del servidor: " + response);

        // Encender/apagar LED según la respuesta
        if (response.toInt() == 1) {
            digitalWrite(LED_PIN, HIGH);
            Serial.println("👏 ¡Aplauso detectado! LED encendido.");
        } else {
            digitalWrite(LED_PIN, LOW);
            Serial.println("❌ No es un aplauso. LED apagado.");
        }

        client.stop();
    } else {
        Serial.println("❌ No se pudo conectar al servidor.");
    }

    delay(2000);  // Esperar 2 segundos antes de la siguiente captura
}