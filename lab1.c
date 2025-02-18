#include <stdio.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"

#define GPIO_OUTPUT_IO 4
#define GPIO_INPUT_IO_BTN 2
#define GPIO_OUTPUT_PIN_SEL (1ULL<<GPIO_OUTPUT_IO)
#define GPIO_INPUT_PIN_SEL (1ULL<<GPIO_INPUT_IO_BTN)

void ceva_acolo(){
    int cnt_btn = 0;
    for( ;; ){
        vTaskDelay(200 / portTICK_PERIOD_MS);
        if(!gpio_get_level(GPIO_INPUT_IO_BTN))
            printf("cnt_btn: %d\n", cnt_btn++);
    }
}

void app_main() {
    //zero-initialize the config structure.
    gpio_config_t io_conf = {};
    //disable interrupt
    io_conf.intr_type = GPIO_INTR_DISABLE;
    //set as output mode
    io_conf.mode = GPIO_MODE_OUTPUT;
    //bit mask of the pins that you want to set
    io_conf.pin_bit_mask = GPIO_OUTPUT_PIN_SEL;
    //disable pull-down mode
    io_conf.pull_down_en = 0;
    //disable pull-up mode
    io_conf.pull_up_en = 0;
    //configure GPIO with the given settings
    gpio_config(&io_conf);

    io_conf.mode = GPIO_MODE_INPUT;
    io_conf.pin_bit_mask = GPIO_INPUT_PIN_SEL;
    io_conf.pull_up_en = 1;
    gpio_config(&io_conf);
    
    int cnt = 0;

    TaskHandle_t xHandle = NULL;
    xTaskCreate(ceva_acolo,"ceva_acolo", 2048, 
                        NULL, 10, &xHandle);

    while(1) {
        printf("cnt: %d\n", cnt++);
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        vTaskDelay(1000 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        vTaskDelay(500 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 0);
        vTaskDelay(250 / portTICK_PERIOD_MS);
        gpio_set_level(GPIO_OUTPUT_IO, 1);
        vTaskDelay(750 / portTICK_PERIOD_MS);
    }
}
