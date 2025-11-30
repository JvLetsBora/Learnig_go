#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiClient.h>

// Definir os pinos da câmera ESP32-CAM AI-Thinker
#define CAMERA_MODEL_AI_THINKER
#define PWDN_GPIO_NUM    32
#define RESET_GPIO_NUM   -1
#define XCLK_GPIO_NUM    0
#define SIOD_GPIO_NUM    26
#define SIOC_GPIO_NUM    27
#define Y9_GPIO_NUM      35
#define Y8_GPIO_NUM      34
#define Y7_GPIO_NUM      39
#define Y6_GPIO_NUM      36
#define Y5_GPIO_NUM      21
#define Y4_GPIO_NUM      19
#define Y3_GPIO_NUM      18
#define Y2_GPIO_NUM      5
#define VSYNC_GPIO_NUM   25
#define HREF_GPIO_NUM    23
#define PCLK_GPIO_NUM    22


// Credenciais WiFi
const char* ssid = "vamos";  // Substitua pelo seu SSID
const char* password = "12345678"; // Substitua pela sua senha
const char* host = "192.168.43.162"; // IP do servidor Python
const uint16_t port = 5000; // Porta do servidor

void setup() {
  Serial.begin(115200);
  // Inicializa a conexão Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Conectando ao WiFi...");
  }
  Serial.println("Conectado ao WiFi");
  
  // Inicializa a câmera
  camera_config_t config;
  config.ledc_channel = LEDC_CHANNEL_0;
  config.ledc_timer = LEDC_TIMER_0;
  config.pin_d0 = Y2_GPIO_NUM;  // D0
  config.pin_d1 = Y3_GPIO_NUM;  // D1
  config.pin_d2 = Y4_GPIO_NUM;  // D2
  config.pin_d3 = Y5_GPIO_NUM;  // D3
  config.pin_d4 = Y6_GPIO_NUM;  // D4
  config.pin_d5 = Y7_GPIO_NUM;  // D5
  config.pin_d6 = Y8_GPIO_NUM;  // D6
  config.pin_d7 = Y9_GPIO_NUM;  // D7
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;  // Use -1 se não houver
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;  // Escolhendo o formato JPEG
  config.fb_location = CAMERA_FB_IN_DRAM;  // Configura o framebuffer na DRAM
  config.frame_size = FRAMESIZE_QVGA;  // Altere conforme necessário (QVGA, VGA, SVGA, etc.)
  config.fb_count = 1; // Tente reduzir para 1 buffer de frame
  config.jpeg_quality = 40; // Ajuste a qualidade do JPEG (12 é alto, 63 é baixo)

  // Configuração da câmera
  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Erro ao inicializar a câmera");
    ESP.restart();
    return;
  }
}

void loop() {
  WiFiClient client;

  // Conecta ao servidor Python
  Serial.printf("Tentando conectar ao servidor %s:%d...\n", host, port);
  if (!client.connect(host, port)) {
    Serial.println("Falha ao conectar ao servidor");
    delay(5000);  // Tentar novamente em 5 segundos
    return;
  } else {
    Serial.println("Conectado ao servidor com sucesso!");
  }

  // Captura uma imagem
  Serial.println("Capturando imagem...");
  camera_fb_t *fb = esp_camera_fb_get();
  if (!fb) {
    Serial.println("Falha ao capturar imagem");
    client.stop();  // Desconectar se falhar
    return;
  } else {
    Serial.printf("Imagem capturada com sucesso! Tamanho: %d bytes\n", fb->len);
  }

  // Envia o tamanho da imagem para o servidor
  Serial.println("Enviando tamanho da imagem...");
  client.write((const uint8_t*)&fb->len, sizeof(fb->len));

  // Envia a imagem para o servidor
  Serial.println("Enviando imagem...");
  client.write(fb->buf, fb->len);

  // Libera a imagem capturada
  esp_camera_fb_return(fb);
  Serial.println("Imagem enviada e buffer liberado!");

  // Desconecta do servidor
  client.stop();
  Serial.println("Desconectado do servidor.");

  // Delay de 10 segundos entre cada captura e envio
  delay(10000); 
}
