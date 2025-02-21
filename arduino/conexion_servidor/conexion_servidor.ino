#include <WiFi.h>
#include <WiFiClient.h>

// Configuración Wi-Fi
const char* ssid = "TU_RED_WIFI";  // Cambia esto por tu Wi-Fi
const char* password = "TU_CONTRASEÑA"; 

// Configuración del servidor
const char* serverIP = "10.253.9.151";  // Cambia esto por la IP de tu MacBook
const int serverPort = 5001;             // Puerto donde escucha el servidor

WiFiClient client;

// Configuración del micrófono
#define MIC_PIN 34   // Entrada analógica del micrófono
#define LED_PIN 2    // LED del ESP32
#define SAMPLE_RATE 44100  // Tasa de muestreo en Hz
#define BUFFER_SIZE 1024   // Tamaño del buffer de audio

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

    // Capturar un buffer de datos de audio
    int16_t audioBuffer[BUFFER_SIZE];
    for (int i = 0; i < BUFFER_SIZE; i++) {
        audioBuffer[i] = analogRead(MIC_PIN);
        delayMicroseconds(1000000 / SAMPLE_RATE);  // Esperar el tiempo adecuado para la tasa de muestreo
    }

    // Crear un archivo .wav en memoria
    uint8_t wavHeader[44];
    createWavHeader(wavHeader, BUFFER_SIZE, SAMPLE_RATE);

    // Enviar datos al servidor
    if (client.connect(serverIP, serverPort)) {
        Serial.println("📡 Enviando datos...");

        // Enviar encabezado .wav
        client.write(wavHeader, sizeof(wavHeader));

        // Enviar datos de audio
        client.write((uint8_t*)audioBuffer, sizeof(audioBuffer));
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

void createWavHeader(uint8_t* header, int dataSize, int sampleRate) {
    int byteRate = sampleRate * 2;  // 16 bits por muestra (2 bytes)
    int blockAlign = 2;  // 16 bits por muestra (2 bytes)

    // RIFF header
    header[0] = 'R';
    header[1] = 'I';
    header[2] = 'F';
    header[3] = 'F';
    header[4] = (dataSize + 36) & 0xff;
    header[5] = ((dataSize + 36) >> 8) & 0xff;
    header[6] = ((dataSize + 36) >> 16) & 0xff;
    header[7] = ((dataSize + 36) >> 24) & 0xff;
    header[8] = 'W';
    header[9] = 'A';
    header[10] = 'V';
    header[11] = 'E';

    // fmt subchunk
    header[12] = 'f';
    header[13] = 'm';
    header[14] = 't';
    header[15] = ' ';
    header[16] = 16;
    header[17] = 0;
    header[18] = 0;
    header[19] = 0;
    header[20] = 1;
    header[21] = 0;
    header[22] = 1;
    header[23] = 0;
    header[24] = sampleRate & 0xff;
    header[25] = (sampleRate >> 8) & 0xff;
    header[26] = (sampleRate >> 16) & 0xff;
    header[27] = (sampleRate >> 24) & 0xff;
    header[28] = byteRate & 0xff;
    header[29] = (byteRate >> 8) & 0xff;
    header[30] = (byteRate >> 16) & 0xff;
    header[31] = (byteRate >> 24) & 0xff;
    header[32] = blockAlign;
    header[33] = 0;
    header[34] = 16;
    header[35] = 0;

    // data subchunk
    header[36] = 'd';
    header[37] = 'a';
    header[38] = 't';
    header[39] = 'a';
    header[40] = dataSize & 0xff;
    header[41] = (dataSize >> 8) & 0xff;
    header[42] = (dataSize >> 16) & 0xff;
    header[43] = (dataSize >> 24) & 0xff;
}