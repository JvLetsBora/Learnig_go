#include "esp_camera.h"
#include <WiFi.h>
#include <WiFiClient.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"

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

SemaphoreHandle_t xImageSemaphore;  // Semáforo binário para sincronização
camera_fb_t *fb = NULL;  // Framebuffer da câmera

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
  config.pin_d0 = Y2_GPIO_NUM;
  config.pin_d1 = Y3_GPIO_NUM;
  config.pin_d2 = Y4_GPIO_NUM;
  config.pin_d3 = Y5_GPIO_NUM;
  config.pin_d4 = Y6_GPIO_NUM;
  config.pin_d5 = Y7_GPIO_NUM;
  config.pin_d6 = Y8_GPIO_NUM;
  config.pin_d7 = Y9_GPIO_NUM;
  config.pin_xclk = XCLK_GPIO_NUM;
  config.pin_pclk = PCLK_GPIO_NUM;
  config.pin_vsync = VSYNC_GPIO_NUM;
  config.pin_href = HREF_GPIO_NUM;
  config.pin_sccb_sda = SIOD_GPIO_NUM;
  config.pin_sccb_scl = SIOC_GPIO_NUM;
  config.pin_pwdn = PWDN_GPIO_NUM;
  config.pin_reset = RESET_GPIO_NUM;
  config.xclk_freq_hz = 20000000;
  config.pixel_format = PIXFORMAT_JPEG;
  config.fb_location = CAMERA_FB_IN_DRAM;
  config.frame_size = FRAMESIZE_QVGA;
  config.fb_count = 1;
  config.jpeg_quality = 40;

  if (esp_camera_init(&config) != ESP_OK) {
    Serial.println("Erro ao inicializar a câmera");
    ESP.restart(); // Garante que o DRAM esteje vazio
    return;
  }

  // Cria o semáforo binário
  xImageSemaphore = xSemaphoreCreateBinary();

  // Criação das tasks (threads)
  xTaskCreatePinnedToCore(threadImageAcquisition, "ImageAcquisition", 8192, NULL, 1, NULL, 0);
  xTaskCreatePinnedToCore(threadImageSending, "ImageSending", 8192, NULL, 1, NULL, 1);
  xTaskCreatePinnedToCore(threadDetectionReceiving, "DetectionReceiving", 4096, NULL, 1, NULL, 1);
}

void loop() {
  // O loop principal pode ficar vazio porque o FreeRTOS gerencia as tasks.
}

// Thread de aquisição de imagens
void threadImageAcquisition(void *pvParameters) {
  while (true) {
    // Captura uma imagem
    fb = esp_camera_fb_get();
    if (!fb) {
      Serial.println("Falha ao capturar imagem");
    } else {
      Serial.printf("Imagem capturada: %d bytes\n", fb->len);
      // Sinaliza que há uma nova imagem disponível
      xSemaphoreGive(xImageSemaphore);
    }
    vTaskDelay(pdMS_TO_TICKS(10000));  // Delay de 10 segundos entre capturas
  }
}

// Thread de envio de imagens
void threadImageSending(void *pvParameters) {
  while (true) {
    // Espera até que o semáforo indique que uma imagem está disponível
    if (xSemaphoreTake(xImageSemaphore, portMAX_DELAY) == pdTRUE) {
      WiFiClient client;
      if (!client.connect(host, port)) {
        Serial.println("Falha ao conectar ao servidor");
        continue;
      }

      // Envia o tamanho da imagem para o servidor
      client.write((const uint8_t*)&fb->len, sizeof(fb->len));

      // Envia a imagem
      client.write(fb->buf, fb->len);
      Serial.println("Imagem enviada");

      // Libera o framebuffer
      esp_camera_fb_return(fb);
      client.stop();
    }
  }
}

// Thread de recebimento de detecção
void threadDetectionReceiving(void *pvParameters) {
  while (true) {
    if (Serial.available() > 0) {
      String detectionData = Serial.readStringUntil('\n');
      Serial.printf("Dados de detecção recebidos: %s\n", detectionData.c_str());
      
    }
    vTaskDelay(pdMS_TO_TICKS(500));  // Verifica a serial a cada meio segundo
  }
}
